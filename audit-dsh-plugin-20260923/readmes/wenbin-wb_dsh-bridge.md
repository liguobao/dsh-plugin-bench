# dsh-bridge

<p align="center">
  <img src="docs/banner.jpg" alt="dsh-bridge banner" width="100%" />
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@wenbin_wb/dsh-bridge"><img src="https://img.shields.io/npm/v/@wenbin_wb/dsh-bridge.svg?style=flat-square&color=38bdf8&logo=npm" alt="npm version" /></a>
  <a href="https://www.npmjs.com/package/@wenbin_wb/dsh-bridge"><img src="https://img.shields.io/npm/dt/@wenbin_wb/dsh-bridge.svg?style=flat-square&color=fbbf24&logo=npm" alt="npm downloads" /></a>
  <a href="https://github.com/wenbin-wb/dsh-bridge/releases"><img src="https://img.shields.io/github/v/release/wenbin-wb/dsh-bridge?style=flat-square&color=10b981&logo=github" alt="GitHub release" /></a>
  <a href="https://github.com/wenbin-wb/dsh-bridge/stargazers"><img src="https://img.shields.io/github/stars/wenbin-wb/dsh-bridge?style=flat-square&color=f43f5e&logo=github" alt="GitHub stars" /></a>
  <a href="https://nodejs.org/"><img src="https://img.shields.io/badge/Node.js-%E2%89%A522.19%20%7C%20%E2%89%A524-339933?style=flat-square&logo=node.js" alt="Node.js version" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/npm/l/@wenbin_wb/dsh-bridge?style=flat-square&color=a855f7" alt="license" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Security-Access%20Auth%20%2B%20PBKDF2-6366f1?style=flat-square&logo=security" alt="Security" />
  <img src="https://img.shields.io/badge/WeChat-ClawBot%20%7C%20iLink-07C160?style=flat-square&logo=wechat" alt="WeChat" />
  <img src="https://img.shields.io/badge/QQ%20Bot-OpenAPI%20v2-12B7F5?style=flat-square&logo=tencentqq" alt="QQ" />
  <img src="https://img.shields.io/badge/Feishu-WebSocket%202.0-00D6B9?style=flat-square&logo=lark" alt="Feishu" />
  <img src="https://img.shields.io/badge/Telegram-Bot%20API-24A1DE?style=flat-square&logo=telegram" alt="Telegram" />
  <img src="https://img.shields.io/badge/Cloudflare-Tunnel-F38020?style=flat-square&logo=cloudflare" alt="Cloudflare" />
</p>

<p align="center">
  <b>简体中文</b> | <a href="README.en.md">English</a>
</p>

> **DeepSeek Harness 多通道远程访问与全域安全门禁插件**
> 
> 手机扫个码，人不在电脑前也能继续用 DeepSeek Harness。无论躺在沙发上、出差通勤、还是跨网协作——都不用守着电脑，也不用自己搭公网服务器，扫码即可在手机、平板或任意设备上接着干。
> 
> 将您本地运行的 DeepSeek Harness 无缝延伸至手机网页、PWA 原生全屏应用、公网安全隧道、以及 **微信 / QQ / 飞书 / Telegram** 机器人矩阵。随时随地调度 AI 编写代码、执行任务、审批操作与管理工作区。

---

## 目录

- [✨ 功能特性](#-功能特性)
- [📦 环境要求与安装](#-环境要求与安装)
- [🚀 核心功能与使用指南](#-核心功能与使用指南)
  - [1. 🛜 局域网访问与多网卡智能切换](#1-🛜-局域网访问与多网卡智能切换)
  - [2. 🌐 公网隧道（Cloudflare 临时/固定域名 & 自建隧道）](#2-🌐-公网隧道cloudflare-临时固定域名--自建隧道)
  - [3. 📱 移动端交互与 PWA 独立全屏 App](#3-📱-移动端交互与-pwa-独立全屏-app)
  - [4. 🗂️ 远程工作区网页选择器](#4-🗂️-远程工作区网页选择器)
  - [5. 🔐 全域安全认证与防篡改门禁](#5-🔐-全域安全认证与防篡改门禁)
  - [6. 🤖 全能 IM 机器人矩阵（微信 / QQ / 飞书 / Telegram）](#6-🤖-全能-im-机器人矩阵微信--qq--飞书--telegram)
  - [7. 📊 运维监控看板与一键平滑重启](#7-📊-运维监控看板与一键平滑重启)
- [💬 常见问题 (FAQ)](#-常见问题-faq)
- [🛠️ 开发与贡献](#️-开发与贡献)
- [⭐ Star History](#-star-history)
- [📄 开源协议](#-开源协议)

---

## ✨ 功能特性

- **🛜 局域网多网卡智能识别与切换**：自动探测物理 Wi-Fi、以太网与虚拟网卡（WSL/VMware/Docker），支持在控制台可视化一键切换并记忆持久化，彻底解决多网卡 IP 不互通问题；
- **🌐 双模 Cloudflare 公网隧道**：免登录一键获取随机临时域名，或填入 Cloudflare Token 绑定固定域名并随 DSH 开机自启；支持 macOS 下 Gatekeeper 隔离自愈与全局探测；
- **📱 原生级移动端交互与 PWA 全屏应用**：动态居中会话标题、复用 DSH 原生侧边栏抽屉与 `[|` 收起图标、防重叠自适应工具栏，支持手机浏览器「添加到主屏幕」作为独立原生 App 运行；
- **🗂️ 远程工作区网页选择器**：手机端点击添加工作区唤出树形目录抽屉浏览器，电脑本机点击自动分流调用系统原生选择窗口；支持 IM 指令 `/addworkspace` 远程注册；
- **🔐 全域安全认证与双防线门禁**：专属二维码 256-bit Token 免密直通、外部访问密码门禁、独立后台管理员防篡改锁；内置物理机（`127.0.0.1`）最高特权与终端一秒救急重置（`reset-auth`）；
- **🤖 全能 IM 机器人矩阵（微信 / QQ / 飞书 / Telegram）**：支持多工作区会话调度、跨重启会话持久化、Markdown 打字机流式输出、Card 2.0 原生一键点击审批与文件双向直传；
- **📊 运维看板与平滑升级**：系统 CPU / 内存 / Uptime 实时看板、网络连通性一键诊断、全局配置 JSON 导出恢复、npmmirror 极速版本检查与平滑重启。

---

## 📦 环境要求与安装

### 环境要求

1. **Node.js ≥ 22**（DSH 要求 `^22.19.0` 或 `≥ 24.0.0`）
2. **dsh CLI 可用**（能在终端直接运行 `dsh` 命令）

```bash
# 检查 Node 版本
node -v   # 应显示 v22.19+ 或 v24+

# 检查 dsh 是否可用
dsh --version
```

### DSH 版本兼容性

本插件**同时兼容新旧 DSH**，无需按 DSH 版本挑选插件版本：

| DSH 版本 | 状态 |
| --- | --- |
| `0.1.0` ~ `0.1.1` | ✅ 支持（回环专用 RPC 通道加固） |
| `0.1.2` ~ `0.1.4` | ✅ 支持 |
| `0.1.5-alpha.1` ~ `0.1.5-rc.2` | ✅ 支持（v2.10.9 起） |

> **关于 DSH 原生鉴权**：DSH 从 `0.1.2` 起为 `dsh web` 内置了浏览器鉴权——启动时会打印带一次性 token 的地址（`http://127.0.0.1:3080/?token=…`），换取一枚绑定回环地址的会话 cookie，此后 `/`、`/api` 及各插件 RPC 通道都要求该 cookie。
>
> 这与本插件的**访问密码门禁是两层互补的防护**，不冲突也不重复：原生鉴权保护的是"本机回环上的 DSH 进程"，本插件的门禁保护的是"经局域网 / 公网隧道进入的远程访问"。本插件的反向代理会在转发时自动注入合法的回环会话 cookie，因此手机 / 隧道访问**无需**手动处理 DSH 的 `?token=`，按本页说明正常使用即可。

### 安装插件

```bash
# 方式一：从 npm 安装最新版（推荐）
dsh plugin --profile web add @wenbin_wb/dsh-bridge

# 方式二：免全局权限的 npx 方式
npx --yes @deepseek-ai/dsh plugin --profile web add @wenbin_wb/dsh-bridge

# 方式三：从源码安装
git clone https://github.com/wenbin-wb/dsh-bridge.git
dsh plugin --profile web add ./dsh-bridge
```

### 升级至最新版

```bash
# 方式一：在设置页「远程访问」底部点击「🚀 一键升级到最新版并重启」（推荐，全自动）

# 方式二：终端强制覆盖安装最新版
dsh plugin --profile web add @wenbin_wb/dsh-bridge@latest
```

> 💡 **提示（pnpm 11 用户）**：如果升级后仍显示旧版，是由于 pnpm 11 的 `minimumReleaseAge` 机制限制。在 Web 控制台点击「一键升级」即可自动跳过限制安装最新版。

---

## 🚀 核心功能与使用指南

启动 DeepSeek Harness 后，在设置面板找到 **「远程访问」** 即可开启全部功能：

---

### 1. 🛜 局域网访问与多网卡智能切换

插件启动后**自动随服务开启**局域网代理，无需手动配置。

<p align="center">
  <img src="docs/screenshots/lan-access.jpg" width="600" alt="局域网扫码访问控制台" />
</p>

* **零配置极速扫码**：同一 Wi-Fi 下打开手机相机扫码即可直达移动端 Web 界面；
* **多网卡智能切换**：当主机存在多张网卡（如物理 Wi-Fi、以太网、WSL 虚拟网卡、VMware、Docker 等）时，控制台自动展示 **「🛜 局域网网卡 / IP 选择」** 下拉框；智能评分高亮推荐物理网卡，点选后二维码与访问 URL 秒级重新生成并**自动持久化保存**。

---

### 2. 🌐 公网隧道（Cloudflare 临时/固定域名 & 自建隧道）

无需公网 IP 与路由器端口映射，随时随地从外网访问电脑上的 DeepSeek Harness：

<p align="center">
  <img src="docs/screenshots/tunnel-access.jpg" width="600" alt="公网隧道配置控制台" />
</p>

- **模式 1：极速免登录临时隧道（默认）**
  1. 直接点击「Cloudflare 隧道」卡片中的「开启」按钮；
  2. 系统全自动准备 `cloudflared` 二进制（macOS 自动剥离 Gatekeeper 隔离属性与自愈校验）；
  3. 几秒内自动生成公网 URL 和二维码，点「重置链接」可随时换新。

- **模式 2：Cloudflare Token 固定域名（永久不变 · 免费）**
  1. 在 [Cloudflare Zero Trust 控制台](https://one.dash.cloudflare.com/) 免费创建 Tunnel 并绑定域名（如 `dsh.yourdomain.com`）——**[📖 从零申请/配置完整教程](docs/cloudflare-fixed-domain.md)**（注册账号 → 接入域名 → 建隧道 → 取 Token → 绑定子域名 → 填回面板）；
  2. 展开卡片底部的 **「⚙️ 高级配置：固定域名 (Cloudflare Token)」**，填入自定义域名与 Tunnel Token 并保存；
  3. 勾选 **「随 DSH 启动自动开启」**，每次 DSH 重启即可自动恢复隧道，**URL 永久固定不变**！

- **模式 3：自建 WebSocket 隧道**
  * 支持连接个人 VPS 隧道中转服务器（[查看自建隧道部署教程](docs/custom-tunnel.md)），具备数据端到端 gzip 压缩与 SSE 响应优化。

> **自建隧道安全须知**：隧道服务端（`scripts/install-tunnel-server.sh`）只对「隧道客户端控制通道」校验 `TOKEN`；公网访客对隧道域名的 HTTP/WebSocket 转发**不再做独立认证**，安全完全依赖插件本地的「访问认证」（`x-dsh-internal-tunnel` 标识使隧道流量无法享受本机回环保留）。请务必在插件设置中开启「安全认证」并设置访问密码/二维码 Token（尤其 `scope=all` 或公网使用时）；未设置任何密码时，任何知道隧道地址的访客都能直接访问您的 DSH。

---

### 3. 📱 移动端交互与 PWA 独立全屏 App

针对手机屏幕与触控操作进行深度优化，无需额外配置即可获得原生 App 级流畅体验：

- **极简顶栏布局**：保留左侧菜单抽屉与右侧快速新建会话，顶部动态居中显示当前会话标题；
- **原生侧边栏抽屉**：完整复用 DSH 原生历史记录与工作区分类，顶部集成原生 `[|` 收起图标，支持边缘滑动与手势开合；
- **PWA 原生全屏支持**：在手机浏览器菜单点击「添加到主屏幕」即可作为 100% 独立原生全屏 App 运行（无浏览器地址栏与底栏）；
- **自适应防重叠排版**：底部工具栏根据屏幕宽度弹性自适应，彻底消除权限预设与模型选择器重叠碰撞。

#### 移动端对话与工作区管理体验

<p align="center">
  <img src="docs/screenshots/remote-web-mobile.jpg" width="23%" alt="移动端新会话主页" />
  &nbsp;
  <img src="docs/screenshots/mobile-chat.jpg" width="23%" alt="移动端已有对话交互" />
  &nbsp;
  <img src="docs/screenshots/mobile-drawer.jpg" width="23%" alt="移动端原生抽屉侧边栏" />
  &nbsp;
  <img src="docs/screenshots/mobile-workspace-picker.jpg" width="23%" alt="移动端远程工作区选择器" />
</p>

#### 远程访问与移动端设置中心

<p align="center">
  <img src="docs/screenshots/mobile-settings-lan.jpg" width="23%" alt="局域网访问控制台" />
  &nbsp;
  <img src="docs/screenshots/mobile-settings-tunnel.jpg" width="23%" alt="公网隧道配置" />
  &nbsp;
  <img src="docs/screenshots/mobile-settings-im.jpg" width="23%" alt="IM 机器人矩阵" />
  &nbsp;
  <img src="docs/screenshots/mobile-settings-security.jpg" width="23%" alt="全局访问安全认证" />
</p>

---

### 4. 🗂️ 远程工作区网页选择器

针对手机端或远程浏览器无法唤起本地电脑文件弹窗的痛点，内置响应式网页树形目录浏览器：

<p align="center">
  <img src="docs/screenshots/mobile-workspace-picker.jpg" width="380" alt="移动端远程工作区网页选择器" />
</p>

* **智能分流**：电脑本机访问（`127.0.0.1`）点击添加工作区直接呼出系统原生文件弹窗；手机或远程访问时自动弹出响应式底部目录抽屉；
* **极速直达**：支持 Windows 驱动器盘符（C盘、D盘）以及系统常用目录