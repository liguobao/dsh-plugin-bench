<div align="center">

# 🔄 dsh-session-sync
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-session-sync` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-session-sync)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-session-sync?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-session-sync?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-session-sync/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-session-sync)

**Cross-device session sync for DeepSeek Harness — a dedicated git mirror of your session store.**

*Sync your sessions between devices, keep both sides on any conflict, never lose a turn.*

> **Official repository.** This is the only official repository of dsh-session-sync, maintained by PerryLink. Same-name repositories under other accounts are not affiliated.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-session-sync.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-top-rated.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-session-sync/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-session-sync/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-session-sync?label=version)](https://github.com/PerryLink/dsh-session-sync/releases)
[![npm version](https://img.shields.io/npm/v/dsh-session-sync)](https://www.npmjs.com/package/dsh-session-sync)
[![npm downloads](https://img.shields.io/npm/dm/dsh-session-sync)](https://www.npmjs.com/package/dsh-session-sync)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (GitHub tag, verified 2026-09-22: full gate chain against the pinned `0.1.7-alpha.2` peers). npm dependency line `0.1.7-alpha.2`, peers `>=0.1.2-rc.1 <0.2.0 || >=0.1.5-alpha.1 <0.2.0 || >=0.1.6-0 <0.2.0 || >=0.1.7-0 <0.2.0`. (adapted 2026-09-22): the conflict fork notice carries the plugin's own producer-owned message source kind - the harness retired the shared `plugin` kind and refuses it on read-back. |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | Anywhere `git` and DSH run (git-based mirror; no platform-specific code) |
| Model | Text-only models fully supported; no vision or extra model capability required |

## What you get

`dsh-session-sync` mirrors your DSH session store into a dedicated git worktree and syncs it to a remote **you** control — no cloud service, no third-party storage:

- **`/sync` command** — `status` (branch, sanitized remote, ahead/behind, dirty files, forks), `diff`, `log`, `pull`, `push`, `help`.
- **`sync_status` / `sync_pull` / `sync_push` tools** — the same surface for the model, inside a turn.
- **Append-only conflict resolution** — session logs are append-only; on any divergence the plugin keeps **both** sides (local version kept, remote version preserved as fork files) and never silently overwrites. Diverged sessions can also fork at the session level.
- **Auto modes** — pull on start, push after every closed turn, and periodic pull, all configurable and all reversible.
- **Confirmation-gated writes** — `pull`/`push` ask first (through `userQuestions` or `approval`); read-only surfaces never ask; with no answerer the operation fails closed.

```text
device A                              remote (your git repo)                  device B
$DSH_HOME/sessions ──mirror──▶ commit ──push──▶ [sessions] ──pull──▶ merge (keep-both + fork)
```

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-session-sync#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-session-sync

# 2. point it at a private git remote and verify the row
dsh --profile web --dump-config | grep -A2 'id: session-sync'
```

Then set the remote in your profile patch (a **private** repository is the baseline) and sync:

```yaml
- insert:
    - id: session-sync
      name: dsh-session-sync
      config:
        remote: git@github.com:you/your-dsh-sessions.git
```

```
> /sync status
> /sync pull
> /sync push
```

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-session-sync#main"` (equivalent to installing from `git+https://github.com/PerryLink/dsh-session-sync.git`). No build step — `index.mjs` and `lib/` are the shipped artifacts.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-session-sync`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-session-sync-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-session-sync` (or remove the row from the profile patch).

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). An id-targeted override replaces the whole row — restate every key you need. `cordis.patch.yml` documents each key inline.

| Key | Default | Meaning |
|---|---|---|
| `enabled` | `true` | Master switch; `false` unregisters the command, tools, listeners, and auto modes |
| `backend` | `git` | Sync backend: `git` (plaintext mirror) or `encrypted` (age-encrypted mirror content) |
| `sessionRoot` | `''` | Session store root; empty = `$DSH_HOME/sessions` (both missing fails load) |
| `repoDir` | `''` | Sync worktree root; empty = `$DSH_HOME/dsh-session-sync/repo` |
| `remote` | `''` | Remote address (required before pull/push; status/diff work without one) |
| `branch` | `main` | Remote branch name |
| `gitBin` | `git` | git executable path |
| `ageBin` | `age` | age executable path (probed for `backend: encrypted`; missing degrades to plaintext) |
| `ageRecipient` | `''` | age recipient (public key or identity string); empty = cannot encrypt, degrades to plaintext |
| `ageIdentity` | `''` | Path to a passphrase-less age secret key for decryption; empty = cannot decrypt, degrades to plaintext |
| `autoPullOnStart` | `false` | Pull once when the plugin mounts (config is the grant; no re-confirm) |
| `autoPushOnTurnEnd` | `false` | Push after every closed turn |
| `pullIntervalMinutes` | `0` | Periodic pull every N minutes (`0` = off, max `10080`) |
| `confirmVia` | `auto` | Confirmation channel: `auto` (userQuestions first, then approval), `userQuestions`, `approval` |
| `graceMs` | `10000` | Grace period for git kills (ms) |
| `commandTimeoutMs` | `120000` | Per-command timeout (ms) |
| `maxOutputBytes` | `262144` | Per-stream collected-output cap (bytes) |
| `commitName` | `dsh-session-sync` | Commit author name |
| `commitEmail` | `dsh-session-sync@localhost` | Commit author email |
| `registerCommand` | `true` | Register the `/sync` command |
| `registerTools` | `true` | Register the `sync_*` tools when the tools service is present |

Example override in your profile patch:

```yaml
- insert:
    - id: session-sync
      name: dsh-session-sync
      config:
        remote: git@github.com:you/your-dsh-sessions.git
        branch: main
        autoPushOnTurnEnd: true
        pullIntervalMinutes: 30
        confirmVia: userQuestions
```

## Tools & surfaces

| Surface | Read-only | Needs confirmation | Notes |
|---|---|---|---|
| `/sync status` | ✅ | — | Branch, sanitized remote,