<div align="center">

# dsh-mask
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-mask` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-mask)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-mask?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-mask?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-mask/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-mask)

**PII masking middleware for DeepSeek Harness — anonymize personal data before it reaches the model, keep it reversible host-side.**

*Phones, emails, ID cards, bank cards, keys, and more become placeholders at the model boundary; the plaintext never enters your session log.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-mask.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-mask/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-mask/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-mask?label=version)](https://github.com/PerryLink/dsh-mask/releases)
[![npm version](https://img.shields.io/npm/v/dsh-mask)](https://www.npmjs.com/package/dsh-mask)
[![npm downloads](https://img.shields.io/npm/dm/dsh-mask)](https://www.npmjs.com/package/dsh-mask)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (adapted 2026-09-18): the session envelope keeps its ignorable field for stored-log read compatibility only - Session.append still cannot stamp it, so audit-gate behavior is unchanged. Verified 2026-09-18 against the dsh-v0.1.7-alpha.1 master checkout (full gate chain + profile install smoke). |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | Anywhere DSH runs (pure host, zero-dependency regex; no browser half) |
| Model | Text models fully supported; no extra model capability required |

## What you get

`dsh-mask` anonymizes personal data **at the model boundary** — before a message reaches the model — and keeps a restore table host-side so placeholders stay reversible:

- **Request-time masking** — `agent/pre-step` messages are rewritten so phones, emails, ID cards, bank cards, and keys (on by default) and IPs (opt-in) become `<PHONE_1>`-style placeholders. The masked text is what gets logged and sent to the model.
- **Restore table** — the `placeholder → original` map lives only in memory and a controlled storage domain (`dsh_mask`); the plaintext never enters the session log.
- **Audit, not plaintext** — the `mask/applied` session event records only "replaced N values + type distribution", never the original text or the mapping.
- **`/mask` command** — `status` (counts + distribution), `on`/`off` (runtime toggle), `restore <text>` (unmap placeholders), `help`.
- **`mask_test` tool** — run a snippet through the detector and see the placeholder result; it never reveals the original values.

```text
user message ──agent/pre-step──▶ placeholders ──model──▶ placeholders ──restore──▶ display
                                   ▲                                                    │
                                   └──────── restore table (memory + dsh_mask) ────────┘
```

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-mask#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-mask

# 2. verify the row mounts
dsh --profile web --dump-config | grep -A2 'id: mask'
```

Then tailor the entity list in your profile patch:

```yaml
- insert:
    - id: mask
      name: dsh-mask
      config:
        entities: [phone, email, id-card, bank-card, key]
```

```
> /mask status
> /mask restore <PHONE_1>
```

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-mask#main"` (equivalent to installing from `git+https://github.com/PerryLink/dsh-mask.git`). No build step — `index.mjs` and `lib/` are the shipped artifacts.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-mask`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-mask-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-mask` (or remove the row from the profile patch).

`dsh-mask` no longer bundles the storage stack. Profiles that already compose it (the `web` profile does, via `@deepseek-ai/dsh-web-app`) provide `storageDomain`, so persistence works out of the box. On a bare profile without storage the plugin still mounts and masks, but the restore table is memory-only (lost on restart) — compose the storage stack in your profile patch, or set `persistRestoreTable: false`.

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). An id-targeted override replaces the whole row — restate every key you need. `cordis.patch.yml` documents each key inline.

| Key | Default | Meaning |
|---|---|---|
| `enabled` | `true` | Master switch; `false` unregisters the listener, the `/mask` command, and the `mask_test` tool |
| `mode` | `regex` | Detection mode; only `regex` is implemented (`regex+ner` for name/address recognition is reserved and fails loud) |
| `entities` | `[phone, email, id-card, bank-card, key]` | Which PII types to mask; `ip` is also regex-capable (opt-in), `person`/`address` require NER |
| `scope` | `[messages]` | Masking surface(s); `messages` masks agent/pre-step messages, `tools` masks tool-result text on tools/post-execute. Accepts a string or an array, e.g. `[messages, tools]` |
| `registerCommand` | `true` | Register the `/mask` command |
| `registerTools` | `true` | Register the `mask_test` tool when the tools service is present |
| `persistRestoreTable` | `true` | Persist the restore table to the controlled `dsh_mask` storage domain (`false` = memory only) |
| `maxRestoreEntriesPerSession` | `500` | Per-session restore entry cap (oldest evicted first) |
| `maxSessions` | `1000` | In-memory session cap (least-recently-used evicted, mapping reloaded on demand) |
| `maskClientEnabled` | `false` | Feature flag for the browser half "reveal" bubble (defensive; off by default until the live slot catalog verifies the target slot). The key is schema-declared and validated, but no runtime code reads it yet, so it changes nothing until the browser half ships |

Example override in your profile patch:

```yaml
- insert:
    - id: mask
      name: dsh-mask
      config:
        entities: [phone, email, id-card, bank-card, key, ip]
        persistRestoreTable: false
        registerCommand: true
```

## Tools & surfaces

| Surface | Reveals plaintext | Notes |
|---|---|---|
| `agent/pre-step` masking | never | Rewrites messages to placeholders before they are logged or sent to the model |
| `tools/post-execute` masking | never | Rewrites tool-result text blocks to placeholders before they are logged or fed back to the model (scope: `tools`) |
| `/mask status` | never | Enabled state, total replaced, type distribution |
| `/mask on` / `/mask off` | never | Runtime toggle (resets to `config.enabled` on restart) |
| `/mask restore <text>` | yes (explicit) | U