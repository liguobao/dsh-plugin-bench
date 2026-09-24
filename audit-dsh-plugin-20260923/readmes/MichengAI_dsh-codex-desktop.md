<p align="center">
  <img src="assets/branding/dsh-codex-desktop-banner.webp" alt="DSH Codex Desktop product banner" width="100%">
</p>

<div align="center">

# DSH Codex Desktop

**Download once. Open a ready-to-use local AI workspace.**

[简体中文](README.zh-CN.md) · [Download](https://github.com/MichengAI/dsh-codex-desktop/releases) · [Changelog](CHANGELOG.md) · [Report an issue](https://github.com/MichengAI/dsh-codex-desktop/issues)

[![Release](https://img.shields.io/github/v/release/MichengAI/dsh-codex-desktop?display_name=tag&label=release)](https://github.com/MichengAI/dsh-codex-desktop/releases)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Desktop package](https://github.com/MichengAI/dsh-codex-desktop/actions/workflows/desktop-package.yml/badge.svg?branch=main)](https://github.com/MichengAI/dsh-codex-desktop/actions/workflows/desktop-package.yml)
![Windows x64](https://img.shields.io/badge/Windows-x64-0078D4?logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-Apple%20Silicon%20%7C%20Intel-000000?logo=apple&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-x64%20%7C%20ARM64-FCC624?logo=linux&logoColor=black)

</div>

> DSH Codex Desktop is a community-maintained desktop distribution of DeepSeek Harness. It is not an official DeepSeek AI product.

DSH Codex Desktop turns [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) into a native, ready-to-run desktop workbench. The installer includes the required Node.js runtime and local DSH runtime: install it, open it, then start working. You do not need to prepare a Node.js environment or launch DSH from a terminal.

## Download and start

Get the current installer from [GitHub Releases](https://github.com/MichengAI/dsh-codex-desktop/releases).

| Platform | Package | Start here |
| --- | --- | --- |
| Windows x64 | `.exe` installer or `.zip` archive | Run the installer, then open **DSH Codex Desktop** from the Start menu. |
| macOS Apple Silicon / Intel | `.dmg` installer | Open the disk image, move the app to Applications, then launch it. |
| Linux x64 / ARM64 | `.AppImage` or Debian / Ubuntu `.deb` | Run the package matching your CPU architecture, or install the deb package, then launch the app. |

1. Download the package for your platform.
2. Install and open **DSH Codex Desktop**.
3. Wait for the built-in local DSH service to finish starting.
4. Create a task, select a model and permission mode, then work in your project.

The application keeps DSH data in your existing user profile (`%USERPROFILE%\.dsh` on Windows), so sessions and settings remain available after application upgrades.

## A complete desktop workbench

| Capability | What you get |
| --- | --- |
| **Desktop conversation workspace** | Project and task navigation, conversation sessions, model selection, permissions, session logs, and a focused desktop window. |
| **Expert presets** | Enable specialist roles for code review, architecture, frontend, backend, operations, and other workflows. |
| **Skill center** | Inspect, enable, disable, upload, and manage local and shared Agent skills from Settings. |
| **Archive management** | Search archived conversations, restore a session when needed, or permanently remove archived records. |
| **IM assistant** | Configure DingTalk, Feishu, Lark, WeChat, WeCom, QQ, Telegram, and other available channels in one place. |
| **Plugin market** | Discover, install, update, enable, and diagnose DSH plugins without leaving the desktop client. |
| **MCP connector** | Add and manage MCP services through OAuth, API keys, HTTP, stdio, or JSON configuration. |
| **Scheduled automation** | Use the built-in DSH scheduling capability to manage recurring tasks from the same workspace. |
| **Safe local runtime** | The app starts DSH on a validated loopback address and keeps the browser UI inside the desktop shell. |

## Product preview

Explore the desktop workspace, light-theme settings, and plugin management pages. The home screen and 11 settings and plugin screenshots come from the newly supplied desktop captures; the conversation, context, and sidebar previews are retained from earlier captures. Plugin versions, counts, and states reflect each capture. Click any image to view it at its original resolution.

<p align="center"><em>Home: project navigation, task entry points, and composer.</em></p>

<p align="center"><a href="assets/screenshots/preview-home.webp"><img src="assets/screenshots/preview-home.webp" alt="Home: project navigation, task entry points, and composer." width="960"></a></p>

<p align="center"><em>Conversation: messages, trajectory, context, and task input.</em></p>

<p align="center"><a href="assets/screenshots/preview-conversation.webp"><img src="assets/screenshots/preview-conversation.webp" alt="Conversation: messages, trajectory, context, and task input." width="960"></a></p>

<details>
<summary>Appearance and desktop pets (2 screenshots)</summary>

<p align="center"><em>Light-theme settings: permissions, language, appearance, and editor preferences.</em></p>

<p align="center"><a href="assets/screenshots/preview-general-light.webp"><img src="assets/screenshots/preview-general-light.webp" alt="Light-theme settings: permissions, language, appearance, and editor preferences." width="960"></a></p>

<p align="center"><em>Pet settings: choose a companion, manage custom pets, and adjust size.</em></p>

<p align="center"><a href="assets/screenshots/preview-pets.webp"><img src="assets/screenshots/preview-pets.webp" alt="Pet settings: choose a companion, manage custom pets, and adjust size." width="960"></a></p>

</details>

<details>
<summary>Our plugin pages (6 screenshots)</summary>

<p align="center"><em>Expert presets: filter, search, and enable specialist roles.</em></p>

<p align="center"><a href="assets/screenshots/preview-experts.webp"><img src="assets/screenshots/preview-experts.webp" alt="Expert presets: filter, search, and enable specialist roles." width="960"></a></p>

<p align="center"><em>Skill management: manage local Agent Skills across sources.</em></p>

<p align="center"><a href="assets/screenshots/preview-skills.webp"><img src="assets/screenshots/preview-skills.webp" alt="Skill management: manage local Agent Skills across sources." width="960"></a></p>

<p align="center"><em>Scheduled automation: examples, task schedules, and run history access.</em></p>

<p align="center"><a href="assets/screenshots/preview-automation.webp"><img src="assets/screenshots/preview-automation.webp" alt="Scheduled automation: examples, task schedules, and run history access." width="960"></a></p>

<p align="center"><em>IM assistant: manage messaging channels, accounts, and incoming messages.</em></p>

<p align="center"><a href="assets/screenshots/preview-im-connect.webp"><img src="assets/screenshots/preview-im-connect.webp" alt="IM assistant: manage messaging channels, accounts, and incoming messages." width="960"></a></p>

<p align="center"><em>Archived conversations: filter by project, search, and restore past chats.</em></p>

<p align="center"><a href="assets/screenshots/preview-archive.webp"><img src="assets/screenshots/preview-archive.webp" alt="Archived conversations: filter by project, search, and restore past chats." width="960"></a></p>

<p align="center"><em>Codex UI settings: feature overview and companion plugin installation status.</em></p>

<p align="center"><a href="assets/screenshots/preview-codex-ui.webp"><img src="assets/screenshots/preview-codex-ui.webp" alt="Codex UI settings: feature overview and companion plugin installation status." width="960"></a></p>

</details>

<details>
<summary>Community plugin pages (5 screenshots)</summary>

<p align="center"><em>Context settings</em></p>

<p align="center"><a href="assets/screenshots/preview-context.webp"><img src="assets/screenshots/preview-context.webp" alt="Context settings" width="960"></a></p>

<p align="center"><em>Sidebar settings</em></p