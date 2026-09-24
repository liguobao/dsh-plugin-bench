# dsh-pi-tui

[English](README.en.md) | 简体中文

[![npm](https://img.shields.io/npm/v/@xmoon76/dsh-pi-tui.svg)](https://www.npmjs.com/package/@xmoon76/dsh-pi-tui)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

基于 Pi TUI 的 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 终端前端。

`dsh-pi-tui` 作为独立的 dsh bundle 安装到 profile 中，提供流式对话、工具调用、会话管理、Subagent、历史搜索、Shell、审批与设置等终端交互。模型、工具、Session、权限、Skills、Plan、Goal、Subagent 等运行时能力仍由 DeepSeek Harness 提供。

![dsh-pi-tui](docs/dsh-pi-tui.png)

## 安装到 DSH Profile

### Stable / latest

稳定版是普通用户的推荐渠道。请先安装 DSH，再将 TUI 添加到 `pi-tui` profile：

```sh
npm install -g --allow-scripts=@deepseek-ai/dsh-subprocess-local,koffi,node-pty,@google/genai,protobufjs,fs-ext @deepseek-ai/dsh@latest
dsh plugin --profile pi-tui -- add @xmoon76/dsh-pi-tui@latest
dsh --profile pi-tui
```

### Next / npm 线（验证）

预览安装使用 DSH 的 `alpha` channel 与 TUI 的 `next` channel；安装 DSH
时需要显式允许其原生安装脚本：

```sh
npm install -g --allow-scripts=@deepseek-ai/dsh-subprocess-local,koffi,node-pty,@google/genai,protobufjs,fs-ext @deepseek-ai/dsh@alpha
dsh plugin --profile pi-tui -- add @xmoon76/dsh-pi-tui@next
dsh --profile pi-tui
```

隔离的 npm 驱动仍按本 checkout 声明的精确 DSH 版本运行，并执行完整的
build/test/package 路径：

```sh
pnpm compat:dsh:npm
```

具体的稳定版最低版本、next 兼容范围和回退路径见[兼容性文档](docs/dsh-compatibility.md)。

### 环境要求

* DeepSeek Harness
* Node.js `^22.19.0 || >=24`

### DSH 与 TUI 版本对应（重要）

| TUI 包版本 | 对应的官方 DSH tags | 说明 |
|---|---|---|
| `0.4.6`（已发布 `@latest`） | `dsh-v0.1.5-rc.1`、`dsh-v0.1.5-rc.2` | 当前稳定版；最低 rc.1，兼容 rc.2 |
| 当前 `next` npm 线（本 checkout；版本 `0.4.5`） | `dsh-v0.1.5-rc.1`、`dsh-v0.1.5-rc.2` | 当前 next 线 |

不要把稳定线与 `next` 线混装。当前 `next` checkout 的 peer floor 是
`>=0.1.5-rc.1`，旧 runtime 会在正常的不兼容边界以非零状态失败。完整的
历史兼容矩阵和 fallback 命令见 [兼容性文档](docs/dsh-compatibility.md)；
要查看 next 的最新集成状态，请看 [next 分支 README](https://github.com/XMoon/dsh-pi-tui/blob/next/README.md)。

新的 Agent preset 使用当前 roster 中选定的 id。DSH 允许合法的自定义
`code` preset；只要当前 roster 存在它，显式输入和持久化状态都会保留 `code`。
DSH V3 migration 负责历史 session header/selection 的 `code -> ptc` 转换；
当前 projection 会原样保留合法的自定义 `code`。只有省略请求的 legacy
settings default `code` 才会在确认 roster 不含 `code` 后回退到 `ptc`。

### Profile management

更新已安装的 TUI：

```sh
dsh plugin --profile pi-tui -- update @xmoon76/dsh-pi-tui
```

查看已安装插件：

```sh
dsh plugin --profile pi-tui -- list
```

卸载：

```sh
dsh plugin --profile pi-tui -- remove @xmoon76/dsh-pi-tui
```

恢复已有 Session：

```sh
dsh --profile pi-tui --session <session-id>
```

## 功能

### 对话与工具

* 流式 Markdown 输出
* Thinking 折叠与展开
* Tool Call 卡片及运行状态
* Tool / System 详情折叠
* Transcript 全文搜索
* 长会话历史折叠
* Context、Token、模型和运行状态显示
* Approval 与 `ask_user_question` 交互
* Plan Review
* Todo / Goal 状态展示
* 可读的终端窗口标题
* 长会话按有界窗口浏览，并保留翻页与实时跟随位置
* Compaction / prune 后不会出现重复的幽灵 Tool Card

`Ctrl+O` 控制工具和系统详情;在全屏 Focus 下它整体展开最近几个 Thought root,或全部收起。`Alt+T` 单独控制 Thinking。

### Focus Mode

`/focus` 可以把运行中的 Thinking、Tool Call 和中间回复聚合为一个实时更新的 Thought 区块。

需要查看过程时可以展开，关闭 Focus 后恢复普通 Transcript 展示。全屏 Focus 中可以按 Thought root 批量展开/收起,也可以单独点击卡片;切换或缩放时会保留 viewport。Focus 只影响界面投影，不修改 Session 中保存的事件。

### Session

支持 DSH 持久化 Session，包括：

* 新建和恢复 Session
* Session 切换
* 重命名
* Fork
* Rewind
* Session lineage
* `/export` — 完整 Session 归档(含子代理与附件),保存到 Client 本地目录
* `/transcript` — 可读 Markdown 对话记录,保存到 Client 本地目录

使用：

```text
/sessions
/fork
/rewind
/export
/transcript
```

空闲且编辑器为空时也可以快速按两次 `Esc` 打开 Rewind。

Rewind 会从选中的历史 User Turn 创建新的 Child Session，并把对应 Prompt 放回编辑器。原 Session 不会被修改。

### 输入历史

`Ctrl+R` 打开输入历史搜索。

支持三个范围：

* Current session
* Current directory
* All directories

历史结果包含 Prompt、工作目录、时间和 Session 信息。选中历史后只恢复到编辑器，不会立即发送。

普通的 `↑` / `↓` 仍用于快速浏览最近输入。

### Subagent 与后台任务

`/tasks` 打开完整 Task Center（当前 Session 的所有后台工作）；Footer 的 `↓` 直接打开轻量 Quick Tasks（只看正在运行的工作）。

Subagent 按完整 lineage 显示，包括嵌套创建的 descendant：

```text
main
├─ subagent A
│  └─ subagent B
└─ subagent C
```

浏览器会区分：

* `continuable`
* `one-shot`
* running / inactive
* nested descendant
* 后台 Job

两个视图共享同一份运行时状态：`A` 切换 Active / All scope，`Tab` 切换类型过滤，`/` 进入搜索，`S`（确认后）停止所选任务，`N` / `Shift+N` 在运行中的任务间跳转，Quick 内 `T` 或底部 "View all" 行进入完整 Task Center，`Esc` 逐层返回。

已经结束的 one-shot Subagent 仍可以打开并查看持久化 Transcript。

对于当前 Session 的直接 `continuable` Child，可以进入交互式 Viewer，并直接向该 Subagent 发送后续消息（走 DSH 官方 `subagents.prompt()` 人类输入通道——按顺序排队为 Child 自己的下一个 turn，并保留 user 来源）。Child 使用自己的 Transcript、Draft 和运行状态，不会修改主 Session 的输入。

更深层的 nested Subagent 默认以只读方式查看。

官方 Subagent 模型选择（DSH `subagent-model-selection` 设置）可在 `/settings`
中开关并维护 allowlist：开启后**新建** Session 的官方 `subagent` 工具可以按调用
选择子 Agent 的 provider/model（受 allowlist 限制）。设置在 Session 组合时采样，
不会改写已在运行的 Session 的工具。

### Shell

编辑器支持两种 Shell 模式：

```text
! git status
```

执行本地命令，并把输出提交到当前 Session。

```text
!! git status
```

只在本地执行，输出不会进入模型上下文。

`!` / `!!` 是独立的编辑器模式，而不是普通文本前缀。进入 Shell 模式后 Prompt 和补全行为会同步切换。

Shell 卡片默认只显示有限的输出预览，`Ctrl+O` 可以展开完整保留内容——全屏 Focus 除外:那里 `Ctrl+O` 负责 Thought root 的整体开关,Shell 卡片保持折叠。

### 文件引用与图片

输入 `@` 可以搜索和补全工作区文件：

```text
@src/index.ts
@"path with spaces/file.ts"
```

`/attach <path>` 是统一的 Client-local 图片/文件入口；`/image <path>` 保持图片专用兼容语义。两者都支持文件与目录补全；带空格、引号或 Windows 分隔符的路径会保留输入方言，目录可以继续展开。

能够解析的相对路径会在提交时转换为明确的文件路径。

支持通过 `Ctrl+V` 添加剪贴板图片，并使用 DSH Attachment 能力保存到 Session。

### 模型与运行设置

TUI 使用 DSH 提供的模型和设置服务。

常用入口：

```text
/model
/settings
/login
/permission
/plan
/goal
/compact
/footer
/statusline
```

模型切换、Reasoning Effort、权限 Preset、Plan 和 Goal 都沿用 DSH 对应的运行时语义。

`/settings` 中的 `Icon style` 可切换 TUI 结构图标的风格:`Emoji`(默认,
彩色)、`Symbols`(紧凑的单格终端符号)、`Minimal`(隐藏装饰性图标,只
保留状态/交互标记);切换立即生效并持久化。

其他插件注册到 `ctx.commands` 的 Slash Command 也会被自动发现。

### Footer 自定义

`/footer` 提供交互式 Footer 编辑器。你可以组合内置状态条目，调整左右位置、顺序、Style、Tone、Prefix/Suffix 和 Importance，也可以创建自己的 Footer 条目。

支持四类条目：

- **Builtin Item**：Model、Context、Token、Tasks、Git branch 等内置状态；
- **Custom Text**：用户创建的固定文本；
- **Custom Command Item**：用户创建的动态命令输出，可和其他条目一起排列；
- **Extension Item**：插件通过 Stable Extension API 提供的 Footer 条目。

在窄终端中，支持 compact 的内置条目会先自动缩短；空间仍不足时再按 Importance 隐藏低优先级内容。运行时 compact 不会修改你保存的 Style。

`/footer` 的 Custom Command Item 和 `footer: command` 是两种不同能力：前者只是一个可以与 Model、Context 等混排的动态条目；后者把整个 Footer 状态表面交给一个用户命令。

完整的 `/footer` 使用方法、Custom Text / Command、YAML 配置、安全模型和排错说明见：

- [Footer 自定义完整指南](docs/footer-customization.md)
- [Extension API（插件作者）](docs/extension-api.md)

`/statusline` 是 `/footer` 的别名。

## 常用按键

| 按键            | 功能                     |
| ------------- | ---------------------- |
| `Enter`       | 提交输入                   |
| `Ctrl+Enter`  | 与 Enter 的忙碌行为相反(默认 steer,`busyEnter=steer` 时入队) |
| `Shift+Enter` | 换行                     |
| `Esc`         | 取消当前交互 / 中断运行          |
| `Esc Esc`     | 空闲时打开 Rewind           |
| `Ctrl+C`      | 键盘退出确认;首次清空草稿       |
| `Ctrl+D`      | 空草稿时键盘退出确认;有内容时向前删除 |
| `Ctrl+S`      | Steer:把队列消息和草稿一起发送到正在运行的回合 |
| `Ctrl+T`      | 切换 Todo 面板              |
| `Ctrl+R`      | 搜索输入历史                 |
| `Ctrl+F`      | 搜索 Transcript          |
| `Ctrl+End`    | 全屏时跳到最新 Transcript 输出 |
| `Ctrl+O`      | 展开 / 折叠工具和系统详情;全屏 Focus 下整体切换 Thought root |
| `Alt+T`       | 展开 / 折叠 Thinking       |
| `Ctrl+G`      | 使用 `$VISUAL`/`$EDITOR` 编辑输入 |
| `Ctrl+V`      | 粘贴图片                   |
| `Tab`         | 补全斜杠命令与文件路径           |
| `@`           | 文件补全                   |
| `!`           | 进入 Shell 模式            |
| `!!`          | 进入 Local-only Shell 模式 |

完整按键和命令以 TUI 中的 `/help` 为准。表中的快捷键是默认值;用户自定义后,以 `/help` 和 `/keybindings` 显示的生效键位为准。

### 自定义快捷键

Host 快捷键是语义 action(`app.*`),通过 context-aware keymap 解析——
UI(页脚提示、`/help`、`/keybindings`)始终显示**生效**的按键,因此
改键后所有提示自动更新。在 `dsh-pi-tui` settings 命名空间中配置,
然后用 `/keybindings reload` 应用(显式 reload——改设置后执行 reload
即生效,无需重启):

```yaml
dsh-pi-tui:
  keybindings:
    app.input.steer: ctrl+s          # 单个按键
    app.permission.cycle: [shift+tab, ctrl+shift+p]   # 多个按键
    app.history.search: ctrl+r
    app.transcript.toggleThinking: false   # 禁用该 action 的按键
    leader: ctrl+x                    # M6:leader 序列
    bindings:
      app.tasks.open: <leader>t
```

- 普通可打印键永远不能绑定到 Host a