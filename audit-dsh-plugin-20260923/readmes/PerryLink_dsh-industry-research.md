<div align="center">

# 🏭 dsh-industry-research
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-industry-research` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-industry-research)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-industry-research?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-industry-research?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-industry-research/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-industry-research)

**Industry and company research domain pack for DeepSeek Harness.**

*Chain maps, public-source tracking, company cards, and auditable reports — every number traces to a source, every gap is declared.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-industry-research.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-top-rated.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-industry-research/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-industry-research/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-industry-research?label=version)](https://github.com/PerryLink/dsh-industry-research/releases)
[![npm version](https://img.shields.io/npm/v/dsh-industry-research)](https://www.npmjs.com/package/dsh-industry-research)
[![npm downloads](https://img.shields.io/npm/dm/dsh-industry-research)](https://www.npmjs.com/package/dsh-industry-research)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

**Research only, not investment advice.** This pack does research support only: no trading, no price prediction, no paid/login-walled sources.

## Compatibility

- DeepSeek Harness `dsh-v0.1.7-alpha.2` (published npm line, verified 2026-09-18; peers `>=0.1.2-rc.1 <0.2.0 || >=0.1.5-alpha.1 <0.2.0 || >=0.1.6-0 <0.2.0 || >=0.1.7-0 <0.2.0`).
0.1.2-rc.1 (adapted 2026-09-02): the session envelope keeps its ignorable field for stored-log read compatibility only - Session.append still cannot stamp it, so audit-gate behavior is unchanged.
Verified 2026-09-18 against the `0.1.7-alpha.2` published peers (full gate chain; the real profile install smoke runs in the weekly and per-PR `compat.yml` job).
- Node `^22.19.0 || >=24.0.0`, ESM only (`"type": "module"`).
- Peer dependencies: `@deepseek-ai/cordis ^4.0.2`, `@deepseek-ai/schemastery ^3.18.2`, and `@deepseek-ai/dsh-tools`, `@deepseek-ai/dsh-skill`, `@deepseek-ai/dsh-skill-filesystem` at `>=0.1.2-rc.1 <0.2.0 || >=0.1.5-alpha.1 <0.2.0 || >=0.1.6-0 <0.2.0 || >=0.1.7-0 <0.2.0` (all composed by the official `dsh-base` bundle).
- Optional, looked up at execution time (never injected): `ctx.web` (public-source retrieval — composed by `dsh-base`) and `ctx.researchReport` (the sibling `dsh-research-report` sealing engine).

## What you get

- **`industry_map`** — build or update an industry chain map (`chain.json`): upstream/midstream/downstream nodes, edges, and metric slots. A metric with a `value` must carry a `sourceRef`; a value-less slot is an explicit gap. Node `status` assertions carry a `statusAsOf`, and an optional `taxonomyCode` must hit the built-in 国民经济行业分类 大类 table. With `renderSvg: true` it also writes a deterministic, tier-layered `chain.svg` network diagram with funnel/hub bottleneck highlighting. A `depth` argument scales the web assist (quick/standard/comprehensive). Seed notes/files and an optional `ctx.web` digest are registered as citable sources (`S1`, `S2`, …).
- **`industry_track`** — public-source policy/news tracking over the official `ctx.web` seam: per-topic search, host allow/block lists, `since` filtering, bounded snapshot fetches with SHA-256 provenance hashes, and append + dedupe into `timeline.jsonl` with a retention cap. Entries may carry a validated `evidenceCategory`; a `depth` argument scales source counts. Fails loud when the web capability is unreachable.
- **`company_scan`** — company cards (`card.json` + `card.md`) from your workspace data files (SHA-256-hashed, with Markdown outlines and figure-candidate lines so every number cites a file and a line), plus an optional `ctx.web` citation complement. Cards carry a listing `status` (with `statusAsOf`), a format-checked `ticker`, and sourced price/value `metrics` (each with `source` + `asOf`). Batch mode (`companies`) isolates one bad company without aborting the batch; `depth` scales the web complement. Text formats only in v1 (no PDF).
- **`industry_report`** — one auditable report from the map + timeline + cards. Before producing, a deterministic delivery contract checks blocks, status/price assertions, and placeholder residue (fail loud, no half-assembled report). Timeline entries are grouped by `evidenceCategory`. A deterministic bull/bear (正反方) synthesis lists sourced, dated values against declared gaps and data-quality findings, is embedded as the report's multi-perspective section, and is forked as a subagent job writing `perspectives-note.md` into the version ledger. With a mounted `ctx.researchReport` engine the evidence/sections/claims are sealed by its `assemble` and per-claim verdicts come back; without one, the builtin fallback writes versioned `reports/<YYYYMMDD-HHmmss>/report.md` + `manifest.json` with a SHA-256 source-traceability table and honestly labels `engine: 'builtin-fallback'`.
- **Artifact version ledger** — `industry_map` / `company_scan` / `industry_report` append to `versions.jsonl` (root-relative path + SHA-256 + timestamp + change type) on every artifact write; reads verify the hash and fail loud on mismatch.
- **Two methodology skills** — `industry-research-method` (chain decomposition, supply/demand framework, sourcing discipline, gap-declaration discipline) and `company-research-method` (company framework, public-source list, compliance wording).
- **Typed Cordis events** — `industry-research/map`, `industry-research/track`, `industry-research/report` emitted after each committed artifact.

## Quick start

### git channel

```sh
# From a scratch profile (pins the commit; runs the self-contained `prepare` build)
dsh plugin --profile demo add "github:PerryLink/dsh-industry-research#<sha>"
# The profile's pnpm-workspace.yaml gains an allowBuilds entry for dsh-industry-research on first add.
```

### npm channel

```sh
dsh plugin --profile demo add dsh-industry-research
```

Both channels install the bundle row (see `cordis.patch.yml`) into the profile's `dsh.profile.bundles` stack and take effect on restart.

Then, in a session:

```
加载 industry-research-method 技能，然后研究白酒行业：
先 industry_map 建产业链图，再 industry_track 跟踪政策，最后 industry_report 出报告。
```

## Install & uninstall

```sh
dsh plugin --profile demo add dsh-industry-research       # install
dsh plugin --profile demo remove dsh-industry-research    # uninstall
```

Verify the row mounts: `dsh --profile demo --dump-config | grep dsh-industry-research`.

## Configuration

All tunables are Schemastery `Config` fields; invalid values fail the profile load loudly.

| Key | Default | Description |
| --- | --- | --- |
| `enabled` | `true` | Master switch; `false` mounts nothing. |
| `industryRoot` | `industry-research` | Artifact root, relative to the session workspace (or absolute). |
| `fetchTimeoutMs` | `20000` | Per-request timeou