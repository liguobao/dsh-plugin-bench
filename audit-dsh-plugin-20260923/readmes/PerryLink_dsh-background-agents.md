<div align="center">

# 👥 dsh-background-agents
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-background-agents` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-background-agents)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-background-agents?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-background-agents?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-background-agents/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-background-agents)

**Interactive long-session background agents plus persistent multi-agent team rooms for DeepSeek Harness — start a durable child agent that keeps working while you keep talking.**

*Steer live conversations and coordinate a team across sessions; everything survives restarts through the harness's own storage.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-background-agents.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-background-agents/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-background-agents/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-background-agents?label=version)](https://github.com/PerryLink/dsh-background-agents/releases)
[![npm version](https://img.shields.io/npm/v/dsh-background-agents)](https://www.npmjs.com/package/dsh-background-agents)
[![npm downloads](https://img.shields.io/npm/dm/dsh-background-agents)](https://www.npmjs.com/package/dsh-background-agents)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

Host `0.1.2-alpha.2` and later fails closed on the session event vocabulary, so this plugin no longer writes its log-only fact events (`background-agents/fact`, `team-room/fact`) there: facts route to the logger/panel channel instead and the projections degrade to an empty fold. Older rc lines (through `0.1.1-rc.2`) keep the ignorable-marker discipline. The client half now rides the current client packages (`dsh-api-session-controller`, `dsh-client-web`) and the current subagent remote (`interruptByParent`, `prompt` with a client-minted `requestId`; the old `history` RPC is gone — result peeks read the child session's `conversation` projection).
0.1.2-rc.1 (adapted 2026-09-04): the session envelope keeps its ignorable field for stored-log read compatibility only - Session.append still cannot stamp it (the third parameter is SurfaceIntent for surface event types only, never an options bag), so fact-gate behavior is unchanged.
0.1.3-alpha.1 (adapted 2026-09-06): the CI harness pin moves to the master checkout (`d347e7039`) - the handle seam (`open → read → close`) of the session-persistence service. The published 0.1.2-rc.1 runtime predates open(), so the cold bg_result read feature-detects the seam and falls back to load() - same behavior on both lines. Verified 2026-09-06 against the dsh-v0.1.7-alpha.1 master checkout (full gate chain + profile install smoke).
0.1.5-alpha.1 (adapted 2026-09-09): `SessionHandleReadResult` now returns `{ eventState, events }`, so the cold `bg_result` read destructures `.events` from the handle seam (the published `load()` fallback is unchanged). The CI harness pin moves to the public tag commit `5dda764ed3aa` (the local checkout is 13 infra commits ahead and unreachable from CI) and the compat probes install the alpha line. Peers widen to `>=0.1.2-rc.1 <0.2.0 || >=0.1.5-alpha.1 <0.2.0` (prerelease-tuple rule: the first arm alone does not match `0.1.5-alpha.1`) and devDeps pin `0.1.5-alpha.1`. Verified 2026-09-09 against `dsh-v0.1.7-alpha.1` (full gate chain). The earlier `0.1.3-alpha.1` claim is superseded: that prerelease falls outside both peer arms.
0.1.5-rc.1 (adapted 2026-09-10): dependency pins move to the published 0.1.5-rc.1 line; no seam change affects this plugin's behavior.
0.1.5-rc.2 (adapted 2026-09-11): dependency pins move to the published 0.1.5-rc.2 line; no seam change affects this plugin's behavior.
0.1.6-alpha.2 (adapted 2026-09-18): the client session service removed its subagent-navigation call, so the action now reports that navigation is owned by the session header (`ui-subagent`'s lineage seat) instead of failing silently; the room panel derives its current session from main-view retention (`retainedBy.mainView`) because `SessionListState.current` is gone. The `agent/created` catch-up listener returns synchronously under its own 2 s bound, and an unreadable child log reports `unavailable` instead of empty text. Dashboard metrics fed by the session-log fact channel remain **unavailable** on this line (a non-surface fact event still cannot be stamped with the ignore marker) — the durable room tables and the panel's projection value are the record. Verified 2026-09-18 (both typecheck rulers + the full test suite); the browser-visible half is **not** machine-verified yet.
0.1.7-alpha.1 (adapted 2026-09-22): the host completed its move to producer-owned message attribution — the catch-all `{ kind: 'plugin', plugin }` source is retired from both the type map and physical-row admission — so every notice this plugin injects now carries its own `kind: 'dsh-background-agents'`, declared by module augmentation; the projection still reads `'plugin'`-kinded notices out of older logs. Tool results are V4 first-class `role: 'tool'` messages (`toolCallId`/`content`/`isError` at the top level, no `{ type: 'tool-result' }` wrapper block), and `listChildren` returned to identity-only `SubagentCatalogEntry` rows — no `kind` discriminator, no diagnostics, no `activity` — so every direct-listing call site classifies by `mode === 'continuable'`. Client-side, `IconBranchOutline16` became `IconBranchOutlineRegular` and `ISessions.refreshSubagents` became `refreshProjections(sessionId)`. Verified 2026-09-22 (both typecheck rulers + the full test suite + build + artifact checks); the browser-visible half is **not** machine-verified yet.

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (GitHub tag, verified 2026-09-22; dev pins `0.1.7-alpha.2`, peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0`) |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | All (host tools; optional Web sidebar panel and team rooms via the storage-domain capability) |
| Model | Any (children inherit the parent's route; `childProvider`/`childModel` override) |

## What you get

`dsh-background-agents` upgrades DSH's fire-and-forget background *jobs* into two coordinated surfaces:

1. **Five steering tools** — `background_agent` starts a durable, continuable child on the official subagent seam (optional `tool_filter` — removes tools, never grants new ones; `persona`; `max_depth`; `childProvider`/`childModel` route). `bg_message` delivers a later turn; `bg_list` reports status (or the descendant tree with `parentId`/`depth`); `bg_result` reads the latest result text (reasoning fallback flagged `textSource: 'reasoning'`); `bg_stop` requests interruption.
2. **Progress and archive** — `autoReport` injects one throttled progress line after each child turn; `reportDelivery: wakeup` starts a parent turn when idle. The idle sweep a