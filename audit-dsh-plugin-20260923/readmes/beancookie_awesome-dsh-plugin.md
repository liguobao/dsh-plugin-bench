<p align="center">
  <a href="https://beancookie.github.io/awesome-dsh-plugin/zh/">
    <img src="https://beancookie.github.io/awesome-dsh-plugin/logo.png" alt="Awesome DSH Plugin" width="120">
  </a>
</p>

# Awesome DeepSeek Harness (DSH) Plugin

<p align="center">
  <a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a>
  <a href="https://beancookie.github.io/awesome-dsh-plugin"><img src="https://beancookie.github.io/awesome-dsh-plugin/badge.svg" alt="awesome · DSH plugin"></a>
</p>

<p align="center">
  <a href="README.en.md">English</a> | 中文
</p>

> [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（`dsh`）插件精选列表。

DeepSeek Harness 是 DeepSeek 开源的 agent harness——既是可直接运行的 Coding Agent（提供 Web 与 headless 两种形式），底层又是一套「一切皆插件」的框架：模型、工具、沙箱、会话存储、UI、乃至 Agent Loop 本身都是插件。插件既可以扩展官方 Coding Agent，也可以替换其核心部件，甚至组装出完全不同的东西。

<p align="center">
  推荐使用 <a href="https://github.com/beancookie/dsh-plugin-registry">dsh-plugin-registry</a> —— 会话内检索并一键安装本列表插件，Web 设置页带「插件市场」面板。
</p>

<details>
<summary align="center">📸 点击查看演示截图</summary>

<p align="center">
  <img src="images/dsh-plugin-registry.png" alt="dsh-plugin-registry" width="600">
</p>

</details>

**503** 个插件 · 欢迎 [PR](#贡献)

## 目录

- [插件](#插件)
  - [🎨 UI 增强](#-ui-增强)
  - [🎭 主题与外观](#-主题与外观)
  - [💬 会话与消息](#-会话与消息)
  - [🧠 记忆](#-记忆)
  - [🛠️ 工具与能力](#-工具与能力)
  - [🧩 技能包](#-技能包)
  - [🔁 工作流与自动化](#-工作流与自动化)
  - [🔔 通知与集成](#-通知与集成)
  - [🔌 模型与账号接入](#-模型与账号接入)
  - [🧑‍💻 开发与运行时](#-开发与运行时)
  - [🎮 娱乐](#-娱乐)
- [相关](#相关)
- [贡献](#贡献)
- [徽章](#徽章)
- [免责声明](#免责声明)

## 插件

### 🎨 UI 增强
- [0xsline/dsh-spotlight](https://github.com/0xsline/dsh-spotlight) — 键盘优先的命令面板（command palette）。
- [a903067276-rgb/dsh-file-mentions](https://github.com/a903067276-rgb/dsh-file-mentions) — DSH 回复中的文件路径可点击：Codex 风格行内打开、文件管理器定位、回合尾部文件 chip 列表。
- [a903067276-rgb/dsh-hud](https://github.com/a903067276-rgb/dsh-hud) — HUD 状态面板：Git 状态、MCP 服务器、技能列表、模型与 token 用量，悬浮侧栏一览无余。
- [AKIRACOD/dsh-drag-and-drop](https://github.com/AKIRACOD/dsh-drag-and-drop) — 拖放 fork：文档以可删除「文件芯片」挂在输入框上方，不打字也能发送。
- [alingalingling/ui-status-label](https://github.com/alingalingling/ui-status-label) — 把鲸鱼娘思考时的 "deep diving" 状态文案自定义成任意你想要的样子。
- [asukasec/dsh-message-preview](https://github.com/asukasec/dsh-message-preview) — 右侧用户消息导航条，根据消息数量与可用高度自适应排布导航块，并支持悬停预览、键盘操作与点击跳转。
- [Bay-Zeddie/dsh-agent-instructions](https://github.com/Bay-Zeddie/dsh-agent-instructions) — 在 dsh Web 设置页里编辑原生 AGENTS.md 的面板：指令链上每层可点选编辑，三种生效范围，并可视化官方指令预算。
- [BeiZi6/dsh-opencodego-usage](https://github.com/BeiZi6/dsh-opencodego-usage) — OpenCodeGo 剩余额度监视器：输入框右下角呼吸指示灯（按剩余额度绿/黄/红），液态玻璃面板显示滚动/周/月用量窗口与重置时间，每 30 秒自动刷新，API Key 自动读取 DSH 凭据。
- [bill9109/dsh-101](https://github.com/bill9109/dsh-101) — DSH 文档阅读模式。
- [bill9109/dsh-drag-and-drop](https://github.com/bill9109/dsh-drag-and-drop) — 跨平台文件拖拽与原始路径插入，无需复制文件。
- [bobcat848/dsh-calculator](https://github.com/bobcat848/dsh-calculator) — 右侧面板展示 DeepSeek API 费用（当前会话 + 全部会话累计）与账户余额，内置官方计价与峰谷计价支持。
- [bpc-oss/dsh-web-billing](https://github.com/bpc-oss/dsh-web-billing) — 人民币/美元 token 计费，官方政策计价与逐条消息费用账本。
- [bunipai/dsh-fare-meter](https://github.com/bunipai/dsh-fare-meter) — 出租车计价器式实时计费：生成时逐秒跳动、空闲归零，内置官方峰谷时段与价格表。
- [CanglongCl/dsh-web-review](https://github.com/CanglongCl/dsh-web-review) — 隔离网页预览，通过元素批注指导源码修改。
- [ccch1mneyyy/dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) — Claude Code 风格全屏终端 UI：像素鲸鱼顶栏、实时工作状态行、思考流式展开。
- [ccq1/dsh-side-panel](https://github.com/ccq1/dsh-side-panel) — 侧边栏集成文件浏览器、终端和 Git 审查，方便预览文件。
- [daetz-coder/dsh-multi-chat](https://github.com/daetz-coder/dsh-multi-chat) — 在 DSH Web 界面里并排运行、监控多个对话实例的插件：多窗口墙 + 自动发现 + 单窗控制，内置带口令认证的局域网网关，手机/平板也能看。
- [dgadelha1/dsh-explorer-plugin](https://github.com/dgadelha1/dsh-explorer-plugin) — 工作区文件树 + Monaco 编辑器：多标签、撤销/重做、实时文件监听（SSE）、VS Code 真实 TextMate 语法高亮（28 种语言）与 Dark+/Light+ 主题，直接嵌入 DSH 网页 GUI。
- [dingyi222666/dsh-focus-chat](https://github.com/dingyi222666/dsh-focus-chat) — 「聚焦会话」精简视图，只关注最终产出结果。
- [dsh-blue/blue](https://github.com/dsh-blue/blue) — DeepSeek Harness 的交互式全屏终端 UI：流式 Markdown 转录、工具调用卡片、审批面板、会话管理、主题热切换——全部组件皆为可热插拔的插件树。
- [dsh-paste-input](https://github.com/dsh-external/dsh-paste-input) — Ctrl+V 粘贴文件 / 拖拽 / 选择。
- [dsh-web-panel](https://github.com/dsh-external/dsh-web-panel) — 内嵌终端 dock + Git Review + 文件视图。
- [dugujun3-cloud/dshos-dock](https://github.com/dugujun3-cloud/dshos-dock) — 工作区 OS 状态条：输入框上方常驻显示任务统计（总数/进行中/待验收）、最近运行事件与自检日期；零依赖只读，数据来自工作区 .dshos/ 文本契约，兼容旧 DSH-OS 布局，30 秒自动刷新。
- [fishxcode/dsh-plugin-deepseek-balance](https://github.com/fishxcode/dsh-plugin-deepseek-balance) — 在 DSH Web 设置中展示 DeepSeek API 余额、余额趋势与每日用量图表。
- [FuqiangCraft/dsh-desktop](https://github.com/FuqiangCraft/dsh-desktop) — 为 DSH 提供桌面通知、多 Agent 可视化画布和可选的屏幕截图工具。
- [Ghost011118/dsh-balance-meter](https://github.com/Ghost011118/dsh-balance-meter) — 输入框 dock 显示 DeepSeek 账户余额与会话花费，自动拉取官方定价，支持高峰/低谷计价。
- [GooodWei/context-vista](https://github.com/GooodWei/context-vista) — 右侧悬浮面板，环形图实时展示上下文 token 用量与费用。
- [Han-1413141/dsh-cost-meter](https://github.com/Han-1413141/dsh-cost-meter) — 会话与当日 API 费用统计、预算图框（已用%）、官方余额、历史看板，支持峰谷计价与官方价格一键同步。
- [Han-1413141/dsh-sticky-disclosure](https://github.com/Han-1413141/dsh-sticky-disclosure) — 一键收起会话中所有展开的区块（Think、工具卡等），常驻计数按钮 + 自定义快捷键。
- [huiliyi37/dsh-tianshu-tui](https://github.com/huiliyi37/dsh-tianshu-tui) — DeepSeek Harness 的终端 UI（TUI）。
- [hutao562/dsh-remote-dsh](https://github.com/hutao562/dsh-remote-dsh) — 在侧边栏顶部加一行，点击后整页切换成另一台 DSH 主机的 Web GUI（通过回环端口访问），并在该行显示那台主机的会话状态（运行中、有新活动、正等你回答）。
- [ice5kysl/dsh-file-explorer-kit](https://github.com/ice5kysl/dsh-file-explorer-kit) — 会话内「文件」页签：以当前会话工作区为根的面包屑浏览，内联预览消毒渲染的 Markdown、图片、带行号文本与 PDF；目录与读取走只读 /dsh-files 宿主路由，无写端点（中英双语）。
- [ice5kysl/dsh-workspace-kit](https://github.com/ice5kysl/dsh-workspace-kit) — 工作区优先的增强侧栏（以低优先级 shadow 内置工作区浏览器，可一键切回官方版）+ ⌘K Spotlight 模糊搜索：软归档/恢复、每工作区图标与强调色、拖拽排序、标题/路径/会话内容搜索；宿主侧附带只读 workspace_find/workspace_list 工具与斜杠命令（中英双语）。
- [jiangnanquan/dsh-ux](https://github.com/jiangnanquan/dsh-ux) — Solarized 浅色主题、紧凑布局、思考/工具链折叠胶囊，以及余额、本轮成本与用量看板的 DSH Web 界面增强插件。
- [Jolly-J/dsh-deepseek-billing](https://github.com/Jolly-J/dsh-deepseek-billing) — 侧边栏底部 DeepSeek 账户余额显示与会话费用估算卡片。
- [Jovan1666/dsh-commandcode-quota](https://github.com/Jovan1666/dsh-commandcode-quota) — 在 DSH 侧边栏「设置」上方显示 Command Code 套餐额度：5 小时 / 每周 / 月度三条窗口的已用百分比、进度条与重置倒计时；另带 /quota 命令与零依赖命令行工具。
- [l541402398/dsh-file-uploads](https://github.com/l541402398/dsh-file-uploads) — 从 Web 输入框上传任意本地文件，以待发送卡片展示，并在设置中管理已存文件。
- [lak321/dsh-filetree](https://github.com/lak321/dsh-filetree) - 工程文件浏览器：会话视图文件页签，目录树 + VSCode 风格编辑器（C 语法高亮/行号/自动缩进/状态栏），跟随当前工作区。
- [lancecheney/dsh-deepseek-balance](https://github.com/lancecheney/dsh-plugins/tree/main/packages/dsh-deepseek-balance) — Session log 按钮左侧的实时计费徽章：余额、每会话消耗、峰谷/平价价格，按模型/货币/思考强度自动切换，每天抓官方定价。
- [Lanxing6480/dsh-galgame](https://github.com/Lanxing6480/dsh-galgame) — DSH Web 聊天界面 GalGame 演出层：立绘差分、流式思考气泡、打字机对话框与 GalGame 式提问/审批选项框，可随时切回普通聊天。
- [Laplace-bit/dsh-smooth-stream](https://github.com/Laplace-bit/dsh-smooth-stream) — 丝滑流式渲染：字跟着模型到达走、换行滑入、不闪，滚动归用户，尊重 `prefers-reduced-motion`。
- [lehhair/dsh-diff-viewer](https://github.com/lehhair/dsh-diff-viewer) — PiUI 风格 diff 查看器，替换 write/edit 工具调用的默认 DiffBlock。
- [liznee/dsh-speech-input](https://github.com/liznee/dsh-speech-input) — 输入框原生麦克风按钮：语音写草稿、5 秒静音自动停止、胶囊听写 UI 与点击预览。中英文支持。
- [lqhl/dsh-pi-tui](https://github.com/lqhl/dsh-pi-tui) — 差分渲染 TUI 前端：流式 Markdown 与工具卡片。
- [Luaphes/dsh-web-attention-badge](https://github.com/Luaphes/dsh-web-attention-badge) — 会话需要你时三处同时亮起：角标、标签页标题计数、按状态换色的鲸鱼 favicon。
- [Meredith2328/dsh-sticky-note](https://github.com/Meredith2328/dsh-sticky-note) — 编辑框工具栏便签，随手记点子和 TODO，自动保存为 Markdown，一键发送到对话。
- [MysaDC/dsh-plugin-description](https://github.com/MysaDC/dsh-plugin-description) — 为 Web 设置页插件卡片补上中英文功能说明。
- [Nagi-ovo/dsh-visualize](https://github.com/Nagi-ovo/dsh-visualize) — 对话内生成式 UI：模型把交互式 HTML 卡片直接画进会话流，带流式预览与沙箱渲染。
- [nonewind/dsh-spend](https://github.com/nonewind/dsh-spend) — DSH Web 用量与费用统计插件：右下角悬浮窗，按模型/按天/按会话多维聚合与预计花费。
- [ds