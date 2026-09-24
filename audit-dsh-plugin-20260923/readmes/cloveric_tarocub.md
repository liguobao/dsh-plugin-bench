<p align="center">
  <strong>English</strong>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="./README.zh-CN.md"><strong>中文文档</strong></a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="https://my.feishu.cn/docx/L5qZd4rfIok8CnxuvfCcatPrnYf"><strong>📖 飞书图文版 (Feishu Doc)</strong></a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="./docs/full-reference.md"><strong>Full Reference</strong></a>
</p>

<p align="center">
  <img src="./assets/github-banner.png" alt="TaroCub: Feishu/Lark-first control for local AI agents" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/cloveric/tarocub/blob/main/LICENSE"><img src="https://img.shields.io/github/license/cloveric/tarocub?style=flat-square&color=818cf8" alt="License"></a>
  <img src="https://img.shields.io/badge/Node.js-%3E%3D20.17-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node.js >= 20.17">
  <img src="https://img.shields.io/badge/TypeScript-5.9-3178c6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/engines-Codex%20%7C%20Claude%20%7C%20Kimi%20%7C%20DeepSeek%20%7C%20Antigravity-F97316?style=flat-square" alt="Codex | Claude Code | Kimi Code | DeepSeek Harness | Antigravity">
  <img src="https://img.shields.io/badge/DeepSeek%20Harness-native%20plugin-0f766e?style=flat-square" alt="Native DeepSeek Harness plugin">
  <img src="https://img.shields.io/badge/channels-Feishu%2FLark%20%7C%20Telegram-2563eb?style=flat-square" alt="Feishu/Lark | Telegram">
  <a href="https://linux.do" alt="LINUX DO"><img src="https://img.shields.io/badge/LINUX-DO-FFB003.svg?style=flat-square" alt="LINUX DO"></a>
</p>

<h1 align="center">TaroCub</h1>

<p align="center">
  <strong>A Feishu/Lark-first gateway for Codex, Claude Code, Kimi Code, DeepSeek Harness, and Antigravity running on your own machine.</strong><br>
  TaroCub runs real CLI agents on your own machine, then gives them durable chat surfaces, files, sessions, tasks, cron, audit logs, and multi-agent workflows.<br>
  Resume local sessions anytime from your phone, whether you are at your desk, commuting, or walking the dog.
</p>

<p align="center">
  <a href="https://my.feishu.cn/docx/L5qZd4rfIok8CnxuvfCcatPrnYf"><strong>📖 Feishu Doc (飞书图文)</strong></a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#quick-start">Quick Start</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#surfaces">Surfaces</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#core-highlights">Core Highlights</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#lark-setup">Lark Setup</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#operator-commands">Commands</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#docs">Docs</a>
</p>

## What This Is

`TaroCub` is a local bridge, not a hosted agent product. It runs the real Codex, Claude Code, Kimi Code, DeepSeek Harness, and Antigravity CLIs on your own computer, then gives them a durable messaging control surface in Feishu/Lark, with Telegram retained as an optional compatibility channel.

> **Feishu/Lark is the primary platform.** The maintainer has not used Telegram as a day-to-day control surface for a long time. Telegram remains available for existing deployments, but new installations should start with Feishu/Lark.

This project was formerly named `cc-telegram-bridge`. The canonical repository is now `cloveric/tarocub`; GitHub redirects the old URL, and existing state directories plus the `cctb` shorthand remain supported for compatibility.

It is built for people who already use CLI agents heavily and want:

- Feishu/Lark-native operation with cards, Docs comments, Sheets, Drive, and group/thread workflows;
- optional phone-first Telegram operation for existing personal-bot deployments;
- durable state for sessions, cron jobs, file delivery, usage, timelines, audit logs, and multi-agent routing.

The intended setup flow is agent-assisted: clone the repo, open it in Codex, Claude Code, Kimi Code, DeepSeek Harness, or Antigravity, and ask the agent to configure the bridge for you. The CLI exists so your local agent can do the boring setup work instead of making you hand-edit every file.

The old long README is preserved as [Full Reference](./docs/full-reference.md). This landing page is intentionally short.

## Quick Start

### Recommended: ask your local agent to configure it

Open this repository in Codex, Claude Code, Kimi Code, DeepSeek Harness, or Antigravity and say:

```text
Read the README and configure TaroCub for me.
Run the Lark wizard, check permissions, install/bind lark-cli, and tell me what I need to scan or approve.
```

That is the preferred path. Manual commands are still below for operators who want to see each step. If you explicitly need the legacy-compatible Telegram channel, ask the agent to configure it with a BotFather token instead.

### Feishu / Lark (recommended)

```bash
git clone https://github.com/cloveric/tarocub.git
cd tarocub
npm install
npm run build

node dist/src/index.js lark setup --detached --install-cli --identity bot-only
node dist/src/index.js lark yolo unsafe
```

`--detached` keeps QR registration alive in tmux, prints one durable registration link, writes progress to `~/.cctb/<lark-instance>/lark-setup.log`, and starts the Lark service when setup completes. Use `--no-start-service` only when you explicitly want to prepare the app without listening yet.

If `lark doctor` reports missing app scopes, open the permission page URL it prints and grant the JSON it prints. PersonalAgent apps activate the grant immediately after confirmation; enterprise custom apps may still require a version publish. Then run:

```bash
node dist/src/index.js lark provision
node dist/src/index.js lark doctor
node dist/src/index.js lark slash sync
```

### DeepSeek Harness web search plugin (native bundle)

Install the standalone native plugin into the `web` profile used by ordinary
Harness and by TaroCub's private Harness hosts:

```bash
dsh plugin --profile web add github:cloveric/deepseek-harness-web-search-plugin
```

The plugin adds source-traceable Brave/Tavily live search and URL extraction.
TaroCub integration and `/tarocub` guidance are optional. Installing it does
**not** create a Feishu/Lark app or start the bridge. The canonical TaroCub
subdirectory source remains compatible. Check, update, or remove it with:

```bash
dsh --profile web --dump-config | grep -A18 -B2 mcp-cctb-search
dsh plugin --profile web update deepseek-harness-web-search-plugin
dsh plugin --profile web remove deepseek-harness-web-search-plugin
```

TaroCub still recognizes installations made under the former
`tarocub-deepseek-harness-plugin` package name so they can be migrated without
breaking managed bots.

### Telegram (optional compatibility channel)

Create a Telegram bot with [@BotFather](https://t.me/BotFather), then run:

```bash
npm run dev -- telegram configure <telegram-bot-token>
npm run dev -- telegram yolo unsafe
npm run dev -- telegram service start
```

`telegram yolo unsafe` maps to `approvalMode: "bypass"`: Codex uses its bypass sandbox mode, Claude Code/Antigravity use their unsafe skip-permissions modes, Kimi selects ACP `auto`, and DeepSeek selects Harness `danger-full-access`. Treat it as equivalent to bypassing normal approval prompts and local sandbox controls.

Send any message to the bot. It will reply with a pairing code:

```bash
npm run dev -- telegram access pair <pairing-code>
```

## Surfaces

| Surface | Best for | Status |
|---|---|---|
| **Feishu/Lark** | Team chat, interactive cards, Docs comments, Sheets/Docs/Drive workflows, group/thread workflows | **Recommended** — the primary, actively-developed channel |
| **Telegram** | Mobile control, voice input, file delivery, multi-bot operations, cron, Agent Bus | Fully supported; longest-tested, but no longer the day-to-day focus |
| **Local CLI** | Operations, setup, debugging, status, backups, direct sends | First-class operator interface |

## Core Highlights

| Highlight | Why it matters |
|---|---|
| **Real CLI engines, not a fake chat backend** | Codex, Claude Code, Kimi Code,