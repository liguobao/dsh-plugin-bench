<div align="center">

<img src="website/assets/readme-cover.en.jpg" alt="Abu — Your AI Desktop Office Assistant" width="100%" />

**English** | [中文](README.zh-CN.md)

# Abu

**Your AI Desktop Office Assistant — Just Leave It to Abu**

A locally-run AI desktop assistant inspired by Claude Code's Cowork mode.
Tell Abu what you need — it reads files, runs commands, writes docs, and builds reports, all on your machine.

[![Release](https://img.shields.io/github/v/release/PM-Shawn/Abu-Cowork?style=flat-square)](https://github.com/PM-Shawn/Abu-Cowork/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue?style=flat-square)](LICENSE)

[Download](#download) · [Quick Start](#quick-start) · [Features](#features) · [User Guide](docs/User-Guide.md) · [Build from Source](#build-from-source)

</div>

---

## Why Abu?

| Feature | Abu | Regular AI Chat | Traditional Automation |
|---------|-----|----------------|----------------------|
| Autonomous planning & task execution | :white_check_mark: | :x: | :x: |
| Read/write local files, run commands | :white_check_mark: | :x: | :white_check_mark: |
| Natural language interaction | :white_check_mark: | :white_check_mark: | :x: |
| 29 built-in skills + self-evolving (Abu grows its own) | :white_check_mark: | :x: | :x: |
| Multi-conversation Project aggregation | :white_check_mark: | :x: | :x: |
| Scheduled tasks & event triggers | :white_check_mark: | :x: | :white_check_mark: |
| IM bot (Lark/DingTalk/WeCom/Slack) | :white_check_mark: | :x: | Partial |
| Multi-agent parallel execution | :white_check_mark: | :x: | :x: |
| Browser & computer control | :white_check_mark: | :x: | Partial |
| 100% local data, privacy-safe | :white_check_mark: | :x: | :white_check_mark: |

---

## What's New

**[Download the latest stable release](https://github.com/PM-Shawn/Abu-Cowork/releases/latest)** · [Read the full changelog](CHANGELOG.md)

Recent highlights: **Workspace file tree + code canvas** (browse / preview / edit files in the side panel, CodeMirror source editing with auto-save, preview auto-refresh, version snapshots with rollback), **declarative progress panel** (the model declares its own plan steps and status via `report_plan`), **inline visualization widgets** (charts / HTML / Mermaid rendered inline in chat), **multi-endpoint provider presets** (Volcengine / Bailian / Zhipu access plans as curated presets + a unified add/edit modal), **per-model capabilities** (vision / tools / reasoning / token limits declared per model), plus **doc comment-to-chat**, **full internationalization**, and **signed + notarized macOS builds**.

> Full changelog per release: see [Releases](https://github.com/PM-Shawn/Abu-Cowork/releases).

## Preview

> Clean interface, powerful capabilities

<table>
<tr>
<td align="center" width="50%"><b>Welcome</b><br/>Natural language input — conversation is the command<br/><br/><img src="website/assets/screenshot-welcome.en.png" width="100%" /></td>
<td align="center" width="50%"><b>Task Execution</b><br/>Autonomous planning & tool invocation for complex tasks<br/><br/><img src="website/assets/screenshot-execution.en.png" width="100%" /></td>
</tr>
<tr>
<td align="center"><b>Web Pages · Live Preview</b><br/>Generate a site and preview it live, side by side<br/><br/><img src="website/assets/screenshot-web-pages.en.png" width="100%" /></td>
<td align="center"><b>Content Creation · Live Preview</b><br/>Draft documents with a real-time Markdown preview<br/><br/><img src="website/assets/screenshot-doc-edit.en.png" width="100%" /></td>
</tr>
<tr>
<td align="center"><b>Plan Mode</b><br/>High-risk tasks show a plan first — runs only after you confirm<br/><br/><img src="website/assets/screenshot-plan-mode.en.png" width="100%" /></td>
<td align="center"><b>Interactive Questions</b><br/>Abu pops an option card when it needs you to decide (single / multi-select)<br/><br/><img src="website/assets/screenshot-ask-question.en.png" width="100%" /></td>
</tr>
<tr>
<td align="center"><b>Multi-Agent Parallel</b><br/>Up to 5 background agents working at once, progress in real time<br/><br/><img src="website/assets/screenshot-multi-agent.en.png" width="100%" /></td>
<td align="center"><b>Desktop Pet · Activity Tray</b><br/>A floating pet on your desktop, its tray showing Abu's live status<br/><br/><img src="website/assets/screenshot-pet.en.png" width="100%" /></td>
</tr>
<tr>
<td align="center"><b>Theme · Dark</b><br/>A polished, low-glare dark theme<br/><br/><img src="website/assets/screenshot-theme.en.png" width="100%" /></td>
<td align="center"><b>Theme · Light</b><br/>Switch between light / dark / follow-system<br/><br/><img src="website/assets/screenshot-theme-light.en.png" width="100%" /></td>
</tr>
<tr>
<td align="center" colspan="2"><b>Labs</b><br/>In-progress features, off by default, opt-in (currently hosting: Desktop Pet)<br/><br/><img src="website/assets/screenshot-labs.en.png" width="60%" /></td>
</tr>
<tr>
<td align="center"><b>Permission Control</b><br/>File access requires user authorization<br/><br/><img src="website/assets/screenshot-permission.en.png" width="100%" /></td>
<td align="center"><b>IM Channel Chat</b><br/>@Abu in Lark/DingTalk to interact<br/><br/><img src="website/assets/screenshot-im-chat.en.png" width="100%" /></td>
</tr>
<tr>
<td align="center"><b>Skills</b><br/>29 built-in skills + self-evolving + custom<br/><br/><img src="website/assets/screenshot-skills.en.png" width="100%" /></td>
<td align="center"><b>MCP Connectors</b><br/>One-click integration with Playwright, GitHub & more<br/><br/><img src="website/assets/screenshot-mcp.en.png" width="100%" /></td>
</tr>
<tr>
<td align="center"><b>Scheduled Tasks</b><br/>Cron-based scheduling for automated workflows<br/><br/><img src="website/assets/screenshot-schedule-create.en.png" width="100%" /></td>
<td align="center"><b>Triggers / Watch</b><br/>HTTP, file changes, IM messages auto-trigger tasks<br/><br/><img src="website/assets/screenshot-triggers.en.png" width="100%" /></td>
</tr>
<tr>
<td align="center"><b>AI Service Management</b><br/>Multi-provider management with health checks<br/><br/><img src="website/assets/screenshot-settings-ai.en.png" width="100%" /></td>
<td align="center"><b>IM Channel Config</b><br/>Connect Lark, DingTalk, WeCom & more<br/><br/><img src="website/assets/screenshot-settings-im.en.png" width="100%" /></td>
</tr>
<tr>
<td align="center"><b>Personal Memory</b><br/>Remembers your preferences and work habits<br/><br/><img src="website/assets/screenshot-memory.en.png" width="100%" /></td>
<td align="center"><b>Security Sandbox</b><br/>Seatbelt sandbox + network isolation for privacy<br/><br/><img src="website/assets/screenshot-security.en.png" width="100%" /></td>
</tr>
<tr>
<td align="center"><b>Soul (Personality)</b><br/>3 proactivity presets + custom SOUL.md for tone & style<br/><br/><img src="website/assets/screenshot-soul.en.png" width="100%" /></td>
<td align="center"><b>Diagnostic Panel</b><br/>One-click self-check across AI / MCP / skills / network + bundle export<br/><br/><img src="website/assets/screenshot-diagnostic.en.png" width="100%" /></td>
</tr>
<tr>
<td align="center"><b>Expert Agents</b><br/>A library of expert agents you can summon by @name<br/><br/><img src="website/assets/screenshot-agents.en.png" width="100%" /></td>
<td align="center"><b>Usage Stats</b><br/>Requests, tokens, cache hits, and per model / skill usage<br/><br/><img src="website/assets/screenshot-usage.en.png" width="100%" /></td>
</tr>
<tr>
<td align="center" colspan="2"><b>Projects & Workspaces</b><br/>Group work into projects, each with its own skills & MCP<br/><br/><img src="website/assets/screenshot-project.en.png" width="60%" /></td>
</tr>
<tr>
<td align="center" colspan="2"><b>Content Safety Scan</b><br/>Three permission modes (Request Approval / Smart Review / Full Autonomy) + scan agents / skills / memory for prompt injection & dangerous instructions<br/><br/><img src="website/assets/screenshot-security-sca