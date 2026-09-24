# dsh-data-quality
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-data-quality` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-data-quality)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-data-quality?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-data-quality?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-data-quality/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-data-quality)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-data-quality.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

[![npm version](https://img.shields.io/npm/v/dsh-data-quality.svg)](https://www.npmjs.com/package/dsh-data-quality)
[![npm downloads](https://img.shields.io/npm/dm/dsh-data-quality.svg)](https://www.npmjs.com/package/dsh-data-quality)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-data-quality/ci.yml?branch=main)](https://github.com/PerryLink/dsh-data-quality/actions)


**Deterministic data profiling, cleaning, and verification for DeepSeek Harness.**

All computation is plain TypeScript in the harness process — the model never does the math. A `ctx.dataQuality` capability seam (Service Definition / local Provider / tool Consumers) exposes three model tools plus a frozen cross-plugin citation-checking contract.

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

## Compatibility

| Component | Version |
|---|---|
| DeepSeek Harness | `dsh-v0.1.7-alpha.2` (adapted 2026-09-18): the peer range now admits the alpha.2 line; there `Session.append`'s third parameter exists only for surface-eligible types and is a `SurfaceIntent`, so the audit gate still skips and the storage-domain report stays the durable copy. Verified 2026-09-18 (dual typecheck rulers + full test suite green). |
| Node.js | `^22.19.0 \|\| >=24.0.0` |
| Package manager | `pnpm@11.7.0` |
| Platform | Windows / macOS / Linux (host-only plugin) |

## What you get

- **`ctx.dataQuality` service** — a Cordis service other plugins may optionally consume (`inject = ['dataQuality']`). Besides the three dataset operations behind the tools, it implements the frozen `verifyCitations(request)` contract: verify that numbers/strings cited in a document match a dataset snapshot, with relative-tolerance numeric comparison and `verified` / `mismatch` / `not-found` / `unverifiable` statuses.
- **`data_profile` tool** — dataset profiling: row/column counts, inferred column types (number/date/boolean/string/empty/mixed), missing rates, unique counts, numeric distributions (min/max/mean/median/p25/p75), IQR outlier counts, mixed-type suspicion notes, and full-table sha256 content-hash duplicate detection with the duplicate rate and a bounded sample of duplicate row indexes. Adds a deterministic DAMA six-dimension scorecard (completeness, uniqueness, validity, consistency, timeliness, accuracy — accuracy is reported undetermined without a declared schema, never fabricated). Optional deterministic systematic sampling for large files.
- **`data_clean` tool** — ordered declarative cleaning rules: `dedupe` (by column group), `fill-missing` (constant/mean/median/forward), `coerce-type` (number/date/boolean; failures counted and set to missing), `normalize-unit` (e.g. 万/亿 suffixes to base units), `trim`, `map-values` (enum mapping). Returns a per-rule audit log, a pre-delivery contract validation summary (dedupe before/after, uniqueness, non-null and type regressions), and a bounded preview; writes the cleaned dataset only when `outputPath` is given, and never overwrites the source.
- **`data_verify` tool** — declarative verification rules: `not-null`, `unique`, `range`, `regex`, `enum`, `cross-column` (e.g. `startDate < endDate`), `freshness` (date column within N days of a reference date). Per-rule pass/fail with capped failing-row evidence; an overall failure is a normal `passed: false` result, not a tool error.
- **`data_report` tool** — read persisted reports back from the `data_quality` storage domain: by exact `reportKey` (path-safe validation, missing keys fail loud) or by `kind` (chronological listing). Returns the report envelope(s) — kind, dataset, timestamp, and the full stored report. `format: html` renders one profile/clean report as a self-contained offline HTML document (inline CSS/JS, no external requests) with the DAMA six-dimension scorecard and the profile/cleaning summary tables.
- **Durable reports** — every profile/clean/verify/citation run persists to the `data_quality` storage domain (JSON backend), keyed by run timestamp plus a dataset-path fingerprint; the key is returned as `reportKey` in tool results. Clean reports also persist the bounded preview and the contract summary, so every model-visible result is reconstructable from its `reportKey`; each clean run additionally persists a `clean-diff` before/after profile report.
- **Session events** — on hosts that can carry them safely, runs append `data-quality/profile` / `data-quality/clean` / `data-quality/verify` events (with the `ignorable` marker where supported). On the published `0.1.7-alpha.2` line (as on earlier rc lines) the append is skipped by design — the storage-domain report is always the durable copy (see "Known limitations").

## Quick start

### npm channel

```sh
dsh plugin --profile web add dsh-data-quality
```

### Tarball channel (no build permission needed)

```sh
pnpm pack                                  # produces dsh-data-quality-<version>.tgz
dsh plugin --profile web add ./dsh-data-quality-<version>.tgz
```

### Git channel

```sh
dsh plugin --profile web add github:YOUR_ORG/dsh-data-quality#<commit-sha>
```

The first `add` fails because pnpm blocks the package's `prepare` build; copy the exact key pnpm printed into the profile's `pnpm-workspace.yaml` and re-run:

```yaml
allowBuilds:
  'dsh-data-quality': true
```

Restart the profile after installing (bundles activate on restart). Then ask the agent, in a workspace containing a CSV:

> Profile `holdings.csv`, then clean it by trimming whitespace, deduplicating on `fund_code`, and normalizing the `holding_value` column's 万/亿 units; finally verify `fund_code` is unique and not null.

## Install & uninstall

```sh
dsh plugin --profile web add dsh-data-quality      # install (npm) — or the forms above
dsh plugin --profile web remove dsh-data-quality   # uninstall
```

## Configuration

All keys are optional (defaults shown); invalid values fail loudly at load. Every key is settable from `cordis.yml` (the bundle ships `cordis.patch.yml` with the same defaults).

| Key | Default | Description |
|---|---|---|
| `enabled` | `true` | Master switch; `false` mounts nothing at all. |
| `maxRows` | `200000` | Hard row cap per dataset load; larger inputs reject loudly (use the tool's `sample` parameter). |
| `maxFileSizeMB` | `64` | Hard file-size cap in MiB per dataset load. |
| `defaultTolerance` | `1e-9` | Default relative tolerance for numeric citation comparison when a citation omits `tolerance`. |
| `evidenceRowLimit` | `20` | Cap on failing-row evidence (verify) and preview rows (clean) in one result. |
| `allowedExtensions` | `['.csv', '.tsv', '.json', '.jsonl']` | Extensions accepted as datasets. |
| `workspaceRoot` | `""` | Absolute root for SERVICE-level calls (e.g. `verifyCitations`) that carry no session workspace; empty = the harness process launch directory. Tool calls always use the session's workspace cwd. |
| `storeReports` | `true` | Persist run reports to the `data_quality` storag