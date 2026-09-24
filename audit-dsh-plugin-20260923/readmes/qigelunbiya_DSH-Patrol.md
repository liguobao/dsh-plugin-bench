# DSH Patrol

<p align="center">
  <strong>Teach once. Patrol repeatedly.</strong>
</p>

<p align="center">
  <a href="https://github.com/qigelunbiya/DSH-Patrol/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/qigelunbiya/DSH-Patrol/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Status" src="https://img.shields.io/badge/status-alpha-orange">
  <img alt="Distribution" src="https://img.shields.io/badge/distribution-GitHub%20source-blue">
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-6.x-3178C6?logo=typescript&logoColor=white">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-green"></a>
</p>

**DSH Patrol** 是面向 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 的浏览器 + Windows 桌面跨应用巡检 / Automation 插件：你只需要用自然语言把巡检流程教给 Agent 一次，验证后它会固化成 Runbook；之后由确定性 Runner 重放，不再让模型每次临场猜步骤。

**DSH Patrol is a browser + Windows desktop patrol automation plugin for DeepSeek Harness. Teach a workflow once, verify it, then replay it deterministically across managed Chromium and desktop applications.**

> 把「每次都让 AI 重新操作网页 / 应用」变成「教一次，后续稳定巡检」。

> **当前状态：Alpha / GitHub-first。** 现阶段推荐直接从 GitHub 克隆源码并使用仓库自带安装脚本。项目稳定后再考虑发布 npm 预构建包；目前 README 不把 npm 作为默认安装入口。

## 为什么用 DSH Patrol

- **自然语言教学**：直接描述“打开哪里、点什么、检查什么、截图什么”。
- **确定性重放**：教学完成后保存为 Runbook，后续重复巡检不依赖模型重新规划整条路径。
- **浏览器开箱即用**：自动寻找 Chrome / Edge / Chromium，使用独立持久 Profile，并自动加载内置扩展。
- **登录态可复用**：专用浏览器 Profile 可以跨 Harness 重启保留 Cookie / Session。
- **安全凭据引用**：Runbook 保存 `${credential:REF}`，不保存明文密码、Token、OTP 或 Cookie。
- **Checkpoint / Resume**：遇到人工令牌、扫码、二次确认等步骤可以暂停，人工完成后继续原 run。
- **截图与页面摘要**：巡检结果可以落地截图、页面文本、JSON / Markdown 报告和确定性摘要。
- **保守的 Selector 自愈**：只在唯一、精确的语义匹配下进行一次重试；真正修改 selector 需要显式确认。
- **Windows Desktop Automation**：桌面应用优先走 Windows UI Automation；不足时依次使用快捷键、Windows OCR、CURRENT 坐标后备。
- **跨应用 Runbook**：同一条流程可以先巡检网页并生成截图，再激活微信/WPS/百度网盘等桌面应用继续操作。
- **应用知识库**：内置 `微信.md`、`WPS.md`、`百度网盘.md`，并支持工作区自定义 Markdown 指南覆盖。
- **跨步骤 Artifact 引用**：桌面步骤可用 `${artifact:last-screenshot}` 获取本轮前面生成的最近截图。

适合的场景包括：内部运维后台巡检、业务系统日常检查、网页状态核对、需要登录态的重复流程、截图留证、人工令牌介入的半自动巡检，以及“网页巡检 → 桌面应用通知/归档”的跨应用工作流。

## Desktop Automation（Windows）

Desktop Automation 与现有 Browser Patrol **彼此独立**：Browser Bridge、受管 Chromium 和网页 Runbook 仍按原逻辑工作；桌面能力通过独立的 `dsh-patrol/desktop-tools` Agent 插件提供。

当前桌面执行策略：

```text
Windows UI Automation
        ↓ 找不到 / 应用自绘
快捷键 / 键盘
        ↓ 仍不足
截图 + Windows OCR
        ↓ 仍不足
基于 CURRENT 视觉证据的坐标点击 / 拖拽
```

主要原语包括：

- `desktop_list_windows` / `desktop_activate_window`
- `desktop_snapshot` / `desktop_click_target` / `desktop_click_ocr_text`
- `desktop_hotkey` / `desktop_press` / `desktop_type_text` / `desktop_paste` 支持稳定顶层窗口 selector，执行前自动重新激活目标应用
- `desktop_type_target`（按 UIA selector 定向聚焦并输入）
- `desktop_wait_for_target`（UIA → OCR 的语义就绪等待；非密码 UIA ValuePattern 也可作为安全的普通文本状态证据）/ `desktop_wait`
- `desktop_screenshot` / `desktop_ocr`
- `desktop_click_coordinates` / `desktop_drag`
- `desktop_set_clipboard_text` / `desktop_set_clipboard_files` / `desktop_paste`
- `desktop_launch_app` / `desktop_open_path` / `desktop_close_window`
- `desktop_delete_path`
- `desktop_list_app_guides` / `desktop_read_app_guide`

需要把成功的桌面操作写入 Runbook 时使用 `patrol_desktop_action`。当前版本按项目调试阶段要求，**TEST MODE 与 NORMAL MODE 的 Desktop Automation 都暂不做动作权限分级**；消息发送、文件删除、关闭窗口等动作不会被 Patrol 自己额外拦截。后续 NORMAL MODE 分级由项目维护者基于真实使用反馈再设计。

### 应用知识库

内置目录：

```text
desktop-knowledge/
├── 微信.md
├── WPS.md
└── 百度网盘.md
```

工作区可以创建：

```text
patrol-desktop-knowledge/微信.md
```

或：

```text
.dsh-patrol/desktop-knowledge/微信.md
```

同名工作区指南优先于插件内置指南。知识库提供快捷键、常见操作顺序和恢复经验，但真正执行前仍以 CURRENT `desktop_snapshot` / `desktop_ocr` 为准。

### 浏览器截图发送到桌面应用

Runbook 支持：

```text
browser_screenshot
      ↓
${artifact:last-screenshot}
      ↓
desktop_set_clipboard_files
      ↓
desktop_paste
```

因此后续可以构建类似：

```text
打开巡检网站
→ 生成网页截图
→ 激活微信
→ Ctrl+F 搜索联系人
→ 打开目标聊天
→ 把本轮网页截图放进剪贴板
→ 粘贴并发送
```

首个桌面实际验证目标为 Windows 微信。

更完整的 Desktop Automation 架构、纯桌面/跨应用流程说明以及微信首轮联调步骤见 [`docs/desktop-automation.md`](docs/desktop-automation.md)。

## 快速开始

### 当前推荐：GitHub 源码安装

现阶段最稳妥的方式是把 **DSH Patrol** 和 **DeepSeek Harness** 都放在本机，然后运行仓库提供的 PowerShell 安装脚本。

前置条件：

- 已安装 Git。
- Node.js `>= 22`。
- 已安装 pnpm。
- 本机已有可运行的 DeepSeek Harness 源码环境。
- Windows PowerShell / PowerShell 7 可执行仓库内的 `.ps1` 安装脚本。

### 1. 克隆 DSH Patrol

```powershell
git clone https://github.com/qigelunbiya/DSH-Patrol.git
cd DSH-Patrol
```

### 2. 安装到你的 DeepSeek Harness

假设 Harness 位于：

```text
D:\deepseek-harness
```

执行：

```powershell
.\scripts\install-local.ps1 `
  -HarnessRoot "D:\deepseek-harness"
```

安装脚本会自动执行依赖安装、类型检查、测试、扩展检查、UTF-8 检查和构建，然后安装 Patrol preset、Host Browser Bridge、Web client integration 与生命周期清理协调器。

### 3. 启动 Harness

```powershell
cd D:\deepseek-harness
pnpm dsh web
```

### 4. 新建会话，选择「巡检模式」

Patrol 会自动启动自己的受管浏览器，不需要手工打开 `chrome://extensions`、开启开发者模式、Load unpacked、填写 WebSocket 地址或点击 Connect。

### 5. 直接描述巡检

例如：

```text
帮我创建一个网页巡检。
巡检名称：Example Domain 测试巡检。
地址：https://example.com
不需要登录。
打开页面，确认存在“Example Domain”，读取页面内容，截图，并生成报告和页面摘要。
```

正常体验应当是：

```text
克隆 DSH Patrol
    ↓
运行 install-local.ps1
    ↓
启动 DeepSeek Harness
    ↓
新建会话并选择「巡检模式」
    ↓
Patrol 自动启动专用浏览器
    ↓
Patrol 自动加载并连接扩展
    ↓
用自然语言教学并确认 Runbook
    ↓
后续由 Runner 重复巡检
```

如果 Managed Browser 自动启动失败，Patrol 应直接报告自动探测 / 启动错误；**不应该把用户退回到手工安装浏览器扩展的流程。**

## 更新 DSH Patrol

如果之前已经 clone 过仓库，需要更新到最新 `main`：

```powershell
cd DSH-Patrol
git checkout main
git pull --ff-only origin main

.\scripts\install-local.ps1 `
  -HarnessRoot "D:\deepseek-harness"
```

然后重新启动 Harness：

```powershell
cd D:\deepseek-harness
pnpm dsh web
```

## GitHub Bundle 直接安装（可选 / Alpha）

仓库已经声明 `dsh.bundle`，因此也可以尝试让 Harness 直接从 GitHub dependency 安装：

```powershell
pnpm dsh plugin --profile web add github:qigelunbiya/DSH-Patrol
```

但当前 GitHub dependency 获取的是 TypeScript 源码，需要执行 `prepare` 构建；pnpm 10+ 的 build-script 信任策略可能要求额外允许 `dsh-patrol` 执行构建。

因此在当前 Alpha 阶段，**面向普通用户仍推荐 `git clone + scripts/install-local.ps1`**，它会显式完成构建和本地集成，问题也更容易定位。

## npm 发布计划

当前项目**不要求 npm 才能安装或使用**。GitHub 源码安装已经可以把插件部署到其他电脑上的 DeepSeek Harness 环境。

未来项目开发稳定后，可以再发布预构建 npm 包，把安装流程收口为：

```powershell
pnpm dsh plugin --profile web add dsh-patrol
```

在 npm 包真正发布并验证之前，**请不要把上面的裸包名命令当作当前默认安装方式**。

仓库已经保留 npm 打包检查和发布准备，后续不需要重新设计整个分发结构。维护者相关说明见 [`docs/publishing.md`](docs/publishing.md)。

## 工作方式

DSH Patrol 的核心原则是：

> **Agent 用于教学、解释和修复；Runner 用于重复执行。**

```text
第一次
自然语言需求
    ↓
Agent 观察网页并教学
    ↓
确认步骤
    ↓
Runbook

后续
Runbook
    ↓
Deterministic Runner
    ↓
浏览器操作 / 条件分支 / 截图 / 页面文本 / 报告
```

这与“每次运行都重新让 LLM 从头决定该点哪里”不同：Patrol 把高成本、非确定性的教学过程和后续高频重放过程分离。

## 本地开发：一条命令同步、安装并启动

如果你是项目维护者，并且目录结构类似：

```text
C:\work\
├── DSH-Patrol\
└── deepseek-harness\
```

在 `DSH-Patrol` 目录直接运行：

```powershell
.\scripts\dev.ps1
```

它会自动完成：

```text
检查工作区是否干净
→ checkout main
→ git pull --ff-only origin main
→ pnpm install / typecheck / test / checks / build
→ 安装 Patrol 到 Harness web profile
→ 启动 pnpm dsh web
```

如果 Harness 不在同级的 `deepseek-harness` 目录：

```powershell
.\scripts\dev.ps1 -HarnessRoot "D:\path\to\deepseek-harness"
```

只安装、不启动 Harness：

```powershell
.\scripts\dev.ps1 -NoStart
```

保留本地改动、不执行 `git pull`：

```powershell
.\scripts\dev.ps1 -SkipPull
```

`dev.ps1` 默认在拉取前检查 Git working tree；如果存在未提交修改会直接停止，避免为了“自动更新”覆盖开发代码。

## v0.2 当前能力

v0.2 的目标是把真实联调中暴露的问题收口，并尽量降低使用门槛：

- 独立 **「巡检模式」** Agent Preset，不在标准模式里全局注入 Patrol。
- Browser Bridge 的 WebSocket/HTTP transport 固定运行在 **Host plane**，巡检 preset 只注册 Agent-scoped `browser_*` 工具。
- Browser Cordis 插件使用 namespace plugin（`name` / `inject` / `apply`），避免 Harness Loader 解包 default export 后丢失 `inject`。
- 内置 **Managed Browser**：自动寻找 Chrome / Edge / Chromium，启动 DSH Patrol 专用持久浏览器 Profile，并由代码加载仓库内置 Chromium 扩展。
- `patrol_doctor` 检查真实 Browser Provider 与连接状态；Agent 不再猜 `browser_*` 工具名。
- Runbook 只允许固定浏览器 allowlist，`browser_eval` 不存在。
- 使用 Harness 原生 `ctx.credentials`，Runbook 只保存 `${credential:REF}`。
- 支持条件登录、checkpoint/resume、截图、页面文本、确定性 page-summary、保守 selector 自愈与显式修复。
- 网页内容始终按 **UNTRUSTED DATA** 处理，不能反向改变 Agent / Tool