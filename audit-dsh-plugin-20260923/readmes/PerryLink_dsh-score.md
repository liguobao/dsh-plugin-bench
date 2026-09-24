<div align="center">

# 🏆 dsh-score
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-score` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-score)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-score?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-score?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-score/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-score)

**Multi-dimensional quality scoring for DeepSeek Harness plugins.**

*Five dimensions, real `gh`/`npm` evidence, one weighted risk card and leaderboard.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-score.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-score/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-score/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-score?label=version)](https://github.com/PerryLink/dsh-score/releases)
[![npm version](https://img.shields.io/npm/v/dsh-score)](https://www.npmjs.com/package/dsh-score)
[![npm downloads](https://img.shields.io/npm/dm/dsh-score)](https://www.npmjs.com/package/dsh-score)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Component | Version |
|---|---|
| DeepSeek Harness | **`dsh-v0.1.7-alpha.2`** (GitHub tag; the peer range admits the alpha.2 line: `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0`). Dev/test pins and the `typecheck:ci` ruler now measure the published `0.1.7-alpha.2` line (the `0.1.6-alpha.2` face was verified 2026-09-18: type gates, unit/assembly suites, artifact build); the `ctx.jobs` seam was migrated to the alpha.2 `SessionId` contract. |
| Node.js | `^22.19.0 \|\| >=24.0.0` |
| Package manager | `pnpm@11.7.0` |
| Platform | Windows / macOS / Linux (host-only plugin) |
| External tools | `gh` CLI on PATH (authenticated for API reads), `npm` CLI on PATH |

## What you get

- `score` tool — one target through the five-dimension pipeline; returns the structured risk card, or `{ kind: 'background', jobId }` with `background: true`.
- `/score` command — batch scoring of a whitespace/comma-separated target list as a `score-batch` background job over `ctx.jobs`, producing a leaderboard snapshot (JSON + Markdown).
- `score_report` tool — fetch any stored score card (`sc_...`), leaderboard (`lb_...`), or the latest leaderboard.
- `score_badge` tool — an embeddable README badge (shields.io flat SVG + endpoint URL) and the five-dimension JSON for one scored target.
- **Five dimensions** (weights configurable, defaults sum to 100): install success `25`, maintenance `20`, documentation `20`, security `20`, compliance `15`.
- **Evidence discipline** — every dimension records its audit links (`source`, sanitized `detail`, `observedAt`); a dimension without evidence reports `no-evidence` (score 0, excluded from the weighted total), never a fabricated number.
- Structured results — every record carries `schema: "dsh-score/v1"` with first-class fields; this is the machine-readable contract downstream tooling consumes.

## Quick start

### Git channel

```sh
dsh plugin --profile web add github:PerryLink/dsh-score#<commit-sha>
```

The first `add` fails because pnpm blocks the package's `prepare` build; copy the exact key pnpm printed into the profile's `pnpm-workspace.yaml` and re-run:

```yaml
allowBuilds:
  'dsh-score': true
```

### npm channel

```sh
dsh plugin --profile web add dsh-score
```

Prebuilt packages need no build allowance. Restart the profile, then use `score` / `/score` from a session.

## Install & uninstall

```sh
dsh plugin --profile web add dsh-score     # install (npm) — or the git form above
dsh plugin --profile web remove dsh-score  # uninstall
```

## Configuration

All keys are optional (defaults shown); invalid values fail loudly at load.

| Key | Default | Description |
|---|---|---|
| `probeTimeoutMs` | `60000` | Deadline for one `gh`/`npm` probe command. |
| `outputTailBytes` | `8000` | Cap on the sanitized output tail recorded per probe. |
| `cacheMaxAgeMs` | `86400000` | How long a cached score card is reused before re-scoring (0 disables the cache). |
| `staleCommitWarnDays` | `90` | Commit/publish age at which maintenance drops to `warn`. |
| `staleCommitFailDays` | `365` | Commit/publish age at which maintenance drops to `fail`. |
| `staleIssueWarnDays` | `30` | Oldest-open-issue age (response proxy) at which maintenance drops to `warn`. |
| `staleIssueFailDays` | `180` | Oldest-open-issue age at which maintenance drops to `fail`. |
| `maxBatchTargets` | `20` | `/score` batch cap. |
| `batchConcurrency` | `1` | Batch concurrency (serial avoids API-rate contention). |
| `weights` | `{install:25, maintenance:20, documentation:20, security:20, compliance:15}` | Per-dimension weights (each 0–100; at least one must be > 0). |

## Tools & surfaces

### `score`

```
score(target: string, refresh?: boolean, background?: boolean)
```

- `target` — a GitHub repo (`github:owner/repo`, `owner/repo`, a git/https URL) or an npm package name.
- `refresh: true` bypasses the score cache and re-gathers evidence.
- `background: true` starts a `score-batch` job and returns its id.

### `/score <targets...>`

Starts one background batch job; progress streams through the job output, and the final line names the leaderboard id for `score_report`.

### `score_report(id?)`

Returns a score card (`sc_...`), a leaderboard (`lb_...`), or — with no id — the latest leaderboard.

### `score_badge(target? | id?, refresh?)`

Generates an embeddable README badge and the five-dimension JSON for one target:

- `target` — score a GitHub repo or npm package (through the cache) and badge it; mutually exclusive with `id`.
- `id` — badge a stored score card (`sc_...`) without re-scoring.
- `refresh: true` — bypass the score cache (only applies to `target`).

Returns the badge (SVG + endpoint + Markdown embed) and the compact five-dimension JSON — see [Badge & JSON API](#badge--json-api).

### Structured result sample

```json
{
  "schema": "dsh-score/v1",
  "scoreId": "sc_8f1c2e4a9b3d7f01",
  "target": { "kind": "repo", "spec": "github:owner/dsh-click#abc123" },
  "scoredAt": "2026-08-16T00:00:00.000Z",
  "durationMs": 3210,
  "pluginVersion": "0.2.11",
  "dimensions": {
    "install": { "dimension": "install", "status": "no-evidence", "score": 0, "weight": 25,
                 "summary": "no dsh-test-drive result recorded for this target (install success unmeasured)",
                 "evidence": [{ "source": "test-drive", "detail": "no test-drive record found in the test_drive domain", "observedAt": "2026-08-16T00:00:00.000Z" }] },
    "maintenance": { "dimension": "maintenance", "status": "pass", "score": 100, "weight": 20,
                     "summary": "active (2026-08-10T00:00:00Z; 0 open issues)",
                     "evidence": [{ "source": "gh-api", "detail": "last activity 2026-08-10T00:00:00Z", "observedAt": "2026-08-16T00:00:00.000Z" }] }
  },
  "total": 88,
  "grade": "B",
  "verdict": "healthy (weighted total 88/100)"
}
```

Scoring: the total is a weighted average over dimensions that gathered evidence 