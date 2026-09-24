<div align="center">

# 📊 dsh-fund-research
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-fund-research` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-fund-research)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-fund-research?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-fund-research?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-fund-research/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-fund-research)

**Deterministic research reports for Chinese public mutual funds, on DeepSeek Harness.**

*Every key number in every report traces back to a hashed source snapshot — gaps declared, never invented. Research only; not investment advice.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-🧩-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-fund-research.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-fund-research/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-fund-research/actions)
[![npm version](https://img.shields.io/npm/v/dsh-fund-research)](https://www.npmjs.com/package/dsh-fund-research)
[![npm downloads](https://img.shields.io/npm/dm/dsh-fund-research)](https://www.npmjs.com/package/dsh-fund-research)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Component | Version |
|---|---|
| DeepSeek Harness | `dsh-v0.1.7-alpha.2` (peer range admits the alpha.2 line: `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0`). On this line `Session.append`'s third parameter is a `SurfaceIntent` for surface-eligible types only, so the `fund-research/*` audit events stay unappended (the tool results and sealed snapshot/report remain the audit trail). Verified 2026-09-18 (dual typecheck rulers + 176 tests). |
| Node.js | `^22.19.0 \|\| >=24.0.0` |
| Package manager | `pnpm@11.7.0` |
| Platform | Windows / macOS / Linux (host-only plugin) |
| Data sources | Tiantian Fund / Eastmoney public endpoints (no key, no login) |

## What you get

- **`fund_research` tool** — one fund code in, a versioned Markdown research report out: overview, performance decomposition, holdings penetration, simplified style attribution, manager profile, risk & gap declarations, disclaimer, and a **number-traceability appendix** mapping every key figure to its snapshot JSON path and verification verdict. Sealed to `fund-reports/{code}/{YYYYMMDD-HHmmss}/` as `report.md` + `manifest.json` + `snapshot.json`. `background: true` runs it as a `fund-report` background job.
- **`fund_snapshot` tool** — a light snapshot card (latest NAV, published stage returns, scale, manager, top-3 holdings) sealed into the fund's day directory.
- **Deterministic metrics, zero model arithmetic** — period/annualized return, volatility, max drawdown, Sharpe; top-N concentration, HHI, industry distribution, quarter-over-quarter holdings comparison; size-value style bands; manager tenure and peer comparison. All pure functions over the sealed snapshot.
- **Traceability as a first-class feature** — before sealing, every key number is checked against the sealed `snapshot.json` through the optional [`dsh-data-quality`](https://github.com/topics/dsh-plugin) service when it is installed, or through the built-in isomorphic fallback checker (`builtin-fallback`) otherwise. The appendix table records value ↔ path ↔ verdict.
- **Honest gaps** — a failed or degraded data source produces an explicit data-gap declaration in the affected section. The plugin never fills a gap with an invented number.
- **Offline mode** — `offline: true` (config or tool argument) serves everything from the storage-domain snapshot layer or the newest on-disk version snapshot, with zero outbound requests. Ideal for tests and reproduction.
- **asOf cutoff** — `asOfDate` (ISO `YYYY-MM-DD`) truncates the NAV series to data on or before that date and stamps the snapshot + report with the cutoff; invalid or future dates fail loudly.
- **Checkpoint resume** — `<reportRoot>/.run-state.json` records each pipeline stage (snapshot/report) with timestamps and an input fingerprint; `resume: true` continues from the first incomplete stage, reusing sealed artifacts, and rejects a fingerprint mismatch.
- **Source discovery record** — every acquisition seals a code-generated `sources-discovery.json` (endpoint roster, primary/fallback resolution, per-source coverage and gaps, degradation reasons) and folds it into the report appendix as 数据源与缺口声明.
- **Multi-fund fan-out** — `codes` accepts an array of fund codes; each fund runs the pipeline independently with per-fund failure isolation (failures become summary gaps), and the result is a summary card (code / asOf / seal hash / verdicts / failure reason).
- **Tracking ledger** — every successful seal appends a deterministic line to `<reportRoot>/.tracking.jsonl`; `includeComparison: true` renders a deterministic 与上次对比 section (NAV range / scale / top holdings) with a gap declaration when no prior record exists.
- **Read-only review** — after sealing, a `fund-review` job reviews the sealed artifacts (gap-declaration completeness, traceability-table consistency, disclaimer) and writes `review-note.md`; it skips gracefully (recorded in run-state) when no jobs service is present.
- **Per-source quality signals** — every source carries deterministic quality metadata (`requested`/`succeeded`/`fieldsPresent`/`parseWarnings`/`degraded`), rendered in the appendix and surfaced in tool values so downstream can downweight (never hard-filter) a low-quality source.
- **Walk-forward stability summary** — `includeWalkForward: true` adds a 样本外稳定性摘要 section: deterministic rolling-window return/Sharpe sign persistence and mean/std, explicitly labelled as statistical description only, not a prediction.
- **Session audit events (host-dependent)** — `fund-research/snapshot` and `fund-research/report` log-only events carry the code, version directory, manifest hash, and gap list (model-visible ⟺ logged) *when the host admits out-of-repo event types*; on `0.1.2-alpha.1`–`0.1.5-alpha.1` hosts the known-type catalog is build-generated in-repo, so the gate appends nothing and the tool results plus sealed artifacts are the audit trail.
- **Methodology skill** — a bundled `fund-research` skill teaches the model the metric口径 (definitions), gap handling, and compliance wording. Computation stays in code.

## Quick start

```text
> 用 fund_research 出一份 161725 的研究报告
```

The agent calls `fund_research({ code: "161725" })`; a minute later the workspace holds:

```text
fund-reports/161725/20260819-153012/
├── snapshot.json            # raw extracted data + computed metrics + per-source sha256
├── sources-discovery.json   # code-generated endpoint roster + coverage + gaps
├── report.md                # the research report with the traceability appendix
└── manifest.json            # snapshot/report hashes, parameters, verify engine, gaps
```

`.run-state.json` sits at the report root and records the pipeline stages for `resume: true`. Every number in `report.md`'s appendix carries a `verified` / `mismatch` / `not-found` / `unverifiable` verdict against `snapshot.json` — recompute any of them from `ra