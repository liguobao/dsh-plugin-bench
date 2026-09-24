<div align="center">

# ⚡ dsh-fast
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-fast` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-fast)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-fast?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-fast?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-fast/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-fast)

**Read-only performance diagnostics for DeepSeek Harness.**

*Observes the session event stream — never the model hot path — and reports where latency and context budget actually go.*

> **Official repository.** This is the only official repository of dsh-fast, maintained by PerryLink. Same-name repositories under other accounts are not affiliated.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-fast.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-fast/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-fast/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-fast?label=version)](https://github.com/PerryLink/dsh-fast/releases)
[![npm version](https://img.shields.io/npm/v/dsh-fast)](https://www.npmjs.com/package/dsh-fast)
[![npm downloads](https://img.shields.io/npm/dm/dsh-fast)](https://www.npmjs.com/package/dsh-fast)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

- DeepSeek Harness `dsh-v0.1.7-alpha.2` (adapted 2026-09-18): the session surface is read through the optional `sessionQuery` service — the deprecated synchronous `Session.eventAt(seq)` accessor is gone, with an equivalent synchronous read as the fallback — and every registration now lives in one lifecycle effect that releases them in reverse order. Internal implementation change: the reported metrics are identical for the same log. Verified 2026-09-18 against the local gate chain (dual typecheck rulers + 70 tests); the compat workflow re-runs the profile install smoke against the published pins.
- Node `^22.19.0 || >=24.0.0`, ESM only (`"type": "module"`).
- Peer dependencies: `@deepseek-ai/cordis ^4.0.2`, `@deepseek-ai/schemastery ^3.18.4`, and `@deepseek-ai/dsh-session`, `@deepseek-ai/dsh-tools`, `@deepseek-ai/dsh-commands`, `@deepseek-ai/dsh-compaction`, `@deepseek-ai/dsh-session-query`, `@deepseek-ai/dsh-storage-domain` at `>=0.1.2-rc.1 <0.2.0 || >=0.1.5-alpha.1 <0.2.0 || >=0.1.6-0 <0.2.0 || >=0.1.7-0 <0.2.0` (devDependencies pin `0.1.7-alpha.2`); the `0.1.2-rc.1` line stays supported at runtime through a structural fallback to the pre-0.1.5 `header.system`.

## What you get

- **Session load timing** — publication-to-first-request latency, classified `open` (fresh) vs `restore` (seeded/resumed), plus the restored seed-event count.
- **Spill-hit statistics** — how many tool results were spilled to a session-scoped artifact (detected from the durable spill notice).
- **Compaction count and trigger** — total compactions, split `manual` (slash command) vs `automatic` (pressure), and total shadowed tokens.
- **Context-injection volume** — system-prompt (AGENTS.md + skills + persona), tool-schema, and surface tokens with their shares of the total; the surface bucket is conversation history only (the meter's surface includes the system node on `0.1.5-alpha.1`, which dsh-fast subtracts).
- **LLM cache hit rate** — input / cache-read / cache-write / output tokens aggregated from provider usage, plus the derived hit rate.
- **Optimization suggestions** — threshold-driven notes (trim skills, tighten tool schemas, compact earlier, enable prompt caching, enable spill-policy, …).
- **Async sampling** — metrics are folded O(1) per event and snapshotted on a timer, never on the append path.

## Quick start

### git channel

```sh
# From a scratch profile (pins the commit; runs the self-contained `prepare` build)
dsh plugin --profile demo add "github:YOUR_ORG/dsh-fast#<sha>"
# The profile's pnpm-workspace.yaml gains an allowBuilds entry for dsh-fast on first add.
```

### npm channel

```sh
dsh plugin --profile demo add dsh-fast
```

Both channels install the bundle row (see `cordis.patch.yml`) into the profile's `dsh.profile.bundles` stack and take effect on restart.

## Install & uninstall

```sh
dsh plugin --profile demo add dsh-fast       # install
dsh plugin --profile demo remove dsh-fast    # uninstall
```

Verify the row mounts: `dsh --profile demo --dump-config | grep dsh-fast`.

## Configuration

All tunables are Schemastery `Config` fields; invalid values fail the profile load loudly.

| Key | Default | Description |
| --- | --- | --- |
| `enabled` | `true` | Master switch; `false` mounts nothing. |
| `privacy.includeCwd` | `false` | Include the sanitized session working directory in reports. |
| `sampling.snapshotIntervalMs` | `60000` | How often active sessions are sampled (ms). |
| `sampling.maxHistorySamples` | `20` | Samples retained per session in the durable history. |
| `thresholds.systemPromptTokens` | `20000` | Warn when the system prompt exceeds this many tokens. |
| `thresholds.toolSchemaTokens` | `8000` | Warn when the tool schema exceeds this many tokens. |
| `thresholds.surfaceTokens` | `60000` | Warn when the conversation surface exceeds this many tokens. |
| `thresholds.cacheHitRateFloor` | `0.1` | Warn when the cache hit rate falls below this (0..1). |
| `thresholds.compactionCountWarn` | `10` | Warn once this many compactions have triggered. |
| `thresholds.compactionShadowTokens` | `40000` | Warn when the average shadowed token count per summary exceeds this. |
| `spill.detectSpilledResults` | `true` | Detect spilled tool results from the durable notice marker. |

## Tools & surfaces

- **`/fast`** — a human slash command that prints the current session's health report: load timing, spill, compaction, context-volume ranking, cache hit rate, and suggestions.
- **`fast_report`** — a model tool returning the same report as structured JSON (so the model can reason over it), with a human-readable text render.

## Permissions & data

`dsh-fast` consumes only public seams: `session/*` and `agent/*` events, the optional `ctx.tokenMeter`, `ctx.storageDomain`, `ctx.commands`, and `ctx.tools`. It is strictly read-only over the session log — it never mutates the model request, tool results, or the session surface. Metrics are persisted to the `dsh_fast` storage domain (one bounded history per session), not to the session log. Report identity and the optional working directory are sanitized before any display or durable write.

## Security boundaries

- **Read-only, zero model-path overhead** — folding is O(1) per event; sampling runs on a timer.
- **No network, no credential handling** — the plugin makes no outbound requests and stores nothing sensitive.
- **Fail-loud configuration** — every tunable is validated at mount; invalid bounds throw.
- **Sanitized display/durable data** — control characters are stripped and strings are budgeted; `cwd` is off by default and path-truncated when enabled.
- **Reversible registrations** — every contribution goes through `ctx.effect()` / `ctx.on()` / `register()`, so uninstall and hot reload are clean.

## Known limitations