<div align="center">

# dsh-clean-desktop-shell

**DeepSeek Harness 的纯净桌面壳（DSH 插件形态）**

只做一件事：给已配置好的 DSH Web 加一层干净的桌面窗口——系统托盘、单实例、像普通软件一样用。无毛玻璃、无花哨材质，**纯净**。

[English](README.en.md) · [中文](README.md)

[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-0078D6?logo=windows&logoColor=white)](https://github.com/Icather/dsh-clean-desktop-shell)
[![License](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)
[![Release](https://img.shields.io/github/v/release/Icather/dsh-clean-desktop-shell?color=blue)](https://github.com/Icather/dsh-clean-desktop-shell/releases/latest)
[![DSH](https://img.shields.io/badge/DeepSeek_Harness-0.1.2-4D6BFE)](https://github.com/deepseek-ai/deepseek-harness)
[![Contributors](https://img.shields.io/github/contributors/Icather/dsh-clean-desktop-shell?color=blueviolet)](https://github.com/Icather/dsh-clean-desktop-shell/graphs/contributors)
[![npm downloads](https://img.shields.io/npm/dt/dsh-clean-desktop-shell?logo=npm&color=cb3837&label=npm%20downloads)](https://www.npmjs.com/package/dsh-clean-desktop-shell)
[![Installs](https://img.shields.io/github/downloads/Icather/dsh-clean-desktop-shell/total?logo=github&color=2ea043&label=installs)](https://github.com/Icather/dsh-clean-desktop-shell/releases)
[![Clones](https://img.shields.io/badge/clones-364%20%2F%2014d-8957E5?logo=github&label=clones)](https://github.com/Icather/dsh-clean-desktop-shell)

</div>

## 这是什么

`dsh-clean-desktop-shell` 是一个 **DSH 插件形态** 的纯净桌面壳：它给已经跑起来的 DSH Web（默认 `http://127.0.0.1:3080`）套一层原生桌面窗口——系统托盘、单实例，像普通桌面软件一样使用。**不做任何视觉改造**：不加毛玻璃、不改界面，纯粹是"窗口壳"。

与生态里其他桌面端方案的最大区别：

| | 其他桌面端（如 dsh-desktop 系列） | 本插件 |
|:--|:--|:--|
| **形态** | 独立 Electron 应用，自带独立 profile | **DSH 插件**，挂载进现有 profile |
| **Profile** | 新建 desktop profile，插件/配置要重装 | **复用现有 web profile**，零迁移 |
| **视觉改造** | 自绘标题栏 / 毛玻璃等 | **零改造**，纯净窗口壳 |
| **跟随上游** | 固定版本 | **已适配 DSH 0.1.2 BrowserAuth**（冷启动自动认证；不接管、不杀外部后端） |

## 核心亮点

**① 像双击桌面应用一样，一键启动 DSH**

不用开终端、不用记命令。**双击桌面快捷方式，DSH 窗口立刻弹出**，和启动任何一个普通软件一样自然：

- 安装包自动创建桌面快捷方式；插件形态首次运行询问 + 托盘「创建桌面快捷方式」一键补建
- 双击即出窗——窗口不等后端、不做启动等待
- 单实例：重复双击只聚焦已有窗口，绝不重复开壳

**② 后端活性实时监测 · 快捷手动自主启停**

托盘**实时显示后端状态**（运行中 / 启动中 / 未运行 / 错误），一键启停：

- **响应监测**：保留 1,500 ms 探测超时。响应失败不等于进程退出：短暂或持续失败都保留已加载页面，只显示连接提示。
- **原页重连**：结合 HTTP 与客户端连接状态，通过客户端自身的连接服务恢复同步，不自动重载。自动重试沿用 4 秒探测节奏；手动重试共用防重复请求检查。
- **快捷启停**：托盘右键一键启动 / 重启 / 关闭后端（带进度弹窗）；「关闭后端」真正停掉 3080 端口上的服务，含外部启动的实例

## 使用

1. 若安装过插件，命令行启动 `dsh` 自动弹出桌面窗口；也可通过插件创建的桌面快捷方式双击，媲美原生桌面端的体验。
2. 使用原网页端的一切功能。
3. 托盘右键可以进行详细设置。正常连接时保持原网页；连接异常时显示恢复提示。

**后端启停等管理操作在托盘右键**：

- 启动 / 重启 / 关闭后端（带进度弹窗；关闭会真正停掉 3080 上的服务，包括外部启动的实例）
- 自动探测后端 · 设置后端安装文件夹（默认自动探测定位）
- 刷新窗口 · 创建桌面快捷方式 · 检查更新 · 仓库主页

**窗口的可靠性（保留页面的连接恢复）**：

- 双击启动立即出窗，不等后端就绪
- 启动时尚无可用页面，显示「后端未连接」页；后端启动就绪后加载
- 只有确认自管进程退出或明确停止已识别的后端，才切回离线页；外部后端失联仍按响应故障提示
- 持续故障提供「立即重试」与「重新加载页面」；后者是会丢失未保存页面状态的显式操作
- 离线页内置快捷按钮：重新加载 / 启动后端 / 自动探测后端 / 设置后端安装文件夹

壳不会因探测失败重建已加载文档，但第三方插件自身的断线处理仍可能改变其局部视图。确认退出与显式重载仍会离开当前页面。

## macOS 状态（v0.1.7 重要说明）

v0.1.7 修复了插件形态在 macOS 上无法定位 `Electron.app` 路径的问题（该 bug 导致窗口在 Mac 上完全静默失败）。

但**当前开发者没有 Mac 实机**，以下事项仍然依赖 Mac 用户验证/贡献：

- **.dmg 安装包未签名、未公证**：Apple 要求年度开发者计划（$99/年）才能给安装包签名+公证。首次打开 .dmg 里的应用，很可能提示「已损坏，无法打开」或「无法验证开发者」。这不是应用本身损坏，是 Gatekeeper 拦截了未签名应用。
  - 临时解决：`xattr -cr "/Applications/DSH Clean Desktop Shell.app"`，然后右键 → 打开。
  - 长期解决：需要一位有 Apple Developer 账号的 Mac 合作者协助签名/公证，或长期把 .dmg 安装体验写为「需要右键打开 / 执行 xattr」。
- **Electron.app 解压后的可执行位、quarantine 扩展属性等**只有真机能确认行为是否完全正确。
- **如果窗口还是没弹出来**：启动失败时会把诊断信息写到 DSH home 下的 `desktop-shell-launch.log`：

  ```sh
  cat "${DSH_HOME:-$HOME/.dsh}/desktop-shell-launch.log"
  ```

  把内容贴到 Issue 即可——里面记录了平台、架构、Node 版本、DSH home、运行时目录和具体报错。没有界面时，这是唯一能回传的信息。

诚挚邀请有 Mac 环境、愿意一起打磨的同学参与：能帮忙验证安装流程、补充签名配置、或者把开机自启/登录项做进 Electron 托盘，欢迎直接提 PR 或在 Issue 里 @ 我，我会把你加入 [CONTRIBUTORS.md](./CONTRIBUTORS.md)。

## 安全与权限：它到底做了什么

第三方安全扫描器（如 [dsh-xray](https://github.com/unStone/dsh-xray)）会给本项目打出「高能力 + 敏感行为」的评级。这个评级**没有误报**——列出的每一条都属实，但每一条都有明确且必要的原因。既然要装进你的机器，就该摊开讲清楚。

| 行为 | 为什么必须这么做 | 代码位置 |
|:--|:--|:--|
| 执行系统命令（spawn） | 壳的核心功能就是**启动 / 重启 / 停止 `dsh web` 后端**，以及探测 3080 端口占用。不调用系统命令无法实现。 | `electron/service.js` |
| 下载约 100MB 的 Electron 运行时 | 首次启动需要。两个源按网络环境自动竞速（3 秒超时）：`github.com` 与 `npmmirror.com`——后者是国内镜像，CN 网络下通常更快。 | `src/host/runtime.js` |
| 访问 `api.github.com` | 仅用于托盘「检查更新」拉取最新 Release 信息。 | `electron/update.js` |
| 读取环境变量 | 只用于定位路径和功能开关：`DSH_HOME`（DSH 主目录）、`DSH_SHELL_ELECTRON_DIR`（复用本地 Electron，跳过下载）、`DSH_SHELL_AUTO_LAUNCH=0`（关闭自动弹窗）、`USERPROFILE` / `APPDATA`（Windows 下定位 `dsh.cmd` 与快捷方式目录）。 | `src/host/common.js`、`src/host/index.js`、`electron/shortcut.js` |
| 修改 DSH 运行时（`cordis.patch.yml`） | **DSH 官方的插件注册机制**，所有 DSH 插件都靠它挂载，并非本项目特有行为。 | `cordis.patch.yml` |

**边界**：不上传任何数据、不读取会话内容、不回传遥测。全部网络请求只有上面两类（下载运行时 / 查更新），且都可通过设置 `DSH_SHELL_ELECTRON_DIR` 完全避免。

安装包的未签名警告（Windows SmartScreen、macOS Gatekeeper）来自**缺少代码签名证书**，与上述行为无关。

## 兼容性与运行边界

扫描器给出的「高能力」评级来自上一节那四类能力（文件 / 网络 / 命令 / 凭据）。下面把兼容范围、依赖、外部服务与失败边界摊开声明，供人工审阅——**声明不等于验收**，逐条注明证据。

### 兼容范围

| 项 | 声明 | 依据 |
|:--|:--|:--|
| Node.js | `>=20.0.0`（`engines.node`） | host 半边用全局 `fetch` 与 `AbortSignal.timeout`；Electron 半边跑在 Electron 33 内嵌的 Node 20.18 上。没有更新 API 的依赖。 |
| DSH | `>=0.1.1 <0.2.0`（`dsh.compatibility.dsh`） | 面向 0.1.x 的插件契约；0.1.2 之前没有 BrowserAuth，host 半边对该代有显式守卫（拿不到 `authenticatedUrl()` 时照常拉起窗口，只是不带 bootstrap URL）。 |

`dsh.compatibility.dshReleases` 逐版本标注实测状态：

| DSH 版本 | 状态 | 证据 |
|:--|:--|:--|
| `0.1.5-rc.1` | `compatible` | 真机端到端：token 横幅 → 插件自动弹壳 → 窗口渲染 UI 并写入 `dsh-auth` cookie；掉线保留页面、确认退出切离线页均实测通过 |
| `0.1.5-rc.2`、`0.1.5-alpha.2` | `unknown` | 未做运行验收 |
| `0.1.1-rc.2` | `unknown` | 「0.1.2 之前」这条代码路径有独立断言（真实 host 模块 + 无 `authenticatedUrl` 的 connection），但没在真实该版本上跑完整验收 |

### 依赖与生命周期脚本

| 类型 | 内容 |
|:--|:--|
| 运行时依赖 | `electron-updater`（托盘「检查更新」）、`semver`（版本比较）。两者都只在 Electron 半边使用；**host 半边不加载任何第三方依赖**。 |
| peer 依赖 | `@deepseek-ai/dsh`（可选）——宿主由 DSH 提供，不随本包安装。 |
| 开发依赖 | `electron`、`electron-builder`、`sharp`、`png-to-ico`（仅构建与图标生成）。 |
| 生命周期脚本 | **无。** 本包不声明 `preinstall` / `install` / `postinstall` / `prepare`；`scripts` 只有 `build` / `check` / `dev` / `icons` / `pack` 这些手动入口。 |
| 安装期脚本例外 | `pnpm.allowScripts` 放行了 `electron` 自身的 postinstall（它要下载 Electron 二进制）。这是**依赖的**脚本、不是本包的，且只在装开发依赖时出现。 |

### 外部服务

| 端点 | 何时访问 | 失败后果 |
|:--|:--|:--|
| `github.com` / `npmmirror.com` | 首次准备 Electron 运行时，两源 3 秒竞速下载（约 100MB） | 两源都失败 → 窗口不启动，并写入 `<DSH_HOME>/desktop-shell-launch.log`（含平台、错误原文与替代方案） |
| `github.com`（rcedit） | 首次给 runtime exe 打任务栏图标（约 1.3MB） | 下载限时 20 秒、整步限时 25 秒，超时只损失自定义图标，**不影响出窗**；下次启动重试 |
| `api.github.com` | 托盘「检查更新」/ 自动更新 | 静默失败，不影响使用 |
| 其他 | 无。不上传数据、不读会话内容、无遥测。 | — |

### 失败边界

- **后端起不来**：显示离线页并每 2.5 秒重探，后端一通立即加载。
- **后端掉线**：保留已加载页面 + 页内提示（不重载、不丢草稿）；只有确认进程退出或用户主动停止才切离线页。
- **非 Windows**：任务栏图标补丁直接跳过（`patchExeIcon` 首行 `isWin` 判断）。
- **找不到 `dsh` CLI**：托盘「设置后端文件夹」手动指定，或设 `DSH_BACKEND_DIR`。

### 一次性 Profile 验收记录

在一台干净的一次性 DSH home + 一次性 profile 上跑完整安装 / 启动 / 卸载循环（**不触碰日常 profile**），DSH `0.1.5-rc.1`、Windows 11：

| 步骤 | 命令 | 结果 |
|:--|:--|:--|
| 安装 | `dsh plugin --profile web add file:<repo>` | 退出码 0（pnpm 2.2s）；`--dump-config` 出现插件条目 |
| 启动 | `dsh web --no-open` | 打印 launch token 横幅；裸 `/` → 401、带 token → 303 + `Set-Cookie: dsh-auth-…`、带 cookie → 200；首页 manifest 含 `dsh-clean-desktop-shell/client.js`（插件在前端已挂载） |
| 插件拉起窗口 | 同上 | host 半边完整走通：`inject(['connection'])` 触发 → `webServer` 可解析 → 铸出 launch URL → `launchShell()` 被调用（用临时探针逐点断言）。**窗口是否可见未在本环境验收**：验收机是 CI 式无 GPU 沙箱，Electron 报 `FATAL: GPU process isn't usable` 后退出，与本插件无关（同一台机器上不带任何 GPU 参数的空白 Electron 应用同样退出，带 `--in-process-gpu` 则正常）。窗口渲染本身在此前用带 GPU 参数的 harness 单独验证过。 |
| 卸载 | `dsh plugin --profile web remove dsh-clean-desktop-shell` | 退出码 0（pnpm 1.4s）；`--dump-config` 中插件条目归零 |
| 回滚 | 卸载即回滚：`dsh.profile.bundles` 与 `dependencies` 同步移除，后端与窗口行为回到未安装状态 | — |

## 安装

**方式一：从 Release 下载安装包（想要独立桌面应用的用户）**

- Windows：下载 `DSH-Clean-Desktop-Shell-Setup-<版本>.exe`
- macOS：下载 `DSH-Clean-Desktop-Shell-<版本>.dmg`（Intel）或 `-arm64.dmg`（Apple Silicon）

安装包会**自动创建桌面快捷方式**，并提供系统托盘等完整桌面体验。

- **Windows**：首次运行安装包可能触发 SmartScreen 警告——**这是未签名程序的正常现象，不是病毒**，见下方「Window