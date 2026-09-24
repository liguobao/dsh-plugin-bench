<p align="center">
<img width="256" alt="AgentKey" src="https://github.com/user-attachments/assets/4c7c78a9-e5d8-45ce-9372-d5bffe8f61c5" />
</p>

<p align="center">
  <strong>One command. Full internet access for your AI agent.</strong>
  <br>
  Browse Twitter, search LinkedIn, scrape social media, read any webpage. Zero config. Just install and go.
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#what-your-agent-can-now-do">Platforms</a> ·
  <a href="#faq">FAQ</a> ·
  <a href="docs/README_zh.md">中文</a>
</p>

<p align="center">
  <a href="https://agentkey.app"><img src="https://img.shields.io/badge/Website-agentkey.app-blue?style=for-the-badge" alt="Website" /></a>
  <a href="https://console.agentkey.app"><img src="https://img.shields.io/badge/Console-console.agentkey.app-7c3aed?style=for-the-badge" alt="Console" /></a>
</p>

<p align="center">
  <a href="https://www.producthunt.com/products/agentkey?embed=true&amp;utm_source=badge-top-post-badge&amp;utm_medium=badge&amp;utm_campaign=badge-agentkey" target="_blank" rel="noopener noreferrer"><img alt="AgentKey - One-stop live data marketplace for your agent | Product Hunt" width="250" height="54" src="https://api.producthunt.com/widgets/embed-image/v1/top-post-badge.svg?post_id=1192591&amp;theme=light&amp;period=daily&amp;t=1784013858323"></a>
</p>

---

**Install AgentKey. Give your AI superpowers.**

AgentKey is the master key for the agent ecosystem. When using Claude, Manus, or other agents, you often need external data: social media, e-commerce, on-chain data, various APIs. That means hunting down API keys, managing subscriptions, or hitting dead ends.

With AgentKey installed, your agent gains all these data capabilities automatically. No per-provider registrations, no juggling separate API bills. One subscription and go.

> ⭐ Star this repo to get notified whenever we add new platform support or release updates.

---

## Use Cases

| You ask your agent to...                               | Without AgentKey              | With AgentKey                                  |
| ------------------------------------------------------ | ----------------------------- | ---------------------------------------------- |
| 🐦 What has Musk been saying on Twitter lately?        | Can't access, tweets blocked  | Pulls all relevant tweets and summarizes them  |
| 📕 What do people think of this product on Instagram?  | Blocked, login required       | Scrapes real posts, organizes by sentiment     |
| 📺 What does this YouTube / Bilibili video cover?      | Can't read, no subtitles      | Reads the video/transcript, extracts key points |
| 📖 Find Reddit threads about this pain point           | 403 blocked                   | Finds relevant threads and extracts solutions  |
| 👔 Check this competitor / candidate's LinkedIn        | 403, access issues            | Opens the page, summarizes key info            |
| 🎵 What's trending on Douyin / TikTok right now?       | Can't scrape the hot list     | Pulls trending topics and tags                 |
| 🌐 What does this webpage say?                         | Returns a wall of raw HTML    | Extracts the content, explains it clearly      |
| 📦 What does this GitHub repo do?                      | Have to click through yourself | Reads README & Issues, one-line summary       |
| 🧾 What has this wallet / fund been buying lately?     | Click through a block explorer | Summarizes recent transactions and positions  |

Before AgentKey: 10 tasks → 10 API keys → 10 separate bills.

Your agent is half-capable at best, constantly needing human help to find data, juggling credentials, drowning in complexity.

Now: one AgentKey handles everything. **AgentKey unifies all the external access your AI needs to do real work.**

---

## New here? Start on the web

Before touching the terminal, you can get a feel for AgentKey directly in your browser — the website and console explain things more visually than this README can.

- 🌐 **[agentkey.app](https://agentkey.app)** — Product overview, supported platforms, live demos, pricing details
- 🎛️ **[console.agentkey.app](https://console.agentkey.app)** — Sign up, manage your subscription, manage your API key, track usage

The one-line install below is what plugs AgentKey into your AI agent. If you only want to look around first, the two links above are the friendlier starting point.

---

## Install

One command. A browser tab opens for login, then you're done. The installer auto-detects every agent on your machine ([40+ supported](https://github.com/vercel-labs/skills#available-agents). Common examples include Claude Code, Codex, Gemini CLI, and Cursor CLI, etc.) and configures each one.

**macOS / Linux**
```bash
curl -fsSL https://agentkey.app/install.sh | bash
```

**Windows** (PowerShell)
```powershell
irm https://agentkey.app/install.ps1 | iex
```

Restart your agent, then ask it something that needs the internet. A running DeepSeek Harness profile watches the home patch through HMR; stopped profiles load it on their next start.

> *"What has Musk been tweeting about lately?"*

That's it. No API key to copy, no JSON to edit. 

<sub>Need to target specific agents or run in CI? → See the "Advanced install options" item in the [FAQ](#faq).</sub>

---

### DeepSeek Harness (DSH)

The one-line installers above detect `${DSH_HOME:-~/.dsh}` or the `dsh` command automatically. They install the AgentKey skill globally at `~/.agents/skills/agentkey`, authenticate with AgentKey, and add one managed Loader block to DSH's home-level patch:

```text
${DSH_HOME:-~/.dsh}/cordis.patch.yml
```

This is a **CLI-managed DSH MCP integration**, not a native installable DSH plugin. The home layer uses Loader id `agentkey`, module `@deepseek-ai/dsh-mcp-client`, and MCP `serverName: agentkey`; it is composed over current and future profiles. Tool allow/deny policy still controls whether a preset, session, or subagent can see the tools.

DSH 0.1.0-rc.7 does not provide an OAuth `authProvider` to its MCP SDK client. A header-free server entry cannot complete 401/RFC 9728 discovery or open a browser. DSH must use the device-code command below so the CLI writes a local Bearer key.

For a DSH-only manual install, run exactly these two steps:

```bash
npx -y skills add chainbase-labs/agentkey -g -a universal -s agentkey -y
npx -y @agentkey/cli --auth-login --only dsh
```

The CLI stores the real API key only in the single local home patch; no key belongs in Git. Re-running the command rotates the key and replaces the managed block. No existing profile is required. During migration it removes only top-level, column-1 AgentKey managed blocks from per-profile patches and renames a legacy `.agent-presets/agentkey` directory to a timestamped backup; the CLI prints that backup path. If it structurally detects an older unmarked AgentKey Loader row, it stops without changing any patch and asks you to remove that top-level `insert` child manually. Symlinked profile patches are inspected read-only: a clean symlink profile is allowed, while either legacy AgentKey form stops installation and reports the path for manual removal.

Only currently running profile processes observe the home-file change immediately through HMR. Stopped and future profiles load it when they start. If an old preset was already active in a session, close that session or restart DSH once after migration.

#### How to confirm DSH installation

1. Open **DSH → Settings → Plugins → Plugin list**, search for configured id `agentkey`, and expand the `mcp-client` row. DSH 0.1 currently renders:
   - Loader path: `include:agentkey` (the stable configured entry id is `agentkey`)
   - module title: `@deepseek-ai/dsh-mcp-client` (the card shortens it to `mcp-client`)
   - Cordis status: `Mounted` (the underlying fiber phase is `active`)

   `Mounted`/`active` proves only that Cordis loaded the row. Because `failOnStartupError: false`, it does **not** prove that MCP authenticated or connected.