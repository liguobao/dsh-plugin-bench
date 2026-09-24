# BrowserSkill

<p align="center">
  <img src="docs/assets/browserskill-readme-banner.png" alt="BrowserSkill — connect your AI agent to your browser" />
</p>

<p align="center">
  <strong>Let AI agents work in your logged-in browser while you keep working.</strong>
</p>

<p align="center">
  English · <a href="README.zh-CN.md">中文</a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#website-debugging">Website debugging</a> ·
  <a href="#deepseek-harness-plugin">DSH plugin</a> ·
  <a href="#documentation">Documentation</a> ·
  <a href="CHANGELOG.md">Changelog</a>
</p>

**BrowserSkill connects your AI agent to Chrome or Microsoft Edge, using the accounts you are already signed into.** Ask it to read pages, fill forms, work through a website, capture a long screenshot, or investigate a failing request. Tasks run in a separate, visible **Agent Window**; an existing tab can be explicitly borrowed and returned when the task ends.

Use the `bsk` CLI with Cursor, Claude Code, Codex, OpenClaw, CodeBuddy, WorkBuddy, Pi, Hermes Agent, or another shell-capable agent. **DeepSeek Harness** has a dedicated plugin with native browser tools and task previews. You choose the agent and model; BrowserSkill provides the browser connection.

## What you can do

| Capability | What it gives you |
| --- | --- |
| **Work with your existing accounts** | Use the browser's current login state to read documents, search internal sites, fill forms, and complete web workflows. |
| **Keep browser tasks visible** | Give the agent its own window, borrow an existing tab when needed, and take over for login, verification, or other human-only steps. |
| **Read, interact, and capture** | Inspect page text and controls, click and type, manage tabs, capture viewport or full-page screenshots, and upload or download files in local mode. |
| **Debug websites with evidence** | Connect actions to requests, response bodies, console messages, and page changes. Inspect performance, slow APIs, and suspected duplicate requests; use explicit HTTP rules or request replay to test a hypothesis. |
| **Choose the right browser** | Name browser instances, bind a task to a specific profile, or pair an agent running on a server with a browser on your computer. |
| **Review what happened** | Reopen browser-local debugging history, export evidence as JSON, or enable a separate operation audit to review task activity. |

Watch a browser task in action:

https://github.com/user-attachments/assets/db782c92-b1d4-4aae-a255-039675937a90

## Quick Start

For local automation, you need **an AI agent + the `bsk` CLI + the browser extension**. The CLI includes the background daemon. The skill teaches your agent how to use it.

| Component | Supported environments |
| --- | --- |
| CLI / daemon | macOS: Apple Silicon and Intel · Linux: x64 and ARM64 · Windows: x64 |
| Extension | Chrome and Microsoft Edge, based on Chromium 125 or later. Other Chromium browsers may work; compatibility is not guaranteed. |
| Agent integration | A shell-capable agent with the BrowserSkill skill, or DeepSeek Harness with the [DSH plugin](#deepseek-harness-plugin). |

### Let your agent set it up

Send this to your agent:

```text
Set up browser-skill on this machine by following https://raw.githubusercontent.com/Tencent/BrowserSkill/main/AGENT_INSTALL.md
```

The guide covers CLI installation, the correct skill or DSH plugin, connection checks, and a first browser task. You will still need to install the extension in the browser you want to use:

**[Install for Chrome](https://chromewebstore.google.com/detail/hhcmgoofomhgciiibhipgmgkgnoenaoi)** · **[Install for Edge](https://microsoftedge.microsoft.com/addons/detail/browserskill/emacgiaaaiojkkpkddmmdfhmokgmnikg)**

<details>
<summary><b>Manual setup</b></summary>

#### 1. Install the CLI

macOS / Linux:

```sh
curl -fsSL https://raw.githubusercontent.com/Tencent/BrowserSkill/main/install.sh | sh
export PATH="${BSK_INSTALL_DIR:-$HOME/.local/bin}:$PATH"
```

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/Tencent/BrowserSkill/main/install.ps1 | iex
```

By default, the binary is installed under `~/.local/bin`. Check it in the terminal or agent environment that will use it:

```sh
bsk --version
```

If an already-running agent cannot find `bsk`, restart it to pick up the new PATH, or configure the installed binary's absolute path.

#### 2. Connect the extension

Install it from the [Chrome Web Store](https://chromewebstore.google.com/detail/hhcmgoofomhgciiibhipgmgkgnoenaoi) or [Edge Add-ons](https://microsoftedge.microsoft.com/addons/detail/browserskill/emacgiaaaiojkkpkddmmdfhmokgmnikg). Open its popup, enable the local connection, and check its status after starting the CLI.

#### 3. Install the skill for your agent

```sh
bsk install-skill
```

Select your harness with **Space**, then press **Enter**. For non-interactive setup, choose it explicitly:

```sh
bsk install-skill --harness cursor --json
```

Use `bsk install-skill --list` to see supported targets and paths. Existing installations are skipped unless you explicitly replace them with `--force`. For another harness, copy the entire [`crates/bsk-cli/skill/`](crates/bsk-cli/skill/) directory into its skills directory as `browser-skill/`, including `references/`.

DSH users should install the [plugin](#deepseek-harness-plugin) instead; it includes the skill.

#### 4. Check the connection

```sh
bsk doctor
```

Resolve any failed checks and confirm that the extension shows **Connected**. Start a new agent session and check that it can discover `browser-skill`; a successful doctor check alone does not confirm skill discovery.

</details>

### Try your first task

Once connected, ask your agent:

```text
Use browser-skill to open https://example.com, summarize the page, and end the browser session when finished.
```

The agent should open an Agent Window, read the page, return the summary, and stop its task. Harnesses that support skill slash commands can also use `/browser-skill`.

<details>
<summary><b>Try the CLI directly</b></summary>

Start a session and keep the returned `session_id`:

```sh
bsk session start --no-focus --json
```

Replace `<id>` with that value in each command below. With multiple connected browsers, select one using `--browser <instance-id-or-name>` when starting the session.

```sh
bsk navigate https://example.com --session <id>
bsk observe --session <id>
bsk screenshot --session <id> --out example.png
bsk session stop <id>
```

Use `bsk --help` or `bsk <command> --help` for command options. Always stop your session when finished, including after a failed task; borrowed tabs are returned to their original window.

</details>

If your agent sandbox removes background processes after each command, use the [sandbox setup guide](docs/sandboxed-agents.md). It explains how to keep the daemon in a persistent host environment and connect with shared `BSK_HOME` and `BSK_AUTO_START=0`.

## DeepSeek Harness plugin

The [DSH plugin](packages/dsh-plugin-browserskill/README.md) adds native `browser_*` tools, browser task previews, and screenshot results to the DeepSeek Harness Web UI. It uses the same `bsk` CLI and extension and includes its own BrowserSkill skill.

With DeepSeek Harness, pnpm, and `bsk` installed and the extension connected, add the plugin to your profile:

```sh
dsh plugin --profile web add @wxg-prc-cpg/browser-skill-dsh-plugin
dsh --profile web
```

Replace `web` with your profile name. Make sure `bsk` is available on the PATH used to start DSH, or set the plugin's `bskPath`. In a conversation, invoke `/browser-skill` and describe the task. A separate `bsk install-skill` step is not needed.

[Plugin usage and configuration](packages/dsh-plugin-browserskill/README.md) · [npm package](https://www.npmjs.com/package/@wxg-prc-cpg/browser-skill-dsh-plugin)

## Website debugging

**Give your agent the browser evidence behind a bug.** Start capture before reprod