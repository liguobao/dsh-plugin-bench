<div align="center">

# 💬 pi-web-ui

**English** | [简体中文](https://github.com/xing-shuyin/pi-web-ui/blob/main/README.zh-CN.md)

_Just open your browser — get all your work done._

<p>
  <a href="https://www.npmjs.com/package/pi-web-ui"><img src="https://img.shields.io/npm/v/pi-web-ui?color=cb3837&logo=npm&label=pi-web-ui" alt="npm version"></a>
  <a href="https://nodejs.org/"><img src="https://img.shields.io/node/v/pi-web-ui?logo=node.js&logoColor=white" alt="Node.js"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/xing-shuyin/pi-web-ui" alt="License"></a>
  <a href="https://www.npmjs.com/package/pi-web-ui"><img src="https://img.shields.io/npm/dm/pi-web-ui?label=downloads" alt="npm downloads"></a>
  <a href="https://github.com/xing-shuyin/pi-web-ui/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/xing-shuyin/pi-web-ui/ci.yml?branch=main&label=CI" alt="CI status"></a>
  <a href="https://github.com/xing-shuyin/pi-web-ui/stargazers"><img src="https://img.shields.io/github/stars/xing-shuyin/pi-web-ui?style=social" alt="GitHub stars"></a>
  <a href="https://github.com/xing-shuyin/pi-web-ui/fork"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat" alt="PRs welcome"></a>
</p>

Chat, code, review, manage files, use the terminal — all in one browser tab. No IDE, no terminal app, no context-switching.

![Chat with prompt templates](https://raw.githubusercontent.com/xing-shuyin/pi-web-ui/main/assets/chat-prompts.jpeg)

</div>

A browser cockpit for AI coding agents (pi / DSH) built around one idea:
**you only need a browser to get everything done.** The agent runs
server-side and streams events to the browser over WebSocket:
thinking blocks, tool calls, file trees, a built-in terminal, model management,
theme switching, and a full settings panel — tuned for daily development.

> **Requirements** — Node.js ≥ 22.19 and a configured pi install.

## More from the author

> **Building with DSH?**
>
> [**dsh-ui-tools**](https://github.com/xing-shuyin/dsh-ui-tools) is the author's companion project for building and extending UI tools in the DSH ecosystem.

QQ群 1126050727

## ✨ Highlights

| 💬 **Chat that works like you do**                                                                                | 🖼️ **Files & images**                                                                               | 🧩 **Extensible by design**                                                                                   | 🔒 **Private by default**                                                        |
| ----------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Streaming replies, steer & follow-up queueing, slash commands, multiple conversations per project, edit-&-re-ask. | Attach files, paste images, ask about pictures (vision bridge), preview anything with GBK fallback. | Drop-in UI **plugins** (extra top-bar tabs + agent tools) and standalone **themes** — no rebuild, no restart. | Loopback-only, credential-safe: provider keys & headers never reach the browser. |

## 📚 Table of Contents

- 🚀 [Features](#features)
- ⌨️ [Keyboard shortcuts](#keyboard-shortcuts)
- 🖼️ [Screenshots](#screenshots)
- 📦 [Install](#install)
- ⚡ [Quick start](#quick-start)
- 🖥️ [System service](#system-service)
- 🐳 [Docker](#docker)
- 🧩 [Plugins](#plugins)
- 🎨 [Themes](#themes)
- 🔧 [Tuning & advanced environment variables](#tuning--advanced-environment-variables)
- 🔒 [Security](#security)
- 🪪 [Code signing policy](#-code-signing-policy)
- 🔐 [Privacy](#-privacy)
- 🌐 [Reverse proxy (nginx)](#reverse-proxy-nginx)
- 🤝 [Contribute](#contribute)
- 📄 [License](#license)

## Features

### 💬 Chat

- **Streaming agent chat over WebSocket** — the pi SDK runs in-process; events are pushed as snapshots (60 ms throttled) and the browser renders them.
- Thinking blocks, tool-call cards and bash outputs with live status (running → finished · waiting for the model · duration).
- **Steer (follow-up queueing)** — send a follow-up while the agent is replying; it is queued and injected as soon as the current turn's tool calls settle (the "Interrupt" equivalent of the pi CLI).
- **Slash commands** — `/` opens a command picker (built-in / extension / template / skill); the built-ins are `/new /name /model /compact /cwd /thinking /resume /reload`, plus `/help` (command list), `/copy` (copy last reply) and `/pi-web-ui:quit` (stop the server). `/new` takes an optional first prompt (`/new fix the failing test`) and sends it as the new chat's first message.
- **Multiple conversations per project** — each conversation gets its own agent runtime and keeps running in the background after you switch away; the "Running conversations" list shows stream progress and lets you switch back.
- **Edit & re-ask** — fork any past question into a new branch and re-prompt; the original conversation stays untouched.
- Long threads auto-collapse messages older than 30 into lazy summary rows (click to expand).
- Question navigation — a floating rail plus per-question tags to jump between questions.
- **Prompt templates** — the empty chat state shows a one-click template gallery (repo init, code review, research, merge conflicts…); click a card to fill the input, or save the current draft as your own template.
- **Auto-retry on model errors** — configurable retry count per conversation (default 6, `0` = fail immediately); when retries run out the failed turn is marked red with a one-click Retry button.
- **Queue control** — a queued steer/follow-up bubble can be dropped (✕) or **recalled (↩)**, which pulls its text back into the composer (appended on a new line if you already typed something — it never overwrites your draft).
- **Message anatomy** — each message header shows the role, the model that produced it and a local `HH:MM` timestamp, and every text block has a copy button. Attachments render as their own collapsible card with a mode chip (`lines` / `ref` / `bridged` / `inline n lines`), a copy button and a vision-bridge “transcribed” note; a skill invocation becomes a skill card with the full `SKILL.md`, next to the arguments you typed.
- **Compaction, visible** — compacted context shows up as a card (“compacted from N tokens”) that auto-expands and jumps when it arrives, and a live banner counts up (“compacting context · 12s”) naming the trigger (manual / threshold / overflow).

### 🗂️ Projects & sessions

- **Switching projects** — the workspace root (what the agent reads/writes and where the terminal starts) changes without a restart:
  - **Bottom-right path in the status bar** — click `📁 <path>` to open the folder picker: type a path (`Tab` completes), `↑` goes up one level, `💻` jumps to the computer root so you can change drives, click a folder to enter it and hit **Select** — or **Select this folder** to take the folder you are browsing. **＋ New folder** creates a directory on the spot; `Esc` or a click outside closes it.
  - **Right panel file tree** — right-click any folder → **Open as project** (the same menu has **Upload files to this folder**).
  - **Left panel → Recent projects**, or `/cwd <path>` from the input box (`/cwd` alone reports the current directory).
  - The startup default comes from `--cwd <dir>` / `PI_WEB_CWD`.
- **Conversations run in parallel** — each conversation has its own agent runtime and keeps streaming after you switch away; up to 8 can be open per project (subagents don't count).
- **Running list** — grouped by project (the current one first), with subagent children indented under their parent, badges for subagent / error (the tooltip carries the reason) / streaming,