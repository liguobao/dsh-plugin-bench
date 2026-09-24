# dsh-loop-guard — DSH 思考循环守护

> 为 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（DSH）提供的思考循环守护插件：模型陷入「只想不做」的退化循环时自动打断，不必再手动中止

**🌏 中文 | [English](README_EN.md)**

`dsh` · `dsh-plugin` · `plugin` · `guard` · `thinking-loop` · `reasoning` · `repetition` · `AI agent` · `思考循环` · `死循环` · `推理退化`

<!-- keywords: dsh, dsh-plugin, deepseek harness, plugin, guard, thinking-loop, reasoning, repetition, circuit-breaker, ai agent, 思考循环, 死循环, 推理退化 -->

## 简介

长上下文 + 高 reasoning effort 下，模型会**退化**：推理里开始出现低熵重复（`好。执行。好。`、`Write. / Output. / Let me write. / Go.` 这种短句轮转），然后停不下来。

麻烦的是 DSH 自带的 `guard/` 家族**抓不到这种情况**——它们都围绕工具调用：

| 内置 guard | 挂载点 | 能抓什么 |
|---|---|---|
| `guard/timeout-policy` | `tools/execute` | 工具调用超时 |
| `guard/repeat-tool-reminder` | `tools/post-execute` | 重复的同一个工具调用链 |

而退化循环的特征恰恰是**完全不调工具**：只有 `reasoning-delta`，零 `text-delta`、零 `tool-call-delta`。于是：

- 两个 guard 都不触发；
- agent-loop 的 `turn()` 从**已完成的消息**推导 `StepEndReason`，流不结束 → step 不 settle → `turnEnds` 永远为 null → `while (true)` 永不 break；
- **回合停不下来，只能由你手动中止**——而界面上只显示「思考中」，看起来和认真推理没区别。不点开 thinking 块根本察觉不到它在空转。

本插件接管 `llm/stream` 瀑布流，按每次模型调用的 chunk 组成做判定，在退化发生时**从流内部切断**，让回合正常结束。

![效果：思考循环被截断，并注入纠正提示](assets/loop-break-notice.png)

上图是实际运行效果：推理块里反复出现 `OK. / Writing. / Let me write. / Go. / Executing. / Now.` 的轮转，插件在重复累积到阈值时截断该次调用，并在下方注入一条提示，让模型回到原本的任务。

## 功能特性

- **四层检测，各管一种形态**：纯推理无输出、复述上一步材料、推理内部的**周期循环**、以及推理内部的**短语池重排**。后两条是互补的，见下。
- **能终止「永不结束的回合」**：这是本插件存在的核心理由。退化循环里流永远不结束，任何「调用结束后再判定」的检测都够不到；只有从流内部切一刀才行。
- **切断后任务继续，不必手动重启**：切断只是结束当前这次调用，回合以**正常完成**收尾，会话照常可用——你原本的任务可以直接往下走。这是它和「卡死到只能手动中止」的根本区别。
- **在 1% 处就切断**：实测一个 **330,188** 字符的循环在 **3,264 字符**（1.0%）时被切断；一个 124,070 字符的在 17,888 字符（14.4%）时被切断。原来这两个都要跑满全程、最后靠人手动中止。
- **误报极低**：在真实会话 119 个「有产出」的调用上，**零误报**；扫描本机全部 735 个会话、40 个触发点，误判 **12 个**（全是「贴代码改前/改后」），已由集中度护栏挡住——见下。
- **精确判据**：判定用的是**逐字周期**和**跨调用复述**，不是时长、也不是比率。
- **纠正信息指向原任务**：切断时注入的提示只说「不要重复，继续完成任务」，**不会**让模型去"给个结论然后收尾"——后者会让它偏离原本在做的事。
- **反应不闩锁**：一次 steer 常常打不破强循环，所以阈值到了会重新计数、再次开火（上限 `maxFires`）。
- **跟随界面语言**：注入的提示读宿主 `locale` 设置，中文环境说中文（默认即中文）。
- **绝不静默重试**：**没有**模型回退、没有自动重发同一请求——把退化模型再喂一遍比循环本身更糟。
- **离线分析器**：`tools/analyze-session.mjs` 用**插件运行时同一个检测器**复跑 session jsonl，回答「这次到底该不该响」。
- **可观测**：切断时写 warn 日志，并注明是哪条规则命中的。

## 使用

### 开箱即用

**装好就能用，不需要任何配置。** 默认值已按真实数据标定：

- 纯推理空转、复述上一步、推理内部周期循环 → 自动打断回合；
- 单次调用刷屏式重复可见输出 → 自动从流内部切断；
- 正常的长推理、正常的重复性输出（表格、日志、CSS、JSON）→ **不误伤**。

### 熔断后会发生什么

**会话继续，任务可以往下走**——不需要你手动重启或重新发指令。

| 项 | 结果 |
|---|---|
| 本次调用 | 被切断，已产生的推理作为正常消息落盘 |
| 回合 | 以 `turn/end` 结束，原因是 `{ kind: 'completed' }`——**和正常完成一样** |
| 会话 | **存活**，agent 回到 `idle`，可直接继续 |
| 已执行的工具调用 | **保留**（`tool/result` 不回滚） |
| 注入的提示 | 一条 `notice`，说明「已连续重复 N 字符，响应被中途截断，不要重复，继续完成任务」 |
| 终止 chunk | 协议合法：切断前先闭合所有 block，再用 `stop` 结束，已用 DSH 自己的 `@deepseek-ai/dsh-llm/invariant` 验证 |

所以体验是：**循环 → 在几百字符处被切断 → 提示它回到任务 → 继续干活**。

**为什么回合是 `completed` 而不是报错**：早先的版本用 `error` finish，那会让 DSH 的会话渲染器拿不到 `assistant/message`（只产生 `assistant/attempt`），于是抛出
`conversation Definition "assistant-step" withdrew materialized target "chat"`，而且 `turn()` 会在 `throwError` 处提前抛出、永远走不到「是否再开一个回合」那一行——既崩界面又无法续跑。改为**闭合 block + `stop` finish** 后走的是正常路径，两个问题一起消失。

代价是**回合结束原因不再有辨识度**（`completed` 与正常完成无法区分）。痕迹留在两处：注入的 `notice`，以及宿主日志里的 warn。这是刻意的取舍——熔断的目的是让会话**继续可用**，不是制造告警。

插件**只结束这次调用，从不结束 agent**——它永远不会调用 `agent.cancel()`。

### 自动续跑（`resumeAfterBreak`）

**通常不需要开。** 熔断本身不会结束会话，任务已经能继续；这个选项只是让它在切断后**不等你发话**就自己往下走：

```yaml
- id: loop-guard
  config:
    resumeAfterBreak: true
```

**关键在于「等」**，这不是实现细节而是整个方案成立的前提：切断发生在流包装器里，此时 agent 还处于 `running`，而 DSH 在这个阶段**刻意压制唤醒**——`wakeDriver()` 只肯为 maintenance 或 aborted 挂起唤醒，所以此刻发 `steer()` / `followup()` 都不会置 `wakeRequested`，`kick()` 的 `finally` 找不到唤醒依据，会话就此停下。唤醒只有在 agent 回到 `idle` 后才有效，插件用 `whenIdle()` 等这个时刻。

续跑消息**带纠正文本，从不是空的**。空消息等于把同一段退化历史原样再喂一遍、不带任何新信息——那正是产生循环的输入。

该选项默认关闭：它是在模型已经证明「不能自主行动」之后、**不经过你同意就再进一次模型**。无人值守的长任务才建议打开。

## 安装

> **说明**：本插件需要 DSH 的 `llm/stream` 瀑布流，DSH **0.1.2-rc.1 及以后**的各条线都可用。

### 方式一：让 AI 安装（最简单）

把本仓库地址告诉 DSH 的 AI 助手即可，例如：「安装 https://github.com/MrWeiCodes/dsh-loop-guard 这个插件」。AI 会替你完成插件装载、依赖与补丁处理；之后重启 `dsh web`。

### 方式二：从 GitHub 安装

```powershell
dsh plugin --profile web add -w github:MrWeiCodes/dsh-loop-guard
```

从 GitHub 装的是源码，`lib/` 需要现场编译，所以**装完可能需要在 profile 的 `pnpm-workspace.yaml` 里放行构建脚本**（pnpm 10 起默认阻止依赖执行构建脚本，按它打印的提示把那一行粘进去再重跑即可）。

> **从本地目录安装的已知问题**：Windows 上若插件目录与 profile **不在同一个盘符**（例如插件在 `G:\`、profile 在 `C:\`），pnpm 会把 `file:` 依赖错误解析成 `C:\Users\<用户名>\...` 而安装失败。此时请改用「方式三」。

### 方式三：手动安装

无 pnpm 或离线环境时的备选路径：

1. 把本仓库克隆到 profile 的插件目录，并在目标目录构建一次：
   ```powershell
   # 示例：web profile
   $dst = "$HOME\.dsh\profiles\web\packages\dsh-loop-guard"
   git clone https://github.com/MrWeiCodes/dsh-loop-guard.git $dst
   cd $dst
   npm install      # 同时编译出 lib/
   npm run build    # 如上一步未生成 lib/，单独执行
   ```
2. 在 profile 的 `package.json` 的 `dependencies` 中加入：
   ```json
   "dsh-loop-guard": "file:./packages/dsh-loop-guard"
   ```
3. 把 `cordis.patch.yml` 的内容并入 profile 的 `cordis.patch.yml`（在文件末尾追加）。
4. 重新安装依赖并重启：`pnpm install`（或 `npm install`）、`dsh web`。

## 更新

- **方式一（AI 安装）的**：直接告诉 AI「更新 dsh-loop-guard 插件」即可。
- **方式二（GitHub 安装）的**：
  ```powershell
  dsh plugin --profile web add -w github:MrWeiCodes/dsh-loop-guard
  ```
  若没有拉到最新提交（git 依赖有缓存），先移除再重新添加：
  ```powershell
  dsh plugin --profile web remove dsh-loop-guard
  dsh plugin --profile web add -w github:MrWeiCodes/dsh-loop-guard
  ```
  然后重启 `dsh web`。**更新到新提交后 commit 号会变**，若 pnpm 再次要求放行构建，按方式二的说明重做一次即可。
- **方式三（手动）安装的**：
  ```powershell
  cd "$HOME\.dsh\profiles\web\packages\dsh-loop-guard"
  git pull            # 或重新拷贝新版本覆盖
  npm install         # 依赖声明有变化时执行
  npm run build
  ```
  然后重启 `dsh web`。

## 卸载

### 方式一（AI 安装）的：让 AI 卸载

直接告诉 AI 助手「卸载 dsh-loop-guard 插件」，AI 会移除插件、清理补丁与依赖。

### 方式二（GitHub）安装的

```powershell
dsh plugin --profile web remove dsh-loop-guard
```

然后重启 `dsh web`。

### 方式三（手动）安装的

1. 从 profile 的 `cordis.patch.yml` 中删除本插件的 `insert` 行。
2. 从 profile 的 `package.json` 的 `dependencies` 中删除 `"dsh-loop-guard": ...`。
3. 重新安装依赖并重启：`pnpm install`（或 `npm install`）、`dsh web`。

### 残留位置清单（AI 卸载时按此清理）

- **插件目录**（方式三安装时）：`$DSH_HOME/profiles/<profile>/packages/dsh-loop-guard/`。`$DSH_HOME` 默认是 `~/.dsh`。
- **依赖与补丁**（方式三安装时）：profile 的 `package.json` 中的 `"dsh-loop-guard": ...` 依赖、`cordis.patch.yml` 中的 `insert` 行。
- 本插件**不写任何自己的配置文件**，也没有全局注册表或系统级写入；卸载后不留配置残留。

## 配置

**默认配置就能用，通常不需要动它。** 只有想调整灵敏度或开启自动续跑时才需要改。

### 全部选项

```ts
interface Config {
  // ── 跨调用判定（调用结束后） ──────────────────────────────
  /** 连续多少次「停滞调用」后反应。默认 3。 */
  maxThinkingSteps?: number
  /** 单次调用的推理至少这么长才参与判定。默认 2048 字符。 */
  minReasoningChars?: number
  /** 跨调用相似度：上一步的推理有多少重现才算「复述」。0 关闭。默认 0.8。 */
  similarityThreshold?: number
  /** 命中后做什么：'warn' | 'steer'（默认） | 'cancel'。 */
  escalate?: 'warn' | 'steer' | 'cancel'
  /** 同一个 agent 最多反应多少次。默认 4。 */
  maxFires?: number
  /** escalate 为 'cancel' 时的取消原因。默认 'thinking-loop'。 */
  cancelCause?: string

  // ── 流内切断（调用进行中） ────────────────────────────────
  /** 连续多少个相同的可见输出 chunk 就切断。0 关闭。默认 60。 */
  maxRepeatedText?: number
  /** 可见输出尾部最长重复周期（字符）。0 关闭。默认 512。 */
  maxRepeatedCycleChars?: number
  /** 可见输出尾部至少要重复多长才判定。默认 256。 */
  minRepeatedCycleChars?: number
  /** 推理尾部最长重复周期（字符）——**这条终止 #5976 的永不结束回合**。0 关闭。默认 512。 */
  maxRepeatedReasoningCycleChars?: number
  /** 推理尾部至少要重复多长才判定。默认 512。 */
  minRepeatedReasoningCycleChars?: number
  /** 推理里「重复行」累计到多少字符就切断——**这条抓没有周期的短语池重排**。0 关闭。默认 2048。 */
  maxRepeatedReasoningLineChars?: number
  /** 重复行占比要达到多少才判定。默认 0.6。 */
  minRepeatedReasoningLineCoverage?: number
  /** 行词汇的集中度：平均每行重复几次。低于此值不算短语池。默认 4。 */
  minRepeatedReasoningLineConcentration?: number

  // ── 切断后的行为 ──────────────────────────────────────────
  /** 日志里标注的错误码。默认 'REPETITIVE_OUTPUT'。（切断本身走 `stop`，不产生错误） */
  breakCode?: string
  /** 切断时注入一条纠正提示，让模型回到原任务。默认 true。 */
  breakCorrection?: boolean
  /** 切断后等回合收尾，不等你发话就自动续跑。默认 false。 */
  resumeAfterBreak?: boolean
}
```

### 常见需求（直接抄）

```yaml
# 1. 更灵敏：连续 2 次停滞就反应
- id: loop-guard
  config:
    maxThinkingSteps: 2

# 2. 