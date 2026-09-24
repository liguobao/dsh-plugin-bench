<p align="center">
  <img src="./assets/logo.svg" alt="DeepTide logo" width="200">
</p>

<h1 align="center">DeepTide</h1>

<p align="center">
  <strong>Built by DeepSeek, for DeepSeek.</strong><br>
  An AI coding agent that flows through your codebase like a tide.
  <br><sub>The name: <strong>DeepSeek</strong> + <strong>tide</strong> (terminal IDE).</sub>
</p>

<p align="center">
  <a href="https://github.com/paean-ai/deeptide/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://www.npmjs.com/package/deeptide"><img src="https://img.shields.io/npm/v/deeptide.svg" alt="npm version"></a>
  <a href="https://github.com/paean-ai/deeptide/stargazers"><img src="https://img.shields.io/github/stars/paean-ai/deeptide?style=social" alt="GitHub stars"></a>
</p>

---

## Three flavors, same team

| | DeepTide for macOS | DeepTide CLI (`deeptide`) | DeepTide CLI Rust (`deeptide-rs`) |
|---|---|---|---|
| **Form factor** | Native macOS app | Cross-platform terminal CLI | Cross-platform terminal CLI **+ native desktop GUI** ([`--gui`](#desktop-gui-deeptide-rs)) |
| **Runtime** | Swift 6 native binary, ~15 MB idle | Bun, ~50 MB resident | Native Rust binary, ~10 MB on disk, no runtime |
| **Platforms** | macOS 15+ | Linux · Windows · macOS | Linux · Windows · macOS |
| **Install** | `curl -fsSL https://deeptide.sh/install.sh \| sh` | `bun add -g deeptide` (this package) | `npm install -g deeptide-rs` |
| **CLI name(s)** | DeepTide.app | `deeptide`, `tide` | `deeptide-rs` |
| **Lineage** | 100% authored by DeepSeek V4 | Powered by open-source [Zero CLI](https://github.com/a8e-ai/zero-cli) | Authored under [`crates/`](./crates) in this repo |
| **Best for** | macOS users who want a tuned native experience | Existing users; richest plugin surface | Headless CI, slow laptops, single-binary deploys |

This repository is the **community front door for all three** — docs, FAQ,
issue tracking — and is the home of two npm packages:

- [`deeptide`](./package.json) — the current TypeScript/Bun CLI (forwards to
  [`@paean-ai/zero-cli`](https://www.npmjs.com/package/@paean-ai/zero-cli))
- [`deeptide-rs`](./npm/deeptide-rs) — the Rust CLI (ships a native binary
  via GitHub Releases postinstall)

The two CLI packages **do not conflict** — they expose different binary
names (`deeptide`/`tide` vs `deeptide-rs`) so you can install both and
switch between them freely while we mature the Rust port.

The Rust port lives under [`crates/`](./crates). It is intended to grow
into the canonical cross-platform CLI over time, but the `deeptide` package
will remain available as long as users find value in it — there is no
forced migration.

It also contains the open-source native local inference runtime under
[`native/`](./native): a hard-forked `ds4` DeepSeek V4 Flash Metal engine plus
`dsgo`, the local OpenAI/Anthropic-compatible gateway intended to pair with
DeepTide.

---

## Install on macOS (recommended)

For Mac users, the recommended path is the native Deeptide build from
[deeptide.sh](https://deeptide.sh/). It downloads the signed build for your
Mac architecture and installs both `deeptide` and the shorter `tide` command:

```bash
curl -fsSL https://deeptide.sh/install.sh | sh
```

Then start with:

```bash
tide auth login   # Paean OAuth, multimodal-aware
tide login        # or save a DeepSeek API key directly
tide              # launch the REPL
tide doctor       # diagnose install + network
```

If you want a native Mac terminal to pair with Deeptide, also try
[Clide](https://clide.app/) — a modern macOS terminal with file explorer,
multi-pane layouts, drag-and-drop, and native voice input.

## Install on Linux / Windows (Zero CLI alias)

> **Prerequisite:** [Bun](https://bun.com/) must be installed and on
> PATH. The CLI runtime requires it (matches the underlying
> [Zero CLI](https://github.com/a8e-ai/zero-cli)). Bun does not
> replace your Node install — it sits alongside.

On non-Mac systems, this npm package is the cross-platform DeepTide-flavored
entrypoint powered by [Zero CLI](https://github.com/a8e-ai/zero-cli). It
installs the `deeptide` and `tide` aliases for a workflow close to Deeptide,
but it is not the Swift-native macOS build from `deeptide.sh`.

```bash
# bun (recommended, fastest install)
bun add -g deeptide

# npm (works too; bun is still required at runtime)
npm install -g deeptide

# pnpm
pnpm add -g deeptide
```

Two commands are installed; pick whichever your fingers prefer:

```bash
tide                          # interactive REPL (preferred — short)
deeptide                      # same thing, full name
tide -p "explain this repo"   # one-shot mode
tide --help                   # all options
```

You can also install the upstream package directly:

```bash
bun add -g @paean-ai/zero-cli
```

## Build the macOS native app from source

The macOS native build is open source at
[paean-ai/deeptide](https://github.com/paean-ai/deeptide) (Swift). Most users
should install from [deeptide.sh](https://deeptide.sh/), but source builders can
inspect and build from the source tree when they need to modify the native
runtime or local inference components.

---

## Quick start (CLI)

DeepTide CLI talks to the **DeepSeek API** by default (matching the
DeepTide native app), and can also drive any Anthropic-protocol-compatible
endpoint via BYOK — Zhipu GLM, Volcengine, Paean, Qwen, Moonshot,
self-hosted gateways, and so on.

```bash
# Default path — DeepSeek
export DEEPSEEK_API_KEY="sk-..."
tide

# BYOK to another provider
tide --base-url https://open.bigmodel.cn/api/anthropic --api-key <GLM_KEY>

# One-shot, non-interactive
tide -p "Explain the auth middleware"
```

For the full configuration surface (settings.json schema, hooks,
permissions, MCP servers, sub-agents, model aliases) see the upstream
[Zero CLI README](https://github.com/a8e-ai/zero-cli#readme), which is
the authoritative reference.

---

## Desktop GUI (`deeptide-rs`)

The Rust port ships a **native desktop app** — a single Rust binary (egui, no
Electron/webview) that is a thin window over the same engine the CLI uses. It
**fully shares the CLI's configuration, session history, and the entire tool
set** — there is no separate config to maintain:

- **Same config** — reads the identical `~/.config/tide/settings.json` (and
  project `.deeptide/settings.json`); set your provider/model/API key once and
  both the CLI and the GUI pick it up.
- **Same sessions** — conversations save to the same on-disk store, so a chat
  started in the GUI is `deeptide-rs --resume`-able from the terminal, and a CLI
  session shows up in the GUI's sidebar to resume with one click.
- **Same tools** — the full agent tool set (Read/Write/Edit, Bash, Glob/Grep,
  WebFetch, MCP servers, sub-agents, …) is available identically.

What it does: streaming chat with **markdown rendering**, live **reasoning**
("💭 thinking") and **tool-call cards**, **interactive tool approvals** (with a
coloured diff preview for Write/Edit), a **session sidebar** (resume past
chats), a **provider/model picker**, **New chat**, **Stop/interrupt**, and a
**cost/usage bar** (↑/↓ tokens · cache · $).

### Launch

```bash
# Via the CLI launcher (execs the desktop binary, sharing this config/cwd):
deeptide-rs --gui

# …or run the GUI binary directly:
deeptide-gui
```

### Build from source

```bash
# From the repo root (the Rust workspace under crates/):
cargo run -p deeptide-gui            # dev run
cargo build -p deeptide-gui --release # release binary at target/release/deeptide-gui
```

Configure a model the same way as the CLI — e.g. `export DEEPTIDE_API_KEY=…`
(or set it in `settings.json`) before launching. Without a credential the GUI
opens in a safe local-echo mode and shows a "no API key" banner. To point it at
a non-default provider, use the in-app picker or `export DEEPTIDE_PROVIDER=…`
(e.g. `deepseek`, `ollama`, `openai`, `gemini`).

---

## Built-in capabilities

DeepTide is an **agentic*