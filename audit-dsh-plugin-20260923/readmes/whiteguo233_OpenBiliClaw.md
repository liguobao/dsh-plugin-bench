<div align="center">

# 🦀 OpenBiliClaw

**通用个性化内容推荐 Agent——本地运行、跨平台理解你、只为你一个人构建**

*A general-purpose personalized content discovery Agent — runs on your machine, understands only you*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Release](https://img.shields.io/github/v/release/whiteguo233/OpenBiliClaw?filter=openbiliclaw-v*&style=flat-square&label=Release&color=success)](https://github.com/whiteguo233/OpenBiliClaw/releases/latest)
[![下载数](https://img.shields.io/github/downloads/whiteguo233/OpenBiliClaw/total?style=flat-square&label=downloads&logo=github)](https://github.com/whiteguo233/OpenBiliClaw/releases)
[![星标](https://img.shields.io/github/stars/whiteguo233/OpenBiliClaw?style=flat-square&label=stars&logo=github)](https://github.com/whiteguo233/OpenBiliClaw)
[![CI](https://img.shields.io/github/actions/workflow/status/whiteguo233/OpenBiliClaw/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/whiteguo233/OpenBiliClaw/actions/workflows/ci.yml)
[![讨论帖](https://img.shields.io/badge/LINUX_DO-讨论帖-orange?style=flat-square&logo=discourse)](https://linux.do/t/topic/1978894)
[![Chrome 应用商店](https://img.shields.io/chrome-web-store/v/cdfjfkdjjhdaccbldipkjhpibnfbiamg?style=flat-square&label=Chrome%20应用商店&logo=googlechrome&logoColor=white&color=4285F4)](https://chromewebstore.google.com/detail/cdfjfkdjjhdaccbldipkjhpibnfbiamg)
[![Gitee 镜像](https://img.shields.io/badge/Gitee-镜像-C71D23?style=flat-square&logo=gitee&logoColor=white)](https://gitee.com/whiteguo233/OpenBiliClaw)
[![DSH 插件市场](https://img.shields.io/static/v1?label=%E2%AD%90%20DSH&message=%E6%8F%92%E4%BB%B6%E5%B8%82%E5%9C%BA&color=7C3AED&style=flat-square)](https://dshfind.com/zh/plugins)

[项目主页](https://whiteguo233.github.io/OpenBiliClaw/) | [English](README_EN.md) | 中文

国内 AtomGit 托管：[OpenBiliClaw](https://atomgit.com/whiteguo233/OpenBiliClaw)（从 GitHub 自动同步源码）

</div>

> ### 🆕 重要更新：OpenBiliClaw 现在可以装进 DeepSeek Harness
>
> 新增 **DSH 客户端插件** —— 把 OpenBiliClaw 装进 [DeepSeek Harness](https://github.com/deepseek-ai/DeepSeek-Harness)：DSH 界面常驻第四栏（推荐 / 内容库 / 对话 / 画像 / 设置），并注册 22 个 Agent Bridge 工具，让 DSH 里的 Agent 也能读推荐、答探测、闭环学习——边用 DSH 干活，边刷跨平台个性化内容。→ [`github.com/whiteguo233/dsh-openbiliclaw`](https://github.com/whiteguo233/dsh-openbiliclaw)
>
> 📱 想要原生 App？Flutter 移动端客户端（Android / iOS / Web / 桌面）在独立仓库 [`OpenBiliClaw-mobile`](https://github.com/whiteguo233/OpenBiliClaw-mobile)：推荐、对话、画像、收藏 / 稍后再看 / 30 天历史一应俱全，连接同一本地后端。

> 🇨🇳 **国内下载（当前 v0.3.221）**：7 个最新包（插件、macOS / Windows 普通版与含模型版）已放到 [123 云盘国内下载](https://4001474255.share.123pan.cn/123pan/IxbZMh-90KO3)，分享永久有效并可直接打开下载；Gitee 附件与源码见 [Gitee v0.3.221 发行版](https://gitee.com/whiteguo233/openbiliclaw/releases/tag/openbiliclaw-v0.3.221)。

## 10 秒看懂 OpenBiliClaw

一个纯本地、私有、开源的自进化跨平台内容发现 Agent：从你的跨平台使用、反馈和对话中持续深化心理画像，带着对你的理解主动去 B 站、小红书、抖音、YouTube、X、知乎、Reddit、Linux.do、Bangumi、V2EX、微博、GitHub 与开放 Web 找内容。

| 跨平台 | 本地优先 | 可调教 |
|---|---|---|
| B 站 / 小红书 / 抖音 / YouTube / X / 知乎 / Reddit / Linux.do / Bangumi / V2EX / 微博 / GitHub / Web | 数据默认留在本机 SQLite | 喜欢、不感兴趣、聊天反馈都会改变后续推荐 |

<p align="center">
  <a href="https://chromewebstore.google.com/detail/cdfjfkdjjhdaccbldipkjhpibnfbiamg"><b>安装浏览器插件</b></a>
  ·
  <a href="#快速开始"><b>让 AI 助手部署后端</b></a>
</p>

<p align="center">
  <sub>喜欢这个方向？<a href="https://github.com/whiteguo233/OpenBiliClaw">欢迎 Star 支持项目继续适配更多平台</a>。</sub>
</p>

<p align="center">
  <img src="docs/images/hero-demo-zh.gif" width="820" alt="OpenBiliClaw 跨平台本地推荐 Agent 演示：信号进入本地后端、生成画像、解释推荐理由、根据反馈继续学习" />
</p>

## 快速开始

普通用户只需四步；Firefox、Docker、脚本和手动部署等备用路径都在 [安装与部署详情](#安装与部署详情)。

1. **装插件** —— [Chrome 应用商店一键安装](https://chromewebstore.google.com/detail/cdfjfkdjjhdaccbldipkjhpibnfbiamg)（自动更新），或从 [Latest Release](https://github.com/whiteguo233/OpenBiliClaw/releases/latest) 下载 zip 手动安装（最新功能先到，商店版可能滞后几天）。
2. **装后端** —— 从同一个 [Latest Release](https://github.com/whiteguo233/OpenBiliClaw/releases/latest) 下载桌面安装包（macOS `.dmg` / Windows `.exe`，开箱即用、常驻菜单栏/托盘）。每个平台有两种安装包:**精简版**(默认,首启自动下载向量模型 bge-m3)与 **`-with-embedding` 完整版**(已内置 bge-m3 ~1.1GB,离线开箱即用)——网络差 / 想离线的选完整版,其余选精简版。**国内用户也可直接从 [123 云盘国内下载（v0.3.221）](https://4001474255.share.123pan.cn/123pan/IxbZMh-90KO3) 获取 7 个最新包。** 想改源码或深度定制,就把下面这句话粘给 Claude Code / Codex CLI / Cursor 等 AI 编程助手：

   ```text
   请按照 https://raw.githubusercontent.com/whiteguo233/OpenBiliClaw/main/docs/agent-install.md 的说明帮我部署 OpenBiliClaw 后端(务必用 Bash 的 curl 下载这个文档,不要用 WebFetch — 会丢关键指令)
   ```

3. **连接来源** —— 在装了插件的浏览器登录 [B 站](https://www.bilibili.com)（默认初始化来源），或改选小红书 / 抖音 / YouTube / X / 知乎 / Reddit / Linux.do / V2EX / 微博 / GitHub。Linux.do、Bangumi、V2EX、微博与 GitHub 均可公开发现；需要账号态的来源仍复用已安装插件，GitHub 则由后端官方 REST API 匿名读取公开 repository。GitHub 可用公开用户名把 starred repositories 用作初始化信号，PAT 只是可选的提额和身份校验方式。
4. **打开界面** —— 浏览器访问 `http://127.0.0.1:8420/web`；手机扫插件二维码打开 `http://<电脑局域网 IP>:8420/m/`，保存到主屏幕即可当 App 用；想要原生 App 体验，可安装独立仓库的 [Flutter 客户端](https://github.com/whiteguo233/OpenBiliClaw-mobile)（Android / iOS / Web / 桌面，安装包见 [Latest Release](https://github.com/whiteguo233/OpenBiliClaw-mobile/releases/latest)），在设置里填后端地址即可连接同一后端。

不在同一局域网时，`OpenBiliClaw-mobile` 的 **Android / iOS 原生 App** 已内嵌 `tsnet`，电脑端
也可让 OpenBiliClaw 自己加入同一 tailnet；Web / Linux / macOS / Windows Flutter 客户端不在
该能力范围。桌面安装包内置 helper；在电脑本机打开桌面 Web 或浏览器插件的
「设置 → 通用 → 应用内 Tailnet 远程访问」，开启后可选择留空走网页登录、填写
`tskey-auth-…` Auth Key，或填写带授权设备 tag 的 `tskey-client-…` OAuth Client Secret，
然后完整重启应用。凭据只在本机私有暂存到下一次启动，不进入 `config.toml`、API 回显或日志。
源码 / 一句话安装则先运行
`openbiliclaw tailnet build-helper`（需要 Go 1.26.6），再运行 `openbiliclaw tailnet enable`
并重启。电脑无需安装或全局开启系统 Tailscale；入口默认关闭、只在 tailnet 私网可见，
不启用 Funnel/Serve，建议同时在本机 Web 设置中开启应用密码（源码安装也可执行
`openbiliclaw set-password`）。详见[应用内 Tailnet](docs/modules/tailnet.md)。

## 用户交流群

<table>
  <tr>
    <td align="center" width="50%">
      <img src="docs/images/user-community-qrcode.png" width="200" alt="QQ 用户交流群二维码" /><br/>
      <b>QQ 用户群</b>
    </td>
    <td align="center" width="50%">
      <a href="https://discord.gg/PU6Xgch8yg"><img src="docs/images/discord-community-qrcode.jpg" width="200" alt="Discord 社区二维码" /></a><br/>
      <b>Discord 社区</b><br/>
      <sub>扫码或<a href="https://discord.gg/PU6Xgch8yg">点击加入</a>，链接长期有效</sub>
    </td>
  </tr>
</table>

## 为什么需要 OpenBiliClaw？

> 名字起源于 B 站（`Bili` = Bilibili，`Claw` = 爪子），项目最早只支持 B 站。从 v0.3.0 起已扩展为通用跨平台 Agent，覆盖 B 站 / 小红书 / 抖音 / YouTube / X / 知乎 / Reddit / Linux.do / Bangumi / V2EX / 微博 / GitHub 与通用 Web，持续接入更多内容平台。

推荐系统本质上是一个**中间商**——平台站在海量内容和海量用户之间做匹配分发。现代推荐系统远比「优化点击率」复杂：它同时权衡点击率、完播率、点赞/投币概率、停留时长、用户留存、创作者生态健康、广告收入等十几个目标，把它们加权压成一个分数来排序。听起来很科学，但问题在于：**这些权重是平台定的，优化目标归根结底是平台的**——用户满意度只是被当作留存和变现的手段，而非目的本身。你以为你在挑内容，其实是中间商在替你决定你能看到什么。结果就是：推荐越来越像你已经看过的东西，偶尔的惊喜全靠运气。

而且每个平台都是一座孤岛。你在 B 站看了三年机械键盘，小红书完全不知道；你在小红书种草的咖啡器具，B 站从来不会推给你。你的兴趣被割裂在不同平台的数据库里，没有人帮你把它们连起来。

**OpenBiliClaw 反过来。** 它是一个本地运行的 AI Agent——先深度理解你，再根据对你的理解**跨平台**主动搜寻你会喜欢的内容。项目从 B 站起步，现已覆盖小红书、抖音、YouTube、X（Twitter）、知乎、Reddit、Linux.do、Bangumi、V2EX、微博、GitHub 和开放 Web：

### 🧠 先懂你，再找内容

不是从视频出发匹配标签，而是从你出发。通过行为分析推断 MBTI、认知风格、深层心理需求，构建五层灵魂画像（事件→偏好→觉察→洞察→灵魂）。它理解的是你这个人，不是你的点击记录。

### 🔮 根据理解主动探索，而非被动匹配

这是和传统推荐最核心的差异：系统会基于对你的理解，**主动猜测你可能感兴趣但从未接触过的领域**。一个关注机械表的人可能会喜欢建筑美学，一个看量子物理科普的人可能对哲学感兴趣——它用心理学桥接逻辑主动出击，猜对了升级为正式兴趣，猜错了安静退出。协同过滤永远不会推给你「没人从这条路径走过」的内容，但 OpenBiliClaw 会。

### 🔒 100% 本地，100% 你的

核心行为、推荐和对话数据留在你硬盘上的 SQLite，配置、画像、凭据与缓存也只保存在本机文件中。LLM 默认用你自己的 API Key，也可实验性复用本机 Codex CLI 的 ChatGPT OAuth 凭据。没有 OpenBiliClaw 运营的云端账号，没有任何人能看到你的画像。这个 Agent 怎么长，完全你说了算——反馈推荐、对话调教、换 LLM、迁移或改数据库，随你。

> 💡 **和其他推荐工具的对比**
>
> | | 各平台官方推荐 | 关键词过滤插件 | OpenBiliClaw |
> |---|---|---|---|
> | 推荐逻辑 | 协同过滤 | 标签匹配 | 心理画像 + 五层记忆 |
> | 内容来源 | 单一平台 | 单一平台 | 跨平台（B 站 · 小红书 · 抖音 · YouTube · X · 知乎 · Reddit · Linux.do · Bangumi · V2EX · 微博 · GitHub · Web） |
> | 信息茧房 | 越推越窄 | 不解决 | 猜测兴趣主动破茧 |
> | 数据归属 | 平台所有 | 通常云端 | 100% 本地 |
> | 推荐解释 | "猜你喜欢" | 无 | 像朋友一样告诉你为什么 |
> | 可定制 | 不可以 | 低 | 换 LLM / 改画像 / 写 Skill |

## 📸 功能预览

核心入口现在有五个：浏览器插件负责平台内交互和登录会话，桌面端 