<div>
  <p align="center">
    <img width="100%" alt="Agent = Model + Harness — 一只连接 DSH 生态的发光鲸鱼" src="assets/media/awesome-deepseek-harness-banner.png">
  </p>
</div>

<p align="center">
  简体中文 · <a href="README_EN.md">English</a> · <a href="README_JA.md">日本語</a>
</p>

<p align="center">
  DeepSeek Harness 终极指南：资料、教程、插件与工具<br>
</p>

<p align="center">
  <a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a>
  <a href="https://github.com/topics/dsh-plugin"><img src="https://img.shields.io/badge/GitHub-dsh--plugin-0969da?style=flat-square" alt="GitHub topic: dsh-plugin"></a>
  <a href="https://github.com/libukai/awesome-deepseek-harness/stargazers"><img src="https://img.shields.io/github/stars/libukai/awesome-deepseek-harness?style=flat-square" alt="GitHub Stars"></a>
  <a href="https://github.com/libukai/awesome-deepseek-harness/issues"><img src="https://img.shields.io/badge/Issues-welcome-brightgreen.svg?style=flat-square" alt="Issues welcome"></a>
</p>

本项目秉持少而精的原则，精选并收录 DeepSeek Harness 相关优质资源，与更多 AI 从业者共同构建更繁荣的 Agent 生态。

> 如果这个项目对你有帮助，欢迎点一个 ⭐；也欢迎关注 𝕏 [@李不凯正在研究](https://x.com/libukai)，获取更多 Agent 实践内容。

## 目录

- [目录](#目录)
- [快速开始](#快速开始)
  - [启动 Web UI](#启动-web-ui)
  - [从源码运行](#从源码运行)
  - [使用 Python SDK](#使用-python-sdk)
  - [安装插件](#安装插件)
- [官方资源](#官方资源)
  - [安装集成](#安装集成)
  - [源码仓库](#源码仓库)
  - [官方文档](#官方文档)
  - [讨论社区](#讨论社区)
- [社区资源](#社区资源)
  - [分析教程](#分析教程)
  - [社区讨论](#社区讨论)
- [第三方客户端](#第三方客户端)
  - [桌面与发行版](#桌面与发行版)
  - [终端、移动与 Web 体验](#终端移动与-web-体验)
- [精选插件](#精选插件)
  - [工作流与 Agent](#工作流与-agent)
  - [上下文、会话与输入](#上下文会话与输入)
  - [浏览器、视觉与界面](#浏览器视觉与界面)
  - [沙箱与执行](#沙箱与执行)
  - [主题与皮肤](#主题与皮肤)
- [外部集成](#外部集成)
- [开发工具](#开发工具)
- [致谢](#致谢)

## 快速开始

[DeepSeek Harness](https://deepseek.com/harness/)（简称 DSH 或 `dsh`）是 DeepSeek AI 开源的 Agent Harness 项目。它基于 [Cordis](https://github.com/cordiverse/cordis)，采用 **Everything is a Plugin（一切皆插件）** 的架构：模型适配器、工具、会话日志、界面和 Agent Loop 都可以通过插件树组合与替换。

当前核验到的官方 GitHub 开发者预览版为 [`0.1.2-rc.1`](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.2-rc.1)；npm `latest` 与 `next` 均已指向 `0.1.2-rc.1`。该 RC 增加完整历史回合导航、精确 Token / 耗时统计、子代理模型选择、ACP 标准控件、定时任务和断线重连，并以可双向继续的 `send_message` 取代单向 `report`。公开 WebFetch 默认启用但有 SSRF 防护；SQLite Session Backend 已移除（旧数据保留，导出需旧版本）；DeepSeek 适配器默认附带已启用插件包名与版本（可关闭），Session 日志增量上传仍为可选且默认关闭。官方同时明示未经安全审计，Sandbox、Approval 与 Permission 不构成完全隔离保证。下方各项目标注的 DSH 版本仅代表作者声明的开发或测试基线，不应自动视为已兼容最新预览版。

### 启动 Web UI

安装 [Node.js](https://nodejs.org/) 22.19.x 或 24+（推荐 24+）后执行：

```bash
npx @deepseek-ai/dsh web
```

默认访问 `http://127.0.0.1:3080`。进入 **Settings → Models** 配置模型服务后即可创建会话。详细步骤见[官方快速开始](https://deepseek-harness.github.io/deepseek-harness/guide/quickstart)和[模型服务配置](https://deepseek-harness.github.io/deepseek-harness/guide/providers)。

### 从源码运行

```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

### 使用 Python SDK

官方 Python SDK 支持通过内置运行时以编程方式调用 Harness，无需在系统中安装 Node.js。当前要求 Python 3.10+，支持情况和平台限制以[官方 Python SDK 指南](https://deepseek-harness.github.io/deepseek-harness/guide/python-sdk)为准。

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install deepseek-harness-sdk
```

### 安装插件

`web` 和 `headless` 是发行版内置的 Profile。外部插件以声明 `dsh.bundle` 的 Bundle 加入指定 Profile：

```bash
dsh plugin --profile web add <package-or-git-spec>
dsh --profile web --dump-config
```

从 Git 仓库安装时，建议固定 commit，并先检查安装脚本。pnpm 可能要求显式授权依赖的构建脚本；这些构建脚本会在 Agent 沙箱之外执行。完整机制见[官方插件打包与安装教程](https://deepseek-harness.github.io/deepseek-harness/develop/basic/publish)。

## 官方资源

官方提供开源仓库、配套论文和较完整的参考文档，并持续运营开发者社区。

### 安装集成

- [@deepseek-ai/dsh](https://www.npmjs.com/package/@deepseek-ai/dsh)：官方 CLI 与 Web UI 的 npm 启动包
- [deepseek-harness-sdk](https://pypi.org/project/deepseek-harness-sdk/)：用于程序化集成 DSH 的官方 Python SDK

### 源码仓库

- [GitHub](https://github.com/deepseek-ai/deepseek-harness)：查看源码、Issue、版本与贡献者
- [Paper](https://github.com/cordiverse/paper)：基于 Cordis 的产品架构详解论文

### 官方文档

- [中文官网](https://deepseek.com/harness/)：了解产品定位和核心理念
- [帮助文档](https://deepseek-harness.github.io/deepseek-harness/guide/quickstart)：使用、插件开发与架构参考入口

### 讨论社区

- [GitHub Discussions](https://github.com/deepseek-ai/deepseek-harness/discussions)：问题反馈、使用交流和提案讨论
- [Discord DeepSeek](https://discord.gg/Ycq5dCaS4)：官方 Discord 社区，以中文讨论为主
- ["DeepSeek Harness"](https://x.com/search?q=%22DeepSeek%20Harness%22%20OR%20dsh-plugin&src=typed_query&f=live)：X 上有关 DSH 的实时搜索结果
- [# dsh-plugin](https://github.com/topics/dsh-plugin)：GitHub 上的 DSH 插件项目集合

## 社区资源

### 分析教程

| 教程                                                                                         | 形式            | 内容                                                                             |
| -------------------------------------------------------------------------------------------- | --------------- | -------------------------------------------------------------------------------- |
| [DeepSeek Harness 从零到一](https://yanhua1010.github.io/dsh-harness-tutorial/)              | 中文教程与 Demo | 包含原理、源码拆解、8 个 Demo 和 `mini-harness` 教学项目                         |
| [DeepSeek Harness：从开机到拆开](https://github.com/alchaincyf/deepseek-harness-orange-book) | 中文实测电子书  | 提供 PDF、EPUB 和 HTML，收录完整系统提示词、129 行默认启动清单与三份原始会话日志 |
| [解剖 DeepSeek Harness](https://xueai.app/slides/learn.html#dsh-1.html)                      | 交互式源码专题  | 拆解会话、上下文、工具、沙箱、Code Mode 和 Subagent 等核心机制                   |
| [Cordis 在做什么：从 DeepSeek Harness 看](https://blog.antinomie.org)                        | 中文架构短文    | 从插件作者视角解释 Cordis 心智模型，讨论复杂度如何转移到系统内部                 |
| [DeepSeek Harness 白皮书](https://github.com/Electricitysheep/dsh-handbook)                  | 中英双语手册    | 14 章覆盖安装、插件开发、安全与成本，提供在线阅读、PDF 和可运行示例；内容采用 CC BY-NC-SA 4.0，基于 `0.1.0-rc.6` |
| [NanoCordis](https://github.com/SheltonLiu-N/nano-cordis)                                    | 可运行的教学实现 | 用约 1,600 行 TypeScript 重建 Cordis 插件框架与 DSH 形态的 Agent Runtime；MIT、npm `0.1.0`、95 项测试，默认 Fake Model 无需 Key，Bash 工具仍需人工批准，真实模型凭据只从环境变量读取 |

### 社区讨论

收录包含完整论述、实践细节或一手背景的公开社交媒体长帖，补充官方资料未覆盖的背景与实践细节。

| 长帖                                                                                                           | 作者与背景                                                                | 内容摘要                                                                                                                                                  |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [从早期参与者视角理解 DSH](https://x.com/jiayuan_jy/status/2087911060154314963)                                | [Jiayuan (JY) Zhang](https://x.com/jiayuan_jy)；作者自述提前一个月获得仓库访问权限 | 将 DSH 同时理解为可运行的 Coding Agent 和 Agent 开发框架；用“乐高汽车”解释一切皆插件，并讨论 Runtime 自扩展、自进化软件雏形、当前成熟度和函数式编程特征。 |
| [从 Agent Runtime / Agent OS 视角理解 DSH](https://x.com/anion_ex/status/2087910193783025853)                  | [Anionex](https://x.com/anion_ex)；内测参与者与插件作者                           | 从模型、工具、策略、存储、上下文、界面和 Loop 的可组合性解释 DSH，并讨论 Agent 对运行时的有限观察与自扩展。                                               |
| [玩了一夜 DeepSeek Harness，我发现它在用《我的世界》的方式干掉 Claude Code](https://www.pingwest.com/a/316436) | 品玩；发布首夜的媒体观察                                                        | 用《我的世界》的原版、Mod、CurseForge 与整合包类比 DSH 本体、插件、目录和发行版，并记录首夜的兼容性与安全争议。                                           |
| [从源码对照 DSH 与 Codex：声明式插件 vs 可替换 Agent Loop](https://x.com/grapeot/status/2088019011561005382)   | [鸭哥](https://x.com/grapeot)；读完源码后与 Codex 逐行对照。展开文见 [yage.ai](https://yage.ai/share/dsh-deep-analysis-20260813.html) | 将 Codex 的声明式插件与 DSH 的命令式进程内插件对照，认为日常写代码并不需要 Cordis 的复杂度；唯一结构性优势是 Agent Loop 本身可热替换，从而为自进化 Harness 提供物理插槽。 |

## 第三方客户端

以下项目提供了独立的用户界面、发行形态或产品化组装，而不只是单个工具能力。

> **分类说明：** 发行版或 Fork 会直接复用、修改或重新打包完整的