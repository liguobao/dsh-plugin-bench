# Awesome DeepSeek Harness Plugins

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

> A community-curated, vendor-neutral catalog of plugins for DeepSeek Harness (DSH) — from developer tooling and data workflows to media, operations, and everyday life.

**Language:** English | [简体中文](docs/README.zh-CN.md)

DeepSeek Harness plugins can connect an agent to tools, services, devices, and repeatable workflows. This list is intentionally broad: if it gives an agent a useful real-world capability, it belongs here.

## Contents

- [Getting started](#getting-started)
- [Plugin catalog](#plugin-catalog)
  - [Developer tools](#developer-tools)
  - [UI & user experience](#ui--user-experience)
  - [Agent orchestration & automation](#agent-orchestration--automation)
  - [Productivity & collaboration](#productivity--collaboration)
  - [Data, research & knowledge](#data-research--knowledge)
  - [Cloud, DevOps & observability](#cloud-devops--observability)
  - [AI, design & media](#ai-design--media)
  - [Business, finance & commerce](#business-finance--commerce)
  - [Life, devices & the physical world](#life-devices--the-physical-world)
- [Add a plugin](#add-a-plugin)
- [Catalog rules](#catalog-rules)

## Getting started

1. Browse a category below and open a plugin's repository or marketplace page.
2. Follow that plugin's installation instructions for DeepSeek Harness.
3. Restart or reload DeepSeek Harness if the plugin requires it.

> The catalog links to third-party projects. Review a plugin's source, permissions, and data-handling policy before installing it.

## Plugin catalog

### Developer tools

- [billion-context-dsh](https://github.com/Tyan66666/billion-context-dsh) — Model-driven context compression (ACP) for DeepSeek Harness, ported from billion-context-pi — the model decides when and what to compress.

- [Code2Skill](https://github.com/leechen298/Code2Skill) — Generate Functions, MCP tools, workflow Skills, and offline test packages from user-authorized source code.

- [deepseek-harness-acp](https://github.com/openma-ai/deepseek-harness-acp) — An ACP profile plugin and standalone server that exposes the full DSH agent to Zed and other ACP clients while sharing DSH credentials and sessions.

- [dsh-artifact](https://github.com/william-jin-cmu/dsh-artifact) — A send_artifact tool that validates model-produced files and delivers structured descriptors through the standard dsh event stream for any client to render.

- [dsh-bash-encoding](https://github.com/lhh010/dsh-bash-encoding) — Automatically detects and decodes Bash output encodings including UTF-16LE, UTF-8, and GBK for Windows and WSL.

- [dsh-custom-tool](https://github.com/FSMargoo/dsh-custom-tool) — Create and manage sandboxed JavaScript tools with a Monaco editor and a model-driven lifecycle.

- [dsh-git-identity](https://github.com/LoserFox/dsh-git-identity) — Pins Git commit authorship to the active environment identity, prioritizing the signed-in GitHub CLI account.

- [dsh-open-in-vscode](https://github.com/FSMargoo/dsh-open-in-vscode) — Open DeepSeek Harness workspace directories in VS Code from the web interface.

- [dsh-recommend](https://github.com/zp-home/dsh-recommend) — Transparent rankings and recommendations for the DSH plugin ecosystem: daily auto-fetched topic data, an open scoring model, and rank/search/recommend tools with a settings-page leaderboard.

- [dhicoc/dsh-reverse-skill](https://github.com/dhicoc/dsh-reverse-skill) — A DeepSeek Harness Cordis plugin that routes an 85-skill pack for reverse engineering and authorized security research.

- [dsh-balance-meter](https://github.com/Ghost011118/dsh-balance-meter) — Live DeepSeek account balance and session cost in the DSH Web composer dock, with auto-fetched official pricing and peak/off-peak support.
- [dsh-spend](https://github.com/nonewind/dsh-spend) — Token usage and estimated spend statistics for the DSH web UI: floating panel with per-model, per-day, and per-session views.

- [dsh-billing](https://github.com/TheTianzz/dsh-billing) — DeepSeek account balance and per-session cost as header pills, slash commands, and an agent tool, with configurable pricing and automatic 12-hour sync of the official price list.

- [plugin-registry](https://github.com/vlln/plugin-registry) — A browser-based plugin management console with official guidance for creating DSH plugins.
- [dsh-chat-import](https://github.com/Nwflower/dsh-chat-import) — Import full-fidelity conversation histories from 13 coding agents (Claude Code / Codex / ChatGPT / Cursor / Gemini / Reasonix / opencode / ZCode / Grok Build / OpenClaw / Pi / Hermes / Kimi) as resumable DeepSeek Harness sessions, with reverse export/sync back to Claude Code.

- [dsh-github-login](https://github.com/Noob-stupid/dsh-github-login) — A visual GitHub device-flow login tool that syncs its token into gh CLI config.
- [dsh-suite](https://github.com/whyihaveyou/dsh-suite) — A living DeepSeek Harness plugin directory with a compatibility CI, searchable catalog, and in-app plugin store.
- [create-dsh-plugin](https://github.com/whyihaveyou/dsh-suite/tree/main/packages/create-dsh-plugin) — A DSH plugin scaffolder with templates and a built-in smoke test.
- [plugin-manager](https://github.com/whyihaveyou/dsh-suite/tree/main/packages/plugins/plugin-manager) — An in-app DSH Web UI plugin store with browsing, search, installation, compatibility badges, and an installed list.
- [dsh-settings-plus](https://github.com/oneinitAI/dsh-settings-plus) — Advanced form- and file-level settings management with a plugin settings registration SDK.
- [dsh-opencodego-usage](https://github.com/BeiZi6/dsh-opencodego-usage) — An OpenCodeGo quota monitor for the DSH Web GUI with rolling, weekly, and monthly usage views.

### UI & user experience

- [deepseek-harness-tui](https://github.com/openma-ai/deepseek-harness-tui) — A Rust terminal client that speaks the DSH SDK JSON-RPC protocol directly and runs standalone or as a profile bundle.

- [DSH Better Sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) — A sidebar workbench with extensible tabs, file viewing and editing, terminal, Git, and sub-agent tools.

- [dsh-annotation](https://github.com/omdsh-dev/dsh-annotation) — Adds Codex-style text annotations: select text, attach a note to the next message, and receive annotation-aware replies.

- [dsh-at-file](https://github.com/FSMargoo/dsh-at-file) — Adds Codex-style @file mentions to search workspace files and attach their contents to prompts.

- [dsh-browser-panel](https://github.com/dsh-external/dsh-browser-panel) — Embeds a headed browser in the DSH Web UI so agents can operate a real browser with visible steps.

- [dsh-cc-tui](https://github.com/ccch1mneyyy/dsh-cc-tui) — A Claude Code-style full-screen terminal interface with streaming thought display, rollback controls, and context/TPS indicators.

- [dsh-genui](https://github.com/omdsh-dev/dsh-genui) — Renders interactive UI components inline in assistant replies, including charts, forms, quizzes, Mermaid diagrams, 3D scenes, and model action events.

- [dsh-grok-tui](https://github.com/chen-001/dsh-grok-tui) — Use dsh via grok-build's tui.

- [dsh-input-history](https://github.com/lhh010/dsh-input-history) — Adds terminal-style Ctrl+Up and Ctrl+Down navigation through sent messages while preserving the latest unsent draft.

- [dsh-message-edit](https://github.com/Moeblack/dsh-message-edit) — Branch-based message editing with reroll, retry, and a version timeline for DeepSeek Harness conversations.

- [dsh-minigames](https://github.com/lhh010/dsh-minigames) — Adds an extensible DSH Web UI panel with 18 offline mini-games for breaks while waiting on agent work.

- [dsh-navbar](https://github.com/vlln/dsh-navbar) — Adds a right-edge navigation strip for quickly jumping between user-message nodes in a conversat