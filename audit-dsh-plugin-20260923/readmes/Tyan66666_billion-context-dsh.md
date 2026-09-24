# billion-context-dsh

[中文](./README.md) | [English](./README.en.md)

> **⚠️ 测试版声明——请勿用于生产环境**
> 本项目（**v0.2.25**）仍处于开发中的测试版。[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 本身也处于**公开测试版**阶段。**请勿将两者用于工程化 / 生产环境**——预期会有破坏性变更与粗糙之处。

<p align="center">
<strong>衷心感谢以下项目——请给它们一个 ⭐：</strong>
<br />
<a href="https://github.com/deepseek-ai/deepseek-harness">DeepSeek Harness</a> ·
<a href="https://github.com/ranxianglei/billion-context-pi">billion-context-pi</a> ·
<a href="https://github.com/ranxianglei/acp-kernel">acp-kernel</a> ·
<a href="https://github.com/ranxianglei/opencode-acp">opencode-acp</a>
</p>

<p align="center">
<strong>Billion-Context</strong> for <a href="https://github.com/deepseek-ai/deepseek-harness">DeepSeek Harness</a>
<br />
由模型决定<em>何时</em>压缩、<em>压缩什么</em>——而不是一个硬性上限。
</p>

---

<p align="center">
<a href="https://www.npmjs.com/package/billion-context-dsh"><img src="https://img.shields.io/npm/v/billion-context-dsh.svg?style=flat-square" alt="npm"></a>
<a href="https://github.com/Tyan66666/billion-context-dsh/blob/main/LICENSE"><img src="https://img.shields.io/npm/l/billion-context-dsh.svg?style=flat-square" alt="license"></a>
<a href="https://github.com/Tyan66666/billion-context-dsh"><img src="https://img.shields.io/badge/GitHub-Tyan66666%2Fbillion--context--dsh-181717?style=flat-square&logo=github" alt="GitHub"></a>
<a href="https://github.com/topics/dsh-plugin"><img src="https://img.shields.io/badge/topic-dsh--plugin-blue?style=flat-square" alt="dsh-plugin"></a>
</p>

<p align="center">
<code>npm install billion-context-dsh</code>
</p>

---

## 为什么？

当对话变长，模型会耗尽上下文。多数工具直接硬截断——悄悄丢弃早期消息。**billion-context-dsh** 给模型一个 `compress` 工具：由 LLM 决定**何时**、**压缩什么**，写成高保真摘要，保留关键细节（文件路径、决策、错误信息）的同时回收上下文空间。

与 DSH 内置的自动压缩（用自动生成的摘要替换一段范围）不同，billion-context-dsh：

- **模型驱动** —— 摘要由模型自己书写，没有第二次 LLM 摘要调用
- **只建议、不强令** —— 自动策略只 *nudge*（提醒），是否压缩、何时压缩由模型决定
- **持久且可恢复** —— 压缩范围成为 checkpoint 节点，原文保留在 append-only 会话日志中；`decompress` 可恢复，`search_context` 可在块内查找
- **长任务稳得住** —— 每一步都接着前面的成果走，关键结论持续可用、不断叠加，超长任务更容易跑完
- **上下文始终精简** —— 每次请求都只用少量、精炼的上下文，只保留关键信息；不做大段统一压缩，细节不随之衰失，token 消耗自然更低

这是 [billion-context-pi](https://github.com/ranxianglei/billion-context-pi)（Pi 编码代理适配器）在 DeepSeek Harness 上的移植：压缩内核（[acp-kernel](https://github.com/ranxianglei/acp-kernel)）原样复用，适配层针对 DSH 的 durable-surface 模型重写——经过验证的映射关系见 [docs](https://github.com/Tyan66666/billion-context-dsh/tree/main/docs)。

## 安装

> 💡 **想让 DeepSeek Harness 帮你装？** 本仓库本身就运行在 DSH 上：把
> [docs/INSTALL.md](docs/INSTALL.md) 交给会话里的 agent，它会读取指南、解析
> 你的 profile、编辑组合配置并验证挂载。前提：① 配置写在 `~/.dsh` 下，需要
> 你批准一次文件权限；② 装完让它调用 `acp_status` 自证。

**方式一（推荐）：DSH 商店 / `dsh plugin` 一键装（bundle）——装完即全局生效，零配置。**

在 DSH 的插件商店里点安装，或命令行执行：

```bash
dsh plugin --profile web add billion-context-dsh
```

命令内部会装包并把本包的 bundle 补丁（[cordis.patch.yml](cordis.patch.yml)）自动挂进该 profile 的层栈。补丁做了两件事：

- **禁用 host 的 `compaction-basic`**——避免同一 realm 内两个后端同时注册 `ctx.compaction` 冲突（现代 DSH 的 web bundle 已自带该禁用，此行为幂等兜底，任何受支持版本下都成立）；
- **把 ACP 引擎挂到 host 平面**——四种模型工具（`compress` / `decompress` / `search_context` / `acp_status`）、`/acp-prune` 命令、nudge、ACP 提示词段对该 profile 的**所有模式**（standard / code / minimal / cordis / 自定义预设）生效。窗口自动探测、工具/命令/nudge 默认全开，**无需任何手工配置**。

装完**重启 `dsh`**（bundle 层在启动时组合），新开会话即可用——让模型调用 `acp_status` 或执行 `/acp-prune status` 自证。shipped 预设（standard / code / cordis）内部的 realm 级 `compaction-basic` 自动压缩兜底仍然保留（这些模式里"自动摘要"照旧，ACP 工具与 nudge 并存）；minimal 等不带 compaction realm 的预设直接使用本引擎。

> **与 DSH 版本的兼容性。** 包把五个运行期 seam 包（`dsh-compaction` /
> `dsh-session` / `dsh-llm` / `dsh-tools` / `dsh-settings`）都声明为 peer
> 依赖，共享同一个
> 范围 `>=0.1.5-alpha.1 <0.1.6-0`——恰好是整条 `0.1.5` 线（所有预发布加最终
> `0.1.5`）。从 `0.1.5` 线起，会话 replace 操作的协议字段由 `{ op, start, end }`
> 改名为 `{ op, startSeq, endSeq }`，且校验严格（只接受这三个字段）；本引擎只
> 输出新形态，因此在更旧的 DSH（< 0.1.5）上每次 `compress` 都会被宿主在运行时
> 拒绝（issue #136）——旧版本不再受支持，请先升级 DSH 再安装本发行版。范围
> 写成显式区间而非 caret 是**有意为之**：caret 会悄悄放进未经验证的 0.1.6+
> 线。把这五个 seam 包一并声明为 peer（而不只是 `dsh-compaction`），是为了让
> 安装在 pnpm 的集成/封存布局下仍能把它们解析到**宿主自己的副本**，而不是
> 某个与宿主不一致的陈旧嵌套副本。
>
> 行为注记（0.1.5 起）：宿主不再允许"不可见"替换节点，引擎清理孤立工具消息时
> 会在其位置留下一条短可见占位消息；宿主的系统提示节点（surface node 0）被排除
> 在可压缩范围表之外。

**方式二：纯 `npm install`（只装包，需要手写组合行）。**

```bash
npm install billion-context-dsh
```

这只把包装进你的项目/全局，**不会**触碰任何 profile——请按下方「两种生效范围与自定义」手写组合行，引擎才会挂载。

**git 源安装（`github:` 规格，插件商店展示的形态）。** 预构建产物 `dist/` 已提交到仓库，从 git 源安装同样开箱即用——**无需任何构建步骤**，pnpm 11 默认拦截构建脚本（`allowBuilds`）的机制对这个包不构成障碍：

```bash
dsh plugin --profile web add github:Tyan66666/billion-context-dsh#v0.2.25
```

建议带 `#<tag>` 安装，拿到与对应 npm 版本完全一致的产物；不带 ref 则装默认分支的最新构建。只有 clone 仓库自行从源码构建（`npm run build`）才需要放行构建。背景与方案取舍见 [docs/git-source-install-design.md](docs/git-source-install-design.md)（issue #92）。

## 两种生效范围与自定义

本节服务于两类人：① 方式二（纯 npm 安装，必须手写组合行）；② 方式一用户想自定义 `config`（bundle 已有默认行为，只需用**同 id** 行覆盖）。

**自定义 config（方式一 bundle 用户）。** 在你的 profile 补丁（如 `~/.dsh/profiles/web/cordis.patch.yml`）里追加一个 `compaction-acp` 行并附 `config:`——同 id 行覆盖 bundle 的默认行：

```yaml
- id: compaction-acp
  name: 'billion-context-dsh'
  config:
    modelContextLimit: 128000   # 可选；省略时自动探测模型真实窗口（回退 128000）
```

**全局生效（host 平面，所有模式）——推荐**。这是方式一 bundle 的默认行为；纯 npm 安装的用户在 profile 补丁中追加以下全部内容（bundle 用户跳过前两行）：

```yaml
# ACP 作为全局压缩后端：四个模型工具 + `/acp-prune` 命令 + nudge + ACP 提示词段，
# 对所有模式（standard / code / minimal / cordis / 自定义预设）生效。
# 必须同时禁用 host 的 compaction-basic：同一 realm 内两个后端同时
# provide `ctx.compaction` 会冲突。（bundle 安装已自动带上这两行。）
- id: compaction-basic
  disabled: true

- insert:
    - id: compaction-acp
      name: 'billion-context-dsh'
      config:
        modelContextLimit: 128000   # 可选；省略时自动探测模型真实窗口（回退 128000）
```

**（可选）自定义提示词文案 —— `config.prompts`。** 所有模型可见的提示词（普通/紧急 nudge 首句、上下文分解、增长行、批量提示、tier 蒸馏行、范围表、ACP system prompt 段、四个工具描述）默认**直接复用 acp-kernel 的 `renderNudgeText`**——效率提示、上下文分解、压缩规则、批量提示全部来自 kernel 原文，仅范围表换成 surface-seq 版（kernel 用 mNNNNN 引用，我们架构没有 `<acp>` 标签；seq 范围表同样携带 `[tool X% | text Y%]` 组成占比并 oldest-first 排序，与 kernel 展示语义一致）。覆盖任一 nudge 槽位后自动切换到模板渲染。模板支持命名占位符（如 nudge 的 `{pct}`、`{philosophy}`、范围表的 `{surface}`），**构造期校验**：占位符拼写错误会在引擎启动时抛错（fail-fast），而不是把字面 `{pct}` 漏进模型上下文：

```yaml
      config:
        modelContextLimit: 128000
        prompts:
          nudge:
            normal: '上下文使用率 {pct}%。这是效率提示——请尽早压缩保持上下文精简。'  # 中文 nudge 首句
          tools:
            acpStatus: '报告 ACP 块账本：压缩块数、回收 token、当前上下文压力。'  # 自定义工具描述
```

可配置槽位清单、每槽可用占位符、空串/`null` 语义见 [docs/configurable-prompts-design.md](docs/configurable-prompts-design.md)。未配置 `prompts` 的部署直接使用 kernel 渲染（对齐 kernel/pi，见设计文档 v6）。

**（可选）运行时设置 —— 编辑 `~/.dsh/settings.yaml` 或 `/acp-prune config`，无需重启。** 六个标量键（`modelContextLimit`、`autoModelContextLimit`、`nudgeMinContextLimitPct`、`nudgeMaxContextLimitPct`、`nudgeEmergencyThresholdPct`、`autoNudge`，见「配置」表中带「运行时热调」标记的行）在宿主 settings 层有一份可热改的副本：编辑 settings 文件或 `/acp-prune config` 会**立即生效于运行中的会话**（组合行 `config:` 仍是起点——分层为 schema 默认 → 组合行 → 用户 settings 段）：

```yaml
# ~/.dsh/settings.yaml
compaction-acp:
  nudgeMaxContextLimitPct: 0.72   # 保存即生效，无需重启
```

```text
/acp-prune config                                  # 列出六个键当前值 + 来源层（user / base / default）
/acp-prune config set nudgeMaxContextLimitPct 0.72 # 热改一个键
/acp-prune config set autoNudge false              # 布尔键（false 是合法值）
/acp-prune config reset nudgeMaxContextLimitPct    # 退回组合行 / 引擎默认
/acp-prune config reset all
```

窗口相关键（`modelContextLimit` / `autoModelContextLimit`）改动会清空窗口探测缓存——下一次 pre-step 按新值重新探测（探测失败也会被缓存，正是靠这个机制在修复网关后重新探测）。无 settings provider 的纯 npm 安装组合下 `/acp-prune config` 降级为指引文案；`settingsEnabled: false` 可整体关闭该集成（组合行专用，不进 settings 层——开关不能关掉自己）。设计细节见 [docs/settings-integration-design.md](docs/settings-integration-design.md)。

**单模式生效（agent preset 的 `compaction` realm）**。先在该 realm 内*禁用（或删除）原有的 `dsh-compaction-basic` 行*，再插入本引擎——同一 realm 内两个后端不能并存：

```yaml
# 先禁用 realm 内默认后端（或直接删掉这一行）
- id: compaction-basic
  disabled: true

# 再插入本引擎
- id: compaction-acp
  name: 'billion-context-dsh'
  config:
    modelContextLimit: 128000   # 可选；省略时自动探测模型真实窗口（回退 128000）
```

> **每个 agent 只留一个上下文管理器。** 两个后端同时 provide `c