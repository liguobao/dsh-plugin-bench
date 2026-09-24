# Lark Agent Bridge

<sub>npm package: `@bihangchi9/lark-agent-bridge` · git repo: `lark-agent-bridge`</sub>

> A Feishu / Lark bridge for local coding agents — *one group, one conversation, one pinned runtime*. Bridges **dsh** (in-process plugin), **CLI** agents (`traex` / `codex`, spawned by a daemon), an **IDE** window (attached over a socket), or a **custom** agent — behind one gateway.

[中文 README](./README.zh.md)

Send a message in a Feishu chat, and a real coding agent — with its own tools, its own project directory, and its own persistent conversation — answers you right there. Each group chat is an isolated workspace pinned to exactly one runtime, so a team can run several projects (and several agents) in parallel, one per group.

---

## What it does

- **Feishu ⇄ your agent.** Inbound Feishu messages drive a live agent; the reply streams back onto a live-updating Feishu message. The agent is whichever runtime this chat is pinned to (dsh / CLI / IDE / custom).
- **Four host classes, one contract.** Every runtime implements the same `AgentAdapter`: dsh runs in-process as a plugin; CLI **spawns** `traex`/`codex`; IDE **attaches** a running window; custom loads your own module. They never silently replace each other.
- **One group, one conversation, one pinned runtime.** Every chat id maps to a stable directory (`<workspaceRoot>/<chatId>`) and one runtime chosen with `/agent`. Different groups never touch each other's files, and a message is never broadcast to several agents. If the pinned runtime is down (e.g. an IDE window closed), that chat fails closed instead of retargeting.
- **Persistent per-chat sessions.** A chat's conversation survives restarts (policy-fingerprint-gated resume-or-create; `/new` really clears it).
- **Files and images.** Send them to the bot and the bridge stores each message in an isolated `.attachments/<messageId>/` folder, then gives the paths to the agent. Limits: 5 attachments per message, images ≤10 MB, other files ≤20 MB; names are sanitized and stale files are swept after 7 days. Whether an image can actually be interpreted depends on the selected model's vision support.
- **Zero-config setup.** On first launch, if no credentials exist, a QR registration wizard runs — scan it in the Feishu app and it connects automatically. No portal spelunking.
- **Slash commands.** `/help`, `/new`, `/where`, `/models`, `/agent`, and `/whoami` manage each chat locally; owner-only `/agent`, `/model`, `/preset`, `/allow`, and `/disallow` change shared chat state. `/agent` pins this chat to one installed runtime and never silently retargets.

## Architecture in one picture

```
①  Feishu Open Platform      ← register a bot here (auto QR wizard does it for you)
        │  gives: app_id + app_secret
        ▼
②  lark-agent-bridge gateway  ← holds the keys, opens a WebSocket to Feishu,
        │                        turns each message into one agent turn,
        │                        routes each chat to its pinned runtime
        ▼
③  the pinned runtime         ← one of:
     • dsh    — in-process Cordis plugin (`dsh web`)
     • CLI    — daemon spawns traex / codex
     • IDE    — daemon attaches a running window over a socket
     • custom — daemon loads your own AgentAdapter module
```

The bot **registration lives entirely on Feishu**. The gateway connects out to Feishu over a long-lived WebSocket (so no public IP or callback URL is needed). For **dsh** the gateway *is* the plugin loaded by `dsh web`; for **CLI / IDE / custom** it is a **separate daemon** (`node lib/daemon.js`), independent of any dsh host.

```bash
pnpm build
node lib/daemon.js                            # spawn traex/codex on PATH
LARK_BRIDGE_RUNTIME=traex node lib/daemon.js
LARK_BRIDGE_IDE_SOCKET=/tmp/ide.sock node lib/daemon.js
LARK_BRIDGE_CUSTOM_ADAPTER=./examples/custom-adapter.mjs node lib/daemon.js
```

CLI **spawns** the binary. IDE **attaches** a Unix-socket JSONL sidecar owned by the current user and not writable by group/others (`chmod 600 /path/to.sock`; window closed ⇒ that line dies). Custom loads an `AgentAdapter` module (see `examples/custom-adapter.mjs`). One group is still one conversation pinned with `/agent`; a dead line is not retargeted.

ByteDance-only overlay (SSO, bytecli, extra presets) lives in a local `internal/` directory that is gitignored. Do not publish it to this GitHub repo; ship it through the internal skill marketplace.

---

## Requirements

- A working **DeepSeek Harness (dsh)** checkout you can launch with `dsh web`.
- **Node.js** `^22.19.0 || >=24.0.0`.
- A **DeepSeek API key** (set `DEEPSEEK_API_KEY`, or configure it in your dsh credentials).
- A **Feishu account** to scan the QR code (the wizard creates the app for you).

## Install

### Option 1: npm package (recommended for users)

The released package contains compiled JavaScript, both access-tier presets,
the bundled `dsh-tool-lark-cli` package, and the setup scripts. Install it in
a **stable directory** — dsh links to that location when registering the
bundle.

```bash
# macOS / Linux
mkdir -p ~/lark-agent-bridge && cd ~/lark-agent-bridge
npm init -y
npm install @bihangchi9/lark-agent-bridge
bash node_modules/@bihangchi9/lark-agent-bridge/scripts/setup.sh
```

```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$HOME\lark-agent-bridge" | Out-Null
cd "$HOME\lark-agent-bridge"
npm init -y
npm install "@bihangchi9/lark-agent-bridge"
powershell -ExecutionPolicy Bypass -File node_modules\@bihangchi9\lark-agent-bridge\scripts\setup.ps1
```

The script preflights Node, installs the `lark-workspace` / `lark-readonly`
presets, and registers both the bridge bundle and its `dsh-tool-lark-cli`
dependency. When `dsh` is available it uses the official `dsh plugin` command,
which **initializes a missing `web` or `headless` profile automatically**.
After setup, launch dsh with **no `--patch` flag**:

```bash
# macOS / Linux
DSH_PERMISSION_MODE=danger-full-access dsh web

# Windows PowerShell
$env:DSH_PERMISSION_MODE = "danger-full-access"; dsh web
```

Different profile / dsh home:

```bash
DSH_PROFILE=headless DSH_HOME=/path/.dsh bash node_modules/@bihangchi9/lark-agent-bridge/scripts/setup.sh
```

For the standalone CLI daemon only, a dsh profile is not required:

```bash
npx -p @bihangchi9/lark-agent-bridge lark-agent-register
npx -p @bihangchi9/lark-agent-bridge lark-agent-bridge
```

### Option 2: source checkout one-command setup (contributors)

> **Build first.** Git contains TypeScript source, while compiled `lib/` is
> git-ignored. A fresh source checkout therefore has no build output; the
> plugin entry is `lib/index.js`, so registering it without building gives dsh
> an empty package and **the host fails to load it**. `pnpm setup` builds for
> you.

```bash
git clone https://github.com/bihangchi9-creator/lark-agent-bridge.git
cd lark-agent-bridge
pnpm setup            # macOS / Linux (scripts/setup.sh) — builds, links, registers
pnpm setup:win        # Windows (scripts/setup.ps1)
```

The script preflights your Node version, **builds the plugin (fails loudly if
the build fails)**, installs the access-tier presets, and registers both the
bridge and its `dsh-tool-lark-cli` dependency. When `dsh` is available it uses
the official `dsh plugin` command, which **initializes a missing `web` or
`headless` profile automatically** — no preliminary `dsh web` launch is
needed. After that, launch dsh directly with **no `--patch` flag**:

```bash
# macOS / Linux
DSH_PERMISSION_MODE=danger-full-access dsh web

# Windows PowerShell
$env:DSH_PERMISSION_MODE = "danger-full-access"; dsh web
```

> Different profile: `DSH_PROFILE=headless pnpm setup`; custom dsh home:
> `DSH_HOME=/path/.dsh pnpm setup` (both env vars work on Windows too). If no
> `dsh` command is available, setup can only use its manual fallback and
> therefore requires an already-initialized profile; it fails before building
> or copying presets, so it leaves no partial installation.

##