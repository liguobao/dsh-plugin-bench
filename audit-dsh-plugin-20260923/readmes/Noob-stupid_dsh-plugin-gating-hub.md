> **English**: [README.md](README.md) | **中文**: [README.zh.md](README.zh.md)

---

<img width="1170" height="609" alt="image" src="https://github.com/user-attachments/assets/b802d606-14ba-4151-9956-ff642ed12b0a" />

# DSH Plugin Gating Hub (dsh-plugin-gating-hub)

*Renamed from `dsh-plugin-hub` — old URLs redirect.*

[![](https://img.shields.io/badge/powered_by-dsh-4D6BFE?style=flat-square&logo=deepseek&logoColor=white)](https://github.com/deepseek-ai/deepseek-harness)
[![Awesome DSH Plugin](https://awesome-dsh-plugin.com/badge.svg)](https://awesome-dsh-plugin.com)
[![GitHub stars](https://img.shields.io/github/stars/Noob-stupid/dsh-plugin-gating-hub?style=flat-square&logo=github)](https://github.com/Noob-stupid/dsh-plugin-gating-hub/stargazers)
[![License](https://img.shields.io/github/license/Noob-stupid/dsh-plugin-gating-hub?style=flat-square)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/Noob-stupid/dsh-plugin-gating-hub?style=flat-square)](https://github.com/Noob-stupid/dsh-plugin-gating-hub/commits/main)
[![Registry CI](https://img.shields.io/github/actions/workflow/status/Noob-stupid/dsh-plugin-gating-hub/registry.yml?label=registry%20CI&style=flat-square)](https://github.com/Noob-stupid/dsh-plugin-gating-hub/actions/workflows/registry.yml)
[![topic: dsh-plugin](https://img.shields.io/badge/topic-dsh_plugin-4D6BFE?style=flat-square)](https://github.com/topics/dsh-plugin)
[![npm version](https://img.shields.io/npm/v/@noob-stupid/dsh-plugin-console?style=flat-square)](https://www.npmjs.com/package/@noob-stupid/dsh-plugin-console)
[![npm downloads](https://img.shields.io/npm/dm/@noob-stupid/dsh-plugin-console?style=flat-square)](https://www.npmjs.com/package/@noob-stupid/dsh-plugin-console)
[![GitHub Release](https://img.shields.io/github/v/release/Noob-stupid/dsh-plugin-gating-hub?style=flat-square)](https://github.com/Noob-stupid/dsh-plugin-gating-hub/releases)[![dsh.so security](https://www.dsh.so/badge/dsh-plugin-hub.svg)](https://www.dsh.so/artifact/dsh-plugin-hub)
[![dsh.so install](https://www.dsh.so/badge/install/dsh-plugin-hub.svg)](https://www.dsh.so/artifact/dsh-plugin-hub)

> **Framework upgrade safety & plugin version gating for DeepSeek Harness (DSH)**: one-click
> framework upgrade with **auto-rollback on failure** → **one-click rollback to the previous
> version** after an upgrade → plugins the new framework cannot load are **auto-disabled** →
> the **plugin upgrade gate** refuses a version the host can't take.
> A **built-in multi-source plugin market & index** (500+ plugins / 300+ skills, zero GitHub
> API calls) rides on top as the **discovery layer** — and **every source is swappable**: install
> source (incl. a private intranet registry), search source (URL template + headers), index source
> (self-hosted intranet index), Git source (incl. a local `file://` bare repo), so plugins can be
> installed on an **intranet-only or fully offline** machine.

## Why DSH Plugin Gating Hub

- 🛡️ **Framework upgrade safety, end-to-end** — one-click upgrade: config backup + full-tree
  checkpoint (rollback point) → online install (service stays up, page never disconnects) →
  version verification → auto-restart. A failed install **auto-rolls the whole tree back**,
  version check catches fake success, 15-min hard timeout + stall detection — the framework is
  never left broken. → [details](docs/upgrade-safety-adapt-gate.md)
- ↩️ **One-click rollback to the previous version** — after an upgrade the framework card keeps
  a 「roll back to previous」 button: stop service → restore full tree → relaunch → health check,
  state visible throughout.
- 🚫 **Incompatible plugins auto-disabled** — the **adapt gate** force-disables plugins the new
  framework cannot load (enable locked; the server rejects `/toggle` with 409 — unbypassable);
  「Check update → Update & adapt」auto-verifies and unlocks them.
- 🔒 **Plugin upgrade gating** — a version/declaration gate (`dsh.engines.framework` /
  `engines.dsh` + `@deepseek-ai/*` ranges, built-in zero-dependency semver engine) decides
  whether a plugin version may run on this host, so an upgrade can't silently take plugins out.
- 🧩 **Built-in discovery layer** — multi-source plugin market (GitHub / Gitee / custom sources)
  plus the static index of `dsh-plugin` repos (500+ by stars) and a Skills tab (up to 300);
  browse, search, one-click install, **zero GitHub API calls** (served via CDN).
  **Every source is swappable** — private intranet npm registry, custom search source (URL template +
  headers), self-hosted index source, Git source (incl. local `file://` bare repo) — so an
  **intranet-only / offline** machine can still browse and install.
- 🤖 **AI Empower** — give the console a package name or GitHub repo, the local AI
  reads its docs and drafts a safe, confirmable deployment plan (install / config /
  start / health-check); server components get an automatic control card.
  → [details](docs/ai-empower.md)

## Install

```sh
# npm release (recommended: prebuilt, no git / build authorization needed)
dsh plugin --profile web add @noob-stupid/dsh-plugin-console

# or install from GitHub source (needs git; allowBuilds authorization on first add)
dsh plugin --profile web add github:Noob-stupid/dsh-plugin-hub
```

Then restart the dsh service → refresh the page → **Settings → Plugins → Plugin Console**.

<details><summary><b>More install options</b> (deploy script / hand it to an AI)</summary>

### Option 2: deploy script (fallback when network is restricted)

Windows (PowerShell):

```powershell
git clone https://github.com/Noob-stupid/dsh-plugin-hub "$env:TEMP\dsh-plugin-console" 2>$null; & "$env:TEMP\dsh-plugin-console\deploy.ps1"
```

Linux / macOS:

```bash
git clone https://github.com/Noob-stupid/dsh-plugin-hub /tmp/dsh-plugin-console 2>/dev/null; bash /tmp/dsh-plugin-console/deploy.sh
```

The script copies the plugin into `$DSH_HOME/profiles/<profile>/node_modules/` and
idempotently appends an enable entry to `cordis.patch.yml`. Afterwards:

1. Restart the dsh service (host code changes need a process restart; CLI restarts the
   process, the desktop client exits and reopens);
2. Refresh the page → Settings → Plugins → **Plugin Console**.

### Option 3: hand it to an AI in one sentence

> Install the DSH plugin hub (dsh-plugin-hub): run `dsh plugin --profile web add @noob-stupid/dsh-plugin-console` (npm release); if there is no dsh CLI, clone https://github.com/Noob-stupid/dsh-plugin-hub to `~/.dsh/profiles/web/node_modules/` and register it in `cordis.patch.yml` (id: plugin-console, name: @noob-stupid/dsh-plugin-console). Restart dsh web afterwards.

Requires: DSH ≥ 0.1.0-rc.6 (web profile, with `dsh-client-modules` / `dsh-host-plugin-inventory`).

</details>

---

## Highlights

| | Benefit | Detail |
|---|---|---|
| 🤖 | **AI Empower ** | Give the console a package name or GitHub repo — the local AI reads docs, drafts a **deployment plan** (install / write config / start service / health check) and executes it safely after your confirmation; server-type components get an automatic control card |
| 🛡️ | **Framework upgrade safety & adapt gate ** | Force-disables plugins incompatible with the new framework (enable locked; 「Check update → Update & adapt」auto-verifies and unlocks); full-tree checkpoint before upgrade, automatic rollback on relaunch failure, one-click rollback to the previous version |
| 🏠 | **Family-bundle cards & safety ** | Same-root subpath exports group into one family card (collapse/expand, batch check-update, one-click unlock-adapted, known-check preview); never-crash safety (pre-enable import probe + patch auto-heal + exports fallback); adapt-gate source-scan hard criterion & migrate detection; deleting a bundle sub-row disables only that row |
| 🚀 | **Server component cards** | Left-side floating card auto-aligned to the main panel: start / stop / status / **open Web UI** buttons, multi-server dropdown, collapsible |
| 🧩 | **Plugin & skill hub** | Auto-