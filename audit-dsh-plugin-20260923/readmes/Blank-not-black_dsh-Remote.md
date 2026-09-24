# DSH Remote

> **把电脑上的 DSH，带到你的掌心。**
>
> DSH Remote 是一套面向 DSH 的远程控制台：在手机或另一台电脑上查看会话、处理审批与提问、传输文件，并掌握主机运行状态。

**中文** · [English](README.en.md)

[![npm](https://img.shields.io/npm/v/dsh-remote-plugin)](https://www.npmjs.com/package/dsh-remote-plugin)
[![Release](https://img.shields.io/github/v/release/Blank-not-black/dsh-Remote?label=release)](https://github.com/Blank-not-black/dsh-Remote/releases/latest)
[![CI](https://img.shields.io/github/actions/workflow/status/Blank-not-black/dsh-Remote/release-build.yml?branch=main&label=CI)](https://github.com/Blank-not-black/dsh-Remote/actions/workflows/release-build.yml)
[![Compat](https://img.shields.io/github/actions/workflow/status/Blank-not-black/dsh-Remote/compat.yml?branch=main&label=compat)](https://github.com/Blank-not-black/dsh-Remote/actions/workflows/compat.yml)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Android](https://img.shields.io/badge/Android-远程控制台-3DDC84?logo=android&logoColor=white)](https://github.com/Blank-not-black/dsh-Remote/releases/latest)
[![WebUI](https://img.shields.io/badge/WebUI-桌面与移动端-5B8CFF)](https://github.com/Blank-not-black/dsh-Remote)
[![dshbase listed](https://dshbase.com/badges/dsh-Remote.svg)](https://dshbase.com/plugins/dsh-Remote/)
[![dsh.so risk](https://www.dsh.so/badge/dsh-remote-2.svg)](https://www.dsh.so/artifact/dsh-remote-2/)
[![dsh.so install](https://www.dsh.so/badge/install/dsh-remote-2.svg)](https://www.dsh.so/artifact/dsh-remote-2/)
[![Awesome DSH Plugin](https://awesome-dsh-plugin.com/badge.svg)](https://awesome-dsh-plugin.com)
[![dsh-remote-plugin on dsh.fish](https://dsh.fish/a/dsh-remote-plugin/badge.svg)](https://dsh.fish/a/dsh-remote-plugin)
[![dshplugin.dev listed](https://dshplugin.dev/badges/blank-not-black-dsh-remote-plugin.svg)](https://dshplugin.dev/plugins/blank-not-black-dsh-remote-plugin)
[![dshfind](https://dshfind.com/api/badge/Blank-not-black/dsh-Remote)](https://dshfind.com/en/plugins/Blank-not-black/dsh-Remote?ref=badge)

<p align="center">
  <a href="#-快速开始">快速开始</a> ·
  <a href="#-应用内截图">查看截图</a> ·
  <a href="#-下载">下载</a> ·
  <a href="https://github.com/Blank-not-black/dsh-Remote/issues">反馈问题</a>
</p>

<p align="center">
  <em>不是把整台电脑搬到手机上，而是把 DSH 最重要的决策面带到你身边。</em>
</p>

DSH Remote 由三个相互配合的部分组成：DSH 插件、独立网关和 Android 应用 / WebUI。插件负责在 DSH 侧提供入口并管理网关；网关负责鉴权、实时连接和文件传输；手机端与桌面端则把不同场景下的远程操作做得更清晰、更顺手。

### 3 分钟开始连接

```sh
dsh plugin --profile web add dsh-remote-plugin
```

完整重启 DSH Web 后，从侧栏打开 DSH Remote。管理控制台会按顺序检查 DSH、网关、局域网地址、主机防火墙、终端配对与实时通道；跟随提示启动网关并扫码，即可在手机继续会话。详细步骤和故障排查见[快速开始](#-快速开始插件模式推荐)。

> 手机和电脑应位于同一可信局域网，或通过 Tailscale 互通。不要把网关端口直接暴露到公网，也不要公开配对令牌。

## ✨ 为什么是 DSH Remote

| 能力 | 你能得到什么 |
| --- | --- |
| 🧠 会话远程控制 | 随时查看会话、继续工作、切换模型和自定义思考档位、处理目标与后台任务 |
| 🔔 实时决策通知 | 审批、提问、任务状态实时到达；网络波动时自动降级并恢复 |
| 📁 文件与图片 | 浏览主机目录、断点传输文件，把照片或相册图片作为会话附件发送 |
| 📊 运行全景 | DSH 版本、网关链路、设备连接、Token、费用和近期活动集中呈现 |
| 🌐 多网络接入 | 支持局域网、Tailscale 和可靠的 WebSocket 隧道 |
| 🎨 一套设计语言 | 手机端、桌面端、插件面板和管理控制台共享主题与状态色 |

## 🧩 三个部分，各司其职

| 部分 | 角色 |
| --- | --- |
| **DSH 插件** | 提供 DSH 内入口，自动管理网关，展示主机与网关状态 |
| **独立网关** | 负责令牌鉴权、实时 mux/host 链路、文件传输和设备监控 |
| **Android 应用 / WebUI** | 提供手机、桌面浏览器和插件内嵌的远程操作界面 |

> 🔐 令牌就是远程控制凭证。默认不额外引入账号系统，部署简单，但请像保护 SSH 密钥一样保护它。

## 🖼️ 应用内截图

真实界面示例，截图中的会话标题、地址和令牌已做模糊处理。

<table>
  <tr>
    <td align="center"><img src="docs/screenshots/mobile-home-0.6.9-rc.1.png" alt="新版手机端主页" width="280"><br><sub>新版主页：链路健康、运行指标与活动</sub></td>
    <td align="center"><img src="docs/screenshots/mobile-settings-0.6.9-rc.1.png" alt="新版手机端设置" width="280"><br><sub>新版设置：服务器、通知、皮肤与反馈</sub></td>
  </tr>
</table>

<p align="center">
  <img src="docs/screenshots/plugin-panel-latest.png" alt="DSH Remote 插件面板" width="520"><br>
  <sub>插件面板：网关状态、用量概览与快捷控制</sub>
</p>

<p align="center">
  <img src="docs/screenshots/gateway-control-latest.png" alt="DSH Remote 网关管理控制台" width="900"><br>
  <sub>网关控制台：版本、设备、请求和 Token 用量一屏掌握</sub>
</p>

## 🎯 适合什么场景

- DSH 在电脑上运行，但你想用手机查看会话、回复提问或处理工具审批。
- 你需要在手机与 DSH 工作目录之间传输文件，或把图片作为当前会话的附件发送。
- 你需要从另一台电脑查看会话、文件、Token 统计和设备连接状态。
- 你希望通过局域网或 Tailscale 访问，而不为 DSH 额外搭建账号系统。

## 🧭 当前界面

### 📱 手机端 / Android 应用

手机端进入后默认显示主页，底部导航为：

| 页面 | 主要内容 |
| --- | --- |
| 会话 | 会话列表、工作台项目、运行状态、归档和新建会话 |
| 文件 | 目录浏览、下载、上传、断点续传、暂停/继续/取消 |
| 主页 | DSH 版本、网关状态、链路健康、待处理事项、近期活动 |
| 统计 | Token 四桶、token 量趋势、费用、高峰占比和近 7 日用量 |
| 设置 | 服务器、令牌、模型提供方、功能测试、通知、后台轮询、皮肤、更新和反馈 |

会话详情页支持实时消息、历史加载、目标控制、子代理中断、斜杠命令、模型切换、模型级思考档位和全屏输入。设置 → 模型中可为自定义提供方的每个模型配置档位名称、档位值、说明和默认档位；选择结果通过 DSH 适配器转换为第三方接口参数。全屏输入会保留会话标题栏，发送动作上移到标题栏；退出全屏可以点击收起按钮、下滑顶部手柄或使用系统返回键。

图片附件入口支持拍照和相册选择。图片会作为 `session.prompt` 的图片内容发送到当前 DSH 会话；图片能力仍取决于当前 DSH 组合和模型路由是否支持图像输入。

### 🖥️ 桌面端 WebUI

电脑浏览器打开网关地址时会自动进入桌面布局：

- 左侧会话列表与工作台项目；
- 文件传输；
- 主页总览；
- 统计抽屉；
- 设置、服务器分组和主题切换；
- 审批 / 提问通知卡片栈。

### 🛠️ 插件面板与管理控制台

DSH 插件入口提供快速状态面板，可查看网关运行情况、设备数、Token 用量和快捷操作。进入管理控制台后可以查看：

- 网关版本、运行时长、端口和 DSH 上游状态；
- 主机 IP、已连接设备、请求数、通道和最后活跃时间；
- Token 统计与近 7 日峰谷用量；
- 令牌复制、二维码配对和令牌轮换；
- 首次连接向导与 Doctor 自检，逐项显示 DSH、网关、网络、终端和实时链路状态；
- 网关启动 / 停止、自愈设置和更新检查。

## 📦 下载

所有正式版资产位于 [GitHub Releases](https://github.com/Blank-not-black/dsh-Remote/releases/latest)。RC 版本只用于真机验收，不会替代 Latest 正式版。

| 平台 | 资产 | 说明 |
| --- | --- | --- |
| Android | `dsh-remote.apk` | 手机远程控制台，支持相机、通知和应用内更新 |
| Windows x64 | `dsh-remote-win-x64.exe` | 单文件网关，不需要额外安装 Node.js |
| Linux x64 | `dsh-remote-linux-x64` | 单文件网关，赋予执行权限后运行 |
| macOS Apple Silicon | `dsh-remote-macos-arm64` | 独立预览产物，未承诺与主版本同步 |

## 🚀 快速开始：插件模式（推荐）

先确认 DSH Web 本身可以在这台电脑上正常打开，然后在安装 DSH 的同一用户下执行：

```sh
dsh plugin --profile web add dsh-remote-plugin
dsh plugin --profile web list --depth 0
```

第二条命令用于确认插件确实装进了 `web` profile。接着：

1. **完整重启 DSH Web 进程**。如果你是手动运行 `dsh web`，先停止旧进程再重新运行；如果你配置了 systemd 用户服务，可执行 `systemctl --user restart dsh-web`。
2. 在 DSH Web 中执行一次 Ctrl+F5，从左侧入口打开 DSH Remote 面板。
3. 在插件面板确认“网关已运行”，然后先在 DSH 主机上打开 `http://127.0.0.1:8787/health`。看到 JSON 即表示网关端口已可用。
4. 从插件面板复制令牌或打开配对二维码。令牌也保存在 `~/.dsh-remote/token`，请勿公开。
5. 安装 Android 应用，在「设置 → 服务器」中扫码，或手动填写 `http://电脑局域网IP:8787` 和令牌。手机中不能填 `127.0.0.1` 或 `localhost`，它们指向手机自己。
6. 另一台电脑可直接打开 `http://DSH主机IP:8787`，桌面浏览器会进入桌面 WebUI。

也可以安装指定版本或 Git 源：

```sh
# 指定正式版本
dsh plugin --profile web add dsh-remote-plugin@0.6.8

# monorepo 插件目录
dsh plugin --profile web add "github:Blank-not-black/dsh-Remote#main&path:/packages/plugin"
```

插件内置网关，默认监听 `0.0.0.0:8787`，并随 DSH 自动启动和自愈。网关意图保存在 `~/.dsh-remote/gateway.enabled`，令牌保存在 `~/.dsh-remote/token`。

## 🩺 网关打不开：按顺序排查

先在 **DSH 所在电脑** 上测试，再测手机。这样可以快速区分“网关没启动”和“网络无法到达”。

```bash
# 1. 网关是否在监听
curl -i http://127.0.0.1:8787/health

# 2. Linux 查看 8787 端口的真实占用者
ss -ltnp | grep ':8787'

# 3. DSH Web 上游是否可访问（默认 3080）
curl -i http://127.0.0.1:3080/
```

Windows 可用 `netstat -ano | findstr :8787`，或在 PowerShell 执行 `Invoke-RestMethod http://127.0.0.1:8787/health`。

| 现象 | 原因与处理 |
| --- | --- |
| 本机 `127.0.0.1:8787` 直接拒绝连接 | 网关未启动、插件未装在 `web` profile、自动启动被关闭，或者端口已被其他进程占用。先查插件面板，再完整重启 DSH Web。 |
| `/health` 返回 `ok: true` 但 `upstreamOk: false` | 网关已打开，是 DSH Web 上游不可达。检查 3080 端口和 DSH Web 进程；不要把 degraded 误当成网关未启动。 |
| 本机能打开，手机打不开 | 确认手机使用的是电脑局域网 IP 或 Tailscale IP，不是 `127.0.0.1`；确认两端网络互通、路由器未启用 AP 隔离，且防火墙允许 **TCP 8787 入站**。不需要对公网放行 DSH 3080。 |
| 页面打开但提示 401/未授权 | 网络正常，令牌不一致。从当前插件面板重新扫码，或重新复制 `~/.dsh-remote/token`。 |
| 页面黑屏或升级后功能没变 | 先 Ctrl+F5 强刷，手机端完全退出 App 后重开，避免旧静态资源缓存。 |
| 改过端口后 8787 打不开 | 实际端口优先级为 `DSH_REMOTE_GATEWAY_PORT` → `~/.dsh-remote/gateway-port` → 8787。手机、防火墙和浏览器地址必须同步修改。 |
| 网关运行中，但管理认证不可用 | 新网关会在健康探测时恢复缺失的令牌文件，且不会覆盖已有文件。检查 `TOKEN_FILE`、`DSH_REMOTE_TOKEN` / `TOKEN` 和文件权限；旧版本进程已丢失令牌时，须在主机上确认进程归属后手动重启一次。插件不会凭公开健康信息强杀进程。 |
| IPv6 DDNS 无法连接 | 插件监听地址优先级为 `DSH_REMOTE_GATEWAY_HOST` → `HOST` → `~/.dsh-remote/gateway-host` → `0.0.0.0`。设置 `DSH_REMOTE_GATEWAY_HOST=::` 或将 `::` 写入该文件后重启网关；独立网关使用 `HOST=::`。IPv4/IPv6 双栈是否同时可用取决于系统 IPv6 配置，默认监听范围保持不变。 |

如果使用 systemd 运行 DSH，还可查看：

```bash
systemctl --user status dsh-web --no-pager
journalctl --user -u dsh-web -n 100 --no-pager
```

> 插件拉起的网关可能是 transient 进程，不要把 `systemctl --user restart dsh-remote-gateway.service` 作为通用重启方式。优先使用插件面板的“启动网关”，或重启 DSH Web 让插件自愈拉起。发布日志或截图前，请隐藏令牌。

## 🧰 