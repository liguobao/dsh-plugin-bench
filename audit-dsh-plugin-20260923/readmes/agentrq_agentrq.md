# AgentRQ ── Agent-Human Collaboration Platform

<p align="center">
  <a href="README.zh-CN.md">简体中文</a>
  <br />
  <br />
  <a href="https://discord.gg/xFSMaEA2b2">
    <img src="https://img.shields.io/badge/Discord-Join%20Community-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" />
  </a>
</p>

AgentRQ is a modern, high-performance platform designed for seamless collaboration between human operators and AI agents. It leverages the **Model Context Protocol (MCP)** to allow AI models (like Claude) to interact directly with your workspace's task management system.

## 🚀 Overview

Think of AgentRQ as a shared workspace where humans and AI agents work together seamlessly. You can break down complex goals into manageable tasks, and delegate work directly to your AI agents. 

Because agents "see" the workspace state via MCP, they can autonomously pull their assigned tasks, update statuses, request permissions for sensitive actions, and communicate with you—all synchronized instantly across the platform in real-time.

## ✨ Features

Real captures from the running app — no mockups.

<table>
<tr>
<td width="50%" valign="middle">

### Visual Task Board

Every task Claude creates appears instantly on your board. See what it's working on, what it needs, and what it just finished — all from a clean, fast dashboard you can open on any device, as a list or a Kanban.

</td>
<td width="50%"><img src="https://agentrq.com/assets/feature-task-board.gif" alt="AgentRQ active tasks dashboard and kanban board" width="320" /></td>
</tr>
<tr>
<td width="50%"><img src="https://agentrq.com/assets/feature-task-scheduling.gif" alt="AgentRQ scheduled task auto-spawning into the dashboard" width="320" /></td>
<td width="50%" valign="middle">

### Task Scheduling

Give any task a launch date, or a recurring cadence — every 15 minutes, hourly, daily, weekly, custom days. A background poller ticks every minute and spawns the task the instant it's due, no server or agent needing to stay awake and wait.

</td>
</tr>
<tr>
<td width="50%" valign="middle">

### Events

Events are named signals — `qa_passed`, `deploy_finished`, `blog_published` — that any task can fire when it completes. Wire one to a workspace and that workspace gets a new task automatically, no polling and no glue code.

</td>
<td width="50%"><img src="https://agentrq.com/assets/feature-events.gif" alt="AgentRQ events list and configured trigger" width="320" /></td>
</tr>
<tr>
<td width="50%"><img src="https://agentrq.com/assets/feature-workflows.gif" alt="AgentRQ workflow node graph" width="320" /></td>
<td width="50%" valign="middle">

### Workflows

A Workflow is Events and workspaces arranged on a graph. Drag a workspace onto an event to subscribe it; drag an event onto a workspace to emit it on completion. No decision-tree DSL, no YAML — just the shape of your release process, visible.

</td>
</tr>
<tr>
<td width="50%" valign="middle">

### Tool Call History

The task detail view's History tab lays out a lane-grouped timeline of every tool call and message in a run — Input, Agent, and Tools. Search it, click into any entry, and see exactly what ran, what it returned, and whether it was allowed or denied.

</td>
<td width="50%"><img src="https://agentrq.com/assets/feature-tool-call-history.gif" alt="AgentRQ tool call history trajectory panel" width="320" /></td>
</tr>
<tr>
<td width="50%"><img src="https://agentrq.com/assets/feature-auto-title.gif" alt="AgentRQ auto-title generation in action" width="320" /></td>
<td width="50%" valign="middle">

### Auto-Title Generation

Write your task description, click the sparkle, and a small language model — downloaded once and cached by your browser — reads it and writes the title. No API call, no server, no data leaving your machine.

</td>
</tr>
<tr>
<td width="50%" valign="middle">

### Speech-to-Text

Click the mic on any task description or reply and dictate it instead. Transcription runs on an in-browser Whisper model — your voice is processed on-device and never uploaded anywhere.

</td>
<td width="50%"><img src="https://agentrq.com/assets/feature-speech-to-text.gif" alt="AgentRQ speech-to-text mic entry point" width="320" /></td>
</tr>
<tr>
<td width="50%"><img src="https://agentrq.com/assets/feature-message-send-delay.gif" alt="AgentRQ message send delay countdown with Send Now and Cancel" width="320" /></td>
<td width="50%" valign="middle">

### Message Send Delay

Give a workspace a countdown — 3s, 5s, 10s, 15s, 30s or 60s — and every chat message waits that long in the thread before it reaches the agent. **Send Now** delivers it early, **Cancel** pulls it back unsent and puts the exact text and attachments back in your composer. Off by default, per workspace.

</td>
</tr>
<tr>
<td width="50%" valign="middle">

### Search & Keyboard Shortcuts

<kbd>⌘K</kbd> (<kbd>Ctrl+K</kbd> off macOS) opens a task finder that matches any word in a title or description, straight from the copy your device already saved — so it answers offline, and tells you how far it looked. Everything else is a bare letter: <kbd>N</kbd> for a new task, <kbd>M</kbd> and <kbd>T</kbd> to flip between a task's chat and its trajectory, <kbd>?</kbd> for the list. Nothing to configure, and nothing to memorise.

</td>
<td width="50%"><img src="https://agentrq.com/assets/feature-keyboard-shortcuts.gif" alt="AgentRQ task finder and keyboard shortcuts sheet" width="320" /></td>
</tr>
<tr>
<td width="50%"><img src="https://agentrq.com/assets/feature-machines-detail.png" alt="AgentRQ machine page: start an agent, running sessions, and live resources" width="320" /></td>
<td width="50%" valign="middle">

### Machines

Install `agentrqd` on a computer you own, enrol it once with a single-use code typed on the machine itself, and it becomes somewhere agents can run — in your repositories, with your toolchain. Pick a workspace and what to run, and it starts in that workspace's folder on that machine. Each machine's page shows what it has left: CPU, memory, uptime, load and free space per filesystem.

</td>
</tr>
<tr>
<td width="50%" valign="middle">

### Live Terminals

Open a running session from any browser and you are at the prompt. Keystrokes go straight through as the bytes your keys produced — <kbd>Esc</kbd> and <kbd>Ctrl-C</kbd> included — resizing reflows the program on the far end, and the session keeps running whether or not anybody is watching. Drop the network and the screen is still there when you come back.

</td>
<td width="50%"><img src="https://agentrq.com/assets/feature-machines-poster.png" alt="AgentRQ live terminal attached to a claude-code session on an enrolled machine" width="320" /></td>
</tr>
</table>

See the full list at [agentrq.com/features](https://agentrq.com/features).

## 🏛 Architecture

AgentRQ follows a decoupled service-oriented architecture:

### Backend (Go / Fiber)
- **API Server**: Fiber-based REST API for workspace and task management.
- **MCP Server**: Integrated `mcp-go` SSE server that exposes tools and resources to AI models.
- **CoreMCP (Supervisor)**: A global MCP server that allows agents to manage all workspaces, tasks, and statistics across the entire platform.
- **Data Layer**: GORM with SQLite for persistent, user-scoped storage.
- **Authentication**: Google OAuth2 integration with JWT-based session management.
- **Event Bus**: Internal pub/sub system for real-time SSE notifications.

### Frontend (Vue.js 3 / Vite)
- **Modern UI**: Tailored with Vue 3, Pinia, and Tailwind CSS.
- **Glassmorphism**: A sleek, premium design language with smooth transitions and real-time updates.
- **Reactive State**: Synchronized with the backend via SSE events.

### Desktop (Electron)
- **Same application, native shell**: the desktop app renders the *same* Vue components as the browser, so the two never diverge.
- **Native notifications**: agent activity reaches you while the window is in the background, with a dock or taskbar badge.
- **Tray, global short