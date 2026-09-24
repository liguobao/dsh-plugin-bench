<p align="center">
  <a href="https://dshdesktop.cn"><img src="assets/desktop-hero-zh.png" alt="DSH Desktop：基于 DeepSeek Harness 构建的开源桌面客户端" width="100%"></a>
</p>

<h1 align="center">DSH Desktop</h1>

<p align="center">
  <strong>基于 DeepSeek Harness 构建的 Windows 和 macOS 开源桌面客户端。</strong>
</p>

<h3 align="center"><a href="https://dshdesktop.cn">一键下载，开箱即用。</a></h3>

<p align="center">
  万物皆「插件」，桌面本身也是「插件」。
</p>

<p align="center"><sub>独立的社区开源项目，与深度求索不存在隶属、合作、授权或背书关系。<br>本仓库目前无深度求索员工或 DeepSeek Harness 上游官方团队成员参与；GitHub Contributors 中显示的上游贡献者来自 fork 继承和同步的提交历史。<br>中文 · <a href="README.en.md">English</a></sub></p>

<p align="center">
  <img src="assets/desktop-chat-zh.png" alt="DSH Desktop 中文对话界面" width="100%">
</p>

<p align="center">
  <a href="https://github.com/anywhere-labs/deepseek-harness-desktop/releases/latest"><img src="https://img.shields.io/github/v/release/anywhere-labs/deepseek-harness-desktop?style=flat&amp;label=release&amp;color=4D6BFE" alt="Latest release"></a>
  <a href="https://github.com/anywhere-labs/deepseek-harness-desktop/releases"><img src="https://img.shields.io/github/downloads/anywhere-labs/deepseek-harness-desktop/total?style=flat&amp;label=downloads&amp;color=4D6BFE" alt="Total downloads"></a>
  <a href="https://github.com/anywhere-labs/deepseek-harness-desktop"><img src="https://img.shields.io/github/stars/anywhere-labs/deepseek-harness-desktop?style=flat&amp;label=%E2%98%85&amp;color=08C" alt="GitHub stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2EA44F?style=flat" alt="MIT License"></a>
  <a href="https://discord.gg/TJeGqKRNM"><img src="https://img.shields.io/badge/Discord-5865F2?style=flat&amp;logo=discord&amp;logoColor=white" alt="Join Discord"></a>
  <img src="https://img.shields.io/badge/macOS%20%7C%20Windows-4493F8?style=flat-square" alt="Supported platforms: macOS and Windows">
</p>

DSH Desktop 将 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 的本地 Web UI、Host 服务和插件系统集成到原生桌面应用中。项目固定并原样运行特定上游版本；DSH Desktop 提供窗口、托盘、终端、更新和工作配置，并通过 DeepSeek Harness 提供的插件机制与上游能力组合。

<a id="run"></a>

## 下载与安装

当前正式安装包支持 Windows x64 和 macOS Universal。无需额外环境，下载安装，一键使用。

| 平台 | 下载 | 安装方式 |
| --- | --- | --- |
| Windows x64 | [下载安装程序](https://www.dshdesktop.cn/api/downloads/windows) | 运行 NSIS 安装程序并按提示完成安装 |
| macOS Universal | [下载 DMG](https://www.dshdesktop.cn/api/downloads/mac) | 打开 DMG，将 DSH Desktop 拖入 Applications |

详细步骤、插件命令和故障排查见[用户指南](docs/user-guide.md)与[常见问题](docs/faq.md)。

我们希望和所有插件作者一起，构建一个开放、可组合、可持续的 DSH 插件生态，让每个插件都能与其他插件共同进步：[DSH 插件生态倡议书](docs/plugin-ecosystem.md)。

<details open>
<summary>❤️ 赞助商</summary>

| Logo | 简介 |
| --- | --- |
| <a href="https://dshdesktop.cn/sponsors/wuying"><img src="assets/sponsors/wuying-cloud-computer-logo.png" alt="阿里云无影云电脑" width="96"></a> | [**阿里云 · 无影云电脑**](https://dshdesktop.cn/sponsors/wuying)<br>感谢 **阿里云** 无影云电脑赞助本项目！无影云电脑个人版面向个人用户提供云上电脑服务，将计算、存储和桌面环境放在云端，支持在多类终端上接入使用，并可按需选择不同规格，适合远程办公、学习、开发和轻量创作等场景。<br><br>[**打开微信注册 →**](https://dshdesktop.cn/sponsors/wuying) |
| <a href="https://www.ucloud.cn/site/active/astraflow?ytag=geo_waituo_dsh"><img src="assets/sponsors/astraflow-logo.png" alt="UCloud 星图 AstraFlow" width="96"></a> | [**UCloud · 星图 AstraFlow**](https://www.ucloud.cn/site/active/astraflow?ytag=geo_waituo_dsh)<br>感谢 **UCloud** 星图 AstraFlow 大模型赞助了本项目！优刻得 **UCloud** 星图 AstraFlow 大模型，支持 200+ 模型一键调用：内置 Kimi K3、DeepSeek V4/V3、Qwen 3、GLM5.2、happyhorse 等全球领先开源大模型，无需自训，开箱即用。<br><br>[**访问官网 →**](https://www.ucloud.cn/site/active/astraflow?ytag=geo_waituo_dsh) |
| <a href="https://88api.ai/sign-up?aff=VnEb"><img src="assets/sponsors/88api-logo.png" alt="88API" width="120"></a> | [**88API**](https://88api.ai/sign-up?aff=VnEb)<br>88API 是一站式多模型 API 聚合平台，平台由海外企业运营，稳定高效支持开票。平台提供 DeepSeek 官转和开源渠道，价格低至 5 折，完美适配 DSH Desktop 项目。一个 API Key 即可统一接入海内外多种模型，覆盖文本对话、图片、音频、音乐和视频生成接口，适用于 AI 编程、Agent 自动化、内容创作及应用开发。<br><br>[**立即注册 →**](https://88api.ai/sign-up?aff=VnEb) |
| <a href="https://onliqiu.com/r/ds2h"><img src="assets/sponsors/liqiu-api-logo.png" alt="立秋 API" width="96"></a> | [**立秋 API**](https://onliqiu.com/r/ds2h)<br>自古逢秋悲寂寥，我言秋日胜春朝。立秋API 是一家稳定、透明、纯血的AI中转站，提供ChatGPT、Claude、Grok、GLM等AI中转服务，按量付费，支持开票，大家都炸我不炸，凌晨依然在线维护，倍率低至 0.09x 起。<br><br>[**注册使用 →**](https://onliqiu.com/r/ds2h) |

</details>

## 文档

普通用户从[用户指南](docs/user-guide.md)开始即可；开发者文档只在需要扩展或维护时才需要阅读。

### 用户文档

| 目标 | 入口 |
| --- | --- |
| 安装和日常使用 | [用户指南](docs/user-guide.md) |
| 快速确认平台、环境和使用边界 | [常见问题](docs/faq.md) |
| 了解数据处理与隐私选择 | [隐私政策](PRIVACY.zh.md) |
| 了解项目为什么存在 | [为什么做 DSH Desktop](docs/why-desktop.md) |
| 查看全部文档与 README 分工 | [文档索引](docs/README.md) |

### 开发者与维护者文档

| 目标 | 入口 |
| --- | --- |
| 阅读插件生态倡议书 | [插件生态倡议书](docs/plugin-ecosystem.md) |
| 编写普通或 Desktop 插件 | [插件开发](docs/plugin-development.md) |
| 参与统一插件 contract 讨论 | [DSH Community Fabric Draft](dsh-community-fabric/README.zh.md) |
| 了解统一插件框架为什么这样设计 | [成熟框架与真实插件调研](dsh-community-fabric/docs/research/mature-plugin-frameworks.zh.md) |
| 查看插件市场的产品与安全设计 | [DSH Community Market](dsh-community-market/README.zh.md) |
| 了解桌面插件可以使用的能力 | [桌面插件接口说明](dsh-plugin-desktop/docs/plugin-services.zh.md) |
| 了解桌面应用如何工作 | [架构说明](docs/architecture.md) |
| 查阅包级构建与发布细节 | [`dsh-plugin-desktop/README.md`](dsh-plugin-desktop/README.md) |

## 主要功能

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Desktop</h3>
      <p>把上游 DeepSeek Harness 的本地 Web UI 带到原生桌面。应用自动启动和管理本地 Harness 服务，集成系统托盘与桌面窗口，无需安装 Node.js 或执行命令。</p>
    </td>
    <td width="50%" valign="top">
      <h3>手机远程控制 <img src="https://img.shields.io/badge/%E5%8D%B3%E5%B0%86%E6%8E%A8%E5%87%BA-F59E0B?style=flat-square" alt="已内置"></h3>
      <p>通过 iOS 和 Android 远程连接 Desktop，在手机上发起任务、查看 Agent 进度，并在需要时继续跟进。已在2.0.9及以上版本中内置</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3><a href="dsh-community-market/README.zh.md">插件市场</a> <img src="https://img.shields.io/badge/%E5%B7%B2%E5%86%85%E7%BD%AE-2EA44F?style=flat-square" alt="已内置"></h3>
      <p>DSH Community Market 已完成并内置，提供插件发现、详情、安装与管理。市场以开放方式连接各种插件数据源：任何人都可以提供、接入和使用符合公开 Schema 的来源，已有 API 也可以通过受审 adapter 加入合作数据源。</p>
    </td>
    <td width="50%" valign="top">
      <h3>共建插件生态</h3>
      <p>DSH 的插件生态由社区共同建设。上游插件、DSH Desktop 插件和其他社区插件遵循统一的约定，可以通过相同的组合机制共同工作；欢迎加入共建，详见 <a href="docs/plugin-ecosystem.md">DSH 插件生态倡议书</a>。</p>
    </td>
  </tr>
</table>

### 首次设置、浏览器与局域网访问

每个尚未初始化的 profile 正常首次启动时，会先显示由 Desktop 自己提供的原生 Setup Wizard。它可以设置窗口模式与系统材质、插件市场、通知、是否用系统默认浏览器自动打开，以及 Web 访问范围；也可以直接跳过。向导完成或跳过以前，Host 和主 DSH 窗口都不会启动。完成或跳过状态按 profile 分别记录；显式恢复启动仍优先进入恢复助手。

Web 服务默认仅监听本机回环地址。开启“用浏览器打开”后，Desktop 会在 Web 服务实际就绪时交给系统默认浏览器打开；这个选项不会改变网络暴露范围。“桌面设置”会在选项下显示实际的本机 URL。局域网访问是一个独立的可选设置，开启后还会显示当前可用的局域网 URL。

> **危险：** 向局域网开放不提供鉴权；所有与你处于同一局域网的人都能直接打开 DSH 并操作你的电脑。请只在完全信任的网络中谨慎开启。

自动更新的固定版本检查请求会在 `X-DSH-Desktop-Version` header 中携带当前安装版本，在 `X-DSH-Desktop-Channel` 中携带 `stable` 或 `beta`，并在 `X-DSH-Desktop-Installation-Id` header 中携带一个由本机生成并持久保存的随机 UUID；它不是从硬件信息推导出的标识。安装包下载会携带通道和 `X-DSH-Desktop-Target-Version`，但下载请求及其重定向不会携带安装标识或当前版本。

## 插件生态

插件是给 DSH 添加能力的扩展包——模型、工具、界面、工作流都可以做成插件，像搭积木一样自由组合。

DSH Desktop 没有修改上游源码，也不是一个固定写死的外壳。固定版本的上游 DeepSeek Harness 原样运行；桌面壳本身——窗口、托盘、终端、更新、工作配置——作为 DSH 插件接入，并通过 DeepSeek Harness 提供的插件机制与上游能力组合进同一个运行时。从核心 agent 到桌面外壳，整个产品遵守同一条"一切皆插件"的规则：与所固定上游版本兼容的插件可以使用，桌面能力也按插件的方式组合、替换和演进。

我们希望插件生态像手机应用一样：每个插件按同一套规则开发，装在一起也能一起工作、互不干扰。

### 给开发者

与许多其他项目不同，这个项目本身就是一个 DSH [插件](docs/plugin-development.md)：桌面壳与第三方插件使用相同的插件组合机制。Desktop 的插件能力已经可以使用。我们提供了 Desktop 服务，让插件开发者能够把插件与桌面能力集成起来：例如查看和切换工作配置，或在当前配置中安装、更新和移除插件。完整用法见[桌面插件接口说明](dsh-plugin-desktop/docs/plugin-services.zh.md)。为什么选择这样的边界、哪些能力不会暴露给第三方插件，见[为什么做 DSH Desktop](docs/why-desktop.md)和[插件开发指南](docs/plugin-development.md)。

## 与 DeepSeek Harness 的关系

DSH Desktop 是基于 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 和 Cordis 插件思想构建的独立社区项目，旨在提供开放、可组合的 DSH 桌面体验。

本仓库由社区独立维护，目前不存在深度求索员工或 DeepSeek Harness 上游官方团队成员参与本项目开发、维护或治理的情形。GitHub Contributors 页面中可能出现的上游贡献者，来自本仓库 fork 时继承及后续同步的上游提交历史；该署名仅反映提交来源，不代表相关人员参与本仓库，也不构成任何隶属、合作、授权或背书关系。

上游项目提供核心的智能体能力、插件系统和 Web UI；DSH De