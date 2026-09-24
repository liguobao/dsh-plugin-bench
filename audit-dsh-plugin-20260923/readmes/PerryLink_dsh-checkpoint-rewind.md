<div align="center">

# ⏪ dsh-checkpoint-rewind
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-checkpoint-rewind` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-checkpoint-rewind)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-checkpoint-rewind?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-checkpoint-rewind?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-checkpoint-rewind/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-checkpoint-rewind)

**Unified DeepSeek Harness checkpoints — session + workspace + config three-state snapshots with one-shot rollback.**

*The Claude Code Checkpoints equivalent, built as a capability-seam plugin: capture before every mutation, restore any of the three states with one approved command.*

> **Official repository.** This is the only official repository of dsh-checkpoint-rewind, maintained by PerryLink. Same-name repositories under other accounts are not affiliated.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-checkpoint-rewind.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-checkpoint-rewind/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-checkpoint-rewind/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-checkpoint-rewind?label=version)](https://github.com/PerryLink/dsh-checkpoint-rewind/releases)
[![npm version](https://img.shields.io/npm/v/dsh-checkpoint-rewind)](https://www.npmjs.com/package/dsh-checkpoint-rewind)
[![npm downloads](https://img.shields.io/npm/dm/dsh-checkpoint-rewind)](https://www.npmjs.com/package/dsh-checkpoint-rewind)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (GitHub tag, verified 2026-09-22; npm pin `0.1.7-alpha.2`, peers `>=0.1.2-rc.1 <0.2.0 || >=0.1.5-alpha.1 <0.2.0 || >=0.1.6-0 <0.2.0 || >=0.1.7-0 <0.2.0`) (adapted 2026-09-22): the host removed `@deepseek-ai/dsh-settings-file` and replaced the `ctx.settings` namespace-registration surface with `SettingsForms`, which projects each Loader entry's `Config` into the Settings form and persists edits on the profile patch — plugin config fields are now declared `volatile()` and read live, strict typert codecs carry only their `create()` factory, and the rewind notice declares its own message-source `kind`. The legacy `settings.register` path is kept for `0.1.5-rc.2`/`0.1.6-alpha.2` hosts. Verified 2026-09-22 against the `dsh-v0.1.7-alpha.1` checkout (typecheck against the alpha.1 type surface + full unit suite + assembled-headless integration). |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | All (host commands + listeners; optional Settings page timeline via the settings capability) |
| Model | Any (no model calls — snapshots and restores are deterministic) |

## What you get

`dsh-checkpoint-rewind` captures a **three-state unified checkpoint** — workspace, session cursor, and plugin config — and restores one or all three with a single approved command:

1. **Three-state record** — every checkpoint stores the workspace state (git tree SHA, or a copy manifest), the session event cursor (`seq` + turn boundary), and a config snapshot, tagged by source (`manual` / `auto` / `guard` / `mutation`).
2. **Four capture triggers** — before every mutating tool (`fs/write-intent`, `fs/edit-intent`, `tools/pre-execute`), on automatic interval (`autoCheckpoint`, default every step), manually (`/checkpoint` and the `checkpoint` tool), and as a guard before every rewind.
3. **git-first provider** — `git stash create` / `commit-tree` produce unreferenced snapshot objects that never touch your worktree, index, or history; restore is worktree-only and path-explicit. Non-git directories (and unborn-HEAD repos) degrade to an incremental `copy` provider with hardlink reuse.
4. **One-shot rollback** — `/rewind workspace|session|config|all <target>` restores the selected states; `preview` is a read-only impact report, `diff <a> <b>` compares two checkpoints, `clear` deletes them (this session; `clear --all` spans all sessions and workspaces).
5. **Fork-based session rollback** — session rollback replays events up to the checkpoint boundary through the official `SessionStore.fork` primitive into a new child session (falling back to the seeded `sessions.create` path when the host has no fork or the checkpoint has no boundary); the original session keeps its full history.
6. **Settings page timeline** — the `Plugins → Checkpoints` tab renders the session's checkpoints with pairwise line-level diffs.

## Why another rewind plugin?

| Plugin | What it sells | Restores files? | Rewinds the session? |
|---|---|---|---|
| **dsh-checkpoint-rewind** (this) | git-object snapshots + three-state rollback + one-shot restore | ✅ full workspace state | ✅ seed-replay child session |
| [Anionex/dsh-turn-rewind](https://github.com/Anionex/dsh-turn-rewind) | persistent Change Ledger of per-mutation deltas | ✅ by replaying inverse deltas | ✅ its own ledger model |
| [LingLambda/dsh-undo](https://github.com/LingLambda/dsh-undo) | pure context rollback to the last completed step | ❌ | ✅ context only |
| [Mongfayi/dsh-recall](https://github.com/Mongfayi/dsh-recall) | message recall (remove a turn and everything after) | ❌ (explicitly) | ✅ turn removal |

The difference in one sentence: **dsh-checkpoint-rewind captures the *workspace state* with side-effect-free git primitives before each mutation, and makes "back to step N" one approved command — guard checkpoint first, files restored second, config restored third, session replayed fourth, each phase logged.** No delta bookkeeping to drift, no message-level editing (that belongs to a different plugin), no cross-device sync.

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-checkpoint-rewind#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-checkpoint-rewind

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A4 'id: checkpoint-rewind'
```

Checkpoints persist through the `storageDomain` service. The plugin mounts without it and never blocks profile startup — checkpoint/rewind commands then return a structured error naming the exact rows to add. Compose the storage stack once to enable checkpoints:

```yaml
- insert:
    - id: checkpoint-rewind-storage
      name: '@deepseek-ai/dsh-storage'
    - id: checkpoint-rewind-storage-json
      name: '@deepseek-ai/dsh-storage-json'
      config:
        root: !!js dshHomePath('checkpoint-rewind/storage')
    - id: checkpoint-rewind-storage-domain
      name: '@deepseek-ai/dsh-storage-domain'
      config:
        backend: json
```

The package is pure ESM with no build step — `index.mjs` and `lib/` are the shipped artifacts. Workspace mutations now create checkpoints automatically; run `/rewind` to list them:

```text
rewind: 3 checkpoints (newest last):
#a1b2c3d4 · (git) · turn 2 step 1 · 2026-08-14 12:00:01 (3 min ago) · trigger: bash · 4 files · 1.2 MiB
#b2c3d4e5 · (git) · turn 2 step 3 · 2026-08-14 12:00:41 · trigger: