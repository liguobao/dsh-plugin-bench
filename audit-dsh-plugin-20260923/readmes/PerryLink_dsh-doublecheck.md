<div align="center">

# dsh-doublecheck
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-doublecheck` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-doublecheck)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-doublecheck?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-doublecheck?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-doublecheck/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-doublecheck)

**The delivery quality gate for DeepSeek Harness: grill the requirements, test the implementation, prove the delivery — then gate the handoff with a deliverable/rework decision.**

*Requirements get interrogated before the first edit; delivery is proven, never claimed.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-doublecheck.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-doublecheck/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-doublecheck/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-doublecheck?label=version)](https://github.com/PerryLink/dsh-doublecheck/releases)
[![npm version](https://img.shields.io/npm/v/dsh-doublecheck)](https://www.npmjs.com/package/dsh-doublecheck)
[![npm downloads](https://img.shields.io/npm/dm/dsh-doublecheck)](https://www.npmjs.com/package/dsh-doublecheck)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2`. Verified 2026-09-22 (dual typecheck rulers + full test suite green); the peer range admits `0.1.2-rc.1`, `0.1.5-alpha.1`, `0.1.5-rc.2`, `0.1.6-alpha.2`, `0.1.7-alpha.1` and `0.1.7-alpha.2`, so no supported host line is dropped. |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | All (pure host; no native code, no direct network requests of its own) |
| Model | Any (the guard itself never calls a model; the critic and reviewer phases run as harness subagents) |

## What you get

`dsh-doublecheck` installs two plugin rows that read and enforce from the same durable session log:

1. **`doublecheck-grill`** — the requirements furnace: the bundled `grill-requirements` skill plus the model-facing `doublecheck_skills`, `doublecheck_spec`, and `doublecheck_report` tools and the per-dimension verification workflow.
2. **`doublecheck-guard`** — the discipline guard: the grill gate, the red/green evidence gates, the adversary review, the `/doublecheck` and `/gate` commands, the live `gate` settings card, and the four-phase delivery gate.

Together they enforce the **discipline loop** — *grill → design → red → green → review → verify*:

```text
grill ──▶ design ──▶ red ──▶ green ──▶ review ──▶ verify
   │
   └─ six requirement dimensions, consensus gate,
      structured spec committed to the session + workspace
```

| Stage | Meaning |
|---|---|
| **grill** | Interrogate the six requirement dimensions; refuse to implement until consensus. |
| **design** | The settled spec is committed via `doublecheck_spec`. |
| **red** | A failing test run proves the gap before implementation edits. |
| **green** | A passing test run after the edits closes the loop. |
| **review** | A forked adversary critic audits the delivery against the spec. |
| **verify** | `doublecheck_report` + a per-dimension verification workflow prove the delivery. |

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-doublecheck#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-doublecheck

# 2. restart and verify the row
dsh --profile web --dump-config | grep -E -A3 'id: doublecheck-(grill|guard)'
```

Both rows (`doublecheck-grill` and `doublecheck-guard`) activate automatically with the profile.

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-doublecheck#main"` — the `prepare` script builds with production dependencies only.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-doublecheck`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-doublecheck-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-doublecheck` (or remove the rows from the profile patch).

For a zero-configuration strict mode (every gate on at `block` intensity, gate coverage required), apply the shipped overlay on top of the bundle patch: `dsh --profile web --patch ./node_modules/dsh-doublecheck/strict.patch.yml`.

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). An id-targeted override replaces the whole row — restate every key you need. `cordis.patch.yml` documents each key inline; Schema defaults are the single source of tuning defaults.

| Key | Default | Meaning |
|---|---|---|
| `specFile` | `'doublecheck-spec.md'` | Workspace file for the committed spec markdown (grill row). |
| `reportFile` | `'doublecheck-report.md'` | Workspace file for the delivery report (grill row). |
| `reportVerify` | `true` | Run the verification workflow by default (grill row). |
| `verifyProvider` | `'fork'` | Subagent provider for the per-dimension checkers (grill row). |
| `verifyMode` | `'all'` | `all` = one parallel checker per dimension; `single` = one combined checker (grill row). |
| `intensity` | `'remind'` | Enforcement strength of the grill, red/green, and review gates (`remind` / `warn` / `block`). |
| `enableByDefault` | `true` | Master switch for sessions without a `/doublecheck on\|off` record. |
| `language` | `'en'` | Injected reminder/deny/review/gate prose language (`en` / `zh`). |
| `guardTools` | `['edit', 'write']` | Mutation tool names both gates watch. |
| `vagueTaskMaxChars` | `200` | Longer tasks are never treated as vague. |
| `remindOnce` | `true` | Inject each reminder at most once per session (durable across restarts). |
| `testToolNames` | `['bash', 'pwsh']` | Shell tool names that can run tests. |
| `testCommandPatterns` | *(pnpm/npm/yarn/bun test, pytest, go/cargo/make test, node --test, deno test, uv run pytest)* | Regexes a command must match to count as a test run. |
| `testFilePatterns` | *(test dirs, `*.test.*` / `*.spec.*`)* | Regexes identifying test files — always editable, exempt from the red gate. |
| `modules.grill` | `true` | Off disables the grill gate. |
| `modules.tdd` | `true` | On enables the red/green evidence gates. |
| `modules.adversary` | `false` | On enables the forked critic review at green. |
| `adversaryModel` | `null` | Critic model route; `null` = main model self-reviews. |
| `adversaryProvider` | `'fork'` | Subagent provider the critic runs on. |
| `adversaryMaxFindings` | `5` | Findings cap (1–20) injected into the session. |
| `adversaryTools` | `['read', 'glob', 'grep']` | Critic tool allowlist; keep it read-only. |
| `adversaryTimeoutMs` | `120000` | Hard time budget for one critic run. |
| `gate.enabled` | `true` | Master switch for the gate panel and the turn-boundary red notice. |
| `gate.planSuggestion` | `true` | Append the plan-mode re-check suggestion to red reports. |
| `gate.reportFile` | `'gate-report.md