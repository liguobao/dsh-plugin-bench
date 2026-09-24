<p align="center">
  <img src="acryl-logo.png" alt="ACRYL logo" width="128" height="128">
</p>

<h1 align="center">ACRYL - Agent Context Relay Yielding Lifecycles</h1>

<p align="center">
  <strong>One persistent development environment. Universal plugin hot-reload across three surfaces.</strong><br>
  Build, run, and swap coding agents without restarting. Install and reload plugins live.
</p>

<p align="center">
  <a href="https://github.com/acryldev/acryl">⭐ Support ACRYL</a> ·
  <a href="https://acryl.dev/">Website</a> ·
  <a href="https://acryl.dev/docs">Documentation</a> ·
  <a href="https://github.com/acryldev/acryl/releases/tag/v0.2.0">Download v0.2.0</a> ·
  <a href="https://discord.gg/cY9KXMex69">Discord</a> ·
  <a href="https://github.com/acryldev/acryl">GitHub</a>
</p>

<p align="center">
  <a href="https://github.com/acryldev/acryl"><img src="https://img.shields.io/github/stars/acryldev/acryl?style=social" alt="Star ACRYL on GitHub"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2EA44F?style=flat" alt="MIT License"></a>
  <a href="https://discord.gg/cY9KXMex69"><img src="https://img.shields.io/badge/Discord-5865F2?style=flat&amp;logo=discord&amp;logoColor=white" alt="Join Discord"></a>
  <img src="https://img.shields.io/badge/version-0.2.0-28A745?style=flat" alt="Version 0.2.0">
</p>

> [!IMPORTANT]
> ACRYL is in active early development. Interfaces, workflows, and packaging may change while the first public foundation is established.

## What's in v0.2.0

**Universal plugin hot-reload** — Install and reload plugins live across Desktop, Web, and CLI without restarting the app.

**Plugin market** — Browse, install, and manage community plugins through a unified market interface.

**Multi-surface parity** — All three surfaces (Desktop, Web, CLI/TUI) share the same hot-reload and market capabilities.

## Install ACRYL v0.2.0

ACRYL has three product surfaces that share the same project model: the CLI, local Web, and Desktop GUI. They are deliberately separate installs, so installing one does not silently install or start the others. The TUI is the CLI's terminal renderer, not a fourth surface.

### Desktop GUI

The GitHub Release assets below install the **ACRYL Desktop GUI**. The app carries the runtime it needs, but it does **not** add the `acryl` command to your shell PATH or leave a web server running after the app exits.

| Platform | Desktop download |
| --- | --- |
| macOS - Apple Silicon | [DMG](https://github.com/acryldev/acryl/releases/download/v0.2.0/acryl-desktop-mac-arm64.dmg) |
| macOS - Intel | [DMG](https://github.com/acryldev/acryl/releases/download/v0.2.0/acryl-desktop-mac-x64.dmg) |
| Windows - x64 | [Installer](https://github.com/acryldev/acryl/releases/download/v0.2.0/acryl-desktop-win-x64.exe) |
| Linux - x64 / Debian | [DEB](https://github.com/acryldev/acryl/releases/download/v0.2.0/dsh-plugin-desktop_0.2.0_amd64.deb) |
| Linux - arm64 / Debian | [DEB](https://github.com/acryldev/acryl/releases/download/v0.2.0/dsh-plugin-desktop_0.2.0_arm64.deb) |

### CLI terminal

The recommended install is the standalone installer: no Node.js or npm required, no install warnings, and it adds `acryl` to your shell PATH automatically.

```bash
curl -fsSL https://acryl.dev/install | bash
```

This installs the prebuilt `acryl` binary to `~/.acryl/bin`, adds it to your PATH, and verifies the download against the release checksum. Open a new terminal (or run `source ~/.zshrc` / `source ~/.bashrc`) and start it:

```bash
acryl
```

Prefer npm? It works, but npm 11+ prints advisory `install-scripts` warnings for ACRYL's native dependencies (`node-pty`, `koffi`, and others). These are npm security notices, not ACRYL errors; the packages still install and run. To install without the warnings:

```bash
npm install -g acryl --allow-scripts=@deepseek-ai/dsh-subprocess-local,@google/genai,koffi,node-pty,protobufjs
acryl
```

The `acryl` command starts ACRYL's terminal UI. It is separate from the Desktop app so terminal users do not need Electron, and desktop users do not receive an unexpected global executable.

### Nix (Flake)

The project provides a Nix flake that builds the TUI and Desktop from source. Nix with flakes enabled is required.

```bash
# Run the TUI (default output)
nix run github:acryldev/acryl

# Run the Desktop GUI
nix run github:acryldev/acryl#acryl-desktop

# Install to your Nix profile
nix profile install github:acryldev/acryl

# Specific release (the flake builds from source at every git tag)
nix run github:acryldev/acryl/v0.1.36

# Enter a development shell
nix develop github:acryldev/acryl
```

The flake exposes `packages.<system>.acryl` (TUI, from source, also `#default`), `packages.<system>.prebuilt` (prebuilt release binary with bundled Node runtime; available on `x86_64-linux`, `aarch64-linux`, and `aarch64-darwin`), `packages.<system>.acryl-desktop`, and `devShells.<system>.default`.

### Devbox

For a reproducible development environment without managing Nix tooling manually, use [Devbox](https://www.jetify.com/devbox):

```bash
# Install Devbox (if not already installed)
curl -fsSL https://get.jetify.dev/devbox | bash

# Enter the development environment
devbox shell

# Build the project
corepack pnpm build
```

### Local Web surface

Start the browser surface explicitly when you want it:

```bash
acryl web
```

This starts a local ACRYL web runtime, prints its local URL, and serves until you stop the command. It is not a hosted ACRYL cloud service and it does not run in the background by default.

> [!NOTE]
> `acryl gui` is reserved for a future CLI-to-Desktop handoff. For now, launch the installed Desktop app directly.

## What is ACRYL?

ACRYL is an agent-agnostic Agentic Development Environment and continuity layer for software work.

The project does not belong to Claude Code, Codex, OpenCode, Pi, Gemini CLI, DeepSeek, or any other individual agent. ACRYL owns the persistent workspace, project context, tasks, artifacts, and handoffs. Coding agents are replaceable workers that enter and leave the same development scene.

```text
Same project
Same context
Same work
Different agents
```

ACRYL is being designed to support native and external coding agents through capability-based providers, including:

- Claude Code
- Codex
- OpenCode
- Pi
- Gemini CLI
- DeepSeek Harness native agents
- ACP-compatible agents
- PTY and CLI agents
- future agents that do not know ACRYL exists

## Core principles

1. **Agent sessions are disposable. Project context is persistent.**
2. **ACRYL owns continuity. Agents perform work.**
3. **Canonical state is durable and agent-independent.**
4. **Agent-specific context is a projection, not the source of truth.**
5. **Everything practical is a plugin or replaceable capability.**
6. **Generated capabilities live outside the stable kernel.**
7. **Every runtime effect must be reversible.**
8. **Capabilities are versioned, permissioned, testable, and auditable.**

## Built on Cordis

ACRYL is built around [Cordis](https://github.com/cordiverse/cordis), the **Meta-Framework of Spatiotemporal Composability**.

Cordis provides the runtime foundation for:

- lifecycle-managed plugins
- named services and replaceable providers
- reactive dependency injection
- typed events and interception
- reversible effects
- scoped composition and isolation
- configuration-driven application profiles
- hot activation and replacement

This lets ACRYL treat agents, models, memory systems, code graphs, tools, workflows, terminals, and UI surfaces as composable capabilities rather than hardcoded subsystems.

Every one of those capabilities is a Cordis plugin, browsable on the public registry at [cordisplugins.github.io](https://cordisplugins.github.io). Complete, pullable compositions of plugins — Blends — are browsable at [acrylblends.github.io](https://acrylblends.github.io); ACRYL itself is just one Blend, the maxed-out one.

```text
                       ACRYL
                 