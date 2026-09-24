<p align="center">
  <img src="./resources/icons/icon.png" width="112" alt="Minke icon">
</p>

<h1 align="center">Minke</h1>

<p align="center">
  <strong>A local-first desktop agent workspace powered by DeepSeek Harness</strong>
</p>

<p align="center">
  English · <a href="./README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="https://github.com/lencx/Minke/releases"><img src="https://img.shields.io/github/downloads/lencx/Minke/total.svg?style=flat" alt="Minke downloads"></a>
  <a href="https://discord.gg/XMX5BEX8K"><img src="https://img.shields.io/badge/Minke-discord-blue?style=flat&logo=discord&logoColor=f2f0ea" alt="Minke Discord"></a>
  <a href="https://x.com/lencx_"><img src="https://img.shields.io/twitter/url?url=https%3A%2F%2Fx.com%2Flencx_" alt="Follow @lencx_ on X"></a>
  <a href="https://www.buymeacoffee.com/lencx"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" height="20"></a>
</p>

Minke is a local-first desktop agent workspace powered by [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness). Work with an agent across conversations, project files, terminals, and visible browser tabs. Take over a page when needed, review and edit the resulting files, or access your workspace from another device.

> [!IMPORTANT]
> Minke is under active development. Features, packaging, and the local data schema may change as the project evolves. This README describes the current source; packaged releases may differ. Minke is an independent community project, not an official DeepSeek product.

## Highlights

Minke builds on Harness's agent capabilities with shared browser control, an integrated desktop workspace, remote access, and local model management.

- **Agent Browser with shared control** — Agents can search, open, and interact with the Web in visible browser tabs. Take control of a live tab without closing it, hand it back when ready, or send annotated page context to the conversation.
- **Flexible workspace and file editing** — Arrange Files, Terminal, Web, Browser History, and Plugins beside the conversation using Harness's split, floating, and fullscreen sidebar tabs, plus Minke's independent bottom panel. Edit source, review diffs, and preview Markdown and HTML drafts in place.
- **Agent workflows and conversation history** — Use Harness's Agent Presets, planning, goals, skills, and subagents. Navigate long conversations through the turn outline, jump to earlier turns, export session logs, and ask the agent to schedule follow-ups in the conversation.
- **Remote access where you already work** — Open your workspace from a phone or another computer through a responsive Web client with PWA support, or use WeChat, Telegram, and Discord to run tasks on the Minke computer. Private Web access supports Tailscale and Cloudflare Access.
- **Cloud and local models** — Use Harness's model providers and custom endpoints, with Minke's model discovery and optional service auto-start for LM Studio and Ollama. Other loopback OpenAI-compatible services can be configured manually.
- **Plugins with visible runtime status** — Discover and install Harness plugins, enable or disable them, and see whether they are running, loading, or failed. Safe mode helps troubleshoot startup while preserving installed plugins.
- **Desktop integration and local storage** — macOS, Windows, and Linux builds provide native menus, customizable shortcuts, built-in updates, synchronized themes, and English and Chinese UI. Sessions, settings, Browser History, and browser session data remain on your machine.

<table>
  <tr>
    <td width="50%"><img src="./assets/minke-new.png" alt="Minke conversation workspace"></td>
    <td width="50%"><img src="./assets/minke-code.png" alt="Minke code workspace with Files diff and Terminal"></td>
  </tr>
  <tr>
    <td width="50%"><img src="./assets/minke-agent-tab.png" alt="Minke settings and workspace"></td>
    <td width="50%"><img src="./assets/minke-agent-browser.png" alt="Minke agent browser"></td>
  </tr>
  <tr>
    <td width="50%"><img src="./assets/minke-remote.png" alt="Minke remote control through WeChat, Telegram, and Discord"></td>
    <td width="50%"><img src="./assets/minke-plugin.png" alt="Minke Plugins workspace and tab layout"></td>
  </tr>
</table>

## Remote access from another device

Minke remote access is a responsive Web client backed by Minke Host—not a
video stream or touch-controlled projection of the Electron window. From a
phone you can continue conversations, start agent tasks, manage project files,
and use a terminal that runs on the Minke computer.

![Minke remote workspace on mobile and desktop](./assets/minke-remote.gif)

> [!NOTE]
> **Tailscale Serve over HTTPS**, **Tailscale Direct IP**, and
> **Cloudflare Access** have all completed end-to-end regression testing and
> are currently available.

- **Tailscale Serve over HTTPS (recommended)** — Best for devices already joined to the same tailnet. It provides a secure HTTPS address and supports PWA installation.
- **Tailscale Direct IP (advanced)** — Binds only to the current device's Tailscale IPv4. Traffic remains end-to-end encrypted by Tailscale, but the address uses HTTP and is not a browser secure context.
- **Cloudflare Access** — Exposes a named tunnel protected by an identity policy, without requiring Tailscale on the phone. It requires a configured Cloudflare Tunnel, Access application, and an explicit allow policy.

### Recommended setup: Tailscale Serve

Minke can expose its Web UI privately through [Tailscale Serve](https://tailscale.com/docs/reference/tailscale-cli/serve). It keeps Harness on the local loopback address, does not bind it to the LAN, and does not enable the public Tailscale Funnel.

1. Install Tailscale on the Minke computer and the phone, sign both into the
   same tailnet, and confirm the computer is connected.
2. In Minke, open **Connections → Device access → Remote access**, select
   **HTTPS Serve**, and enable remote access. Minke connects in the
   background; no restart is required.
3. Copy or open the displayed
   `https://…ts.net` address on the phone.

### Install as a PWA

Open a Tailscale Serve or Cloudflare Access HTTPS address, choose
**Install Minke** in the sidebar, and accept the browser install prompt. On
iPhone or iPad, use **Share → Add to Home Screen**. The installed app launches
in standalone mode; when connectivity is poor it shows connection or offline
feedback instead of silently presenting cached workspace content.

Minke activates only one remote route at a time, owns its foreground proxy
while the app is running, and stops it on exit. The remote page can start
agent tasks and use local tools already authorized in Minke, so grant access
only to trusted tailnet members or Cloudflare Access identities.

## Installation

Download Minke only from the official [GitHub Releases](https://github.com/lencx/Minke/releases) page. The links below always point to the latest stable release.

| Platform | Architecture | Package |
| --- | --- | --- |
| macOS | Apple Silicon (`arm64`) | [Download `.dmg`](https://github.com/lencx/Minke/releases/latest/download/Minke-macos-arm64.dmg) |
| macOS | Intel (`x64`) | [Download `.dmg`](https://github.com/lencx/Minke/releases/latest/download/Minke-macos-x64.dmg) |
| Windows | `x64` | [Download `.exe`](https://github.com/lencx/Minke/releases/latest/download/Minke-windows-x64.exe) |
| Linux | Debian / Ubuntu (`x64`) | [Download `.deb`](https://github.com/lencx/Minke/releases/latest/download/Minke-linux-x64.deb) |
| Linux | Fedora / RHEL (`x64`) | [Download `.rpm`](https://github.com/lencx/Minke/releases/latest/download/Minke-linux-x64.rpm) |
| Linux | `x64` (portable AppImage) | [Download `.AppImage`](https://github.com/lencx/Minke/releases/latest/download/Minke-linux-x64.AppImage) |

Release checksums are available in [`SHA256SUMS`](https://github.com/lencx/Minke/releases/latest/download/SHA256SUMS).

Packaged macOS, Windows, 