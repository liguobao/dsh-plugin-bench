<div align="center">

# 🐋 Awesome DeepSeek Harness Plugins

**A curated directory of 306+ [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (`dsh`) plugins across 14 categories — every entry with ⭐ stars and a `dsh plugin add` command. Bilingual (EN + 中文), machine-readable data, auto-sync CI.**

![plugins](https://img.shields.io/badge/plugins-306-blue) ![categories](https://img.shields.io/badge/categories-14-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen)

**English** · [中文版](README.zh.md)

[Quick Start](#quick-start) · [Hot Plugins](#hot-plugins) · [Categories](#categories) · [Browse All](#browse-all-plugins) · [Full Index](INDEX.md) · [Contributing](CONTRIBUTING.md)

</div>

---

## 🧭 What is this

[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) is DeepSeek's open-source agent harness — a ready-to-run coding agent whose core is an "**everything is a plugin**" framework: models, tools, sandboxes, session storage, the UI, and even the agent loop itself are plugins.

This repository is a **community-maintained plugin index**: it organizes DSH plugins scattered across GitHub into browsable categories. No website, no runtime — just a readable, clickable, contributable directory.

- ✅ Official install: `dsh plugin --profile <name> add <pkg>` (forwards to pnpm; npm / git / tarball)
- ✅ Official discovery: npm + the GitHub [`dsh-plugin`](https://github.com/topics/dsh-plugin) topic (**no built-in marketplace**)

## ✨ Why this directory

Several `awesome-dsh-*` lists already exist. This one is different:

- **14 hand-curated categories** with clear boundaries ([taxonomy](docs/taxonomy.md)) — not a flat name dump
- **Star counts + install commands** on every entry — judge popularity and install in one glance
- **Bilingual** (English primary + 中文) with a one-click toggle
- **Inline collapsible browsing** — expand every category right here in the README
- **Machine-readable data** ([web/data.js](web/data.js)) + generation scripts + auto-sync CI

## ⚡ Quick Start

Three ways to use this directory:

1. **Browse** — expand any category below (or jump into a category file); each entry links straight to its GitHub repo.
2. **Search** — press `t` (or `Ctrl+F`) on the repo page and search keywords like `mcp`, `memory`, `TUI`, `multi-agent`.
3. **Consume programmatically** — read [`web/data.js`](web/data.js) (generated from the category files; see [web/README.md](web/README.md)).

## 🔥 Hot Plugins

Top community plugins by GitHub stars:

<!-- hot:start -->

| # | Plugin | Description | ⭐ |
|---|---|---|---|
| 🥇 | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | Official core repo: "everything is a plugin", driven by Cordis. | 234247 |
| 🥈 | [deepseek-harness-desktop](https://github.com/anywhere-labs/deepseek-harness-desktop) | Modern DeepSeek Harness desktop experience | 28696 |
| 🥉 | [awesome-dsh-plugin/awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) | Community curated list (105 plugins + sites + badges). | 16742 |
| 4 | [dsh-desktop](https://github.com/dataelement/dsh-desktop) | Cross-platform desktop app | 8710 |
| 5 | [dsh-web-ui](https://github.com/zhu1090093659/dsh-web-ui) | DSH Web UI plugin and skin collection: task board, Git graph, right panel, mobile remote, skin center | 7962 |
| 6 | [deepseek-ai/awesome-deepseek-agent](https://github.com/deepseek-ai/awesome-deepseek-agent) | Official curated list of DeepSeek agents. | 6136 |
| 7 | [dsh-market](https://github.com/dsh-market/dsh-market) | The plugin market inside DSH: a Settings page to browse and search the full community catalog by category, with confirmed one-click installs and an installed-plugins view. | 4443 |
| 8 | [modlens](https://github.com/liustack/modlens) | Vision bridge for text-only models: paste an image, get structured JSON evidence (OCR, layout, semantics). | 4019 |
| 9 | [DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) | Full sidebar workbench with file rendering and editing, terminal, Git, and subagents; third-party plugins can register new tabs. | 3730 |
| 10 | [dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) | Claude Code-style full-screen terminal UI: pixel-whale header, live status line, and streaming thought expansion. | 3166 |

<!-- hot:end -->

## 📊 Stats

| Metric | Value |
|---|---|
| Plugins listed | **306** entries (306 unique) |
| Categories | **14** top-level |
| Ecosystem reference | `dsh-plugin` topic ~3300+ repos · compat radar 286+ |

## 🗂 Categories

<!-- catindex:start -->

| # | Category | Plugins | Description |
|---|---|---|---|
| 1 | [🛠️ Tools](plugins/tools.md) | 31 | deterministic tools, git, test runners, safe delete |
| 2 | [🧩 Skills](plugins/skills.md) | 16 | engineering discipline, skill migration, book-to-skill |
| 3 | [🔌 MCP](plugins/mcp.md) | 8 | MCP server management, webfetch, vision MCP |
| 4 | [🎨 UI / Skins / Themes](plugins/ui-themes.md) | 45 | skins, themes, generative UI, input enhancements |
| 5 | [🖥️ Desktop / TUI / Mobile](plugins/desktop-tui-mobile.md) | 23 | desktop shells, terminal TUI, mobile, companions |
| 6 | [🤖 Agent Orchestration](plugins/agent-orchestration.md) | 10 | agent teams, plan/execute, A2A, cross-session messaging |
| 7 | [🧠 Context / Memory](plugins/context-memory.md) | 24 | long-term memory, context compression/audit, session control |
| 8 | [👁️ Multimodal / Vision](plugins/multimodal.md) | 18 | image Q&A, OCR, screenshots, computer use |
| 9 | [🔁 Workflow / Automation](plugins/workflow-automation.md) | 21 | deep research, cron, condition wakeup, review loops |
| 10 | [📡 Notifications / Channels](plugins/notifications-channels.md) | 19 | Telegram/WeChat/Feishu bots, SSH, desktop notify |
| 11 | [🌐 Browser / Search](plugins/browser-search.md) | 16 | browser control, scraping, search providers |
| 12 | [🏗️ Infra / Plugin Mgmt](plugins/infrastructure-dev.md) | 33 | plugin managers, health checks, sandboxes, telemetry |
| 13 | [🎮 Fun / Other](plugins/fun-other.md) | 32 | games, pets, stickers, learning, design |
| 14 | [🏛️ Official & Meta](plugins/official-meta.md) | 10 | core repo, awesome lists, compat radar, community hub |

<!-- catindex:end -->

## 📚 Browse All Plugins

Expand any category to browse all plugins inline — no need to leave this page.

<!-- categories:start -->

<details>
<summary>🛠️ Tools · 31</summary>

| Plugin | ⭐ | Description | Install |
|---|---|---|---|
| [dsh-toolkit](https://github.com/omdsh-dev/dsh-toolkit) | 27 | Zero-dependency toolkit: time / encoding / json / calculator / csv / regex / markdown / diff / stat / schema — ten deterministic tools in one install. | `dsh plugin add @deepseek-ai/dsh-toolkit` |
| [dsh-tool-calculator](https://github.com/omdsh-dev/dsh-tool-calculator) | 8 | Safe math expression evaluator, zero-dependency recursive-descent parser. | `dsh plugin add @deepseek-ai/dsh-tool-calculator` |
| [dsh-tool-csv](https://github.com/omdsh-dev/dsh-tool-csv) | 4 | Parse/query/aggregate/convert CSV (RFC 4180) with a zero-dependency state-machine parser. | `dsh plugin add @deepseek-ai/dsh-tool-csv` |
| [dsh-tool-diff](https://github.com/omdsh-dev/dsh-tool-diff) | 4 | Structured comparison and unified diffs for text/JSON/CSV/Markdown. | `dsh plugin add @deepseek-ai/dsh-tool-diff` |
| [dsh-tool-encoding](https://github.com/omdsh-dev/dsh-tool-encoding) | 4 | base64/url/hex encoding, common hashes, and UUID generation. | `dsh plugin add @deepseek-ai/dsh-tool-encoding` |
| [dsh-tool-json](https://github.com/omdsh-dev/dsh-tool-json) | 3 | JSON queries with a JMESPath subset. | `dsh plugin add @deepseek-ai/dsh-tool-json` |
| [dsh-tool-markdown](https://github.com/omdsh-dev/dsh-tool-markdown) | 3 | HTML↔Markdown conversion, GFM table normalization, and TOC generation. | `dsh plugin add @deepseek-ai/dsh-tool-markdown` |
| [dsh-tool-regex](https://github.com/omdsh-dev/dsh-tool-regex) | 3 | Test/extract