<div align="center">

# 🏠 dsh-team-rooms
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-team-rooms` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).

**Persistent, cross-session multi-agent team rooms for DeepSeek Harness — members, a message bus, a shared task board, and a shared timeline that survive restarts.**

*Each member is an independent DSH session; the room is the shared durable object between them.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-team-rooms/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-team-rooms)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-team-rooms.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-team-rooms)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-team-rooms/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-team-rooms/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-team-rooms?label=version)](https://github.com/PerryLink/dsh-team-rooms/releases)
[![npm version](https://img.shields.io/npm/v/dsh-team-rooms)](https://www.npmjs.com/package/dsh-team-rooms)
[![npm downloads](https://img.shields.io/npm/dm/dsh-team-rooms)](https://www.npmjs.com/package/dsh-team-rooms)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-team-rooms?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-team-rooms?ref=badge)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

> **Extracted from [`dsh-background-agents`](https://github.com/PerryLink/dsh-background-agents) 0.9.6.** The background-agent half of that plugin (`background_agent` and the five `bg_*` tools) is superseded by DSH's native continuable subagents; the team-room half had no native equivalent and lives on here as its own package. Storage domains, session logs, and settings written by 0.9.6 keep working unchanged — see *Compatibility*.

## Compatibility

Host `0.1.2-alpha.2` and later fails closed on the session event vocabulary, so this plugin no longer writes its log-only fact events (`team-room/fact`) there: facts route to the logger/panel channel instead and the `teamRoom` projection degrades to an empty fold. Older rc lines (through `0.1.1-rc.2`) keep the ignorable-marker discipline. The client half rides the current client packages (`dsh-api-session-controller`, `dsh-client-ui-slots`, `dsh-client-ui-settings`, `dsh-client-locale`, `dsh-client-web`).

**Data compatibility with `dsh-background-agents` 0.9.6 is a hard rule.** These strings are byte-identical to 0.9.6 and must never be renamed: the storage domain `team_rooms`, the `teamRoom` projection key, the `team-room/fact` session event type, and the `team-rooms` settings-slot id. An existing profile therefore keeps its rooms, its member logs, and its settings page when you swap the plugin.

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (verified 2026-09-18; dev and runtime pins `0.1.7-alpha.2`, peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0`) |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | All (host tools; the settings page needs the Web client half and the storage-domain capability) |
| Model | Any (rooms carry no model route — members are ordinary sessions) |

## What you get

`dsh-team-rooms` turns several independent sessions into one coordinated team:

1. **The `/room` command family** — `create`, `join`, `leave`, `list`, `send`, `tasks`, `task add|assign|claim|done|delete`. Rooms are named, owned, and addressed by a stable room id you can paste into another session.
2. **Eight `room_*` tools** — `room_list_rooms`, `room_post`, `room_read`, `room_list_tasks`, `room_create_task`, `room_claim_task`, `room_transfer_task`, `room_complete_task`. The model works the shared board and the bus from inside its own session; `room_transfer_task` asks for approval before a cross-member handoff.
3. **A durable room store** — members, the message bus (directed or broadcast), the task board, and the timeline live in the `team_rooms` storage domain (SQLite or JSONL backend — the deployment chooses; the plugin adds no service of its own) and recover across DSH restarts.
4. **A Web settings page** — the Team Rooms settings section shows member status, the task board, and the timeline of every room the current session belongs to, read from the `teamRoom` session projection and written back through the host `/room` command.

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-team-rooms#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-team-rooms

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A4 'id: team-rooms'
```

The bundle patch carries the plugin row; no Config key is required. The repo commits its build output (`lib/`), so git installs need no build step. Rooms mount wherever the storage domain is composed (`@deepseek-ai/dsh-storage-domain`, part of every `@deepseek-ai/dsh-base` profile); without it the `/room` command and the `room_*` tools stay dormant while everything else still loads.

Then, inside any session:

```
/room create release-prep
/room send <roomId> kickoff: I own the changelog, who takes the docs?
/room task add <roomId> draft the migration note
/room task claim <roomId> <taskId>
```

Paste the printed room id into another session and `/room join <roomId>` — that session is now a member, receives room deliveries as ordinary messages, and sees the same board.

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-team-rooms#main"` — committed `lib/`, no `prepare` or `allowBuilds` step.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-team-rooms`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-team-rooms-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-team-rooms` (or remove the row from the profile patch). Your rooms stay in the `team_rooms` storage domain and come back if you reinstall.
- ⚠️ **Do not mount this and `dsh-background-agents` at the same time.** While the deprecation window is open both packages are published, and both register the same eight `room_*` tools, the same `settings.section` slot id (`team-rooms`) and the same `team_rooms` storage domain — so the two room halves collide. If you already run `dsh-background-agents`, remove it first (`dsh plugin --profile web remove dsh-background-agents`). Your rooms survive either way: they live in the storage domain, not in the plugin.

## Configuration

Every tunable is a validated Schemastery `Config` field — change it in cordis.yml, never in code. Nothing is required.

| Key | Default | Meaning |
|---|---|---|
| `maxRooms` | `16` | Hard cap on team rooms across the profile |
| `maxMembersPerRoom` | `8` | Hard cap on members per room (`>= 2`) |
| `maxRoomsPerMember` | `4` | Hard cap on rooms one member session may join |
| `busRetention` | `200` | Bus messages kept per room |
| `timelineRetention` | `500` | Timeline events kept per room |
| `taskRetention` | `50` | Completed tasks kept per room |
| `maxMessageCh