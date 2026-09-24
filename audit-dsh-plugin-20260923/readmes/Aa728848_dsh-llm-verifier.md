# DSH LLM Verifier

> 基于 [llm-as-a-verifier/llm-as-a-verifier](https://github.com/llm-as-a-verifier/llm-as-a-verifier) 迁移构建的 DSH 原生模型可配置复核插件（Verifier）。

---

## 它是什么？

`dsh-llm-verifier` 为 DeepSeek Harness（DSH）引入了一套**独立的裁判复核机制**。在主 Agent 负责生成代码、执行命令与工具交互的同时，Verifier 会收集当前任务目标、各候选方案过程以及真实的终端执行结果，交由你在设置中指定的独立 DSH 模型进行仲裁：评估哪个方案更可靠、当前任务的实际完成进度、以及是否存在未发现的潜在错误。

插件提供五个显式工具，并支持可配置的宿主级自动会话验收：

- `verifier_compare`：对两个候选执行过程进行成对比较（Pairwise Comparison）；
- `verifier_select`：在多个候选方案中通过锦标赛机制选出最优解，供 Best-of-N / 多候选编排器直接调用；
- `verifier_track`：评估任务在已有检查点（Checkpoint）的完成度与进展，供 Goal / Workflow 等长任务编排器直接调用；
- `verifier_best_of_n`：**唯一会自己生成候选的工具**——用当前会话模型并行起草 N 份完整候选，再用独立裁判排序，并额外给出与验收门控同源的**绝对分**（见[关键交付物的 best-of-N](#关键交付物的-best-of-n)）；
- `verifier_current_session`：显式提取当前 DSH 会话记录，进行脱敏并执行复核；
- **自动路由与早评审**：智能或严格策略在 `agent/turn-stopping` 生命周期边界按阶段调度 `select → compare → track → current_session`（`verifier_best_of_n` 永不自动触发）。第一阶段只信任 Workflow 的版本化候选协议与发生真实变化的 Todo 快照；普通 Subagent 输出必须经第二阶段的证据引用分类，避免把不同子任务误当候选。此外，**智能模式**还会在 `agent/pre-step`（下一次模型生成之前）对已完成的 Workflow 候选信封做一次受限的 `compare/select` 早评审，让选择结果直接影响接下来的实施；该入口不跑语义分类、`track`、最终验收或候选生成，严格模式不参与；
- **自动验收门控**：候选选择与进度检查完成后，宿主运行同一会话验收逻辑；未通过时以插件 steering 反馈要求 Agent 修复并重新验证，而不是依赖模型是否主动想起工具。

## 安装与启用 (Installation & Usage)

### 1. 使用 `dsh plugin` 安装

DeepSeek Harness（DSH）通过 profile 独立管理各个运行环境的插件依赖。请使用 `dsh plugin` 命令将插件安装至目标 profile（如 `web`）：

```bash
# 方式 A：从 npm 官方 Registry 安装（推荐）
dsh plugin --profile web add dsh-llm-verifier
```

> [!NOTE]
> `dsh plugin add` 安装成功后，DSH 会自动识别包内的 `dsh.bundle` 声明并完成插件层自动对齐（Reconcile），**无需手动修改任何配置文件**。

### 2. 启动与配置

启动 DSH Web 客户端：

```bash
dsh web
# 或
dsh --profile web
```

启动后进入前端界面，打开 **`设置 → LLM Verifier`** 即可可视化配置裁判所使用的 Provider、Model、推理强度（Reasoning Effort）、最大并发与缓存策略。

### 3. 常用管理命令

```bash
# 更新插件至最新版本
dsh plugin --profile web update dsh-llm-verifier

# 卸载插件
dsh plugin --profile web remove dsh-llm-verifier

# 查看当前 Profile 已安装的插件与依赖列表
dsh plugin --profile web list
```

### 4. 作为独立库引用（可选）

如果你在其它 TypeScript / JavaScript 项目中需要复用核心评分标尺与锦标赛算法，可直接作为普通 npm 依赖安装并引入：

```bash
pnpm add dsh-llm-verifier
```

```typescript
import {
  extractScore,
  extractProgressScore,
  bradleyTerry,
  pivotRoundPairs,
} from 'dsh-llm-verifier/core'
```

## 本地开发

```bash
pnpm install
pnpm run build      # 生成 lib/，宿主加载的就是这份产物
pnpm run typecheck  # 按 package.json 里锁定的 @deepseek-ai/dsh-* 版本检查类型
pnpm test           # vitest 单元测试
```

当 DSH 本体是本地 checkout（默认位于同级目录 `../deepseek-harness`）时，用下面的命令按**实际运行版本**检查类型：

```bash
pnpm run typecheck:local   # 依据 tsconfig.local.json，把 @deepseek-ai/dsh-* 解析到本地 checkout 的 lib/types
```

两套类型定义可能不同步：例如 `Session.events` 在 DSH 0.1.5 已被 `snapshotEvents()` 取代，`tool/code-dispatch` 也已改名 `tool/ptc-dispatch`。插件内部的 `sessionEvents()` 同时兼容两种会话形态，两类派发事件都会计入证据，因此 0.1.1 与 0.1.7 宿主都可以运行。

DSH 0.1.7 又搬动了两处判定地基，两侧形态插件都读：

- **工具结果从内容块变成独立消息**。0.1.6 及以前，一条工具结果是一个 `tool-result` 内容块，真正的输出套在里面、失败标志 `isError` 挂在块上；0.1.7 删除了该块类型，工具结果改为 `role: 'tool'` 的独立消息，`isError` 上移到消息本身。`session.ts` 的 `toolResultBlocks()` / `toolResultFailed()` 是这两个差异的唯一读取点，旧宿主的嵌套输出仍会被渲染成 `[Tool Result]` 证据。
- **注入消息的来源改为生产者自报**。0.1.7 删除了 `MessageSourceMap` 的统一包装 `{ kind: 'plugin', plugin }`（持久化准入还会直接拒绝该包装），改为每个生产者声明自己的 `kind`。插件在 `src/message-source.ts` 声明并使用 `kind: 'llm-verifier'`；宿主读取旧日志时会把历史包装行改写成 `plugin:<名称>`，那只是历史行的显示名，不影响判定。

客户端面（Web 设置页与看板）另有两处只随新版本线变化：提供 `ctx.slots` 的包是 `@deepseek-ai/dsh-client-ui-renderer`（`@deepseek-ai/dsh-client-runtime` 在 0.1.2 就已删除，插件类型一律取自 `@deepseek-ai/cordis` 的 `Context`）；宿主图标名在 0.1.7 整体由尺寸后缀改为笔画后缀。图标是具名导入、且该模块对客户端 bundle 是 external，一份源码无法同时满足两套名字，因此插件改为按名探测两种拼写、都缺失时渲染空——旧宿主不会因此白屏。

typecheck 门禁按 `package.json` 的 `devDependencies` 解析，已随宿主推进到 `0.1.7-rc.1`（此前从 `0.1.1-rc.2` 上移到 `0.1.7-alpha.1`）：客户端面的图标名在 0.1.7 才改名，一份源码只能对齐一侧，宿主面的旧形态兼容由运行时代码与回归测试保证。从 `0.1.7-alpha.1` 到 `0.1.7-rc.1` 的宿主改动对本插件消费的所有宿主面**全是加法**（`tools/pre-execute` 侧只新增可选 `projectContent`，`dsh-session` / `dsh-llm` / `dsh-settings` / `dsh-agent` / `dsh-credentials` / 客户端槽位与图标包源码零改动），因此这一步只换版本线，不动插件代码。

其中一处更隐蔽的差异是 `deepFreeze`：0.1.1 的 `@deepseek-ai/dsh-llm` 会重新导出它，0.1.5 已把它移到 `@deepseek-ai/dsh-util-values`。插件因此自带一份等价的兜底实现，并同样**放过 `AbortSignal`**——冻结那个还在重试循环里使用、尚未被订阅的信号，会让传输层首次 `addEventListener`（Node ≥26.5）或超时/取消时的 `controller.abort()`（所有 Node 版本）抛 `Cannot assign to read only property`。

### 发布到 npm

`pnpm publish`（或 `npm publish`）会先触发 `prepublishOnly` → `pnpm run verify:release`，即**按 npm 锁定版本**执行 typecheck、单元测试并重新构建 `lib/`，确保发出去的产物来自 npm 依赖而非本地 checkout 的类型；`typecheck:local` 只在本机核对，不参与发布。

发布内容由 `package.json` 的 `files` 字段决定：`lib`（构建产物、source map 与 `lib/types` 类型声明）、`src`、`cordis.patch.yml`、`README.md`。`tsconfig.local.json` 之类的本机文件不会进入 tarball。

`peerDependencies` 中逐个列出的 `^0.1.5-alpha.1`、`^0.1.7-alpha.1`、`^0.1.7-rc.1` 等预发布范围是必需的，而且从 DSH 0.1.7-rc.1 起**由宿主强制执行**：按 semver 规则，预发布版本只有在同一 `x.y.z` 段存在带预发布的比较符时才算满足，因此不能简化成 `>=0.1.1-rc.2 <0.2.0`（那样会漏掉 `0.1.2-alpha.*`、`0.1.5-rc.*`、`0.1.7-alpha.*` 等宿主）。宿主启动 profile 时对每一个 `@deepseek-ai/dsh` / `@deepseek-ai/dsh-*` 条目跑 `semver.satisfies(运行版本, 范围, { includePrerelease: true })`，**任何一条不满足**就把该插件行停用（bundle 层直接跳过整个 bundle），并在 stderr 写出原因。所以缺少某条宿主版本线的后果不是"少个功能"，而是**插件整体不加载**；应急可用 `dsh plugin allow-version` 为该插件的精确版本做一次性豁免。当前声明覆盖到 `0.1.7-rc.1`，与本机 `dsh --version` 报告的运行版本一致。

统计数据有两条传输路径：优先走 `/api/llm-verifier/statistics`（Connection 的 exact Fetch 路由，带 Host/Origin 栅栏与浏览器鉴权），宿主较旧时回落到插件自己的 `/llm-verifier` RPC 通道（同样经过鉴权）。裸的 webServer 路由已被移除。

## 迁移来源

本插件的核心评估理论、A–T 评分标尺、进度判定算法以及概率基准锦标赛（Probabilistic Pivot Tournament）均源自开源项目：

- **上游项目**：[llm-as-a-verifier/llm-as-a-verifier](https://github.com/llm-as-a-verifier/llm-as-a-verifier)
- **上游 Claude Code 插件**：[TurboAgent](https://github.com/llm-as-a-verifier/TurboAgent)——API 代理形态，对每一次 LLM 请求无差别做 N 并发采样 + PPT 锦标赛选优。本插件的 `every-step`（每步选优）档与它对齐（在线拦截、`llm/stream` 缓冲回放、多模型备选池），但保留预算门控与 fail-closed 语义；两者运行方式的逐项对比与取舍见 [.agents/notes/implemented/feature/2026-09-16-every-step-process-selection.md](.agents/notes/implemented/feature/2026-09-16-every-step-process-selection.md)

本插件将上游算法的评分、锦标赛与运行策略移植为 TypeScript 实现，并深度集成了 DSH 的模型路由、设置面板、附件管理、会话日志与工具生态。上游实现是本插件的算法基准；本仓库内置离线黄金数据与 Python / TypeScript 一致性测试（Parity Tests）。两者共享算法基础，但本插件在此之上做了一组**明确列出的本地变体**——它们既不是"未修正的上游缺陷"，也不是可以笼统忽略的实现细节；改动其中任何一项，都要同步本节、`AGENTS.md` 与 `parity.test.ts`。

## 与上游的关系：共享算法基础与本地变体

### 评分（scoring）

概率期望评分中，同一字母可能对应多个 token 表面形式（受约束解码同时提供 `"A"` 与 `" A"`，二者都表示字母 A）。它们是同一次采样的互斥结果，因此本插件把它们**相加**得到该字母的概率；上游 Python 参考实现则保留其中较大的那个：

```python
# llm_verifier/fine_grained_reward.py:678
# 核对基准：上游 main @ 8db8a114355a9d7fdf9a8d1d5c87f6aeebd18770（pyproject version 0.2.0）
probs[val] = max(probs.get(val, 0.0), p)
```

`max` 会系统性低估"概率质量被拆到两种写法上"的字母（例：`" A"=0.4, "A"=0.4, " T"=0.5, "T"=0.1` 时，求和得 ≈0.5714，取最大值只有 ≈0.4444，足以跨过通过阈值），因此这里选择求和。该聚合在上游也没有被测试或文档固定下来，属于可自由取舍的实现细节；一致性测试的 fixture 有意不覆盖该情形（否则会必然失败）。

### 赛制（probabilistic pivot tournament）

上游在最后把 ring 与**完整的** pivot pairs 一起累积；本插件按**无序边**删掉与 ring 重合的 pivot 边，因此每个无序候选对全程只被评判一次，请求更少，胜率权重也不会被重复计入。这不只是成本差异，它会改变 `wins/counts` 的聚合值：用固定的 ring `[(3,2),(2,0),(0,1),(1,3)]`、pivots `[3,2]` 与一组固定 reward 复现，上游加权下胜者是候选 **3**（≈0.567932），本地去重下胜者是候选 **0**（≈0.540820）。两者都**不是**最高分平局，所以这不是"等价实现"，而是刻意选择的聚合语义；`parity.test.ts` 的 `offline aggregation fixtures` 把两边的期望值分别锁定，避免只有同级 Python checkout 存在时才能发现差异。

相同 seed 也不保证相同 ring：上游用 `random.Random(seed)`，本插件用自带的 `seededRandom`。ring 本身由随机置换构造，seed 只保证同一实现内可复现，跨语言不承诺逐位相同。

### 运行策略（runtime policy）

以下都是本插件在 DSH 宿主约束下做出的本地选择，不属于"上游契约"：

- **解析失败 fail closed**：判决解析不出就报错，绝不静默给分或静默通过。上游 `select` 默认 `on_error="tie"`、解析失败可回落 0.5，那不适合作为门控。
- **重复候选短路**：逐字节相同的候选不送判官（compare 返回中性 tie，select 全同返回 0 调用）。上游的多数投票短路会直接返回未评判的候选，本插件不采纳其语义。
- **两候选赛制**：`select` 只有两个候选时按单对处理，A/B 槽位用固定但非对称的 `orientPair` 决定。
- **温度与轮次**：判官温度默认 `0.2`（上游 1），自动路由默认 1 轮、最终验收 2 轮。
- **K=1 位置定向**：上游在 K≥2 时逐次交换 A/B 槽位（`fine_grained_reward.py` "Odd reps swap the prompt slots"），其 benchmark 默认 K=4。本插件在 `engine.ts` 的 `orientRoundPairs()` 里按"谁更少坐 A 位谁坐 A 位"逐对定向，**不增加任何模型调用**。这只在 K=1（本插件自动路由的默认值）下等价于消除一个未修正偏好；K≥2 时两边等价，不能描述成"上游在所有配置下都有位置偏差"。
- **宿主门控**：自动路由、最终验收、计划预审、团队任务闸与预算策略都是 DSH 特有的运行策略，上游没有对应概念。

## 