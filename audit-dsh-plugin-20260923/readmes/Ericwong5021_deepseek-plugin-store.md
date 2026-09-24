<div align="center">

[<img src="docs/banner.png" alt="DeepSeek Plugin Store" width="100%">](https://deepseekplugin.store)

# DeepSeek Plugin Store

**发现、安装 DeepSeek Harness 生态中的社区插件、工具与扩展。**

[![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)
[![Governance Publisher](https://github.com/Ericwong5021/deepseek-plugin-store/actions/workflows/governance-publish.yml/badge.svg)](https://github.com/Ericwong5021/deepseek-plugin-store/actions/workflows/governance-publish.yml)
[![Catalog Plugins](https://img.shields.io/badge/catalog_plugins-1732-c9362b?style=flat-square)](#all-catalog-plugins)
[![License: CC0-1.0](https://img.shields.io/badge/license-CC0--1.0-292522?style=flat-square)](LICENSE)

[**浏览插件商店 →**](https://deepseekplugin.store) · [提交插件](https://github.com/Ericwong5021/deepseek-plugin-store/issues/new?template=plugin-submission.yml) · [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)

**中文** · [English](README.en.md)

</div>

---

本目录从 [`dsh-plugin`](https://github.com/topics/dsh-plugin) Topic、编辑精选和提交 Issue 中发现候选。发现不等于收录；公开项目以 Registry 为准，新准入必须具备固定提交证据并声明 `package.json:dsh.bundle`。历史迁移记录可能保持 `legacy-pending`，但不会被当作已验证插件。

> **1732 个已收录插件** · **5195 个隐藏候选** · **3448 个通过结构预检** · 上次治理数据：2026-09-01 05:37 UTC

Topic 中发现但尚未进入 Registry 的项目保持隐藏候选状态，不会获得 DSH 直接安装入口。

## 目录

- [按分类浏览](#browse-by-category)
- [插件治理](#plugin-governance)
- [数据榜单](#rankings)
- [安装插件](#installing-plugins)
- [全部目录项目](#all-catalog-plugins)
- [收录你的插件](#get-listed)

<a id="browse-by-category"></a>
## 按分类浏览

| | 分类 | 项目数 |
|:--:|:--|--:|
| ✨ | [编辑精选](#editor-picks) | 8 |
| 🎨 | [UI 增强](#ui-enhancements) | 359 |
| 🔁 | [工作流与自动化](#workflow-automation) | 451 |
| 🛠️ | [工具集](#tools) | 608 |
| 🔔 | [通知与监控](#notifications) | 81 |
| 🧑‍💻 | [开发辅助](#dev-helpers) | 178 |
| 🎓 | [学习与教育](#learning) | 40 |
| 🧩 | [其他](#misc) | 7 |

<a id="plugin-governance"></a>
## 插件治理

- **真值源**：`registry/plugins/<id>.json` 管理公开插件；`governance/state/**` 记录候选、仓库观测和分类状态；`data/*.json` 和 README 是可重建发布物。
- **准入证据**：检查公开且未归档的仓库、可解析的根 `package.json`、有效 `dsh.bundle`、Manifest 引用文件、README 指引和默认分支检查，并保存固定 commit SHA。准入流程不执行外部仓库代码。
- **验证边界**：`verified` 表示结构和证据通过，不是安全审计或运行时兼容性保证；`legacy-pending` 只是显式的历史迁移状态。
- **分类顺序**：人工复核 > 已接受的维护者分类 > LLM 分类 > Manifest/文本/关键词证据 > 历史迁移。人工结论不会被自动分类覆盖。
- **定时分类**：LLM 分类 Action 每天 00:43 UTC（北京时间 08:43）处理一批插件，批次大小由 `LLM_CLASSIFIER_LIMIT` 配置；定时运行不会自动续跑下一批。
- **全量回溯**：治理发现 Action 每周日从第一个历史分区开始，自动串行扫描四个 Topic 时间分区；每个分区独立通过治理 PR 后再进入下一个分区。
- **PR 门禁**：Schema、身份唯一性、路径范围、不可变证据、治理策略和 Catalog 确定性必须全部通过。
- **发布**：定时发现产生治理状态 PR；通过门禁后合并，Publisher 同步生成 Catalog、榜单和中英文 README。

<a id="rankings"></a>
## 数据榜单

### 热门

| # | 插件 | 分类 | Stars |
|--:|:--|:--|--:|
| 1 | [toolclub/dsh-agent-team-gui](https://github.com/toolclub/dsh-agent-team-gui) | 智能体编排 | ★43 |
| 2 | [leechen298/Code2Skill](https://github.com/leechen298/Code2Skill) | 插件开发 | ★4 |
| 3 | [omdsh-dev/dsh-auto-chess](https://github.com/omdsh-dev/dsh-auto-chess) | 插件开发 | ★3 |
| 4 | [bitterSmilezzz/dsh-mac-desktop](https://github.com/bitterSmilezzz/dsh-mac-desktop) | 桌面与移动端 | ★2 |
| 5 | [JasonJin2006/dsh-sound-effects-plugin](https://github.com/JasonJin2006/dsh-sound-effects-plugin) | 插件开发 | ★2 |

### 上升趋势

<sub>当前证据不足，暂不发布该榜单。</sub>

### 新收录

| # | 插件 | 分类 | 指标 |
|--:|:--|:--|--:|
| 1 | [toolclub/dsh-agent-team-gui](https://github.com/toolclub/dsh-agent-team-gui) | 智能体编排 | 2026-08-18 |
| 2 | [sjh9714/dsh-what-changed](https://github.com/sjh9714/dsh-what-changed) | 导航与面板 | 2026-08-18 |
| 3 | [ymh0000123/dsh-theme-endfield](https://github.com/ymh0000123/dsh-theme-endfield) | 主题与布局 | 2026-08-18 |
| 4 | [JohnXu22786/worktree-mgr](https://github.com/JohnXu22786/worktree-mgr) | 文件与终端 | 2026-08-18 |
| 5 | [LL-cmyk-so/dsh-balance-widget](https://github.com/LL-cmyk-so/dsh-balance-widget) | 通知与监控 | 2026-08-18 |

### 最近活跃

| # | 插件 | 分类 | 指标 |
|--:|:--|:--|--:|
| 1 | [ymh0000123/dsh-theme-endfield](https://github.com/ymh0000123/dsh-theme-endfield) | 主题与布局 | 2026-08-18 |
| 2 | [sjh9714/dsh-what-changed](https://github.com/sjh9714/dsh-what-changed) | 导航与面板 | 2026-08-18 |
| 3 | [LL-cmyk-so/dsh-balance-widget](https://github.com/LL-cmyk-so/dsh-balance-widget) | 通知与监控 | 2026-08-18 |
| 4 | [toolclub/dsh-agent-team-gui](https://github.com/toolclub/dsh-agent-team-gui) | 智能体编排 | 2026-08-18 |
| 5 | [yangzhe1003/dsh-web-search-firecrawl](https://github.com/yangzhe1003/dsh-web-search-firecrawl) | 搜索与浏览 | 2026-08-17 |

<sub>榜单只从已验证、Manifest 观测通过、分类无待复核且处于 active/incubating 状态的插件中生成。热度和涨幅不代表本项目背书。</sub>

<a id="installing-plugins"></a>
## 安装插件

```sh
# npm 包，预构建，推荐使用
dsh plugin --profile <name> add <npm-package>

# GitHub 源码，首次安装时按提示允许构建，然后重试
dsh plugin --profile <name> add github:<owner>/<repo>
```

> ⚠️ 从 GitHub 源码安装的插件会在你的设备上执行构建脚本。请只安装你信任的来源，并尽可能固定到具体提交： `github:owner/repo#<sha>`.

<a id="all-catalog-plugins"></a>
## 全部目录项目

<a id="editor-picks"></a>
<details>
<summary><strong>✨ 编辑精选</strong> <sup>8 个插件</sup></summary>

### 编辑精选

- [zhu1090093659/dsh-web-ui](https://github.com/zhu1090093659/dsh-web-ui) ★5278 · `dsh-web-ui` — dsh-web is a DeepSeek Harness Web GUI plugin bundle that provides pluggable interface extensions including a task board, remote control, SSH panel, Git visualization, image understanding, and themes.
- [omdsh-dev/DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) ★3111 · `dsh-better-sidebar` — An extensible DSH sidebar and bottom-panel workbench with file viewing and editing, terminal, Git, browser, chat, and background task pages.
- [ccch1mneyyy/dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) ★2701 · `@deepseek-harness-tui/dsh-tui` — An interactive terminal interface for DeepSeek Harness with themes, live status visualization, context metrics, and session navigation.
- [Small-tailqwq/dsh-deep-whale](https://github.com/Small-tailqwq/dsh-deep-whale) ★1829 — Provides whale-themed skins for the DeepSeek Harness web GUI along with a manager for discovering, switching, and customizing skins.
- [Nagi-ovo/dsh-ads](https://github.com/Nagi-ovo/dsh-ads) ★588 · `@dsh-external/dsh-ads` — An entertainment theme that transforms the DSH web interface with fictional advertisements, popups, and plugin recommendation placements in a 2005 portal style.
- [omdsh-dev/dsh-gomoku](https://github.com/omdsh-dev/dsh-gomoku) ★16 · `@yejiming/dsh-gomoku` — Adds an interactive 15×15 Gomoku board to DSH for human-versus-AI or AI-versus-AI matches, with editable player prompts and displayed reasoning.
- [Small-tailqwq/dsh-deepcel](https://github.com/Small-tailqwq/dsh-deepcel) ★15 — A DeepSeek Harness Web GUI skin that reorganizes sessions, tools, settings, and navigation into an interactive spreadsheet-like workspace.
- [SailingLoong/loongport-dsh](https://github.com/SailingLoong/loongport-dsh) ★2 · `loongport` — LoongPort configures verified or manually supplied OpenAI-compatible service endpoints and credentials for DeepSeek Harness.

</details>

<a id="ui-enhancements"></a>
<details>
<summary><strong>🎨 UI 增强</strong> <sup>359 个插件</sup></summary>

### UI 增强

- [nexu-io/open-design](https://github.com/nexu-io/open-design) ★88235 · `open-design` — OpenDesign is a local-first desktop design workspace that uses coding agents to create and refine prototypes, dashboards, presentations, documents, images, and videos with previews and file exports.
- [tt-a1i/archify](https://github.com/tt-a1i/archify) ★13814 — Archify turns repositories or system descriptions into validated interactive architecture, workflow, sequence, data-flow, and lifecycle diagrams with multi-format exports.
- [anywhere-labs/deepseek-harness-desktop](https://github.com/anywhere-labs/deepseek-harness-desktop) ★11525 · `@deepseek-ai/dsh-root` — A Windows and macOS desktop client for DeepSeek Harness with local service management, windows, system tray integration, terminal access, and plugin marketplace features.
- [crafter-station/petdex](https://github.com/crafter-station/petdex) ★3876 · `petdex` — Petdex provides installable animated desktop pets that display and react to