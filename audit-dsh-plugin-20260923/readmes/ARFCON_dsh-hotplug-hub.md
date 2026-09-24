> 面向 AI 编程协作者：开始任何工作前，请先阅读本目录的 `AI_AGENTS.md`，并遵循其中的同步/检查/上报流程。

<p align="center">
  <img src="https://img.shields.io/badge/version-v1.0.4-6c5ce7" alt="version" />
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-2d3436" alt="platform" />
  <img src="https://img.shields.io/badge/license-MIT-00b894" alt="license" />
  <img src="https://img.shields.io/badge/stack-WebView2%20%2B%20C%23%20WinForms-0984e3" alt="stack" />
</p>

<div align="center">
  <a href="#english">🇬🇧 English</a> · <a href="#简体中文">🇨🇳 简体中文</a>
</div>

---

<a id="english"></a>

# Dseam World — DSH-Hotplug-Hub

**DSH-Hotplug-Hub** is the plugin manager for **Dseam World** — a Windows desktop application (WebView2 + C# WinForms) that manages DSH plugins, Skills, and MCP servers, with global memory. It works **alongside** DSH Desktop, without touching the DSH Desktop installation directory, by installing everything into the unified official profile at `~/.dsh/profiles/web`.

## About

A hot-plug package manager for [DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness). It introduces the concept of a **hotpack** — a versioned, portable bundle of plugins that can be imported, activated, deactivated, or removed without modifying the host. Built on the same mechanism as [dsh-hub](https://github.com/ARFCON/dsh-hub-DSH): `typert` Remote API + web page + atomic profile writes + `link` assembly.

## Current Version

| | |
|---|---|
| **Release** | **v1.0.4** |
| Releases page | <https://github.com/ARFCON/dsh-hotplug-hub/releases/tag/v1.0.4> |
| Windows installer | `DSH-Hotplug-Hub-win-x64-setup-v1.0.4.exe` |
| Windows portable | `DSH-Hotplug-Hub-win-x64-portable-v1.0.4.zip` |
| Linux installer | `DSH-Hotplug-Hub-linux-x64-setup-v1.0.4.sh` |
| Linux portable | `DSH-Hotplug-Hub-linux-x64-portable-v1.0.4.tar.gz` |
| macOS installer | `DSH-Hotplug-Hub-macos-x64-setup-v1.0.4.command` |
| macOS portable | `DSH-Hotplug-Hub-macos-x64-portable-v1.0.4.zip` |

## Key Features

- **Plugin management** — install / disable / uninstall plugins and plugin bundles.
- **Skill management** — scan a fixed source directory (default `%APPDATA%\reasonix\skills`, overridable via `DSH_SKILL_SOURCE_DIR`) for all `SKILL.md` files, then install / disable with a single click. Backed by the `dseam-skillmcp` CLI.
- **MCP management** — add / remove / disable `STDIO` and `streamable-http` MCP servers, written uniformly into the `dseam-skillmcp` manager module.
- **Global memory** — view / edit / delete entries per project via the built-in memory feature. When the AI needs key information (preferences / rules / constraints / notes / memories / project goals), it triggers the memory prompt and never lets the AI edit or delete memories on its own.
- **Bundled Skill/MCP manager** — `dseam-skillmcp` (derived from `dsh-skill-mcp-panel`, MIT), shipped with installer / EXE, auto-installed into the profile; no separate download needed.
- **Version consistency** — `dseam-skillmcp` and `dsh-hub` are embedded in the installer / portable app and updated atomically with each release; no repeated downloads.
- **Tray resident** — close to system tray; background processes keep running; double-clicking the icon reopens the existing window.
- **Self-check & self-heal** — on startup, auto-checks Node / pnpm / profile / plugins / config; auto-installs or repairs the environment if needed.

## The 5 Tabs

| Tab | Description |
|---|---|
| **Plugin management** | Import hotpack JSON (paste or pick a file), preview, download, activate / deactivate / remove, show store state. |
| **Plugin market** | Real GitHub market by topic tags; one-click install of entries. |
| **AI assembler** | Conversational assembly (persona switch + natural language) driven by real LLMs (DeepSeek / OpenCode / OpenRouter / Sensetime / Moonshot / Zhipu / MiniMax, OpenAI-compatible endpoints); validates hotpack manifest + README, writes a hotpack JSON in one click. |
| **Global memory** | Show the `~/.dsh/memory` global-memory directory path and store entry count. |
| **Self-check** | Run `check()` remote service; show Node/pnpm versions, profile state, patch state, plugin conflicts, pack/store state. |

## Installation

### Option 1 — Installer (recommended)

1. Download `DSH-Hotplug-Hub-win-x64-setup-v1.0.4.exe` from the Releases page.
2. Double-click and choose an install location (default `%LOCALAPPDATA%\Programs\DseamWorld`).
3. The installer auto-creates desktop / start-menu shortcuts and launches when finished.

Silent install:

```powershell
DSH-Hotplug-Hub-win-x64-setup-v1.0.4.exe --silent
DSH-Hotplug-Hub-win-x64-setup-v1.0.4.exe --silent --dir "D:\MyApps\DseamWorld"
```

### Option 2 — Portable

- **Windows**: unzip `DSH-Hotplug-Hub-win-x64-portable-v1.0.4.zip`, then double-click `DSH-Hotplug-Hub.exe` (WebView2 runtime DLLs are included in the same directory).
- **Linux**: `tar -xzf DSH-Hotplug-Hub-linux-x64-portable-v1.0.4.tar.gz`, then run `./dsh-hotplug-hub`.
- **macOS**: unzip `DSH-Hotplug-Hub-macos-x64-portable-v1.0.4.zip`, then double-click `Start-DSH-Hotplug-Hub.command`.

### Option 3 — From source

Requires Node.js 18+ (LTS recommended), pnpm, and the `dsh` CLI.

```bash
./install.sh          # auto-detect desktop / web / headless profile
./install.sh web      # target a specific profile
```

## hotpack Format

```json
{
  "hotpack": "1.0",
  "id": "pack.research",
  "name": "Research hotpack",
  "version": "1.0.0",
  "description": "Literature + mind-map + note sync",
  "tags": ["research", "study"],
  "plugins": [
    { "id": "literature", "name": "@dsh-community/dsh-tool-literature", "version": "1.2.3", "source": { "type": "npm" } },
    { "id": "mine", "name": "my-plugin", "source": { "type": "path", "path": "~/dev/my-plugin" } },
    { "id": "team", "name": "team-tool", "source": { "type": "github", "repo": "owner/team-tool", "ref": "v1.0.0" } }
  ]
}
```

Supported sources:

- `npm` — exact version required; `pnpm add --save-exact` into the profile, shared pnpm global store.
- `path` — link a local directory directly (same as `graph-memory`); supports `~` and `$DSH_HOME` expansion.
- `github` — zip → `~/.dsh/hotplug-store/<name>@<ref>` → link; official codeload first, then `ghfast.top` / `gh-proxy` / `ghproxy` mirrors.

## Directory Structure

```text
dsh-hotplug-hub-test/              # repo root
├── packages/shared-core/          # shared core: contracts / types / shared logic
├── release/                       # build EXE, installer, WebView2 DLLs, embedded C# contracts
├── scripts/                       # team scripts: sync / check / test / install
├── launcher/                      # Node CLI: assemble / check / launch / heal / status
├── dsh-hotplug-hub/               # hotplug-hub plugin + dsh-pack-hub
├── vendor/dseam-skillmcp/         # Skill/MCP manager source (MIT)
├── installer/                     # historical installer factories
├── uninstaller/                   # uninstaller factories
├── assembly/                      # assembly packs (hotpack 1.0, dshpack single-entry)
├── sandbox/                       # temporary profile sandboxes
├── 开发文档/                       # team docs & conventions
├── README.md                      # this file
└── LICENSE                        # MIT License
```

## Development

```powershell
# Before editing — sync the repo
pwsh -File scripts/sync-repo.ps1

# Before committing — full checks
pwsh -File scripts/check-before-upload.ps1

# After each change — record to global memory
pwsh -File scripts/remember-doc.ps1 -DocPath README.md
```

Team conventions live in `AI_AGENTS.md` and `开发文档/团队/`.

## Changelog

Full change history: [`开发文档/开发历史.md`](开发文档/开发历史.md)

## License

[MIT](LICENSE)

---

<a id="简体中文"></a>

# Dseam 世界（DSH-Hotplug-Hub）

**DSH-Hotplug-Hub** 是 **Dseam 世界** 的插件管理器——一款 Windows 桌面应用（WebView2 + C# WinForms），用于管理 DSH 的插件、Skill 与 MCP 服务器，并提供全局记忆。它与 DSH Desktop **并存运行**，不改动 DSH Desktop 安装目录，而是把所有内容统一安装到官方 profile `~/.dsh/profiles/web`，随 DSH 