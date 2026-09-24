<p align="center">
  <img src="docs/banner.jpg" alt="DSH Pocket" width="100%">
</p>

<h1 align="center">DSH Pocket</h1>

<p align="center"><a href="README.en.md">English</a> | <a href="README.md">中文</a></p>

<p align="center"><a href="https://trendshift.io/repositories/166736?utm_source=trendshift-badge&amp;utm_medium=badge&amp;utm_campaign=badge-trendshift-166736" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/166736/daily?language=JavaScript" alt="shaobeichen%2Fdsh-pocket | Trendshift" width="250" height="55"/></a></p>

<p align="center">
  <a href="https://www.npmjs.com/package/dsh-pocket"><img alt="npm" src="https://img.shields.io/npm/v/dsh-pocket?color=4d6bfe&label=npm"></a>
  <a href="https://www.npmjs.com/package/dsh-pocket"><img alt="downloads" src="https://img.shields.io/npm/dm/dsh-pocket?color=4d6bfe"></a>
  <a href="https://github.com/shaobeichen/dsh-pocket/actions"><img alt="CI" src="https://github.com/shaobeichen/dsh-pocket/actions/workflows/release.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-GPL--2.0-red.svg"></a>
  <a href="https://github.com/shaobeichen/dsh-pocket/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/shaobeichen/dsh-pocket"></a>
  <a href="https://awesome-dsh-plugin.com/zh/"><img alt="Awesome DSH Plugin" src="https://awesome-dsh-plugin.com/badge.svg"></a>
</p>

> 把 **DeepSeek Harness 装进你的口袋**：一个包、一个设置页，手机扫二维码就实时看到电脑上的同一个界面——人在外面也能用。

<p align="center">
  ⭐ 顺手留颗 Star，作者能高兴一整天 &nbsp;·&nbsp; <a href="https://github.com/shaobeichen/dsh-pocket">行，给你一颗 Star</a>
</p>

## 这是什么

**你不在电脑前，也想用电脑上的 DeepSeek Harness。**

- 下班路上，agent 在电脑上跑任务，你想掏出手机看看它干到哪了、结果如何
- 出门在外，突然想让电脑上的 agent 查点资料、写段代码，但没有远程桌面、没有 SSH
- 电脑在宿舍/办公室，你人在外面，想随时"操控你的 DeepSeek Harness"——发任务、看输出、点审批

DSH Pocket 就是干这个的：**装上它，手机扫个码，就能实时看到并操控电脑上的 DeepSeek Harness 界面**——人在外面也能用。

实际效果——手机上的界面就是电脑上的界面，实时同步：

<p align="center">
  <img src="docs/interface.jpg" alt="手机上的 DSH 界面" width="100%">
</p>

## ✨ 特性

| 特性                    | 说明                                                                                                                                                                               |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 📶 局域网扫码           | 装好即用：设置 → 手机访问，打开就有局域网二维码，手机连同一 WiFi 扫码即开（自动识别本机局域网 IP，**WSL 环境自动取 Windows 物理网卡 IP**）                                         |
| 🚪 局域网开关           | 设置页可**一键关闭/开启局域网访问**（切换时弹窗提醒）：关闭后局域网二维码/链接立即失效，仅公网可用                                                                                 |
| 🌐 公网扫码（人在外面） | 点「开启公网访问」→ cloudflared 隧道 → 出公网二维码，4G/任何网络都能访问                                                                                                           |
| 🏷️ 公网固定域名         | 可选「**命名隧道**」模式：填 Cloudflare Tunnel Token + 自己的域名，公网地址**固定不变**（重启不再变；见下方说明）                                                                  |
| 🔐 访问密码             | 公网链接默认使用 **8 位随机密码**（每次开启公网自动换新；**可自定义固定密码**——自定义后不再换新）；局域网有独立的默认 **8 位随机密码**（默认开启，设置页可**一键关闭**——关闭后局域网扫码直连） |
| 🔑 自定义密码           | 公网/局域网密码都可在设置页**设成自己固定的 8–64 位密码（英文字母大小写或数字）**（自定义后公网不再自动换新）                                                                         |
| 🧘 会话保持             | 手机输一次密码后**长期免输**（登录状态绑定电脑上的 dsh web 进程：只要它不重启，手机不用再输；**dsh web 重启/更新后需重新输入一次**）                                               |
| ⚡ 实时同步             | 流式输出走 WebSocket 全透传——**电脑上在输出，手机上同步在滚**，可双向操作；内置心跳保活（防路由器 NAT/省电机制静默断链，断线自动重连）                                             |
| 📱 移动端适配           | 窄屏自动变抽屉布局（移植 dsh-web-mobile，MIT）：侧栏抽屉、会话全宽、状态栏安全区、触控优化                                                                                         |
| 🧭 可选右边栏           | 手机端显示原生右边栏入口；普通手机可在设置中关闭以保持紧凑，折叠屏展开后可更方便地同时使用终端底栏和右边栏                                                                         |
| 📁 文件浏览             | 移动端「文件浏览」入口需要宿主提供 explorer 面板（dsh-web-ui 组件）；官方 DSH 未内置时入口自动隐藏，不会出现"点了没反应"                                                           |
| 🗜️ 传输压缩             | 大 JSON 响应自动 gzip/brotli（长会话 17MB → ~1MB，brotli 质量 6：快且省流量），手机加载更快、更省流量                                                                              |
| 🔁 隧道自动恢复         | DSH 重启后自动重新拉起之前开着的公网隧道，无需手动重开                                                                                                                             |
| 🧩 零依赖安装           | 一个 npm 包、一个设置页，没有核心/适配器要分开装；无需账号、无需服务器                                                                                                             |

## 🚀 怎么用

**入口在哪**：安装完成并重启 `dsh web` 后，打开 **设置**，左侧边栏就能看到 **「手机访问」** 入口（和「通用设置」「模型」同级）：

<p align="center">
  <img src="docs/entry.jpg" alt="手机访问入口" width="70%">
</p>

**前提**：电脑上已装好 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)。如果终端提示 `dsh: command not found`（找不到 dsh 命令），先安装：

```sh
npm install -g @deepseek-ai/dsh     # 全局安装；验证：dsh --version
# 不想全局装？每次命令前加 npx：npx @deepseek-ai/dsh <命令>
```

```sh
# 1. 装插件（一个包全都有）
dsh plugin --profile web add dsh-pocket -w

# 2. 重启 dsh web
npx @deepseek-ai/dsh web
```

### 局域网（同一 WiFi）

设置 → **手机访问** → 手机扫「📶 局域网」二维码 → 打开链接**输入局域网密码**（显示在设置页局域网区块，点「刷新」可换新，或点「自定义」设成自己固定的 8–64 位密码——英文字母大小写或数字）→ 打开的就是电脑上的 DSH，实时同步。

> 「**局域网访问**」开关默认**开**：可一键**关闭/开启**（切换时弹窗提醒）——关闭后局域网二维码/链接立即失效（手机打不开），**公网不受影响**；想恢复时再点「开」即可。
>
> 局域网密码**默认开启**（安全优先）。如果只有自己用、嫌每次输密码麻烦，可在设置页局域网区块把「局域网访问密码」切到**关**——之后局域网扫码直连、无需密码（仅同一局域网设备可访问；**公网始终要密码**，不受影响）。
>
> 手机登录一次后**长期免输**：只要电脑上的 dsh web 不重启，再次打开手机不用再输入（**dsh web 重启/更新后需重新输入一次**）。
>
> 高级选项：自动识别在 Tailscale/VPN 等场景下可能选不到可达地址。可在「局域网地址」下拉框手动选择已检测到的 IP；一般不需要修改。

### 公网（人在外面）

同一页点「**开启公网访问**」→ **每次都会先弹出安全免责声明**，勾选「我已知情」后才能开启（公司/涉密网络请先确认合规）→ 等隧道建立（首次会下载 cloudflared，macOS/Linux 走清华镜像秒下）→ 手机扫「🌐 公网」二维码 → 打开链接**输入访问密码**（密码显示在设置页公网区块，默认是**每次开启公网变新的 8 位随机密码**，也可点「自定义」设成 8–64 位固定密码——英文字母大小写或数字，自定义后不再换新）→ 人在外面（4G/公司网）也能访问。

> 更新到新版本：`dsh plugin --profile web update dsh-pocket --latest -w`（跨大版本时 `--latest` 是必须的，`^0.x` 范围不会自动升到 1.x）。

### 公网固定域名（命名隧道，可选）

默认「快速隧道」的公网地址每次重启都会变（前缀随机）。想要**固定公网地址**，可用 Cloudflare **命名隧道**（需要 Cloudflare 账号 + 自己的域名）：

1. 在 [Cloudflare Zero Trust](https://one.dash.cloudflare.com/) → **Networks → Tunnels** 创建一条 Tunnel，复制 **Tunnel Token**
2. 在该 Tunnel 的 **Public Hostname** 里把你的域名（如 `pocket.example.com`）的 Service 指向 `http://127.0.0.1:3081`
3. 回到设置页公网区块：模式切到「**命名隧道**」，粘贴 Tunnel Token、填写固定域名，保存
4. 点「开启公网访问」→ 公网地址固定为你的域名，**重启不再变化**

注意：命名隧道模式下公网密码**不自动轮换**（地址固定，重启后密码不变），建议配合「自定义密码」主动管理；Tunnel Token 只存本机（`$DSH_HOME/dsh-pocket/settings.json`，仅本机可读），设置页不回显。

## ⚠️ 安全（必读）

- **DSH 能执行你电脑上的代码**。**局域网**二维码/URL 配上独立 **8 位密码**才是钥匙（密码**默认开启**，可关——关闭后局域网扫码直连，仅同一网络设备可访问），**请勿把局域网二维码、URL 或密码发给别人**
- **开启公网访问前必须阅读并勾选免责声明**（每次开启都会弹框；服务端强制校验，无法绕过）：公网 = 把能执行代码的 DSH 暴露到互联网，请使用强密码、用完即关、涉密网络勿用
- **公网**默认有 **8 位随机密码**保护：链接随机分配、默认每次开启换新密码、旧链接立即作废——泄露了也进不来，改密码/重开即可作废；**自定义密码可设为 8–64 位英文字母或数字，且不再自动换新**
- 手机登录状态与电脑上的 dsh web 进程绑定：**电脑 dsh web 一直开着就不用重复输入；重启/更新后需重新输入一次**
- **登录限速**（防暴力破解）：同一 IP 连续输错 **5 次**锁定 **60 秒**；全局失败超阈值时短暂全锁（防换 IP 分布式扫描）；输对密码后计数清零
- 公网 URL 由 cloudflared 随机分配，**每次重启会变化**（旧链接自动失效，相当于天然轮换）；**命名隧道固定域名**模式下地址不变、密码不自动轮换，请配合自定义密码管理
- **公网判定是 fail closed**（issue #66）：除本机（loopback）和局域网私网地址外，**一切陌生域名（包括你自建隧道/反向代理指向本机端口的固定域名）一律按公网处理、强制公网密码**——不存在「换域名绕过密码」的口子
- 局域网模式不暴露公网，只有同一网络内的设备能访问
- 适合个人自用；公网密码存本机 `$DSH_HOME/dsh-pocket/token`（默认每次开启公网自动换新，**自定义后不换**），局域网密码存 `$DSH_HOME/dsh-pocket/token-lan`（设置页手动刷新），开关/自定义标记存 `$DSH_HOME/dsh-pocket/settings.json`
- **CLI 模式（命令行直跑 `dsh-pocket`）也有密码**（issue #90 修复前这条路是无认证的）：默认随机生成 8 位密码，打印在终端、并已内嵌进二维码（**扫码体验不变**），手动敲地址时需要填写，本机访问免密。`--pin <值>` 或 `DSH_POCKET_PIN=<值>` 自定义（至少 6 位）；`--no-auth` 可关闭，**不推荐**——那等于把能执行代码的 DSH 裸暴露给任何能连上该端口的人

## 💻 DSH Desktop（桌面版）

- 桌面版里 dsh-pocket 的**扫码同屏**正常可用；**更新/重启由桌面版管理**（插件内这两项自动停用）
- ⚠️ 桌面端 **advanced 模式**暂不支持手机访问（该模式禁用网页布局、手机拿不到 layout 服务，会白屏）——请切回 **compatibility** 模式后重启；advanced 模式下手机打开会看到明确的提示层

## 🩹 常见问题（