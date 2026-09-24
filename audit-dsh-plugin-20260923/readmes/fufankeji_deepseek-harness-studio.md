<p align="center">
  <a href="https://www.beyondata.com/">
    <img src="apps/web/public/dsh-desktop/beyondata-logo.png" alt="赋范空间 Logo" width="92" height="92">
  </a>
</p>

<h1 align="center">DeepSeek Harness Studio</h1>

<p align="center">
  <a href="https://github.com/fufankeji/deepseek-harness-studio/stargazers"><img src="https://img.shields.io/github/stars/fufankeji/deepseek-harness-studio?style=flat&logo=github&label=Stars" alt="GitHub Stars"></a>
  <img src="https://img.shields.io/badge/Desktop-App-2563EB" alt="Desktop App">
  <img src="https://img.shields.io/badge/Electron-Desktop-47848F?logo=electron&logoColor=white" alt="Electron Desktop">
  <img src="https://img.shields.io/badge/Plugin%20Center-online-22C55E" alt="公开插件中心已上线">
  <img src="https://img.shields.io/badge/Preset%20Square-online-6366F1" alt="Preset 广场已上线">
  <img src="https://img.shields.io/badge/Application%20Center-online-0F9D8A" alt="应用中心已上线">
  <img src="https://img.shields.io/badge/Vision-Auto%20Routing-7C3AED" alt="视觉增强自动路由">
  <img src="https://img.shields.io/badge/Local%20Models-Ollama%20%7C%20vLLM%20%7C%20SGLang-0EA5E9" alt="支持 Ollama、vLLM 和 SGLang 本地模型服务">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/fufankeji/deepseek-harness-studio?color=22C55E" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/macOS%20%7C%20Windows-supported-3B82F6" alt="macOS and Windows">
</p>

<p align="center"><a href="https://www.beyondata.com/"><strong>官方网站</strong></a> · <strong>中文</strong> · <a href="README.en.md">English</a></p>

<p align="center"><strong>赋范空间出品 · DeepSeek Harness 的零代码桌面增强</strong></p>

<p align="center"><strong>视觉增强 + 本地模型 + 插件市场 + Preset 广场 · 0 代码一键部署和使用</strong></p>

<p align="center">自动发现并推送生态新插件，AI 智能推荐值得安装的能力；无需命令行即可完成搜索、校验、安装、启停与卸载。</p>

<p align="center"><a href="https://github.com/fufankeji/deepseek-harness-studio/releases/download/desktop-preview-v0.1.0-rc.19/DeepSeek-Harness-Desktop-0.1.0-rc.19-macos-arm64-preview.zip"><strong>下载 macOS arm64 开发预览版</strong></a> · <a href="https://github.com/fufankeji/deepseek-harness-studio/releases/download/desktop-preview-v0.1.0-rc.19/DeepSeek-Harness-Desktop-Windows-x64-0.1.0-rc.19-Setup.exe"><strong>下载 Windows x64 开发预览版</strong></a></p>

<p align="center">
  <img src="assets/plugin-discovery-hero.jpg" alt="DeepSeek Harness Studio 视觉增强、插件市场、Preset 广场、零代码一键部署、插件自动推送与 AI 智能推荐" width="100%">
</p>

<p align="center">
  <strong>点击快速查看功能演示</strong>
</p>

https://github.com/user-attachments/assets/0717f7c7-a872-4d2b-acc2-3a1c4874c732

## 核心功能

> 下表只列已经进入源码、桌面组合和用户操作链路的能力；远期设想不再与现有功能混排。

| 能力 | 可以做什么 |
| --- | --- |
| **桌面工作区与会话管理** | 使用原生目录选择打开本地项目，按 Workspace 管理和搜索会话，并完成重命名、归档、Fork 与历史接续。 |
| **长会话目录与全文跳转** | 在对话右侧按用户、助手和工具生成完整历史目录；点击摘要会自动加载尚未渲染的旧消息，收起目录并跳转、高亮对应完整原文。 |
| **插件发现与 Agent 推荐** | 浏览精选、最近更新和生态热门插件，按场景筛选或搜索，也可以直接描述需求让 Agent 从公开 `dsh-plugin` 目录筛选候选。 |
| **插件可信安装与生命周期恢复** | 安装前检查确定版本、权限、兼容性与风险，安装后统一启用、停用、更新和卸载；未完成事务会自动回滚，运行清单仍不一致时进入可停用／卸载的插件安全模式。 |
| **Preset 广场与七套内置工作流** | 浏览赋范官方与社区 Agent Preset，查看 Skills、工具和环境要求后安装，并从“已安装”直接用于新会话。 |
| **应用中心与 FF–LLM Wiki** | 从独立一级入口启动拥有专属界面、数据和运行流程的完整 AI 应用，并按需显示应用侧边栏快捷入口。 |
| **多模型与本地推理** | 配置 DeepSeek 与其他兼容提供方，或从一级入口连接 Ollama、vLLM、SGLang 和自定义 OpenAI-compatible 服务。 |
| **原生视觉、兼容视觉与图片附件** | 使用 DeepSeek 图文模型直接处理图片，或调用已验证的云端／自托管视觉路线；图片附件会持久保存并沿单一路径发送。 |
| **Plan、Goal、Todo、Jobs 与 Workflow** | 进入规划模式，管理目标和待办，查看当前进程中的后台任务，并在对话中复盘多阶段 Workflow 的成员状态。 |
| **SubAgent 与多 Agent 协作** | 创建一次性或可继续的子 Agent，查看父子会话谱系、运行状态和耗时，并在支持的子会话中继续交流或停止当前轮次。 |
| **项目规则、上下文引用与产出文件** | 读取仓库指令，使用 `@file`／`@session` 引用上下文，并在回答末尾查看、打开或定位 Agent 实际产出的文件。 |
| **权限、沙箱与人工确认** | 为当前或后续会话选择只读、工作区写入和完全访问；危险权限、工具审批和 Agent 主动提问都在界面中显式确认。 |
| **主题皮肤与跨平台桌面交付** | 切换内置或本地背景并自动适配界面配色；通过 GitHub Releases 获取 macOS arm64 与 Windows x64 预览包。 |

## 近期路线图

> 以下能力尚未形成完整的一等产品入口，不计入当前功能。

| 方向 | 计划补齐的产品能力 |
| --- | --- |
| **独立能力中心** | 为不依赖 Bundle 包装的 MCP Server、Skills 与工具提供单独的发现、连接和项目级组合管理。 |
| **可视化 Agent 编排** | 在现有 Preset 与 SubAgent 运行能力之上，提供自定义 Agent、角色分工和团队流程编辑器。 |
| **远程控制与自动化** | 在明确权限和审计边界后，补齐浏览器／桌面操作、移动端接续和消息通知入口。 |

## 项目简介

DeepSeek Harness Studio 使用 Electron 承载 DeepSeek Harness 的 Web 工作区，并由桌面主进程启动和管理本地 `dsh web` 服务。这个仓库提供完整源码开发环境，使用者可以从 GitHub 克隆或下载代码，在本地安装依赖、编辑源码、启动桌面应用并继续开发。

桌面安装包只通过本仓库的 GitHub Releases 发布，不使用第三方下载站。目前已经提供经过真实 Electron 验收的 macOS arm64 预览 ZIP 和 Windows x64 预览安装程序；需要继续开发时，仍可获取完整源码并在本地启动。

## Workspace 与 Agent 执行能力

- **Workspace 和会话**：原生选择本地目录；按 Workspace 分组、搜索和删除登记；会话支持重命名、归档和在最后一个完成轮次处 Fork。
- **长会话目录**：右侧轻量目录覆盖当前会话的完整历史，而正文仍按页加载；目录摘要最多 80 字，点击未加载项目会自动连续翻页，定位后收起面板并高亮完整消息。
- **计划与工作管理**：通过 Plan、Goal 和 Todo 组织当前任务；Jobs 面板展示当前进程内的后台任务，进程重启后不会把这些运行中任务继续当作存活任务。
- **Workflow 与 SubAgent**：对话记录会展示 Workflow 的阶段、成员和结局；SubAgent 目录支持父子谱系导航、继续对话，以及停止运行中可继续子会话的当前轮次。
- **引用与交付物**：`@file` 和 `@session` 把文件或会话作为上下文；成功产出的文件会出现在回答末尾，并可通过本地 Host 打开或在文件夹中定位。
- **人机协作**：Agent 可以发起结构化单选、多选或自定义问题；工具审批、完全访问和计划评审都要求用户在界面中明确作答。
- **安全边界**：权限预设把沙箱模式与审批策略固定到会话；凭据经只写接口保存，页面不会读取或回显已经存储的密钥值。

## DeepSeek Harness v0.1.1-rc.2 兼容能力

Studio `0.1.0-rc.19` 已整合 DeepSeek Harness `0.1.1-rc.2` 的核心与 Web 能力，同时保留赋范的插件中心、插件发现、Preset 广场、应用中心、主题皮肤和桌面恢复链路。Studio 版本号与 Harness 上游版本号分别管理；页面顶部下载链接与本版本一致。

- **多模态能力**：保留 Pro／Flash 文本模型，接入 `DeepSeek-V4-Flash-Vision-Exp`、可持久图片附件和 Files API 图片复用；失效引用会有界重传，解析失败时整次请求回退为受限内联图片。
- **Agent 运行能力**：接入 `@` 文件／会话引用、Plan、Goal、后台 Jobs、Workflow、SubAgent、并发 Web Search 与 Windows 持久 PowerShell PTY。
- **桌面适配**：Host 使用 `--no-open`，保留原生目录选择、插件事务恢复和既有用户数据目录；历史插件锁文件不兼容时自动进入不改写锁文件的兼容恢复。

## 插件生态：先发现值得装的，再完成安装与管理

### 插件发现：不知道装什么，就从这里开始

不知道插件去哪里找、哪些最近刚更新、哪些正在受到生态关注？从左侧进入 **插件发现**，应用会自动读取在线目录，把分散的插件整理成可以直接浏览和行动的推荐页面。

<p align="center">
  <img src="assets/plugin-discovery-desktop.png" alt="DeepSeek Harness Studio 插件发现真实桌面界面" width="100%">
  <br><sub>真实 Desktop 界面：目录精选、最近更新、生态热门、场景分类、搜索以及安装与管理入口。</sub>
</p>

- **每天都有新发现**：打开页面即可看到目录精选、最近更新和生态热门，不必逐个仓库搜索。
- **按场景快速筛选**：覆盖 Agent 与工作流、Web UI、浏览器与搜索、视觉与媒体、记忆与上下文、模型与服务、开发工具、集成与通知。
- **直接搜索答案**：按插件名称、功能关键词或作者检索，并查看头像、简介、版本和更新时间。
- **发现后立即使用**：未安装插件可直接进入安全安装流程；已安装插件可一键转到插件中心继续管理。

### 不知道准确包名？让 Agent 先替你筛选

只知道“想要一个桌面宠物”这类需求时，不必先猜 npm 包名。在 **插件发现** 中输入自然语言描述，应用会把它作为 `/find-plugins` 请求交给当前 Agent；Agent 加载内置技能、只读查询公开 `dsh-plugin` 目录，并把最相关的候选、版本、作者、更新时间和匹配理由返回当前对话。

<p align="center">
  <img src="assets/plugin-agent-finder-desktop.webp" alt="Agent 在真实桌面客户端中执行 find-plugins，搜索桌面宠物并返回五项插件推荐" width="100%">
  <br><sub>真实 Desktop 验收：对话发出“找一个桌面宠物插件”，Agent 加载 <code>find-plugins</code>、执行公开目录搜索，并从 8 个结果中列出 5 个相关候选。</sub>
</p>

- **不要求记住关键词**：直接说明目标、使用场景或希望解决的问题。
- **推荐依据可核对**：结果包含精确包名、版本、发布者、更新时间和逐项匹配理由。
- **搜索与安装分开确认**：推荐结果只代表公开目录元数据；选定包名后仍通过 **插件中心** 完成兼容性检查和确认安装。

### 插件中心：在线安装、启停与移除

<p align="center">
  <img src="assets/plugin-center-avatars-desktop.png" alt="DeepSeek Harness Studio 公开插件中心真实界面" width="100%">
  <br><sub>真实 Desktop 界面：插件头像、公开目录、已安装区域、“安装”按钮与三点管理入口。</sub>
</p>

选定插件后进入 **插件中心**，可以用短包名、完整 npm 包名或明确 GitHub 仓库查找发布到 npm 公共 Registry 的插件与 Skill Pack。`dsh-plugin` 只是发现信号；GitHub 也只用于映射已发布 npm 包，Studio 不会直接安装仓库源码。确定版本仍须通过 Bundle、完整性和运行兼容校验。

- **在线发现**：搜索公开插件，查看版本、能力、权限、兼容性和风险说明。
- **一键安装**：下载确定版本并校验包身份、完整性和 Bundle 声明；确认后自动安装并重启 Harness Host 验证运行状态。
- **已安装管理**：集中查看系统、公开目录和本地来源，通过三点菜单启用、停用、更新或卸载插件。
- **安全移除**：卸载默认保留配置与插件数据；需要清理数据时，再由用户单独确认。

## Preset 广场已上线：一键安装完整工作方式

插件通常解决“让 Agent 多一个工具”，Skill 解决“教 Agent 按什么方法做”，而 **Agent Preset** 解决的是更完整的问题：把角色、工作规则、Skills、Plugin/MCP 与 Harness 标准工具组合成一套可以反复使用的工作方式。用户不需要逐项理解和手工配置，安装一个 Preset 后，就能直接用对应角色创建新会话。

| 能力层 | 它是什么 | 主要解决什么 |
| --- | --- | --- |
| **Skill** | 可复用的方法、步骤与约束 | 告诉 Agent 一类任务应该“怎么做” |
| **Plugin / MCP** | 可执行工具或外部服务连接 | 让 Agent 能真实读写系统、调用服务并完成动作 |
| **Agent Preset** | 角色、Skill、工具与运行规则的组合 | 把零散能力装配成一套开箱即用的数字员工或工作流 |

当前源码已经提供与“插件中心”“插件发现”平级的 **Preset 广场**，并完成发现、详情、安全安装、已安装管理、用于新会话、删除与重新安装的桌面端闭环。

<p align="center">
  <img src="assets/presets/preset-square-desktop.png" alt="DeepSeek Harness Studio Preset 广场真实桌面界面，展示赋范官方内置工作流" width="100%">
  <br><sub>真实 Desktop 界面：Preset 广场、赋范官方内置目录、搜索与排序，以及安装、查看详情和用于新会话入口。</sub>
</p>

> **使用路径：** 发现 Preset → 查看能力组成与前置条件 → 一键安装 → 在“已安装”中选择“用于新会话” → 按工作流完成任务 → 随时删除或重新安装。

1. 从左侧导航进入 *