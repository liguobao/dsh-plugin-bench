# dsh-enhanced-plugins

[中文](README.zh.md) | English

An enhancement suite for [DeepSeek Harness (DSH)](https://github.com/deepseek-ai/deepseek-harness): **six independently installable Cordis bundles plus one Windows companion**.

- Does not modify DSH core; every Web feature uses public plugin extension points.
- Installs everything in one pass or keeps only the independently packaged features you select.
- Keeps Host, Web Client, and Windows Companion lifecycles and security boundaries separate.

[Features](#features) · [Quick start](#quick-start) · [Feature guide](#feature-guide) · [Compatibility and migration](#compatibility-and-migration) · [Configuration](#configuration) · [Development](#development-and-verification)

## Features

The installer only needs the stable “feature ID.” Every feature also has a self-contained selective package.

| Feature | Feature ID | Selective package | Platform and entry point | What it adds |
| --- | --- | --- | --- | --- |
| [Windows Launcher](#1-windows-launcher) | `windows-launcher` | `dsh-enhanced-windows-launcher` | Windows Start menu | Tray controls for Web, Headless, profiles, source builds, and diagnostics |
| [Desktop alerts and pet](#2-desktop-alerts-and-pet) | `notification` | `dsh-enhanced-notification` | Windows; Settings → Desktop Pet | Task sounds, a custom WAV library, and a native animated pet |
| [Plugin Community](#3-plugin-community) | `plugin-market` | `dsh-enhanced-plugin-market` | Web; Settings → Plugin Community | Discover community plugins and install through the DSH manager |
| [MCP server manager](#4-mcp-server-manager) | `mcp-server-manager` | `dsh-enhanced-mcp-server-manager` | Web; Sidebar Plugins → bundle → row configuration | Manage stdio / Streamable HTTP servers and import local configuration |
| [Edit last message](#5-edit-last-message) | `edit-last-message` | `dsh-enhanced-edit-last-message` | Web; latest user message | Change that turn and regenerate in the same session |
| [Product subagents](#6-product-subagents) | `sub-agent` | `dsh-enhanced-sub-agent` | Web; Settings → Subagents | Enable or disable Claude Code / Codex tools in real time |
| [Execution monitor](#7-execution-monitor) | `agent-team-monitor` | `dsh-enhanced-agent-team-monitor` | Web; current conversation composer | Dispatch, member progress, callbacks and internal step/tool details |

The historical aggregate package is `dsh-enhanced-plugins`. Launcher-managed installs now express “all” as every independent Profile package plus the required global Launcher, so any one Profile feature can later be removed without changing the others.

## Quick start

### 7.2.4: native plugin installation and system proxy support

- Plugin Community installs directly through the native DSH plugin manager, without its own preflight, installation records, or removal flow. DSH owns build approval and installation outcomes.
- Windows Launcher supplies the system's manual HTTP/HTTPS proxy when no explicit proxy is configured, fixing direct-connection timeouts during index synchronization. Update Launcher and restart DSH to apply this change.
- The aggregate, all six standalone bundles, and Windows Launcher use `7.2.4`, supporting DSH `0.1.6-alpha.2` at the verified baseline `ddefc45fbc7f8e46dd73185e68295696d1297887`.

### 7.2.3: DSH 0.1.6-alpha.2 compatibility

- Fix Launcher-started DSH tool calls failing with `Cannot read properties of undefined (reading 'prepare')`: source checkouts now launch Web, Headless, and profiles through the built `apps/cli/lib/bin.js`, avoiding mixed source/build module identities under `tsx`. Reinstall Launcher and restart Web after updating.

Plugin `7.2.3` was validated against DSH `0.1.6-alpha.2` at source commit `ddefc45fbc7f8e46dd73185e68295696d1297887`. Current supported pairings are maintained in [`dsh-compatibility.json`](dsh-compatibility.json). If the remote table lacks this plugin version or DSH version, the installer checks the bundled table before refusing installation.

The `model-input-types` feature is retired because DSH now provides per-model Text and Image controls under Settings → Models → Custom settings → Model options. An update removes the old standalone bundle while preserving model settings in DSH. MCP configuration remains on the bundle row in sidebar Plugins and discards unsaved drafts when its page closes. Team Monitor follows the main Conversation through `mainView` references and opens members through `uiWorkspace.openSession()`, independently of sidebar-retained children. All six bundles and Windows Launcher share this release. Typecheck rejects DSH artifacts missing the new configuration and session-reference APIs.

This release reduces repeated Launcher layout during navigation, scrolling, and feature filtering, and refreshes button labels when launch mode changes. Each function retains its latest execution log, with bounded reads for the UI.

Choose Browser or Source Desktop at the top of Launcher Overview. The saved choice also controls login startup; existing settings default to Browser. Source Desktop reuses the bound DSH checkout and the Launcher toolchain: Start Desktop runs `pnpm run start:desktop`, while Build and Start runs `pnpm run dev:desktop`. Missing build artifacts disable ordinary startup and direct you to Build and Start. Install the checkout dependencies with `pnpm install --frozen-lockfile` first. Desktop output and failures appear in Desktop Logs; Stop terminates only the Launcher-owned invocation. An active build invocation blocks starting Web against the shared artifacts. The old `DesktopExecutable` setting is ignored; no EXE selection is required.

The official source command regenerates `apps/desktop/.desktop-build/development/project` on each launch. Its data defaults to the sibling `home` directory there, or the inherited `DSH_HOME`; DevTools stay closed unless explicitly enabled with `DSH_DESKTOP_OPEN_DEVTOOLS=1`. This source mode disables the official package-management UI and has no public argument to inherit Web bundles. Launcher therefore does not copy Web plugins into its generated profile. The packaged Desktop application owns its separate `desktop` profile; `dsh plugin --profile desktop` remains unsupported.

Recovered inbox edits retain replacement semantics. Missing or stale edit targets fail explicitly instead of silently appending ordinary input.

### Requirements

- Node.js 22.19.x, or Node.js 24 and later.
- A recent DSH Web profile that runs from source; see the [DSH Web UI quickstart](https://deepseek-harness.github.io/deepseek-harness/guide/quickstart).
- Supported DSH source baseline: [`0.1.6-alpha.2`](https://github.com/deepseek-ai/deepseek-harness/tree/ddefc45fbc7f8e46dd73185e68295696d1297887). Additional validated versions can be listed in [`dsh-compatibility.json`](dsh-compatibility.json) without a plugin code release.
- This DSH version no longer requires `fs-ext` for Session locking. Follow the target checkout’s native build requirements; Launcher uses the system .NET Framework `csc.exe`. Do not skip dependency install scripts.
- Windows Launcher, native sounds, and the desktop pet require a full Windows desktop edition with Windows PowerShell 5.1: Windows 10 version 1607 or later, or Windows 11. The required OS capabilities are the same on Home, Pro, Education / Pro Education, and Enterprise; Windows in S mode, IoT / reduced-footprint editions, and Windows 10 versions 1507 and 1511 are outside this baseline. Windows feature updates outside Microsoft's lifecycle are best-effort because the required Node.js toolchain does not guarantee end-of-life operating systems. The installer does not depend on a particular `tar.exe`. The remaining features are cross-platform.

> [!IMPORTANT]
> DSH remains a developer preview. If a DSH upgrade causes compatibility issues, check the verified version and commit above first.

> [!CAUTION]
> **Check the DSH/plugin repository layout before copying an install command:**
>
> - **Sibling-di