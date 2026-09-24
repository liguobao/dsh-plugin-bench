# dsh-ssh-tui

[![npm](https://img.shields.io/npm/v/dsh-ssh-tui?style=flat-square&color=4b6fff)](https://www.npmjs.com/package/dsh-ssh-tui)
[![npm downloads](https://img.shields.io/npm/dm/dsh-ssh-tui?style=flat-square)](https://www.npmjs.com/package/dsh-ssh-tui)
[![CI](https://github.com/cyjyyd/dsh-ssh-tui/actions/workflows/ci.yml/badge.svg)](https://github.com/cyjyyd/dsh-ssh-tui/actions/workflows/ci.yml)
[![dshfind](https://dshfind.com/api/badge/cyjyyd/dsh-ssh-tui)](https://dshfind.com/zh/plugins/cyjyyd/dsh-ssh-tui?ref=badge)

给跳板机、无桌面服务器、高延迟 SSH 用的 DeepSeek Harness 终端。纯 ANSI、增量重绘，
不需要浏览器。

English: [README.en.md](README.en.md)

如果你主要在 SSH 里写代码——公司跳板、测试机、只有键盘的会话——可以从这里开始。
本机桌面终端若更在意主题和布局，也可以继续用你已经习惯的界面。

已经在付 SuperGrok / X Premium 的话，用独立插件 [dsh-llm-xai-oauth](https://github.com/cyjyyd/dsh-llm-xai-oauth) 把订阅接进 dsh（headless / web / 本 TUI 都能用），复用本机 grok-bridge token，不需要 xAI API Key。

本插件已被 [dshfind 插件目录](https://dshfind.com/zh/plugins/cyjyyd/dsh-ssh-tui) 收录：

[![dshfind](https://dshfind.com/api/card/cyjyyd/dsh-ssh-tui?lang=zh)](https://dshfind.com/zh/plugins/cyjyyd/dsh-ssh-tui?ref=badge)

安装（官方 CLI，无需 clone）：

```bash
dsh plugin --profile tui add dsh-ssh-tui@latest
dsh --profile tui
```

当前 `dsh` 必须带 `--profile`（`dsh plugin add …` 会报缺选项）。装进别的 profile 把 `tui` 换成那个名字即可。

**更新必须带 `@latest`。** `dsh plugin` 只是把后面的参数转给 profile 目录里的 pnpm。写成 `add dsh-ssh-tui`（没有版本）时，pnpm 会沿用 `pnpm-lock.yaml` 里已经钉死的版本（常见就是一直停在 0.3.7）。也不要把 `--profile` 写到 `add` 后面：`dsh plugin add --profile tui add dsh-ssh-tui` 不是合法用法。卸载：`dsh plugin --profile tui remove dsh-ssh-tui`。

## 官方 headless 和这个 TUI

官方没有预置 TUI。远程机器上的默认终端入口是 `dsh --profile headless`：跑完一个任务，把**最后一条助手回复**打到 stdout 就退出。思考、工具调用、子代理、计划都在会话日志里，终端上看不到。

下面两帧是**同一条任务**。上：官方 headless 的 stdout（按 `@deepseek-ai/dsh-headless` 的契约：只打印最终文本）。下：本插件把同一组事件画进 88 列 SSH 窗口。

![官方 headless stdout 对照 dsh-ssh-tui](docs/screenshots/compare.png)

上：`$ dsh --profile headless "…"` 之后只有最终 Markdown。  
下：思考默认折叠、`edit` 整行红/绿 diff、两个子代理各自一张卡、计划条钉在输入框上方。

单独看：[headless stdout](docs/screenshots/headless.png) · [dsh-ssh-tui](docs/screenshots/workspace.png)

## 弱网 SSH 上过程还在

同一条任务，按 **2 kB/s** 限速回放真实增量绘制（88×30，一帧一次 `stdout.write`）。官方 headless 这条链路上只会在全部结束后突然打出最终 Markdown；这里思考、`edit` diff、子代理卡和计划条是随着字节到达逐步出现的。

![2 kB/s SSH 上回放同一任务](docs/screenshots/slow-link.gif)

协议（可复现，不靠模型估）：`npm run screenshots:slow` → `docs/screenshots/slow-link.json`。这次回放 14 次绘制、约 **18.0 KB**，在 2 kB/s 上大约 **8.8 s** 画完。数字是这条固定事件序的 stdout 字节账。

## 功能一览

- 纯终端渲染，无需浏览器/鼠标/重量级终端框架，适合慢速或远程 SSH；
- 模型思考流默认折叠，显示 `▸ 思考中 ⠹ · N 字 · Ns` 动画；结束后折叠为
  `▸ 已思考 · N 行`，可单独展开；思考过程中也能实时展开/收起查看原文；
- 工作区支持 markdown 渲染：多级标题（H1 放大/下划线、H2 下划线、H3 着色）、
  粗体、斜体、行内代码、代码块、列表、引用与链接；模型最终回复以普通白色显示，行内 `**粗体**` 用更亮的粗体区分；
- 系统提示词 / `system-reminder` / `AGENTS.md` 等注入折叠为「提示词注入:系统预设 AGENTS.MD」卡片，默认收起，Enter 展开看全文；
- 工具调用卡片化：标题默认色，状态球绿/黄/红表示成功/运行中/失败（成功不再跟 `[ok]` 重复；失败仍标 `[error]`）；
  连续读/编辑同一路径会叠成一张卡（`×N` + 累计字数/行数，编辑 diff 跟随追加，合并时翻牌动画）；
  shell 命令浅灰、路径 cyan；编辑工具 git 风格 diff（`-` 暗红底 / `+` 暗绿底 /
  文件统计），头部带 git 红绿增删行数（如 ` -13 +24`），默认收起，Enter 展开；
  正文超出窗口时单独全览（Esc 返回）；JSON 参数与结果自动转可读内容；
- 转录区滚动回看（`PgUp`/`PgDn`、鼠标滚轮），点击思考/工具标题行直接展开收起；
- 输入框下方两行底栏：第一行链路芯片 + 按宽度丢组的会话数字（轮次、入/出 token、速度）；
  第二行只留一个活动词（运行中 / 工具 N / 子代理 N / 压缩中…），身份收到右侧（含 `目录:srv`；点击打印完整工作目录）；
  身份里始终带 `sub:<子代理模型>`（如 `sub:grok-4.5(xhigh)`）：`/submodel` 选模型、`/subeffort` 选档位（带括号后缀）；
  子代理跟随主模型时它就是身份行的暗色；只有 `/submodel` 钉到**别的提供商**才变色并补上 `提供商/` 前缀
  （如 `sub:xai/grok-4.5`）——完整路由在顶栏与 `/status`；
- 恢复旧会话会切到该会话记录的工作目录；新建会话用启动时的当前目录；
- 历史会话启动选择器：`dsh --profile tui --resume`（或 `resume`）先选会话再进入；
- 终端窗口标题栏：运行中旋转图标 + `运行中 · 工具 N`，完成后 `✓ 已完成`，并响
  一声终端铃（`DSH_TUI_NO_BELL=1` 关闭）；
- 审批、`ask_user_question`、计划模式、子代理进度、`/mode` 模式切换、`/model` 模型切换、
  `/disconnect` 断线策略等完整支持；
- `/approval auto` 自动审批模式（Codex 式）：读类/构建/测试、工作区 `edit`/`write`/`read` 自动放行；
  `rm -rf`、`sudo`、`curl|sh`、`git push --force`、敏感路径只读等危险命令自动**拒绝**，并把原因
  回给模型由其自行调整；`npm publish`、解释器 `-c`/`-e` 等未识别形状交给**子代理模型 AI 复核**
  （用户消息 + args/reason/sandbox，英文界面走英文审核员；`authorization=yes` 才放行）；
  仍未可判定时接入才询问、断开时自动拒绝——配合 `/disconnect continue` 断线后回合不停摆；
  `/approval status` 另报本轮 AI 复核次数；
- 每个子代理都是独立可折叠卡片，默认收起，运行中带旋转动画；多个子代理互不混排；
- 进入计划模式、待审计划、提问用户都会显示对应卡片和底部提示，而不是只塞进系统消息。
- 工作区底部有 Codex 式「处理中」动画卡：思考里第一个闭合的 `**加粗**` 作为 shimmer
  标题（还没出现就保持「处理中」），运行中的工具摘要在 `└` 下自动折行（最多 3 行，末行
  加省略号），带计时和 Esc 中断；回复开始流式输出时自动让位。

- 0.7 起：模型回复可**拖选自由复制**（按住拖过一段，走 OSC 52 写回本机剪贴板；工具卡仍是点击展开）；
  底栏收敛成一条带优先级的芯片带（先丢文字后丢组，`⚠` 可点击打开 `/doctor`）；**额度条常驻**并标注窗口
  （`5Hr`/`1Wk`/`1Mo`，默认显示最小窗口，未取到时显示 `?%` 并每 15 秒重试）；`/mode` 分组显示并可用 `/` 过滤；
  极简视图逐文件列 `+/-`；工具 diff 为**行级**、只高亮变化字符、≥100 列时并排显示；
  `DSH_TUI_LINE_MODE=1` 纯行模式（屏幕阅读器 / `tee`）；`ssh-tui.keys` 可改键位（冲突会明确拒绝）；
  `DSH_TUI_COLOR_DEPTH` 指定色深（truecolor / 256 / 8 / none）。

## 环境要求

- Node.js ≥ 22.19
- DeepSeek Harness CLI：`npm i -g @deepseek-ai/dsh`（已验证 `0.1.2-rc.1` 与 `0.1.5-rc.1`。`0.1.5-alpha.1` / `0.1.5-alpha.2` / `0.1.3-alpha.2` 走同一套 handle API + `agent/assistant-stream` 兼容层。`0.1.3-alpha.1` 只在 GitHub 有 tag，npm 未发布，无法本地装包验证）
- pnpm（`dsh plugin` 通过 pnpm 管理 profile 依赖）
- 支持 ANSI 的终端（推荐 SSH 直连；Windows 用 PowerShell / Windows Terminal）
- Windows：Host 与显示端之间的本地通道使用命名管道
  `\\.\pipe\dsh-tui-<DSH_HOME 摘要 8 位>-<会话名>-<会话摘要 8 位>`（Windows 只能监听命名管道，
  不能监听 `.sock` 文件；名字里同时带 DSH_HOME 与会话 id 的摘要，所以不同 home、不同会话都不会撞名，
  结束进程即自动回收）。Host 的 stderr 记录在 `%USERPROFILE%\.dsh\tui-socks\<会话名>-<摘要>.err`，
  会话锁仍在 `%USERPROFILE%\.dsh\tui-locks\`。

## 部署指南

推荐安装就是文首那条 `dsh plugin --profile tui add dsh-ssh-tui@latest`。CLI 会从 npm 拉包、写入 profile 依赖，并把本插件加入 `dsh.profile.bundles`（因为包内声明了 `dsh.bundle`）。

可选：把 SuperGrok 订阅接进 dsh（独立插件，不依赖本 TUI）：

```bash
dsh plugin --profile tui add dsh-llm-xai-oauth@latest
dsh plugin --profile headless add dsh-llm-xai-oauth@latest
```

SuperGrok 的 access token 大约 1 小时过期。TUI 打开时会刷新即将过期的 token，`/usage` 遇到 401 也会再刷一次。机器长时间不开 dsh 时，请另开刷新进程，否则一打开就是 401：

```bash
npx dsh-llm-xai-oauth daemon --install
```

说明见 [dsh-llm-xai-oauth](https://github.com/cyjyyd/dsh-llm-xai-oauth)。

先确认链路再开 TUI（无 TTY 时 TUI 会直接退出）：

```bash
dsh --profile headless "Reply with exactly: tui-install-ok. Do not use tools."
dsh --profile tui          # 必须在真实终端 / SSH 会话里
```

### SSH 断了之后

合盖、跳板 idle、换网会拆掉当前 TTY。TUI 把 SIGHUP / stdin 关闭 / 写 TTY 失败
当成挂断：放下显示器并 flush 日志。**空闲断线不保活**（Host 退出，下次从日志
`--resume`）；模型思考 / 回复 / 工具 / 子代理等忙碌状态则 **Host 留下**。
重新 SSH 后同一条命令会优先接入那个进程（选择器标「可接入」），不要再开第二份 Host：

Windows 上也一样保活，但走的路不同：宿主由系统 PowerShell 的 `Start-Process -WindowStyle Hidden`
拉起，因此有**自己的隐形控制台**（既不随用户的窗口关闭，也不会让工具调用闪窗）。唯一的例外是
机器上找不到 PowerShell：那时回退成直接子进程，关窗会连带结束正在跑的回合（会话不坏，
`--resume` 从日志重建），**并且启动横幅下面会有一行提示**说明这一点。见 [docs/platform.md](docs/platform.md) 的《四种死法》。

```bash
dsh --profile tui --resume                 # 选择器（活进程优先接入）
dsh --profile tui --resume <session-id>    # 有活进程则接入，否则从日志恢复
```

同一 `sessionId` 不能同时开第二份 Host（会抢 jsonl 和审批）。锁在
`$DSH_HOME/tui-locks/`，显示通道在 `$DSH_HOME/tui-socks/`。进程死后残留锁会在
下次启动时核对 pid，已死则自动从日志接管。调试可设 `DSH_TUI_NO_SESSION_LOCK=1`。

一个会话同时只有一块屏幕：新窗口接入时 Host 会通知旧窗口「你已被接管」（`FRAME_REPLACED`），
旧窗口退出，不会两个窗口互相抢显示。

链路探测（`CSI 6n`，终端回 `CSI row;col R`）做了三层防护：Host 收到 HELLO 之前就先测（不把
整屏重绘的时间算成链路）；每次重问前等链路安静**一整个应答窗口**（350ms，超时后放宽到
800ms），这样「上一个请求的回复」必然已经落地并被丢掉；采样取中位数，并丢掉比中位数快 4
倍以上的（那是别人请求的回复，相对判定所以 `ssh localhost` 的 2ms 链路照样算得出来）。
代价是每次接入多约 0.4–0.6 秒探测时间，换来的是 50ms 链路不再出现 2ms / 1900ms 的跳变。

这些回复也不可能再进输入框：relay 整条 stdin 管道常驻过滤（含跨 read 拆分的），Host 键
处理前再过滤一次；连 Host 启动那几百毫秒里敲的键也会被暂存、接入后补发，不再被丢掉。
`DSH_TUI_DEBUG=1` 时会打印每次采样与丢弃原因。

忙碌时默认断线会暂停当前轮次（取消），接上后再发一句才会继续。`/disconnect continue` 或
`ssh-tui.disconnect: continue`（也可用 `DSH_TUI_DISCONNECT=continue`）则不取消，
Host 在后台跑完这一轮；审批和提问等接上后再弹。空闲断线直接退出，不占后台。
留下的 Host 持有该会话的内核写锁（`session.lock`），而 Web 端打开同一会话时正是被这把锁挡下的
（`resume failed for session … is already owned by an active write handle`）。所以它**跑完留下来的那一轮后最多再等 1 分钟**
（`DSH_TUI_IDLE_EXIT_MS`，或 settings.yaml 的 `ssh-tui.idleExit`，毫秒；设 `0`/`off` 恢复旧行为）

按键可改：`ssh-tui.keys`（动作 `pageUp` / `pageDown` / `toggleCard` / `copy` / `cancel`，如 `keys: { pageUp: ctrl+b }`）。
冲突或未知的名字**不会静默生效**：启动时提示，且该键保持默认或变成无操作。
纯行模式：`DSH_TUI_LINE_MODE=1`（或 `ssh-tui.lineMode: true`）——不画帧，逐事件追加纯文本行，
适合屏幕阅读器、`tee`