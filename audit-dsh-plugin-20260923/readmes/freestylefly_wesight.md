# WeSight

<p align="center">
  <img src="public/readme-banner.svg" alt="WeSight desktop AI agent workspace" width="900">
</p>

<h3 align="center">
  Desktop AI Agent Workspace for Local Coding Agents
</h3>

<p align="center">
  <a href="https://github.com/freestylefly/wesight/stargazers"><img src="https://img.shields.io/github/stars/freestylefly/wesight?style=flat-square&color=1b79ff" alt="GitHub stars"></a>
  <a href="https://github.com/freestylefly/wesight/network/members"><img src="https://img.shields.io/github/forks/freestylefly/wesight?style=flat-square&color=14b8a6" alt="GitHub forks"></a>
  <a href="https://github.com/freestylefly/wesight/releases/latest"><img src="https://img.shields.io/github/v/release/freestylefly/wesight?style=flat-square&color=f59e0b" alt="Latest release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/freestylefly/wesight?style=flat-square&color=64748b" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/platform-macOS%20Apple%20Silicon%20%2B%20Intel-111827?style=flat-square&logo=apple&logoColor=white" alt="macOS Apple Silicon and Intel">
  <img src="https://img.shields.io/badge/platform-Windows%20x64-0078d4?style=flat-square&logo=windows11&logoColor=white" alt="Windows x64">
</p>

<p align="center">
  <strong>English</strong> | <a href="README_zh.md">简体中文</a>
</p>

WeSight is an open-source desktop control console for local AI agents. It helps you install or reuse Claude Code, Codex, Kimi Code, OpenClaw, Hermes Agent, OpenCode, Qwen Code, DeepSeek-TUI, and the built-in agent runtime, then gives them a visual workspace for chat, tools, files, IM channels, skills, model providers, runtime metrics, and desktop companion workflows.

> Public releases ship signed and notarized macOS builds for Apple Silicon and Intel, plus a Windows x64 installer. If WeSight helps your agent workflow, a Star makes the project easier for more builders to discover.

## Quick Links

- Website: [wesight.ai](https://wesight.ai/)
- Latest release: [github.com/freestylefly/wesight/releases/latest](https://github.com/freestylefly/wesight/releases/latest)
- Screenshots: [Screenshots](#screenshots)
- Core features: [Core Features](#core-features)
- Agent engines: [Agent Engines](#agent-engines)
- Product roadmap: [Product Roadmap](https://github.com/users/freestylefly/projects/1)
- Development: [Quick Start](#quick-start)

## Why WeSight

Terminal-native coding agents are powerful, while their setup, model routing, permissions, IM entry points, file changes, and runtime metrics often live in separate places. WeSight turns those moving pieces into one desktop workspace:

- Install, detect, and reuse local agent CLIs from a beginner-friendly UI.
- Run coding agents through a visual chat with tool panels, slash commands, file diffs, and permission prompts.
- Connect agent tasks to IM channels such as Feishu, with per-engine configuration.
- Track every task with engine, model, token usage, TTFT, TPS, tool latency, steps, status, and duration.
- Extend workflows through SkillHub skills, built-in skills, scheduled tasks, memory, and a desktop pet that follows active work.

## Screenshots

<table>
  <tr>
    <td width="50%">
      <img src="public/readme/screenshots/cowork-chat.png" alt="WeSight Cowork chat">
    </td>
    <td width="50%">
      <img src="public/readme/screenshots/agent-engines.png" alt="WeSight agent engine settings">
    </td>
  </tr>
  <tr>
    <td><strong>Cowork Chat</strong><br>Run local coding agents as a desktop chat with engine and model controls.</td>
    <td><strong>Agent Engines</strong><br>Configure Claude Code, Codex, Kimi Code, OpenClaw, Hermes Agent, OpenCode, Qwen Code, DeepSeek-TUI, and the built-in runtime.</td>
  </tr>
  <tr>
    <td width="50%">
      <img src="public/readme/screenshots/runtime-dashboard.png" alt="WeSight runtime dashboard">
    </td>
    <td width="50%">
      <img src="public/readme/screenshots/live-workspace.png" alt="WeSight live workspace">
    </td>
  </tr>
  <tr>
    <td><strong>AI Runtime Dashboard</strong><br>Inspect engine, model, tokens, TTFT, output-phase TPS, estimated model TPS, cost, and status.</td>
    <td><strong>Live Workspace</strong><br>Watch file writes, code changes, tool activity, and generated artifacts while the agent works.</td>
  </tr>
  <tr>
    <td width="50%">
      <img src="public/readme/screenshots/skills-marketplace.png" alt="WeSight skills marketplace">
    </td>
    <td width="50%">
      <img src="public/readme/screenshots/studio-pet.png" alt="WeSight studio and desktop companion">
    </td>
  </tr>
  <tr>
    <td><strong>Skills Marketplace</strong><br>Browse SkillHub categories, install skills locally, and manage installed skills from WeSight.</td>
    <td><strong>Studio & Pet</strong><br>Use a visual office-style workspace and desktop companion to follow active agent tasks.</td>
  </tr>
</table>

## Core Features

- **Agent Engines** - Run Claude Code, Codex, Kimi Code, OpenClaw, Hermes Agent, OpenCode, Qwen Code, DeepSeek-TUI, or the built-in runtime from the same workspace.
- **One-click setup** - On macOS, WeSight can install supported local CLIs or detect the ones already present on the machine.
- **Unified model providers** - Configure official OpenAI, Anthropic Claude, Google Gemini, DeepSeek, Qwen, Moonshot, Ollama, OpenRouter, GitHub Copilot, and custom OpenAI-compatible endpoints.
- **Local CLI configuration** - Use existing Claude Code, Codex, Kimi Code, OpenClaw, Hermes Agent, OpenCode, Qwen Code, or DeepSeek-TUI accounts and config when you already have a working terminal setup.
- **Graphical tool execution** - View commands, files, permissions, slash commands, outputs, generated images, and tool results inside the chat flow.
- **IM Agent Hub** - Route Feishu messages into OpenClaw, Hermes Agent, Claude Code, or Codex, with per-engine bot profiles.
- **AI Runtime Dashboard** - Measure calls by engine, model, source, status, tokens, completion time, TTFT, output-phase TPS, estimated model TPS, tool latency, and agent steps.
- **Live Workspace** - Open a right-side workspace for live code writing, static diffs, runtime monitoring, task todos, skills, and artifacts.
- **SkillHub Marketplace** - Discover, categorize, install, enable, disable, update, and remove local WeSight skills.
- **Scheduled Tasks** - Create recurring agent jobs for research, reports, monitoring, inbox cleanup, and reminders.
- **Memory and personalization** - Extract useful preferences from conversations and reuse them across future sessions.
- **Desktop pet and studio** - Keep a lightweight desktop companion and a pixel-style studio view for active tasks.

## ❤️ Sponsors

> [Want to appear here?](public/readme/community/wechat-personal.jpg) Add me on WeChat and include your product name plus a short project sponsorship note in the friend request.

| Sponsor | Description |
| ------- | ----------- |
| <a href="https://pptoken.cc/"><img src="public/readme/sponsors/pptoken.png" alt="PPToken" width="240"></a> | Project sponsor. PPToken provides API relay and key distribution for ChatGPT, Claude, Gemini and other mainstream AI models, with low latency, high availability, pay-as-you-go billing, and flexible subscription plans. |
| <a href="https://ciyuan.today/"><img src="public/readme/sponsors/ciyuan-api.jpg" alt="Ciyuan API" width="240"></a> | Project sponsor. Ciyuan API aims to become a one-stop AI interface platform for developers, providing stable, low-latency, and highly available large model API services to make AI application development simpler. |

## Agent Engines

| Engine           | Best For                                                    | Setup Path                                      |
| ---------------- | ----------------------------------------------------------- | ----------------------------------------------- |
| Built-in runtime | General desktop cowork sessions and skills                  | Included in WeSight              