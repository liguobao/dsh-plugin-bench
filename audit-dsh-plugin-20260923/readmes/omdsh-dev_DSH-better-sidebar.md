# dsh-better-sidebar

> [!IMPORTANT]
> **已适配 DSH 原生侧边栏 API**（v0.19.0 起）：右列就是 DSH 自己的右侧栏——插件的每个 tab 类型与 tab 体通过 `ctx.sidebarRightTabs` / `ctx.sidebarRight` 注册与打开，聊天里的文件打开统一走 `ctx.sidebarRight.openResource('dsh-resource://file/…')`，插件**不再自绘右侧面板**（旧的浮窗能力同步移除）。自绘的底部工作台与开放给其他插件的 `ctx.betterSidebar` 服务保持不变，接入方式见[插件接入指南](docs/external-plugin-guide.md)。
>
> **v0.21.1 起宿主支持下限是 DSH `0.1.7-rc.1`**（peer 下限 `^0.1.7-rc.1`；npm dist-tag `alpha`，`latest` 仍是 **v0.19.1**）。DSH 0.1.7 自带完整的文档预览（表格 / PDF / 图片 / Office），因此插件**把只读预览整体让给内置**（只保留 Markdown / HTML / 可编辑的代码编辑器）、**把外链接管收敛为「只认领声明了 `urlTarget` 的链接」**（按协议分流的三个外链接管设置项已删除），并**重写了设置接入面**（偏好迁到 profile 里本插件的挂载行，旧的 `settings.yaml` 段在首次启动时自动回迁）；文件树同时获得**实时刷新**。**0.1.6-alpha.2 及更早的用户请停留在 v0.19.1**——注意 **0.20.0 这一版从未发布到 npm**，这些变更全部落在 v0.21.1。**按 DSH 版本选插件版本的对照表见[安装](#-安装)。**

<!-- Hero -->
<div align="center">
  <b style="font-size: 1.15em;">一个服务化的侧边栏框架，一套开箱即用的完整工作台</b><br /><br />
  <a href="https://www.npmjs.com/package/dsh-better-sidebar"><img alt="npm version" src="https://img.shields.io/npm/v/dsh-better-sidebar" /></a>
  <a href="https://www.npmjs.com/package/dsh-better-sidebar"><img alt="npm downloads" src="https://img.shields.io/npm/dm/dsh-better-sidebar" /></a>
  <a href="https://github.com/omdsh-dev/DSH-better-sidebar/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/omdsh-dev/DSH-better-sidebar/actions/workflows/ci.yml/badge.svg" /></a>
  <a href="https://github.com/omdsh-dev/DSH-better-sidebar/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/omdsh-dev/DSH-better-sidebar" /></a>
  <a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" /></a>
  <a href="https://dshfind.com/zh/plugins/omdsh-dev/DSH-better-sidebar?ref=badge"><img alt="dshfind" src="https://dshfind.com/api/badge/omdsh-dev/DSH-better-sidebar?lang=zh" /></a><br /><br />
  <a href="https://www.npmjs.com/package/@deepseek-ai/dsh?activeTab=versions"><img alt="支持的 DSH 版本（v0.21.1）：0.1.7-rc.1+" src="https://img.shields.io/badge/DSH-0.1.7--rc.1%2B-4d6bfe" /></a>
  <a href="https://github.com/topics/dsh-better-sidebar"><img alt="插件生态：GitHub topic dsh-better-sidebar" src="https://img.shields.io/badge/%E6%8F%92%E4%BB%B6%E7%94%9F%E6%80%81-topic%20dsh--better--sidebar-4d6bfe" /></a><br /><br />
  <img alt="文件管理" src="https://img.shields.io/badge/-文件管理-4d6bfe" /> <img alt="编辑预览" src="https://img.shields.io/badge/-编辑预览-4d6bfe" /> <img alt="内置浏览器" src="https://img.shields.io/badge/-内置浏览器-4d6bfe" /> <img alt="文件变动" src="https://img.shields.io/badge/-文件变动-4d6bfe" /> <img alt="后台任务" src="https://img.shields.io/badge/-后台任务-4d6bfe" /> <img alt="侧边对话" src="https://img.shields.io/badge/-侧边对话-4d6bfe" /> <img alt="插件接入" src="https://img.shields.io/badge/-插件接入-4d6bfe" /><br /><br />
  <b>右侧栏 + 底部面板双工作台</b>，并把 <code>ctx.betterSidebar</code> 服务开放给所有插件——<br />
  通过 <code>registerTab</code> / <code>registerFileViewer</code> 注册新的侧边栏页面与文件预览器。
</div>

<div align="center">
  🌏 <a href="./README.md"><b>中文</b></a> · <a href="./README_EN.md">English</a>
</div>

<div align="center">
  <img alt="dsh-better-sidebar 工作台截图" src="https://github.com/user-attachments/assets/991c4b70-d45a-461f-a8c8-0a28b4218e60" />
  <video src="https://github.com/user-attachments/assets/23187822-047e-45cc-b480-fe997bd55b86" muted autoplay loop playsinline controls width="100%"></video>
</div>

## 📑 目录

- [✨ 功能一览](#-功能一览)
- [🚀 安装](#-安装)
- [🖼️ 特性巡礼](#-特性巡礼)
- [🌐 插件生态](#-插件生态)
- [🆕 最近更新](#-最近更新)
- [⌨️ 快捷键](#-快捷键)
- [🔌 服务化扩展](#-服务化扩展)
- [🛠️ 开发与构建](#-开发与构建)
- [🔐 安全](#-安全) · [⚠️ 已知限制](#-已知限制) · [🖥️ 平台支持](#-平台支持)
- [💬 社区](#-社区) · [🤝 参与贡献](#-参与贡献) · [⭐ Star History](#-star-history) · [🔗 友情链接](#-友情链接)

## ✨ 功能一览

- **🗂️ 文件工作台**：资源管理器（懒加载目录树，**展开的目录由宿主按目录 watch、改动后自动重列**；软链接按目标类型展示——目录软链接可展开、失效链接标红；文件树与文件 tab 按扩展名显示图标——markdown / 图片 / PDF / 代码 / 配置 / 压缩包等各有 glyph，插件可经 `registerFileIcon` 注册自定义图标与目录图标）+ **可编辑**的 CodeMirror 编辑器；Markdown（含 Mermaid 图表，strict 安全渲染 + 点击放大；README 级内嵌 HTML——徽章墙 / `<details>` 折叠 / 表格内联标签经 DOMPurify 消毒真实渲染；浮动目录大纲一键跳转）与 HTML（沙箱 iframe + 两个宿主没有的逃生门开关）仍由插件渲染
- **🌐 浏览器与文档预览（由 DSH 内置提供）**：网页 tab 是宿主自己的 `ui-sidebar-browser`（多开 / 后退前进刷新 / 沙箱 iframe，**0.1.7 起只在 desktop profile 挂载**）；表格 / PDF / 图片 / Office 预览是宿主自己的 `ui-sidebar-documentpreview`（宿主侧 Office→PDF 转换、电子表格 worker 表格、图片 / PDF 缩放视口、按目录自动刷新）。插件**不再认领**这些格式，只保留宿主没有的那一半：**外链接管**——只认领有 tab 类型通过 `urlTarget` 明确声明的链接，其余一律放行给宿主（正文链接的去向由宿主用户设置 `linkOpening` 决定）
- **💻 终端（DSH 内置）**：右侧栏终端由 **DSH 内置**的 `ui-sidebar-terminal` 提供（shell 选择 / 重命名 / 断线重连 / 刷新后恢复 / 主题跟随）。插件不再自带终端实现
- **📂 模型侧边栏打开（可选）**：全局设置开启后注入 `sidebar_open` 工具——模型可主动在侧边栏打开文件 / 文件夹（树以该目录为根）/ HTTP(S) 网页（网页 tab 需要宿主提供 `browser` kind，即 desktop profile）
- **🌿 文件变动**：Git 视角（真 diff / 历史 / 暂存·提交·还原 / worktree·子仓库选择）与本轮文件视角（模型读 / 写 / 编辑实时追踪，按文件分组、按类型筛选）**双视角合一**；统一 diff 渲染（改蓝配对 + 行内字符级高亮 + 语法着色（含 mjs/cjs/mts/cts、CSS/SCSS/Less、HTML/XML/SVG/Vue、GraphQL、JSONC/JSON5）+ 上下文折叠），底部可拖拽预览面板，可一键展开为独立 diff tab（落进工作台的 diff 分栏）；`.md` 操作（读 / 写 / 编辑）预览头部可切换**阅读模式**——经共享 MarkdownText 渲染 GFM 表格 / 任务列表 / 删除线 / 脚注 / 数学公式，本地图片自动改写为 `/sidebar/file` 媒体路由；含 ```mermaid 围栏时走编辑器同款懒加载 mermaid 渲染器（图可点击缩放 / 平移）；**敏感内容脱敏**——凭据形态路径整文件遮罩、普通文件按内容形态遮值（api_key: / Bearer / sk- / AKIA / ghp_ / PEM 等，字段名保留），默认开启、预览面板一键开关（localStorage 记忆），仅影响显示、不改会话数据。已知边界：mermaid 无引号节点标签含被遮密钥时，图回退源码（规避：标签加引号）；`.html` 操作（读 / 写 / 编辑）预览头部可切换**渲染模式**——复用编辑器同款 `/sidebar/html` 路由 iframe，相对资源（./style.css、img/x.png）同路由解析，分段读取也渲染完整文档，恒定沙箱（opaque origin + CSP 头，无逃生门）；`.pdf` 操作（读 / 写 / 编辑）同样可切换**渲染模式**——复用编辑器同款 PDF 预览（媒体路由字节流 + 显式 Blob，浏览器原生查看器内嵌，附下载入口）
- **🧩 后台任务页**：subagent 拓扑 + 后台任务（退出码 / 实时输出 / 强制终止）
- **💬 侧边对话(beta)**：Codex 风格的侧边线程——继承主会话完整上下文（含进行中的回合与工具调用）独立运行，不进入主会话；线程内可持续追问，一键「保存为新会话」提升为顶层会话
- **🖥️ 原生右侧栏 + 底部工作台**：右列交给 DSH 原生右侧栏——插件把每个 tab 类型注册成原生 tab（文件打开走 `dsh-resource://file/**`，并接管内置「文件」页 / 文件树），插件自己只保留底部工作台（分栏 / 随会话持久化），开合按钮挂在会话头右侧
- **🔁 会话隔离**：布局 / Tab / 面板按会话持久化，陈旧状态自动净化
- **⚙️ 声明式设置**：设置页「侧边卡片」逐项独立开关，二级设置经齿轮弹窗
- **⚡ 按需加载**：启动只拉 ~325KB 核心，编辑器 / Mermaid 图表 / 第三语言词典等重依赖用到才按需拉取（[设计文档](docs/plans/2026-08-12-lazy-chunks-design.md)）
- **🌏 多语言**：界面文案跟随 DSH 语言（zh / en）实时切换；安装 `@huanlin/dsh-plugin-better-locale` 后支持日语（ja）等第三语言覆盖（见下方「🌏 第三语言覆盖」）

> 🔌 **核心理念**：服务优先——内置的 5 tab + 3 viewer 与第三方插件通过同一套 `ctx.betterSidebar` API 注册，能力完全对等；官方不再内置、可由生态提供的功能，交由生态插件实现（已有 **28+ 生态插件**，见下方「🌐 插件生态」）。接入文档见「🔌 服务化扩展」与 [外部插件接入指南](./docs/external-plugin-guide.md)。

## 🚀 安装

**前置**：已装好 DSH（`dsh web` 能正常运行），Node.js ≥ 20、pnpm ≥ 10。

**支持的 DSH 版本**：
<a href="https://www.npmjs.com/package/@deepseek-ai/dsh?activeTab=versions"><img alt="支持的 DSH 版本（v0.21.1）：0.1.7-rc.1+" src="https://img.shields.io/badge/DSH-0.1.7--rc.1%2B-4d6bfe" /></a>

> 📌 **通道与支持线**：`v0.21.1` 是**正式版**（npm dist-tag `latest`），适配 DSH **0.1.7-rc.1+**（peer 下限 `^0.1.7-rc.1`，CI 钉 `@deepseek-ai/dsh@0.1.7-rc.1`）。**装 DSH 请写精确版本号**：0.1.7-rc.1 在 npm 上走 `next` 通道，`alpha` 此刻指的是 0.1.7-alpha.2——`npm i -g @deepseek-ai/dsh@0.1.7-rc.1`。**npm `latest` 由此从 `v0.19.1` 前移到本版**——注意 `v0.20.0` 与 `v0.21.0-alpha.1` **从未发布到 npm**（中间的 `0.21.0-rc.1` 只在 `alpha` 通道上存在过），本仓库从 0.19.1 直接跳到这条 0.21 线。**下限必须动**：semver 的预发布规则让 `^0.1.6-alpha.2` 在数学上永远匹配不到任何 `0.1.7` 预发布版。**DSH 0.1.6-alpha.2 及更早（含 npm `latest` 的 0.1.5-rc.3）的用户请固定安装 `dsh-better-sidebar@0.19.1`**——0.1.7 的破坏面足够大（`dsh-settings` 整体重写、`ui-primitives` 图标具名导出整族改名、会话格式 v3→v4），本版不写运行时兼容层；DSH 0.1.5-alpha.2 及更早同样请用旧版（`0.19.0-alpha.1` / `0.18.x` / `0.17.1`）。

> 🧭 **按你的 DSH 版本选插件版本**（**`0.21.1` 起的支持线是 DSH `0.1.7-rc.1` 及之后的 0.1.7 线**；0.1.7 的两个 alpha 与 0.1.6 及更早都不在这条线内）：
>
> | 你的 DSH 版本 | 安装命令 | 版本 / peer 声明 |
> | --- | --- | --- |
> | **0.1.7-rc.1+**（含之后的 0.1.7 正式版） | `dsh plugin --profile web add dsh-better-sidebar@latest` | **0.21.1**，`^0.1.7-rc.1` |
> | 0.1.7-alpha.1 / 0.1.7-alpha.2 | **没有可装版本**——先把 DSH 升到 rc.1，再跑上一行：<br>`npm i -g @deepseek-ai/dsh@0.1.7-rc.1` | — |
> | 0.1.6-alpha.2 及更早、`0.1.5-rc.*`（含 npm `latest` 的 0.1.5-rc.3） | `dsh plugin --profile web add dsh-better-sidebar@0.19.1` | **0.19.1**（= npm `latest`），`^0.1.5-rc.1` |
> | `0.1.5-alpha.2` | `dsh plugin --profile web add dsh-better-sidebar@0.19.