# DSH Box

**English** · [简体中文](README.zh-CN.md)

**Managed DeepSeek Harness desktop runtime** — run, isolate, and extend multiple DeepSeek Harness environments on your own machine, no browser tab required.

DSH Box is a lightweight desktop shell built with [Tauri 2](https://tauri.app) that installs, launches, and manages independent DSH **Containers** — each with its own DSH version, profile, plugins, skills, workspace, and logs — and renders them in an embedded WebView.

![The Container view: each container has its own DSH version, profile and host process, with start, open and rebuild controls](docs/images/containers.png)

## Highlights

- **Isolated containers** — one DSH version, profile, workspace and host process each.
- **Embedded WebView** — the DSH UI opens in a native window; no ports, no URLs to paste.
- **Ready in seconds** — a pulled Harness version arrives with its client artifacts built; `run` is a copy (~10s).
- **Plugin dependency graph** — what loads, in what order, why: depth bands, halves apart, fold a depth away.
- **Resources: extract, inject, edit** — conversations, keys and plugin state as named copies; any YAML block editable by key path.
- **An agent surface** — `dshbox apply -f` configures resources from one document; every verb answers `--json`.
- **Zero-dependency install** — bundled Node, npm, pnpm and Git (Windows), in a clean room.
- **Version manager** — install any Harness tag and pin a version per container.
- **Boxfiles** — `FROM` + `ADD` describes a template; build once, run many.
- **Portable templates** — every payload is materialised into the template, so containers depend on nothing mutable.
- **Bundles** — group plugins and skills, then export quick (URLs kept) or full (one archive).
- **Tasks you can watch** — queued, logged with timings, cancellable, with history.
- **A slow daemon never freezes the window** — commands run off the main thread and every RPC is bounded.
- **RPC + events** — one `POST /rpc` and one SSE stream serve the UI, the CLI and agents alike.
- **Network-friendly** — GitHub mirror, npm registry mirror, automatic proxy detection.
- **Tray and background service** — `dshboxd` keeps working with the window closed.
- **Lightweight** — Tauri, not Electron.
- **Bilingual UI** — English and 简体中文.

![The plugin list: one row per installed plugin, with kind, storage, cache state, auto-indexed mark, and the templates and containers it came from](docs/images/resources-plugins.png)

---

## Install

Download the installer for your platform from the **Releases** page of this repository:

| Platform | Artifact | Notes |
|---|---|---|
| Windows (x64) | `dshbox_<version>_x64_<locale>.msi` | MSI installer with bundled runtime and sidecar |
| Linux (x64) | `dshbox-<version>-amd64.deb` | Debian/Ubuntu package |
| macOS (arm64) | `dshbox-<version>-arm64.dmg` | Apple Silicon |

> Grab the latest version from the [Releases page](https://github.com/Nexus-Aethra/DSHBox/releases) — artifact names follow the `<product>-<version>-<arch>` convention. Every tagged release carries all three platforms, built by the [release workflow](.github/workflows/release.yml).

No runtime prerequisites on Windows — the bundled Node/npm/pnpm/Git runtime travels inside the installer. Linux needs a system Git (`apt install git` or your distro equivalent); its configuration is isolated per-runtime-directory, so your host `~/.gitconfig` is never read by DSH Box builds.

---

## Quick start

1. **Launch DSH Box** and pick a writable *runtime directory* when prompted (all DSH data lives there).
2. Open **Resources** → **DSH Versions** → **Load versions**, then install the DSH tag you want.
3. Open **Resources** → **Templates**, then pull an official DSH template or build a reusable template from a Boxfile.
4. Open **Container** → create a Container from that template (name and profile).
5. The first create prepares the Container in its final directory (offline dependency install, local plugins, frontend build). Press **Start** — DSH Box launches that prepared copy and opens the DSH UI in the embedded WebView.
6. Use **Resources** to import plugins/skills, assemble bundles, or create Boxfiles for reusable plugin-enabled templates.

### Tray

The app minimizes to the system tray on close. Use the tray menu to open the window or start/stop/restart the `dshboxd` background service.

---

## Architecture

DSH Box separates a Tauri **desktop shell**, a framework-free Rust workspace, a background **daemon** (`dshboxd`), and a small React frontend. The split exists so all business logic — plugin fetching, container lifecycle, template resolution, background tasks — is testable without a UI, and so a CLI or external agent can drive the same flows the UI does.

![DSH Box architecture: the React UI talks to the Tauri shell over IPC, the shell and the CLI both drive the dshboxd daemon over loopback RPC, and the daemon supervises one DSH host per container from the bundled runtime](docs/images/architecture.svg)

### Layered components

| Layer | What lives here | Why |
|---|---|---|
| Frontend (React 18 + Vite, `src/`) | Pages, components, `useTaskQueue`/`useContainers`/`useResources`/`useSettings` hooks. **No business logic** — pages fire RPC requests and react to daemon SSE events. | Keeps the Box UI thin and lets any client (UI/CLI/agent) share the same code path. |
| Desktop shell (Tauri 2, `src-tauri/src/`) | Browser window, tray, Tauri IPC adapters. Listens on `127.0.0.1` to the daemon's loopback HTTP server. All real work is delegated to `dshboxd` over HTTP RPC. | One source of truth for state changes — UI and CLI cannot drift. |
| Daemon (`src-tauri/crates/dshboxd`) | Long-lived background service. Owns the queue, the data store, the template index, container registry, and the SSE event bus. Single HTTP entry point (`POST /rpc`) plus `GET /events?token=…`. | Background work (installs, rebuilds, uninstalls) survives the desktop window closing. |
| Crate workspace (`src-tauri/crates/`) | Framework-free Rust crates: `box-foundation`, `box-runtime`, `box-scheduler`, `box-state`, `box-toolchains`, `box-dsh-versions`, `box-containers`, `box-extensions`, `box-image`, `box-template-core`, `box-data-scheduler`, `box-logger`, `box-dsh-context`, `box-server-core`, `box-api`, `box-client`. | Pure functions + unit tests; only the top-level `dshbox` binary and `dshboxd` link Tauri/HTTP. |

The dependency direction is one-way: `foundation / runtime / scheduler / state` → functional crates → Tauri/desktop adapters. Feature crates do not depend on Tauri or one another's mutable state.

### Daemon — dual-mode RPC + SSE event stream

Every UI / CLI action lands on `POST /rpc` with a JSON body of `{"method": "...", "params": {...}, "token": "..."}`. The daemon's dispatch table decides for each handler whether to **synchronously** return JSON (`List templates`, `Read settings`, …) or **asynchronously** enqueue a worker (`Install`, `Build`, `Start container`, `Rebuild`, `Uninstall`, …). Async handlers return a `TaskRecord` immediately; the client subscribes to `GET /events?token=…` for `task_stage` / `task_log` / `task_finished` / `resource_added|updated|removed` events. The daemon threads one connection per request, so a long task never blocks the liveness probe.

This means the same HTTP surface serves every consumer — the desktop app's Tauri IPC handlers, the CLI (`dshbox rpc …`), and external agents calling `curl -d '…' http://127.0.0.1:7923/rpc`. There is no "client fallback" or local-state divergence: the daemon's resource map and task queue are the only sources of truth.

A task's log file is the UI's only window into it: the daemon writes it, the desktop streams the lines into the panel, and a step the user waits minutes for says what it is doing and how long it took.

![The task panel: a container start with its log expanded, one line per step with timings](docs/images/tasks.png)

### Boxfile and the built-template pipeline

A **boxfile** (`.dsh`) is 