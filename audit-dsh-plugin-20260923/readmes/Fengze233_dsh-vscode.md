# DSH for VS Code 🐳

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Marketplace](https://img.shields.io/visual-studio-marketplace/v/Fengze233.dsh-vscode-panel?label=Marketplace&color=4D6BFE)](https://marketplace.visualstudio.com/items?itemName=Fengze233.dsh-vscode-panel)
[![GitHub stars](https://img.shields.io/github/stars/Fengze233/dsh-vscode?style=social)](https://github.com/Fengze233/dsh-vscode)
[![DSH Plugin](https://img.shields.io/badge/DSH%20Plugin-dsh--plugin-4D6BFE)](https://github.com/topics/dsh-plugin)
[![VS Code](https://img.shields.io/badge/VS%20Code-%E2%89%A51.91-blue)](https://code.visualstudio.com/)

**English** | [中文](README.zh.md)

Use the [DeepSeek Harness (DSH)](https://github.com/deepseek-ai/deepseek-harness) web UI right inside VS Code: click a sidebar icon to embed DSH, which auto-starts (or reuses) the `dsh web` service — code and AI interface side by side, no more switching between terminal, browser, and IDE.

Works with **DSH 0.1.2 and newer**, including its one-time-token browser authentication (auto sign-in, no manual step) — see [DSH ≥0.1.2 authentication](#-dsh-012-authentication--the-local-relay). Older DSH (≤ 0.1.1, no auth) keeps working unchanged.

## 📸 Screenshot

![DSH for VS Code screenshot](docs/screenshots/overview.png)

## 🎬 Demo video

[![如何在 VSCode 中使用 DeepSeek Harness？用 DSH！！（Bilibili）](docs/screenshots/video-cover.jpg)](https://www.bilibili.com/video/BV1p8bD6dE18)

*59-second demo on Bilibili (Chinese): [BV1p8bD6dE18](https://www.bilibili.com/video/BV1p8bD6dE18)*

---

## ✨ Features

- 🖱️ **One-click open**: a DSH whale icon in both the left Activity Bar and the right Secondary Side Bar — click either to embed the DSH page in that sidebar;
- 🚀 **Automatic service management**: auto-detects the port — reuses an already-running `dsh web`, otherwise starts one silently in the background and loads it once ready;
- 🔄 **Live status sync**: four-state status bar indicator (running green / starting yellow / failed red / stopped gray); click it to toggle the panel;
- 🛟 **Error fallbacks**: port occupied, `dsh` missing, start timeout, crash/disconnect — each has a dedicated page with one-click reconnect; if the configured port is taken by another program, the extension temporarily falls back to the first free port for that session, never a blank screen;
- 🌐 **Bilingual UI**: copy follows the VS Code display language — Chinese for `zh-*`, English otherwise;
- 📋 **Copy/Paste/Context menu, works out of the box**: fixes the macOS webview quirk where `Cmd+C` / `Cmd+V` and the right-click menu silently fail inside the embedded DSH page — the panel ships its own standard edit shortcut simulation and a context menu (Copy/Paste/Cut/Select All/Undo/Redo), while plain-browser usage and every existing feature stay untouched;
- 🧹 **Clean exit**: closing the window stops the auto-started service, no zombie processes; manually started services are never touched;
- 🔒 **Security boundary**: loopback addresses only (127.0.0.1 / localhost / [::1]); no credentials are read.
- 🔐 **DSH 0.1.2 auth-aware**: the extension parses the one-time launch URL from the service log, exchanges it for DSH's signed browser cookie (valid 30 days, survives service restarts) and serves the panel through a local loopback relay that presents that session for the iframe — so the embedded UI keeps working even though DSH's `SameSite=Strict` cookie can never be used inside a cross-site iframe. A session that expires is re-acquired automatically (a self-started service) or after one paste (an externally started service);
- 🔝 **Editor title-bar icon**: a DSH whale button sits in the top-right of the editor tab bar (like Claude Code) — one click opens the right-side DSH panel;
- 🌐 **SSH Remote (opt-in)**: when connected to a remote host, run dsh on the remote and open the panel through a VS Code tunnel (`dsh.remote.enabled`, off by default);
- 🖼️ **Free image upload**: send images even when the active model has no vision — the image is cached in the workspace and dispatched as a file-path reference, letting the model inspect it with an image tool (files are cleaned up when the panel closes; opt-out via `dsh.image.fallback`);
- 🪟 **No surprise browser window**: `dsh web` is started with `--no-open` by default (restore with `dsh.openInBrowser`).
- 🧠 **File context integration**: the panel toolbar shows the current file with an *Add* button and an *Auto-follow* toggle — inject the current file into the AI context in one click, or let it follow automatically as you switch files (injected into the most recent session of the current project, auto-created if none);
- 🖱️ **Right-click menus**: "Add to Context / Ask DSH / Send Selection" directly from the editor, the explorer, and the editor title bar;
- 📁 **Workspace adaptation**: switching VS Code workspaces restarts the DSH service with the new project as its working directory and idempotently registers the DSH workspace.

## 📥 Installation

**Option 1: Marketplace (recommended)**

Search for `DSH` (publisher Fengze233) in the VS Code Extensions view, or run:

```bash
code --install-extension Fengze233.dsh-vscode-panel
```

Marketplace page: <https://marketplace.visualstudio.com/items?itemName=Fengze233.dsh-vscode-panel>

**Option 2: .vsix package**

1. Download the latest `dsh-vscode.vsix` from [Releases](https://github.com/Fengze233/dsh-vscode/releases);
2. In VS Code press `Ctrl+Shift+P` → run `Extensions: Install from VSIX...` → select the file;
3. Reload the window (`Developer: Reload Window`).

**Option 3: Build from source**

```bash
git clone https://github.com/Fengze233/dsh-vscode.git
cd dsh-vscode
npm install
npm run package        # produces dsh-vscode.vsix, then install as in Option 2
```

**Prerequisite**: the `dsh` CLI from [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) must be installed and on your PATH (the extension detects it and shows a hint if missing).

## 🚀 Usage

1. After installation, a DSH whale icon appears in both the left Activity Bar and the right Secondary Side Bar;
2. Click either icon: the extension auto-starts (or reuses) `dsh web` and embeds the DSH page in that sidebar;
   - Click the **right** icon → the panel opens on the right, leaving the file explorer untouched;
   - If `dsh.port` is occupied by another program, the extension automatically switches to the first free port for this session only (your setting is unchanged; a notification tells you the temporary port);
3. Panel title bar buttons: `Open in Browser` `Restart Service` `Stop Service` `Copy URL` `Show Logs`;
4. The bottom status bar shows the service status; click it to toggle the panel.

### Command palette (prefixed `DSH:`)

| Command | Description |
|---|---|
| `DSH: Open Panel` | Open the left panel |
| `DSH: Open in Secondary Side Bar` | Open the right panel |
| `DSH: Open in Browser` | Open the DSH page in the system browser |
| `DSH: Restart Service` | Restart the extension-managed service |
| `DSH: Stop Service` | Stop the extension-started service |
| `DSH: Copy URL` | Copy the DSH page URL |
| `DSH: Show Logs` | Open the extension log output channel |
| `DSH: Copy Logs` | Copy the full DSH log (environment info + service log) to the clipboard for bug reports |
| `DSH: Retry Bridge Install` | Reinstall the bridge and restart the service |
| `DSH: Uninstall Bridge` | Remove the bridge package and restore `cordis.patch.yml` |

## 🔐 DSH ≥0.1.2 authentication & the local relay

DSH 0.1.2 introduced mandatory browser authentication. On startup `dsh web` prints a one-time launch URL:

```
dsh web: http://127.0.0.1:3080/?token=<one-time token>
```

Visiting it returns `303` plus a signed session cookie (`HttpOnly; SameSite=Strict`, bound to the request `Host`, 30-day lifetime). Every page and every `/api` call then requires that cookie; without it DSH answers `401 dsh web authentication required`.

**Why a relay is needed.** The panel is 