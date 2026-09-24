# dsh-tianshu-tui — DeepSeek Harness coding 终端 

[![npm](https://img.shields.io/npm/v/@huiliyi37/dsh-tianshu-tui.svg)](https://www.npmjs.com/package/@huiliyi37/dsh-tianshu-tui)
[![license](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![node](https://img.shields.io/node/v/@huiliyi37/dsh-tianshu-tui.svg)](https://www.npmjs.com/package/@huiliyi37/dsh-tianshu-tui)
[![release](https://img.shields.io/github/v/release/huiliyi37/dsh-tianshu-tui?include_prereleases)](https://github.com/huiliyi37/dsh-tianshu-tui/releases)
[![dshfind](https://dshfind.com/api/badge/huiliyi37/dsh-tianshu-tui?lang=zh)](https://dshfind.com/zh/plugins/huiliyi37/dsh-tianshu-tui?ref=badge)

中文 | [English](README.en.md)

![dsh-tianshu-tui](docs/promo.png)

**dsh-tianshu-tui**是官方 [DeepSeek Harness] 上的交互式终端 TUI 面板插件。渲染核心为自研极简 ANSI引擎，轻量渲染使用体验极度流畅。（由作者的[天枢 Tianshu-harness] https://github.com/huiliyi37/Tianshu-harness 演进而来。UI 是纯展示层：所有 agent 状态都来自会话事件流，流式 Markdown/工具卡、16+ 主题、slash 命令与选择器、输入历史与本地偏好持久化、LSP 诊断。在此之上做了工程层的改造，如图像与视觉桥接、代码智能检索、memory记忆与跨会话召回等。


## 文档

| 文档 | 说明 |
|---|---|
| [快速开始](docs/getting-started.md) | 安装、启动与常见问题 |
| [交互手册](docs/interaction.md) | 快捷键与命令全表 |
| [配置](docs/configuration.md) | 装配选项、环境变量与运行时配置 |
| [架构](docs/architecture.md) | 分层、数据流与设计决策 |
| [主题](docs/themes.md) | 16 个内置主题与自定义 |
| [插件生态](docs/plugins.md) | 伴生插件与扩展点 |
| [VS Code](docs/vscode.md) | 在 VS Code 中使用 |
| [ADAPTER.md](ADAPTER.md) | TUI ↔ harness 边界契约 |
| [贡献指南](CONTRIBUTING.md) | PR 规范与验证矩阵 |
| [开发说明](DEVELOPING.md) | 结构、构建与发布 |

## 安装

本包不是独立程序。须先有官方 CLI [`@deepseek-ai/dsh`](https://www.npmjs.com/package/@deepseek-ai/dsh)（npm `latest`，当前 `0.1.5-rc.1`；需 ≥ `0.1.5-rc.1`，peer 依赖对齐）。只 `npm i` 本包跑不起来。

**一键安装（推荐）**：仓库自带跨平台脚本，自动检测 Node/pnpm、经 pnpm 安装官方 CLI + 装配本插件并启动（国内网络默认走 npmmirror 镜像）：

```sh
# macOS / Linux（bash）
bash <(curl -fsSL https://raw.githubusercontent.com/huiliyi37/dsh-tianshu-tui/main/scripts/install-tui.sh)
# 只安装不启动：
bash <(curl -fsSL https://raw.githubusercontent.com/huiliyi37/dsh-tianshu-tui/main/scripts/install-tui.sh) --no-launch

# Windows（PowerShell）
powershell -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/huiliyi37/dsh-tianshu-tui/main/scripts/install-tui.ps1 | iex"
# 只安装不启动：
powershell -ExecutionPolicy Bypass -File scripts\install-tui.ps1 -NoLaunch   # 克隆仓库后本地跑
```

### 1. 准备环境

- [Node.js](https://nodejs.org/) `^22.19 || >=24`
- [`pnpm`](https://pnpm.io/installation)（`dsh plugin` 会转发给它；没有时 `corepack enable` 即可——Node 自带 corepack）

> ⚠ **npm 11 的 OOM 坑**：官方 CLI `@deepseek-ai/dsh` 依赖树较大（60+ 子包），**npm 11（Node 24 自带）安装时会 JavaScript heap out of memory**（卡住数分钟后 OOM，实测复现）。请用 pnpm（下方命令）。若你已经在用 `npx -y @deepseek-ai/dsh` 且卡住/报 heap OOM，切到 pnpm 即可。

**不要直接敲 `dsh`。** 若 PATH 上已有旧的 `dsh`（例如 `~/.local/bin/dsh`，`dsh --version` 低于 `0.1.0-rc.8`），会走到本地 staging，出现 `ERR_FS_EISDIR` / `Path is a directory .../@deepseek-ai/dsh`。请始终用下面的 `pnpm dlx` 命令。

### 2. 把本插件装进 tui profile

```sh
pnpm dlx @deepseek-ai/dsh plugin --profile tui add @huiliyi37/dsh-tianshu-tui
```

pnpm 可能提示 peer missing，可忽略：peer 由官方 `dsh` 宿主提供，不必另装。没有 pnpm 也可以 `npx -y pnpm dlx @deepseek-ai/dsh plugin --profile tui add @huiliyi37/dsh-tianshu-tui`。

从 npm 安装后，每次启动会对照 npm `latest`：有新版本就写入 profile，提示重启后生效。也可在 TUI 里敲 `/update` 手动检查（只查不装，给出更新命令）。不想联网检查时设 `DSH_TUI_SKIP_UPDATE=1`。`github:` / `link:` 安装不会改写成 npm 包。

也可以从 Git 装：`pnpm dlx @deepseek-ai/dsh plugin --profile tui add github:huiliyi37/dsh-tianshu-tui`（仓库已包含 `lib/index.js`，不必再打包）。

### 3. 启动

```sh
pnpm dlx @deepseek-ai/dsh --profile tui
```

看到欢迎页品牌 **dsh-tianshu-tui** 即成功。`Ctrl+Q` 或 `/exit` 退出。

已全局安装官方 CLI（`pnpm add -g @deepseek-ai/dsh`）且 `dsh --version` 不低于 `0.1.0-rc.8` 时，把上面的 `pnpm dlx @deepseek-ai/dsh` 换成 `dsh` 即可。

### 4. agent 预设（`/preset`）

命令是 `/preset`（没有 `/presets`）。本包 bundle 对标官方 web：关掉 host 上的 agent 面，挂上 `@deepseek-ai/dsh-agent-presets`（依赖钉死 `0.1.5-rc.1`，npm `latest` 仍停在过时的 `0.0.1-rc.1`）。`plugin add` 本包即连带装上花名册；新会话在 `setup` 里 `mount`，`/preset` 换的是官方 shipped 面（标准 / PTC / 极简 / 创造），不是叠在 `dsh-base` 工具上。

用法：

- `/preset` —— 列出每套预设的能力与工具集，`*` 标当前项；footer / 欢迎顶栏也会显示当前短名（标准 / PTC / 极简 / 创造）。说过话后还附最近一次请求的 `wire:` 工具面
- `/preset <id>` —— 切换到指定预设（仅空白会话可换：先 `/session new` 再切；`ptc`/`creative` 是 `code`/`cordis` 的别名）

若 `npx` 仍报 `ERR_FS_EISDIR`，是 `~/.dsh/profiles/node_modules` 里旧的安装 fallback 与官方 CLI 冲突。换干净目录再启动：

```sh
DSH_HOME=/tmp/dsh-tianshu pnpm dlx @deepseek-ai/dsh plugin --profile tui add @huiliyi37/dsh-tianshu-tui
DSH_HOME=/tmp/dsh-tianshu pnpm dlx @deepseek-ai/dsh --profile tui
```

不要在 DeepSeek Harness 工作区根目录对本包跑 tsdown：会把未发布的 `@deepseek-ai/dsh-root` 写进 bundle，加载必失败。

需要图片再询问能力时，再装配同仓伴生包 `vision-ask/`。LSP 模型工具面（`lsp_goto_definition` / `lsp_find_references` / `lsp_diagnostics`）已随本包内置（`@huiliyi37/dsh-lsp` 伴生插件，bundle patch 自动 insert）——装 TUI 一个包即得展示桥 + 模型工具面，二者共享同一 LSP server 集（不双份 spawn）。TUI 桥的诊断源探测顺序：内置伴生插件 `lsp` 服务（getDiagnostics 形状）→ 官方 `ctx.lsp` seam（deepseek-harness 的 dsh-lsp，经 query(getDiagnostics) 适配）→ 内置桥降级。⚠ 此前单独装过旧社区版（`github:omdsh-dev/dsh-lsp`）的用户请先 `plugin remove` 旧版再升级——新旧同时装配会重复注册同名模型工具。

## 更新说明

当前 npm `latest`：[`@huiliyi37/dsh-tianshu-tui@1.0.0-rc.1`](https://www.npmjs.com/package/@huiliyi37/dsh-tianshu-tui)（[GitHub Release](https://github.com/huiliyi37/dsh-tianshu-tui/releases/tag/v1.0.0-rc.1)）。

**1.0.0-rc.1（2026-09-14）**：1.0.0 的首个候选版，版本号进入 1.0 线。收录 0.1.2-rc.31 之后的四项收敛——**重试路径正文丢失修复**（LLM 重试成功后该 step 的正文曾被整段丢弃：宿主每次尝试都是独立 attempt，按 step 粒度去重是模型性错误）；失败尝试的正文前落 `⟳ 未完成的尝试` 标记，避免它与成功正文被读成一段连续答案；assistant 流语义合并到 `adapter/assistant-stream` 单点维护（此前四处各自实现，同一宿主行为变更需四处联动）；移除两处无消费方的死状态（`SessionManager` 快照层、`TranscriptView.streaming` 聚合）。⚠ 需宿主 ≥ 0.1.5-rc.1；node ≥ 24.4。

**0.1.2-rc.31（2026-09-14）**：修复 #58——0.1.5 宿主正常回合的助手正文不渲染（attempt 事件只在报错/中断路径出现，正常回合正文随 assistant/message 内嵌流到达；现于 message 边界回退渲染，防重复由同 step 流式增量把关）。⚠ 需宿主 ≥ 0.1.5-rc.1；另请确保 node ≥ 24.4（0.1.5 宿主 CLI 入口依赖 `import.meta.main`，过旧 node 下静默无输出）。

**0.1.2-rc.30（2026-09-12）**：宿主线上到 0.1.5（官方 `latest` 已切 0.1.5-rc.1）——流式事件 `assistant/chunk`→`assistant/attempt` 批量改批、sessionPersistence 新契约（快照列表 + open/read 句柄）、遗留库时间渲染防御；真机 pty e2e 全绿。⚠ 需宿主 ≥ 0.1.5-rc.1。

**0.1.2-rc.29（2026-09-09）**：宿主线上到 0.1.2-rc.1（官方 `latest` 已转正，修复 #56 启动即崩）——`Session.events` 移除改 `snapshotEvents()`、userQuestions 改 waterfall answerer（global 注册）、`CallId→ToolCallId`、preset `code→ptc`、fork 血缘改 `isSeeded`+`inheritedEventCount`、bundle patch 补 `subagent-model-selection-settings`；旧宿主（≤0.1.1-rc.2）启动即 fail-loud 附升级/回退指引。⚠ 本次升级需宿主 ≥ 0.1.2-rc.1。

**0.1.2-rc.28（2026-08-29）**：回应 #55 的 vim 优化——光标形态分模式（NORMAL 反色块 / insert 竖线）、历史搜索两阶段输入（编辑段可输 n/N，`Enter` 后跳转、搜索对象显式标注）、搜索命中子串高亮（含 `/scroll`）；另投递失败自动回填输入行 + README 键位表一致性守卫。

**0.1.2-rc.27（2026-08-29）**：回流 Tianshu 两项——错误时刻可行动（错误落底 + 指引之外，最近一条已投递消息自动回填输入行，`↩` 告知「可能未被完整处理」，改一下即可重发；成功回合清底料、有草稿不抢写）；plan-review 决策卡视觉分层（dim 决策区分隔线 + approve `❯`/success 主操作高亮，主题不传时渲染不变）。




**0.1.2-rc.23（2026-08-27）**：LSP 三件套对齐上游 0.6.0 官方 seam 线（单 `lsp` 工具四操作 + 本地 provider 默认 tsserver），诊断源能力门控防 `/lsp` 面板退化；宿主 peer 对齐 `^0.1.1-rc.2`。

**0.1.2-rc.22（2026-08-27）**：LSP 模型工具面随包内置首版（伴生插件自动挂载，装 TUI 一个包即得展示桥 + 模型工具面；旧社区版请先移除）。

**0.1.2-rc.21（2026-08-27）**：社区反馈三连修——输入框光标反色化（#50）、preset 缺省 standard（#48）、`malformed SSE payload` 根因定位并上报官方（#49）。

完整版本历史见 [CHANGELOG.md](CHANGELOG.md)；TUI 内 `/changelog` 查看（`/changelog all` 全部）。

## 亮点

- **终端内的完整会话工作区** — 实时渲染、只增滚动转录、启动时会话恢复、`/fork` 探索分支、`/rewind` 回退（会话截断 + 可选文件回退）、`/export` 导出 Markdown 转录、中轮转向（`/steer` / `Ctrl+T`）。
- **图片端到端** — 剪贴板粘贴（`Ctrl+V` / 终端菜单粘贴）、以终端图形协议内联渲染（kitty / iTerm2）、经 harness 附件服务投递、让具备视觉能力的模型真正看见——主模型不识图时自动经独立视觉模型把图片转成描述（视觉桥）。
- **完整输入面** — grok 风格 slash 下拉菜单（模糊前缀匹配、MRU 排序、ghost 预览）、`@`-路径 Tab 补全与 `@mention` 展开、bracketed paste、可选 vim 键位、外部编辑器（`Ctrl+E`）、历史搜索（`Ctrl+F`/`Ctrl+R`）——`Ctrl+.` 随时调出完整键位表。
- **终端内交互面** — 结构化提问面板（数字键选择、plan-review 反馈模式）、带内联 `diff` 预览的挂起审批卡片、模式循环（`Shift+Tab`：normal → plan → always-approve）、命令面板，以及 status / config / skills / tasks / 委派树 / workflow 实时面板。
- **推理过程可视化** — think 通道以实时头行流动、在滚动区折叠为紧凑行（`✻ 思考 (3.2s) · 12 行`）、`Ctrl+O` 原位展开（对标竞品：默认折叠）。
- **个性化 harness 集成** — `/doctor` 终端诊断、`/memory` 项目记忆浏览器、`/btw` 后台 agent 侧问、`/model` + `/eff