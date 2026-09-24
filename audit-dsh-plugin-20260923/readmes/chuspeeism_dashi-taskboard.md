[English](README.md) | [简体中文](README.zh-CN.md)

# Codex Taskboard

A local-first issue board that runs in a browser and can be embedded in Codex through the standalone CDP launcher or its injection script. The same HTTP API powers the React UI and the `taskctl` CLI used by the bundled Codex Skill.

![Codex Taskboard product screenshot](docs/assets/codex-taskboard.png)

## Requirements

- Node.js 22.5 or newer
- macOS App and DMG builds: Xcode Command Line Tools and Rust 1.88 or newer with the `aarch64-apple-darwin` and `x86_64-apple-darwin` targets. `npm install` installs the Tauri CLI used by this project.
- Windows NSIS builds: the Microsoft Store Codex App, Rust 1.88 or newer, and Visual Studio Build Tools with the C++ workload and Windows SDK.

## Run locally

```bash
npm install
npm run build
npm start
```

Open <http://127.0.0.1:47823>. The SQLite database is stored at `.data/taskboard.sqlite`.

For development with live frontend reload:

```bash
npm run dev
```

The Vite UI runs at <http://127.0.0.1:5173> and proxies API requests to the local service.

## Use the CLI

Run it from the project:

```bash
npm run taskctl -- project create \
  --id my-project \
  --name "My project" \
  --workspace-path /absolute/path/to/repository

npm run taskctl -- issue create \
  --project my-project \
  --title "Implement the next slice" \
  --status todo \
  --priority high \
  --labels product,mvp
```

Use `npm link` if you want `taskctl` on your shell path. Set `CODEX_TASKBOARD_URL` to point the CLI at another local or LAN service. Cloud deployments are configured through the **loopback companion** (device-local loopback service for auth and path mapping—not a chat persona) with `taskctl cloud login`.

## Install the Codex Skill

Copy or symlink `skills/manage-taskboard` into the Codex skills directory, then start a new Codex task:

```bash
ln -s /absolute/path/to/codex-taskboard/skills/manage-taskboard \
  ~/.agents/skills/manage-taskboard
```

The desktop app keeps this same directory synchronized with its bundled Skill. The Skill teaches Codex to inspect an issue, move it to `in_progress`, use optimistic versions, verify the work, and then move it to `in_review`; it moves the issue to `done` only after the user explicitly confirms acceptance or asks to mark it complete.

## Embed in Codex

### Manual: use a dedicated CDP port

Keep the existing Codex window open. From the Taskboard repository, start a second Codex instance with a dedicated CDP port:

```bash
open -n -a /Applications/ChatGPT.app --args \
  --remote-debugging-port=9231 \
  --remote-allow-origins=http://127.0.0.1:9231
```

After the new Codex window appears, run the injector in another terminal:

```bash
CODEX_TASKBOARD_HOST=127.0.0.1 \
npm run codex:inject -- --port 9231 --open
```

Keep the injector terminal running while using the embedded panel. The original Codex window remains unchanged, and the new window receives the Taskboard sidebar entry. If port `9231` is occupied, use another port in both commands.

### Recommended: launch an independent Taskboard window with one command

Keep existing Codex windows open and run:

```bash
CODEX_TASKBOARD_HOST=127.0.0.1 npm run codex
```

This starts the local Taskboard service when needed. It reuses an open Codex with a reachable CDP renderer, opens Taskboard in the native browser panel of an ordinary Codex without CDP, or launches the official macOS Codex app with an independent profile and loopback-only port `9231` when no Codex is open. It injects a native-looking Taskboard entry after Plugins when CDP is available and keeps watching both the service and replacement renderers. Keep this command running while using the embedded panel. The launcher does not modify `ChatGPT.app` or its `app.asar`.

The source launcher writes its authenticated endpoint to `.data/launcher-runtime.json`. A `taskctl` command installed with `npm link` reads this file by default, so a normal shell and a Codex task opened from the panel use the same Taskboard service without an extra environment variable.

### macOS App: open and inject without a terminal

For Tauri development, run:

```bash
npm run app:dev
```

To build the local App and DMG, install the two Rust targets once, then run the build:

```bash
rustup target add aarch64-apple-darwin x86_64-apple-darwin
npm run app:build
```

Open `src-tauri/target/universal-apple-darwin/release/bundle/macos/Codex Taskboard.app` from Finder. The DMG is in `src-tauri/target/universal-apple-darwin/release/bundle/dmg/`. If you only want the stable App, download the current DMG from [GitHub Releases](https://github.com/chuspeeism/dashi-taskboard/releases/latest).

The App contains its own Node runtime, Taskboard service, built web UI, Skill, CLI wrapper, and injection script. It starts the service, reuses an open Codex with a reachable CDP renderer, opens Taskboard in the native browser panel of an ordinary Codex without CDP, or launches the official Codex app when no Codex is open. It waits for the renderer, injects the sidebar entry when CDP is available, and opens the panel without showing a terminal window. The App can be copied away from this checkout; the target Mac only needs the official Codex app and does not need this repository, a system Node installation, or a separate Codex CLI installation. Taskboard data is stored in `~/Library/Application Support/Codex Taskboard`, and launcher output is written to `~/Library/Logs/Codex Taskboard/codex-taskboard-launcher.log`.

### Linux App: Ubuntu 24.04 x64 packages

The first Linux desktop release supports Ubuntu 24.04 LTS on x64 only. Install the official ChatGPT desktop `.deb` first and confirm that `chatgpt` opens it. Then download either the Codex Taskboard `.deb` or `.AppImage` from [GitHub Releases](https://github.com/chuspeeism/dashi-taskboard/releases/latest). Replace `<file>` below with the downloaded filename.

Install the `.deb` package:

```bash
sudo apt install ./<file>.deb
```

Or run the AppImage:

```bash
chmod +x ./<file>.AppImage
./<file>.AppImage
```

To build both packages on Ubuntu 24.04 x64, run:

```bash
npm ci
npm run app:build:linux:x64
```

This first release does not support ARM64, Fedora, RPM packages, or other Linux distributions.

### Windows code signing

For official Windows releases after the application is approved: **Free code signing provided by [SignPath.io](https://signpath.io/), certificate by [SignPath Foundation](https://signpath.org/).** Current Windows CI artifacts remain unsigned until that approval. See the [Code signing policy](docs/code-signing-policy.md), [Privacy policy](PRIVACY.md), and [Windows uninstall instructions](docs/windows-uninstall.md).

The local build uses ad-hoc code signing for direct verification. A public macOS download still needs Developer ID signing and Apple notarization.

### Windows App: tray launcher and bundled Taskboard

Install the official Codex App from the Microsoft Store. To build the current-user NSIS installer on Windows x64, run:

```powershell
npm ci
npm run app:build:windows
```

The installer is written to `src-tauri/target/x86_64-pc-windows-msvc/release/bundle/nsis/`. It installs a tray launcher, bundled Node runtime, local service, built web UI, Skill, `taskctl.cmd`, and injection script. Taskboard data is stored in `%APPDATA%\Codex Taskboard`; logs are stored in `%LOCALAPPDATA%\Codex Taskboard\Logs`; the Skill is copied to `%USERPROFILE%\.agents\skills\manage-taskboard`.

Windows CI artifacts are intentionally unsigned and do not auto-update. Review [the code-signing policy](docs/code-signing-policy.md) before distributing a build. See [Windows uninstall](docs/windows-uninstall.md) for retained-data behavior.

Codex 26.715.52143 ships a renderer CSP that blocks arbitrary HTTP iframes. The launcher therefore enables CDP CSP bypass, reloads that renderer once, installs the document-start script, and waits until the Taskboard OOPIF is actually loaded. CDP is unauthenticated to other proce