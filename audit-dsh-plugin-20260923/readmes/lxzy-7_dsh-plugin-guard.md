# dsh-plugin-guard

> Install safety net for [DeepSeek Harness](https://github.com/deepseek-ai/dsh): pre-install snapshots, one-click / automatic rollback, guarded boot, and incident reports that auto-trigger agent analysis.
>
> DeepSeek Harness 的插件安装安全网：安装前自动快照、一键/自动回退、守护启动、事故报告自动触发 Agent 分析。

---

## English

### What it does

A bad plugin install can leave the app unable to boot, and fixing it by hand usually means digging through config files. This plugin automates the whole chain:

```
Install a plugin (any method)
   │  tools.guard hook: automatic snapshot BEFORE the install (in-process)
   ▼
Guarded boot (boot-guard script)
   │  snapshot before boot → start dsh web → health check
   ├─ healthy ─────────────────────────────► passes through untouched
   └─ unhealthy ─► auto-rollback to last good snapshot → retry once
                   → write an incident report + set a pending marker
                   → the next session's prompt tells the agent to analyze it
                   → after fixing, call `incident_resolved` to clear the marker
```

### How it detects problems (important to understand)

The guard does **not** statically inspect plugin code, and it does **not** try to "test" a plugin in isolation. Detection works at three levels:

1. **Snapshots are pure file copies.** Taking a snapshot just copies 5 config files (`package.json`, `pnpm-lock.yaml`, `pnpm-workspace.yaml`, `cordis.yml`, `cordis.patch.yml`). No plugin is run, no behavior is evaluated.

2. **Boot-level detection does run the harness — with your plugin loaded.** The `boot-guard` script starts the whole `dsh web` process (which loads every installed plugin, including the one you just added) and then health-checks HTTP `/` within a timeout. If a plugin breaks boot — load error, startup crash, unresponsive server — the check fails, and the guard automatically kills the tree, rolls back to the last good snapshot, and retries once. So **yes**: to catch a boot-breaking plugin, the harness (and therefore that plugin) has to actually start. That is the one moment where "running the plugin" is part of detection. Since v0.3.1 the check also confirms the **web client actually rendered** (a plugin crash that black-screens the page with an error leaves HTTP 200 up — the guard's client reports render crashes, and the boot-guard rolls back instead of calling a black screen "healthy"); incident reports additionally record the **dsh version per snapshot** and flag when a boot failure follows a harness update that a profile rollback cannot undo. **Since v0.3.2, when rollback and the retry both fail** (a DSH update made a plugin incompatible), the boot-guard diagnoses the offending plugin from the boot logs, **quarantines it** (appends `disabled: true` to `cordis.patch.yml`), boots without it, and clearly reports which plugin was pulled out and how to restore it (`dsh-guard quarantine --undo <id>`).

3. **Runtime-only problems are not detected at install time.** If a plugin installs and boots fine but only misbehaves later (crashes under a specific operation, corrupts state, etc.), no generic guard can predict that without running your real workload. When such an incident happens, `dsh_rollback action=incident` builds a problem-localization report (last boot logs, server stderr, and a diff of the profile config against the last good snapshot) and sets a pending marker so the next session automatically focuses on diagnosing it. And because a snapshot is always taken before any mutation, you can always roll back manually afterwards.

In short: the guard never *judges* whether a plugin is "good". It guarantees that (a) every mutation is reversible, (b) boot failures roll back automatically, and (c) incidents get analyzed instead of silently breaking your setup.

### Install

```sh
# From GitHub source (current):
dsh plugin --profile web add github:lxzy-7/dsh-plugin-guard

# From the tarball stored in the repo:
dsh plugin --profile web add https://raw.githubusercontent.com/lxzy-7/dsh-plugin-guard/main/dist/dsh-plugin-guard-0.3.2.tgz
```

Restart `dsh web`. This is a standard **bundle plugin**: it joins the profile layer stack and takes effect automatically. (Once published to npm, `dsh plugin --profile web add dsh-plugin-guard` also works.)

**Enable guarded boot (strongly recommended):** launch through `scripts/boot-guard.ps1` (Windows) or `scripts/boot-guard.sh` (macOS/Linux) instead of running `dsh web` directly. Example on Windows, inside your launcher:

```cmd
@echo off
set DSH_HOME=%~dp0.dsh-home
cd /d %~dp0
powershell -NoProfile -ExecutionPolicy Bypass -File node_modules\dsh-plugin-guard\scripts\boot-guard.ps1
```

**Optional CLI shim (covers manual terminal installs):** the package ships a `dsh-guard` bin (`scripts/guard-cli.js`). Put it on your PATH and run `dsh-guard snapshot` before `dsh plugin add <pkg>` from a terminal, or wrap your own `dsh` wrapper with it. This covers installs that do not go through the in-process `tools.guard` hook.

**One-click manual rollback (Windows):** the package also ships `scripts/rollback.cmd`. After install it lives at `$DSH_HOME/profiles/<profile>/node_modules/dsh-plugin-guard/scripts/rollback.cmd` — right-click → *Create shortcut* (or copy the file anywhere) and double-click it to restore the last good snapshot of every profile and re-run `pnpm install --frozen-lockfile`. Rollback also deletes any orphaned bundle-plugin symlinks left in `node_modules` (pnpm never removes a stale `link:` entry — "Already up to date" — so the guard does it directly against the restored `package.json`). It works even when the app cannot start, and it self-derives `DSH_HOME` when the environment does not set it.

### Usage

**Settings panel — 备份管理 (Backup Manager).** In the web UI, open **设置 (Settings) → 备份管理**: per-environment snapshot lists, **load a specific backup**, **create a manual snapshot**, and **set how many snapshots each environment keeps (minimum 2)**. Since v0.3.0 the plugin also registers a **设置 → 插件 → 插件配置** settings card (rc.7 plugin-owned settings surface): it edits the same keep-count through the harness `settings` service (schema-validated, revision-fenced), and the 备份管理 panel plus the CLI stay in sync via `config.json`.

**Agent tools** (registered for every session in the profile):

| Tool | Purpose |
|---|---|
| `dsh_snapshot` | Manually snapshot one profile or all profiles |
| `dsh_rollback` | list / rollback / status / incident (Node-based, cross-platform) |
| `incident_resolved` | Mark a pending incident as resolved after analysis/fix |

**CLI** (`dsh-guard`, usable even when the app will not start):

```
snapshot  [--profile X] [--tag T] [--reason R] [--force]
list      [--profile X]
rollback  [--profile X] [--id I | --good] [--skip-install]
keep      [N]                     # show or set the per-profile cap (min 2)
health    [--port N]
incident  [--kind K] [--no-marker]
resolve
profiles
```

### Configuration

`$DSH_HOME/guard/config.json` (auto-created on first write; all optional):

```json
{
  "keepSnapshots": 10,
  "port": 3080
}
```

- `keepSnapshots` — how many snapshots each profile retains (clamped to 2–100, default 10). Pruning removes older ones.
- `port` — web port used by health checks / incident reports (default 3080). Set it if your `dsh web` runs on another port. You can also pass `--port` to the CLI.

Every path is anchored at `$DSH_HOME` (defaults to `~/.dsh` when the env var is unset):

```
$DSH_HOME/rollbacks/<profile>/<stamp>/    snapshots (5 config files + manifest.json)
$DSH_HOME/guard/logs/                     boot/server logs, incident reports, last-boot.txt
$DSH_HOME/guard/pending-incident.json     pending incident marker
$DSH_HOME/guard/config.json               guard settings (keepSnapshots, port)
```

### Rollback semantics

- Rollback = restore the 4 config files + `pnpm install --frozen-lockfile` to reproduce `node_modules` exactly.
- pnpm resolution order: absolute path recorded in the snapshot manifest (same e