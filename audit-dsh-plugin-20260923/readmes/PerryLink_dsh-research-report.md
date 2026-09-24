<div align="center">

# 📑 dsh-research-report
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-research-report` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-research-report)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-research-report?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-research-report?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-research-report/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-research-report)

**A verifiable research-report engine for DeepSeek Harness.**

*Every claim is bound to immutable evidence snapshots, verified byte-for-byte, and sealed into a versioned report whose manifest hash anyone can recompute.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-research-report.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-top-rated.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-research-report/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-research-report/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-research-report?label=version)](https://github.com/PerryLink/dsh-research-report/releases)
[![npm version](https://img.shields.io/npm/v/dsh-research-report)](https://www.npmjs.com/package/dsh-research-report)
[![npm downloads](https://img.shields.io/npm/dm/dsh-research-report)](https://www.npmjs.com/package/dsh-research-report)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

- DeepSeek Harness `dsh-v0.1.7-alpha.2` (verified 2026-09-18). npm dev/test line `0.1.7-alpha.2`; peers `>=0.1.2-rc.1 <0.2.0 || >=0.1.5-alpha.1 <0.2.0 || >=0.1.6-0 <0.2.0 || >=0.1.7-0 <0.2.0`. The compat matrix pins all four declared peer lines. On this line `Session.append`'s third parameter is a `SurfaceIntent` for surface-eligible types only, so `research-report/*` events still do not land in the session log: the ledger journals are the durable source of truth and the audit mirror activates only once a host knows the vocabulary (the regression lock in `test/events-gate.spec.ts` pins that).
0.1.5-alpha.1 (adapted 2026-09-09): the session envelope keeps its ignorable field for stored-log read compatibility only - Session.append still cannot stamp it, so audit-gate behavior is unchanged. Verified 2026-09-11 against the published 0.1.5-rc.2 types (full local gate chain); the compat workflow pins both declared peer lines.
- Node `^22.19.0 || >=24.0.0`, ESM only (`"type": "module"`).
- Peer dependencies: `@deepseek-ai/cordis ^4.0.2`, `@deepseek-ai/schemastery ^3.18.2`, and `@deepseek-ai/dsh-session`, `@deepseek-ai/dsh-tools`, `@deepseek-ai/dsh-system-prompt`, `@deepseek-ai/dsh-web`, `@deepseek-ai/dsh-jobs` at `>=0.1.2-rc.1 <0.2.0 || >=0.1.5-alpha.1 <0.2.0 || >=0.1.6-0 <0.2.0 || >=0.1.7-0 <0.2.0`.
- Optional siblings (never required): `ctx.web` providers for URL capture/gather, `ctx.jobs` for background assembly, `ctx.dataQuality` (dsh-data-quality) for dataset citation cross-checks.

## What you get

- **Evidence ledger** — a content-addressed snapshot store (`<ledgerRoot>/objects/<sha256>` + JSONL journals). The same content is stored exactly once; snapshots are immutable; every read recomputes the hash, so tampering or deletion is detected instead of trusted.
- **Claim ↔ evidence binding** — claims register with the evidence ids they rely on; the ledger keeps the binding and every verification verdict (latest wins).
- **Byte-level verification** — every number and quoted span in a claim must be locatable verbatim in the bound snapshots. No bound evidence, or no checkable literal, marks the claim `unverified`; bound evidence that cannot confirm or deny the claimed literals marks it `insufficient`; a label whose snapshot value differs (the claimed value absent) marks it `disproven`; tampered/missing snapshots mark it `contradicted`. No semantics, no embeddings — auditable byte checks.
- **Optional numeric bridge** — when a claim cites a structured workspace dataset (CSV/JSON) and `dsh-data-quality` is mounted, citations are cross-checked with tolerances through its frozen `verifyCitations` contract; a dataset mismatch disproves the claim.
- **DOI evidence (zero network)** — DOI origins are validated deterministically (`10.xxxx/xxxx` structure, a prefix whitelist, and a DOI character set); invalid DOIs fail loud. Optional journal/year metadata is accepted, and `requireJournalMetadata` gates academic DOI evidence only when enabled.
- **Versioned sealed reports** — `<reportRoot>/<slug(topic)>/<YYYYMMDD-HHmmss>/report.md` + `manifest.json` + `verification.jsonl` + `disconfirmation.jsonl`; the seal hash is the SHA-256 of the manifest, which itself carries the report hash, every evidence hash, and the hash of each audit journal.
- **Pre-delivery re-audit & seal interception** — before sealing, every bound claim is re-verified offline and journaled to `verification.jsonl`; verdict drift, tampered/missing bound evidence, or a journal serialization failure blocks the seal (fail loud, no tunable).
- **Falsification ledger** — every contradicted or disproven claim is recorded in `disconfirmation.jsonl` (claim + evidence references + reason) and listed in the report's `falsification log` appendix.
- **Negative knowledge** — a disproven claim is remembered by its content hash (`disproofs.jsonl`); the same text re-reported against unchanged evidence is forced back to `disproven` and only re-verifies once the evidence changes.
- **Read-only verifier loop** — after sealing, a deterministic `verifySealedReport` fallback (zero network, zero model) recomputes the seal and audit hashes and re-checks every claim, writing the machine check to `verifier-note.md`; when `ctx.jobs` is mounted a read-only verifier job is also spawned (the model review is an enhancement, never a replacement).
- **Standalone verifier CLI** — `dsh-research-verify --report <dir> [--seal <sha256>] [--ledger <dir>] [--format json|sarif]` recomputes the seal hash + per-claim re-checks from the sealed directory alone and prints a JSON envelope or a SARIF 2.1.0 document (see [Verifier CLI](#verifier-cli)).
- **Session-anchored evidence** — `evidence_add` accepts an optional `sessionRef` (`sessionId` + `eventRange`, validated loud); the anchor is stored, rendered in Appendix B, and registered in the manifest and `verification.jsonl`. Session-anchored evidence verifies honestly as `unverified` (`session-anchored evidence requires a manual check against the session log`).
- **Honest gaps** — unverified, insufficient, contradicted, and disproven claims keep a visible `[未核实]` / `[证据不足]` / `[与证据矛盾]` / `[已证伪]` marker in the report body and are listed in Appendix A. Nothing is silently passed.
- **No deep-research loop** — retrieval orchestration is deliberately reused: `ctx.web` for search/fetch, `ctx.jobs` for long runs. Planning and synthesis stay with the model (or an upstream plugin).

## Quick start

### git channel

```sh
# From a scratch profile (pins the commit; runs the self-contained `prepare` build)
dsh plugin --profile demo add "github:YOUR_ORG/dsh-research-report#<sha>"
# The profile's pnpm-workspace.yaml gains an allowBuilds entry for dsh-research-report on first add.
```