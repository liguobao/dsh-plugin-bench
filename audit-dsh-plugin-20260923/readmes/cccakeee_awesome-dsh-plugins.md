# awesome-dsh-plugins

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
![Catalog](https://img.shields.io/badge/catalog-2792-2563eb)
![Verified](https://img.shields.io/badge/verified-1998-16a34a)
![License](https://img.shields.io/badge/license-MIT-f59e0b)

[English](README.en.md) | **简体中文** | [🌐 网站](https://deepseekharnessplugins.com)

> 一个面向 [DeepSeek Harness（DSH）][1] 的精选插件目录。项目优先收录**可由 DSH Profile 装载**、具备可复现安装说明且源码公开的社区扩展；技能、预设与相关应用会明确区分，不把“使用 DeepSeek API”或仅贴有 `dsh-plugin` 标签的项目误当作原生插件。

DeepSeek Harness 目前处于 **Developer Preview**。官方采用 Cordis 的“Everything is a plugin”架构：Profile 组合 Bundle，外部插件通常以 `package.json` 的 `dsh` 字段及 patch 文件声明挂载方式。[1] [2] 因此，本目录中的安装方法和兼容性应在你自己的 DSH 版本上先行验证。

**快照日期：2026-09-23。** 本版主目录收录 **1998 个**经源码或安装清单核验的插件与 Skill，按 22 个能力分类组织（与配套网站 [deepseekharnessplugins.com](https://deepseekharnessplugins.com) 同构）；完整清单已拆分到 [`docs/categories/`](docs/categories/) 的 22 个分类页面。同时提供 **全量聚合目录 [`CATALOG.md`](CATALOG.md)（2792 个仓库）**，合并 GitHub 搜索与多个社区目录去重后得到。**聚合 ≠ 可装载、可兼容、可安全运行**；只有本目录核验子集进入主目录，证据见 [data/verified-plugins.csv](data/verified-plugins.csv) 与 [data/audit-results.csv](data/audit-results.csv)。[3]

| 导航 | 内容 |
| --- | --- |
| [全量聚合目录](#全量聚合目录) | **2792 个** DSH 相关仓库的完整聚合（含未审核候选）；[审计日志](data/audit-results.csv) |
| [已核验插件目录](#已核验插件目录) | 按 22 个能力分类的已核验可装载扩展（与[网站](https://deepseekharnessplugins.com)同构） |
| [界面与体验](#界面与体验) · [会话与消息](#会话与消息) · [其他](#其他) · [桌面与应用](#桌面与应用) · [MCP 与协议](#mcp-与协议) · [插件工具](#插件工具) · [Web 界面与前端](#web-界面与前端) · [主题与皮肤](#主题与皮肤) · [安全与鉴权](#安全与鉴权) · [聊天与 IM](#聊天与-im) · [命令行与终端](#命令行与终端) · [语音](#语音) · [清单与资源](#清单与资源) · [用量与计费](#用量与计费) · [Agent、自动化与工作流](#agent自动化与工作流) · [集成与分享](#集成与分享) · [开发者工具](#开发者工具) · [知识与研究](#知识与研究) · [设计、媒体与视觉](#设计媒体与视觉) · [网页与浏览器](#网页与浏览器) · [生态与资源](#生态与资源) · [纯属好玩](#纯属好玩) | 22 个分类锚点 |
| [官方内置能力](#官方内置能力不是社区插件) | 随 DSH 源码发行的官方运行时构件 |
| [相关项目与观察名单](#相关项目与观察名单不计入主目录) | 相关但并非已核验原生插件的项目 |
| [安装与安全](#安装与安全) | 安装惯例、权限提示与审计建议 |
| [贡献规则](#贡献与维护) | 新项目的提交格式与审核门槛 |

## 全量聚合目录

[`CATALOG.md`](CATALOG.md) 是自动生成的**全量聚合目录**：它把 GitHub `dsh-plugin` / `deepseek-harness` 话题、名称搜索、[`dsh-plugin` 主题页候选快照](data/dsh-plugin-topic-candidates.csv)以及多个社区目录（[bruc3van/awesome-dsh-plugin](https://github.com/bruc3van/awesome-dsh-plugin)、[Alex-Yanggg/awesome-DSH-plugin](https://github.com/Alex-Yanggg/awesome-DSH-plugin)、[awesome-dsh-plugin/awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin)、[AdamPlatin123/awesome-dsh-plugins](https://github.com/AdamPlatin123/awesome-dsh-plugins)）中发现的**全部**仓库合并去重。机器可读版本是 [`data/repositories.csv`](data/repositories.csv)。

- 聚合池是**发现清单**，不是推荐或兼容性列表；只有 `✅` 已核验子集进入下方主目录。
- 用 [scripts/aggregate.py](scripts/aggregate.py) 重新拉取并重建 `CATALOG.md` 与 `data/repositories.csv`（需要 `gh` 登录）。

## 已核验插件目录



下列条目已核验至少一个原生特征：可复现的 `dsh plugin` 安装命令、`dsh.bundle` / `cordis.patch.yml` 声明，或 DSH/Cordis 可挂载的 `apply` 入口。**“已核验”不代表作者、代码质量或安全性背书。**

> 每个分类的**完整清单**已拆到 [`docs/categories/`](docs/categories/) 下的独立页面，顶部均附有对应网站分类的链接；下方仅展示每类最近活跃的若干条目。



| 导航 | 内容 |
| --- | --- |
| [全量聚合目录](#全量聚合目录) | **2792 个** DSH 相关仓库的完整聚合（含未审核候选）；[审计日志](data/audit-results.csv) |
| 分类目录（完整清单） | [界面与体验](docs/categories/ui-experience.md) · [会话与消息](docs/categories/sessions-messages.md) · [其他](docs/categories/utilities.md) · [桌面与应用](docs/categories/desktop.md) · [MCP 与协议](docs/categories/mcp.md) · [插件工具](docs/categories/plugin-tools.md) · [Web 界面与前端](docs/categories/web-ui.md) · [主题与皮肤](docs/categories/theme.md) · [安全与鉴权](docs/categories/security.md) · [聊天与 IM](docs/categories/chat-im.md) · [命令行与终端](docs/categories/cli.md) · [语音](docs/categories/voice.md) · [清单与资源](docs/categories/lists.md) · [用量与计费](docs/categories/billing.md) · [Agent、自动化与工作流](docs/categories/agents-workflows.md) · [集成与分享](docs/categories/integrations-sharing.md) · [开发者工具](docs/categories/developer-tools.md) · [知识与研究](docs/categories/knowledge-research.md) · [设计、媒体与视觉](docs/categories/media-vision.md) · [网页与浏览器](docs/categories/web-browser.md) · [生态与资源](docs/categories/ecosystem-resources.md) · [纯属好玩](docs/categories/fun.md) |
| [官方内置能力](#官方内置能力不是社区插件) | 随 DSH 源码发行的官方运行时构件 |
| [相关项目与观察名单](#相关项目与观察名单不计入主目录) | 相关但并非已核验原生插件的项目 |
| [安装与安全](#安装与安全) | 安装惯例、权限提示与审计建议 |
| [贡献与维护](#贡献与维护) | 新项目的提交格式与审核门槛 |



### 界面与体验

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [JRJRJPRO/dsh-chat-tree](https://github.com/JRJRJPRO/dsh-chat-tree) | Adds a clickable conversation tree beside the DSH chat and stores branch metadata on the DSH side. | `dsh plugin --profile web add github:JRJRJPRO/dsh-chat-tree` | MIT；Compatibility is tied to the DSH Web client surface and session model; recheck after host UI changes. |
| [yanzwzz/dsh-whale-girl-pet](https://github.com/yanzwzz/dsh-whale-girl-pet) | Adds a configurable whale-girl desktop pet, task-state feedback, token/cost dashboards, and related Web UI controls to DSH. | `dsh plugin --profile web add dsh-whale-girl-pet` | MIT；Compatibility is pinned to DSH 0.1.7-alpha.1 and the plugin handles usage, balance, weather, and profile configuration data; review network and account-data behavior before use. |
| [A8Chann/dsh-pet-live2d](https://github.com/A8Chann/dsh-pet-live2d) | Adds a draggable Live2D pet to DSH Web GUI with session-state animations, dress-up controls, and settings. | `dsh plugin --profile web add dsh-pet-live2d; # or from this repository subdirectory:; dsh plugin --profile web add "github:A8Chann/dsh-pet-live2d#path:/dsh-live2d-pet"` | MIT；The code is MIT, but bundled DS whale model assets are CC BY-NC-SA 4.0 and Cubism Core is proprietary; commercial use and redistribution require separate license review. |
| [VDERR/dsh-echocat-skill-panel](https://github.com/VDERR/dsh-echocat-skill-panel) | Audits per-turn DSH skill use and provides an in-app skill install, update, disable, and removal panel. | `dsh plugin --profile web add dsh-echocat-skill-panel` | MIT；allowInstall and allowPrivateHosts affect filesystem and network installation behavior; the documented install script also edits a DSH profile and requires a restart. |
| [Nwflower/dsh-claude-style](https://github.com/Nwflower/dsh-claude-style) | Restyles the DSH web UI with Claude-like layout, controls, model picker, branding, and local font routes. | `dsh plugin --profile web add dsh-claude-style` | MIT；Anthropic Sans/Serif font files are Anthropic property and personal-use only, outside the MIT license; the README says they are not shipped in the npm package. Only one theme should be active at a time. |
| [hkkz9522/dsh-session-manager](https://github.com/hkkz9522/dsh-session-manager) | Adds archive, delete, move, preset migration, search, tags, notes, review flags, and priority controls to DSH Web sessions. | `dsh plugin --profile web add npm:dsh-session-manager; alternatively dsh plugin --profile web add github:hkkz9522/dsh-session-manager; restart DSH Web and force refresh with Ctrl+Shift+R if needed.` | MIT；Deletion is permanent; the README documents confirmation, path and artifact checks, symlink refusal, atomic annotation writes, and recovery behavior. |
| [kirkchinese/CiteCiter](https://github.com/kirkchinese/CiteCiter) | Creates source-aware native DSH Topics for citations, follow-up questions, learning boards, attachments, and permissions. | `npm install -g @deepseek-ai/dsh@latest; dsh plugin --profile web add @kirkchinese/dsh-citeciter@0.8.2; dsh web` | MIT；Requires the README's DSH 0.1.5-rc.1/Desktop 2.0.9 baseline and Node ^22.19.0 or >=24.0.0; README marks 0.8.0 deprecated and says macOS is not yet tested. |
| [xohmai/dsh-session-delete](https://github.com/xohmai/dsh-session-delete) | Manages archived and all sessions from a DSH settings page, moving deletions to a restorable trash and supporting purge. | `dsh plugin --profile web add github:xohmai/dsh-session-delete; restart dsh web.` | Apache-2.0；Deletion and purge affect local session data; review the trash and purge behavior before enabling. |
| [FeatherHunter/dsh-prompt](https://github.com/FeatherHunter/dsh-prompt) | Adds prompt templates, a /prompt input trigger, smart re