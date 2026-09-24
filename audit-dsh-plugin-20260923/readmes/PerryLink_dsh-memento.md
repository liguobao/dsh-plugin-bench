<div align="center">

# dsh-memento
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-memento` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-memento)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-memento?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-memento?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-memento/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-memento)

**Bounded, layered, approval-gated, auditable cross-session memory for DeepSeek Harness.**

*A typed `ctx.memory` seam, a write-approval gate no model path can bypass, and an audit trail you can rebuild — from the approval pair plus the plugin's own audit table, with the session-log gap named out loud.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-memento.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-top-rated.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-memento/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-memento/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-memento?label=version)](https://github.com/PerryLink/dsh-memento/releases)
[![npm version](https://img.shields.io/npm/v/dsh-memento)](https://www.npmjs.com/package/dsh-memento)
[![npm downloads](https://img.shields.io/npm/dm/dsh-memento)](https://www.npmjs.com/package/dsh-memento)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (adapted 2026-09-22): the `0.1.7` line replaced the whole settings registration surface (`installSettingsSection` / `SettingsProvider.installSection` / `SettingsNamespace` / `SettingsScope`) with live Config forms, so both halves follow the new contract — a form's namespace is the profile entry id (`memento`), its editable fields are the `.volatile()` ones, and an accepted edit is committed into the running plugin instead of remounting it. The browser half reads that form through `ctx.configForms.get(entryId)` (the `ctx.settingsScope` service is gone). Both halves keep their `installSection` / `settingsScope` branches for the `0.1.2-rc.1`, `0.1.5-alpha.1` and `0.1.6-0` lines the peer range still advertises, and the new `>=0.1.7-0 <0.2.0` clause is what makes the target host itself installable (the old range excluded it by semver's prerelease rule). Still no plugin event-registration surface — `KNOWN_SESSION_EVENT_TYPES` does not carry `memory/*`, and `Session.append`'s third argument only carries a `SurfaceIntent` for surface-eligible types, so the audit gate stays adaptive and skips as before (it says so once per process and in `/memory audit`). Type evidence comes from three faces: the local checkout's built types, the pinned published line in `node_modules`, and the browser half under a DOM lib. |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | Windows / macOS / Linux (pure host; no native code, no network) |
| Model | Any |

## What you get

`dsh-memento` is a capability seam, not another memory warehouse: a typed `ctx.memory` service, a local SQLite provider (`node:sqlite`, WAL, `0600`, at `$DSH_HOME/dsh-memento/memory.db`), and its consumers — the `memory` tool and a frozen snapshot injected into the system prompt.

- **The approval gate cannot be bypassed.** Every write path (`add` / `replace` / `remove` / `seed`) is forced through the approval waterfall inside the service, not in the tool layer. `writePolicy: ask | auto | off` is model-invisible configuration; `replace` / `remove` / `consolidate` carry the full text of the entries they change in the approval payload, and a denied write still lands a `*-denied` audit row.
- **Model-visible ⟺ logged.** The injected snapshot lands verbatim in `system/message`; every write is reconstructable from `approval/asked` + `approval/decided` + the plugin's own audit table.
- **Bounded and honest.** Hard per-track/per-layer character budgets (default user 2000 / agent 4000). A full store fails with a structured error (usage + limit) — never truncated, never auto-compacted.
- **The audit gap is visible.** `/memory audit` lists the plugin audit table and appends one line when the session-log side is not written: this harness does not know the `memory/*` session event types, and appending unknown types would make the session unloadable, so writes are audited through `approval/asked` + `approval/decided` and the plugin's table instead. The gate is adaptive — the line disappears on its own once the host knows those types.

Two tracks × two layers × per-agent key: a `user` track (facts about the user) and an `agent` track (environment facts and conventions), each split into `user-global` and `workspace` layers, isolated per `agentPreset`. The snapshot is frozen once per session at first prompt assembly and never changes mid-session.

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-memento#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-memento

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A3 'id: memento'
```

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add git+https://github.com/PerryLink/dsh-memento.git`.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-memento`.
- **tarball channel**: `npm pack` in this repo, then `dsh plugin --profile web add ./dsh-memento-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-memento` (the memory database and session logs are kept).

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). Invalid values fail loudly at load. Override under the `memento` row.

**Settings panel.** On the `0.1.7` line the plugin's own `Config` **is** its settings page: the form's namespace is the profile entry id (`memento` — the `id:` of this bundle's row), the editable fields are exactly the ones the plugin declares `.volatile()` (every key below except `enabled`), and an accepted edit is merged into the profile's plugin row and committed into the running plugin — no file editing, no restart. Nearly everything applies live (write policies, language, budgets, limits, proposals, panel, `dbPath` / `auditRetentionDays` via a store reopen, `retrieval.vector` via a retriever swap); what a plugin registers at load time (`snapshotOrder`, tool descriptions) is re-read on reload, and the page marks those fields. Numeric bounds are declared in the schema as well, so an out-of-range edit is refused at write time instead of leaving an unusable config behind. On the older lines (`0.1.2-rc.1`, `0.1.5-alpha.1`, `0.1.6-0`) the same card edits the `dsh-memento` settings namespace exactly as before; with no settings service at all, everything falls back to the composed cordis config. The floating panel button can be hidden from the same page (`panel.enabled`).

| Key | Default | Meaning |
|---|---|---|
| `enabled` | `true` | Master switch; `false` removes the service, tools, snapshot, command, panel, and answerer (not editable from the settings page — a disabled plugin has no settings entry) |
| `panel.enabled` | 