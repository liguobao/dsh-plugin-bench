<div align="center">

# 🚚 dsh-claude-move
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-claude-move` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-claude-move)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-claude-move?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-claude-move?ref=badge)

**Migrate Claude Code, Codex, OpenCode and Hermes into DeepSeek Harness — copy sessions, memories, skills, instructions and slash commands as resumable DSH sessions, copy-only and approval-gated.**

*Keep your Claude Code history when you move: one install, resumable sessions, live sync with a running Claude Code, and a four-source migration wizard.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-claude-move.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-top-rated.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-claude-move/test.yml?branch=master&label=CI)](https://github.com/PerryLink/dsh-claude-move/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-claude-move?label=version)](https://github.com/PerryLink/dsh-claude-move/releases)
[![npm version](https://img.shields.io/npm/v/dsh-claude-move)](https://www.npmjs.com/package/dsh-claude-move)
[![npm downloads](https://img.shields.io/npm/dm/dsh-claude-move)](https://www.npmjs.com/package/dsh-claude-move)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

- Targets `dsh 0.1.7-alpha.2` (web profile, session format V4 on the current line); peer dependencies require `>=0.1.2-rc.1 <0.2.0 || >=0.1.5-alpha.1 <0.2.0 || >=0.1.6-0 <0.2.0 || >=0.1.7-0 <0.2.0`. Verified 2026-09-22 (checkJs type gate + 291 assertions, 38 suites). Imported logs satisfy the current restore boundary again: `tool/result` is written as the V4 first-class tool-role message, and the resume handoff carries a producer-owned message source kind (`dsh-claude-move`) because 0.1.7-alpha.1 retired the catch-all `{ kind: 'plugin', plugin }` source in both the type layer and durable-row admission. The panel's "open session" button renders disabled with an explanatory title when the host exposes no `sessions.open()`. Node `^22.19 || >=24`.
`0.1.2-rc.1` (adapted 2026-09-04): the session envelope keeps its ignorable field for stored-log read compatibility only - Session.append still cannot stamp it, so audit-gate behavior is unchanged.
- 0.4.0 ships a dual-baseline `sessionPersistence` runtime shim, feature-detected by API shape (never by version): the legacy API (`create`/`append`/`readFrom`, `list()` returning headers) and the handle seam (`create` returning a `SessionHandle`, `list()`/`stat()` returning snapshots) both work. The handle seam is published on the alpha line (`@deepseek-ai/dsh-session-persistence` / `-jsonl` `0.1.5-rc.2`), so the compat workflow covers it. On the handle path every append is followed by `flush()` (durability barrier) and a paired `close()` (single-writer ownership); headers are stamped with the backend's current format version plus an explicit `isSeeded`; missing assistant model sources fall back to the provider. Both write paths are shaped by the format version the backend itself reports: synthesized `assistant/message` events carry `stream: []` from format 2 up (the restore boundary asserts `Array.isArray(data.stream)`, so without it a log was written and readable but could not be resumed), and `tool/result` is a V4 first-class tool-role message from format 4 up but the v3 `tool-result` wrapper below it — a log is never written in a shape its own backend would refuse. Import-scan cleanup refuses to run when a listed element's `header.id` cannot be resolved, so `imports.json` is never silently cleared.
- Last verified against a fresh tarball install: real scan, real batch import (idempotent re-import), workspace attach and persistence artifacts confirmed; macOS/Linux covered by the CI matrix. Imported logs use the backend's current session format (V4 on `0.1.7-alpha.1`, V3 on the `0.1.6` line, v0 on `<= 0.1.2-rc.1`) and cannot be read by `dsh <= 0.1.2-rc.1` (upgrading is one-way; re-import from the source transcript is the fallback). Export reads every one of those shapes back.

### Compatibility matrix (public seams only)

| Surface | Used | Fallback when absent |
|---|---|---|
| Host services (`tools` / `sessionPersistence` / `workspaceRegistry` / `commands` / `systemPrompt` / `skills` / `webServer`) | required where listed | optional services register reactively; missing `fs` fails loud |
| `sessionPersistence` dual baseline: legacy `listSnapshots` / `readFrom` / `append` vs handle `open` / `stat` / snapshot `list()` | feature-detected at runtime (API shape, never version) | the `header.id` resolution guard aborts the scan loudly instead of silently clearing `imports.json` |
| `streamText`-capable `fs` / `ctx.jobs` / `ctx.agents.resume` | feature-detected | whole-file read with loud rejection / own job map / handoff inject |
| Client shell services (`sessions.refresh/open`, `workspaces.refresh`) | feature-detected at panel apply | full-page reload |
| Newer platform capabilities are never hard requirements — the plugin stays bootable on the oldest supported line (`0.1.2-rc.1`). | | |

## What you get

1. **Auto-discovery** — `claude_scan` locates the Claude data root (`$CLAUDE_CONFIG_DIR`, fallback `~/.claude`) and indexes every project/session, memory, skill, global `CLAUDE.md` and `settings.json`, with incremental caching and parallel scanning (`scanConcurrency`).
2. **Full-fidelity import** — `import_claude` turns transcripts into balanced, resumable DSH sessions (`turn/start → step/start → user/message → assistant/message → tool/call → tool/result → step/end → turn/end`), repairs interrupted tool calls, and stream-imports transcripts larger than `maxTranscriptBytes` in chunks.
3. **One `claudecode` workspace** — every imported session lands in a dedicated workspace (default `$DSH_HOME/claudecode`); `workspaceMode: 'per-project'` restores one-workspace-per-project grouping.
4. **Copy-only & incremental** — nothing on either side is moved, rewritten, or deleted; re-running appends only the new turns (`force: true` saves an extra full copy under a new id).
5. **Personal context, always fresh** — memories injected as a live prompt section, Claude skills registered as real DSH skills (global + project-level), global + project `CLAUDE.md` injected early.
6. **Four-source migration wizard** — `/move` plus `move_detect` / `move_preview` / `move_run` migrate Claude Code, Codex, OpenCode and Hermes, approval-gated and idempotent (`move.json`).
7. **Web panel & commands** — `/claude-import-all`, `/resume-claude`, `/claude-move-reset`, `/claude-export`, and a floating migration panel.
8. **Bidirectional export** — `claude_export` (or `/claude-export <sessionId>`) writes a DSH session back out as a resumable Claude Code JSONL transcript (`user`/`assistant`/`tool` turns, `thinking` + `tool_use`/`tool_result` pairing, best-effort `cwd` mapping), so history can leave DSH again.

## Four-source migration wizard

```text
/move              # one-shot wizard: detect → preview → execute → report (all four sources)
move_detect        # scan Claude Code / Codex / OpenCode / Hermes
move_preview       # per-item plan: new |