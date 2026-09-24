<div align="center">

# 🛡️ dsh-defend
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-defend` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-defend)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-defend?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-defend?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-defend/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-defend)

**Prompt-injection, jailbreak, and secret-leak defense for DeepSeek Harness.**

*Rules decide the known. Interception decides the rest — and everything is audited.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-defend.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-defend/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-defend/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-defend?label=version)](https://github.com/PerryLink/dsh-defend/releases)
[![npm version](https://img.shields.io/npm/v/dsh-defend)](https://www.npmjs.com/package/dsh-defend)
[![npm downloads](https://img.shields.io/npm/dm/dsh-defend)](https://www.npmjs.com/package/dsh-defend)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (verified 2026-09-22; peer ranges `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0`). On this line `Session.append`'s third argument exists only for surface-eligible event types and is a `SurfaceIntent`, so the non-surface `defend/detection` type still cannot stamp the `ignorable` marker: session-log audit stays fail-closed-disabled and `/defend` renders that state explicitly. Session format V4 has no `tool-result` content block — this plugin never produced one, and its two content walkers keep a **read-only** fallback for the retired V3 wrapper so sessions written before the upgrade still scan. Verified 2026-09-22 (dual typecheck rulers + full test suite + build + self-contained/artifacts gates + pack; exactly one copy of the host type graph). |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | All (pure host; no native code, no network) |
| Model | Any (detection runs before content reaches the model) |

## What you get

`dsh-defend` puts two independent layers in front of the agent:

1. **Destructive-delete guard** — the executable form of the 8·14/8·16 postmortem lesson. On `tools/pre-execute`, recursively deleting shell commands are refused unless **every** target is an explicit absolute path inside the session workspace and outside the protected prefixes (home config, `.dsh`/`.claude`, system directories). Dry-run markers (`-WhatIf`, `--dry-run`, `git clean -n`) pass, because they are exactly the check the lesson demands.
2. **Detection layer** — ported from four upstream assets (all Apache-2.0, see THIRD_PARTY_NOTICES.md): 25 Prompt-Injection-Payloads rules, 25 Jailbreak-Detector patterns through a pure-TypeScript Aho-Corasick automaton, 12 secret grammars from Secret-Key-Leaker-Detect plus the issuers' public references, and the Prompt-Attack-Dataset kept verbatim as the regression benchmark.

Three interception points, one decision model each:

| Point | Scanned | Decision |
|---|---|---|
| `agent/pre-step` | inbound user messages | allow → `next()`; ask → approval; block → reject the step |
| `tools/pre-execute` | tool arguments | allow → `next()`; ask → approval; block → deny |
| `tools/post-execute` | tool results | allow → `next()`; ask → approval; block → corrective feedback |

Defaults: `ask` for every family, `block` for **critical** secrets (the upstream interrupt-on-sight semantics). No approval answerer = fail closed. Every pass-through calls `next()` — downstream policy plugins are never short-circuited.

```text
inbound message ── agent/pre-step ── scan ── clean → next()/enter
tool arguments ── tools/pre-execute ── scan ── allow → next()
tool results   ── tools/post-execute ── scan ── block → feedback
                                  │
                                  └─ defend/detection audit (rule id, family,
                                     severity, decision — never matched text)
```

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-defend#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-defend

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A3 'id: dsh-defend'
```

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-defend#main"` — the `prepare` script builds with production dependencies only.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-defend`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-defend-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-defend` (or remove the row from the profile patch).

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). An id-targeted override replaces the whole row — restate every key you need. `cordis.patch.yml` documents each key inline.

| Key | Default | Meaning |
|---|---|---|
| `enabled` | `true` | Master switch for both layers |
| `action` | `deny` | Destructive-delete guard action (`deny` / `ask`) |
| `toolNames` | `['bash','persistent-bash','terminal-bash']` | Tool names whose command arguments the guard reviews |
| `detection.enabled` | `true` | Detection-layer switch |
| `detection.maxScanChars` | `10000` | Scan cap per interception (head only) |
| `detection.normalizeUnicode` | `true` | NFKC-normalize text before scanning (blocks lookalike-Unicode bypass) |
| `detection.secretMinEntropy` | `3.0` | Minimum Shannon entropy (bits/char) to admit a secret regex hit; `0` disables |
| `detection.injectionAction` | `ask` | Injection family: `allow` / `ask` / `block` |
| `detection.jailbreakAction` | `ask` | Jailbreak family: `allow` / `ask` / `block` |
| `detection.secretAction` | `ask` | Secret family: `allow` / `ask` / `block` |
| `detection.secretBlockCritical` | `true` | Critical secrets always block regardless of `secretAction` |
| `detection.audit` | `true` | Write `defend/detection` session audit events |
| `detection.allowUnmarkedAudit` | `false` | Keep writing session audit on hosts whose `Session.append` predates the `ignorable` marker (every released line so far) or that fail-closed on unknown event types (host `0.1.2-rc.1`+), accepting the unresumable-session hazard |
| `detection.maxReportEntries` | `200` | In-memory report ring-buffer cap |
| `registerCommand` | `true` | Register the `/defend` command |
| `registerTool` | `true` | Register the `defend_report` tool |

## Tools & surfaces

| Surface | Kind | Notes |
|---|---|---|
| `defend_report` | tool | Totals (recorded/blocked/asked), per-family counts, and the 20 most recent matches — never matched text |
| `/defend` | command | The same summary as text |
| `agent/pre-step` | listener | Inbound message scanning (enter/reject) |
| `tools/pre-execute` | listen