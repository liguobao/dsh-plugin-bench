<div align="center">

# 📌 dsh-session-pin
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-session-pin` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-session-pin)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-session-pin?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-session-pin?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-session-pin/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-session-pin)

**Pin sessions and workspaces to the top of the DeepSeek Harness sidebar with per-pin row colors.**

*A dual-face (host + browser) plugin: two pin levels, an 8-color swatch per pin, and a navigation organizer — boards, tags, saved views, health summaries, and `/goto`.*

> **Official repository.** This is the only official repository of dsh-session-pin, maintained by PerryLink. Same-name repositories under other accounts are not affiliated.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-session-pin.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-session-pin/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-session-pin/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-session-pin?label=version)](https://github.com/PerryLink/dsh-session-pin/releases)
[![npm version](https://img.shields.io/npm/v/dsh-session-pin)](https://www.npmjs.com/package/dsh-session-pin)
[![npm downloads](https://img.shields.io/npm/dm/dsh-session-pin)](https://www.npmjs.com/package/dsh-session-pin)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (GitHub tag; verified 2026-09-22: dual-ruler typecheck + unit/composition suites + static seam checks; browser pass pending maintainer). npm dependency line `0.1.7-alpha.2`, peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0`. |
| Node | `>= 22` (development floor) |
| Platforms | Web GUI (dual-face: host + browser) |
| Model | Any (UI-only — no model traffic, no session events) |
| `session/pin` events | Pre-flight-gated: written only when the host's runtime event vocabulary knows the type (the alpha-line append can no longer stamp the `ignorable` marker, so the vocabulary is the single gate signal — adapted 2026-09-18); otherwise the projection degrades to the settings cache and one warning fires before the first write. |

## What you get

`dsh-session-pin` keeps the conversations that matter at the top of the sidebar and colors them so you can find them at a glance:

- **Two pin levels** — pin whole workspaces and individual sessions; a pinned workspace moves to the front of the workspace list and a pinned session to the front of its account.
- **Per-pin row colors** — a swatch after each pin cycles an 8-color preset palette (Shift+click clears); the row gets a left accent bar plus a translucent tint.
- **Four pin surfaces** — a hover `[pin][swatch]` pair on every row, a pin toggle in the session header, a sidebar foot action with a pinned panel, and per-browser durable pinning that keeps pins and colors across restarts.
- **Click-to-open** — clicking a pinned row in the sidebar or the pinned panel opens the session in the current window (the same seam `/goto` uses); both navigate through the host's session-retain channel on the alpha line.
- **Zero core changes** — a standalone plugin for the stock DSH Web GUI; every surface degrades gracefully on older baselines.

```text
┌─ Workspaces ────────────────────────────┐
│ 🎨 Workbench            ███             │  ← pinned workspace, tinted red
│   📌 Implement login flow         3h    │  ← pinned session, tinted teal
│     Fix the auth bug              1h    │  ← hover shows a gray pin + swatch
│   Refactor the DB layer           2d    │
└─────────────────────────────────────────┘
```

## Navigation organizer

Four browser-local capabilities organize multi-session work on top of pinning. All state rides the same `session-pin` store (per-browser; nothing is uploaded), and each has a Config switch.

- **Boards** — pins join named groups; the board chip row creates, renames, and deletes boards and drag-reorders them (order persists per-browser), while the pinned panel groups each board's pins under a collapsible header.
- **Tags & views** — entities carry up to 8 tags (≤24 chars each), set per row from the panel's manage button (which also assigns the pin's board); the filter bar matches text and tags, and any filter state saves as a named view (up to 20) for one-click switching.
- **Health summary** — each pinned session row appends a read-only, sanitized line (`N msgs · you|ai · relative time`) derived from the public session snapshot — counts and directions only, never content.
- **`/goto <keyword>`** — a composer line starting with `/goto` plus Enter jumps: a unique title/tag match opens it, several matches list in a prompt, none explains. The command line never reaches the model.

## How it works

- **Host half** (`src/index.ts`) — declares the `session-pin` settings form as the plugin's own live Config: the two pinned id lists, the two color maps, the organizer state, and the host policy (`maxPins`/`reorderOnLoad`/`pruneStale` plus the five feature switches) are all `.volatile()` fields. On the `0.1.7` settings contract a form's namespace is the local id of its profile entry, so the bundle patch's `id: session-pin` row names the form, the Plugins page edits it, and accepted edits are hot-applied to the running plugin; no session events, no model traffic.
- **Browser half** (`src/client.ts`) — assembles a framework-free `PinStore` (the host half's live Config form read through `ctx.configForms.get(entryId)`, degrading to a versioned `localStorage` document with cross-tab sync), a `PinController` (two-level toggle / color cycle / prune / reorder state machine), and the UI: the row overlay, the optional row-slot registration, the header toggle, the sidebar foot action, and the pinned panel. Ordering goes through `ctx.workspaces`.
- **Log-backed write channel** — on builds mounting the built-in `dsh-session-pin` service, every session toggle commits through the `session.setPinned` RPC first (the `session/pin` event log is the canonical residence) and mirrors the commit into the settings store; a failed or slow RPC degrades to a direct settings write.
- **Log-backed projection read** — `enableLogBacking` (host Config, fail-closed default off) mounts a projection reader that folds live `session/pin` events into the canonical pin set and mirrors the folded `pinned`/`colors` into the live Config, which becomes the idempotent cache for the log-backed state. The event schema, the pure fold (`foldPinEvents`), and the pre-flight-gated append seam (`PinLogAppender`) live in `src/pin-log.ts`: the host's runtime event vocabulary alone gates the write BEFORE the first append (the alpha-line append can no longer stamp the `ignorable` marker, so the old marker probe is gone), so hosts that cannot safely carry the event — a vocabulary that does not know the type fails closed on read — never receive one; the