<div align="center">

# 🔁 dsh-translate
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-translate` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-translate)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-translate?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-translate?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-translate/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-translate)

**Vendor parameter translation and deterministic JSON repair for DeepSeek Harness.**

*Same request, every vendor. Broken JSON, fixed without inventing data.*

> **Official repository.** This is the only official repository of dsh-translate, maintained by PerryLink. Same-name repositories under other accounts are not affiliated.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-translate.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-translate/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-translate/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-translate?label=version)](https://github.com/PerryLink/dsh-translate/releases)
[![npm version](https://img.shields.io/npm/v/dsh-translate)](https://www.npmjs.com/package/dsh-translate)
[![npm downloads](https://img.shields.io/npm/dm/dsh-translate)](https://www.npmjs.com/package/dsh-translate)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | Main version **`dsh-v0.1.7-alpha.2`** (verified 2026-09-18: dual typecheck rulers + `node --test` 80/80 + self-contained/artifacts gates). npm dev/test pins now `0.1.7-alpha.2`; peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0`. |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Form | Pure-host JS plugin (no browser half) |
| Model | Any model — repair is deterministic, no extra model calls |

## What you get

Two independent surfaces, one bundle:

- **`/translate`** — the vendor parameter translation table: `temperature`, `top_p`, `max_tokens`, `stop`, `system`, and 8 more canonical parameters mapped across **11 vendors** (OpenAI, ERNIE, Qwen, Anthropic, Google, DeepSeek, Mistral, Cohere, xAI, Groq, Azure). Ask for a pairwise mapping, list vendors/params, or convert a whole standard request (`transformRequest` in `lib/rosetta.mjs`).
- **The repair layer** — a `tools/post-execute` listener plus the `fix_json` tool. When a successful tool result carries broken JSON as a string (string-rooted or `json`-rooted output schema, or a tool opted in by name), the layer repairs it deterministically: markdown-fence extraction, escape repair, trailing-comma removal, truncation closure, and required-field completion with explicit `null` placeholders. **No value is ever invented** — a result that still violates the schema fails closed, and failed tool results are never flipped into successes.

```text
tool result (success, JSON text) ──▶ extract fence ──▶ parse
    │ ok? ──▶ schema-validate ──▶ accept { kind: 'accept', value }  (registry re-validates + re-renders)
    │ broken ──▶ escape / trailing-comma / close / fill-null ──▶ validate
    │ unrepairable ──▶ next()  (original value preserved) + translate/fix audit (counts only)
```

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-translate#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-translate

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A2 'id: dsh-translate'
```

Then ask the agent to check a mapping or repair a payload:

```
> /translate openai ernie max_tokens
> Use fix_json to repair: {"a": 1,} against {"type":"object","properties":{"a":{"type":"integer"}},"required":["a"]}
```

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-translate#main"` — pure JS, no build step.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-translate`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-translate-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-translate` (or remove the row from the profile patch).

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). An id-targeted override replaces the whole row — restate every key you need. `cordis.patch.yml` documents each key inline.

| Key | Default | Meaning |
|---|---|---|
| `enabled` | `true` | Master switch; `false` registers nothing |
| `repair.enabled` | `true` | Post-execute repair layer switch |
| `repair.toolNames` | `[]` | Extra tool names whose JSON-text results may be repaired (on top of string-rooted / `json`-rooted schemas) |
| `repair.strategies.escapeRepair` | `true` | Escape raw control characters inside strings |
| `repair.strategies.trailingComma` | `true` | Remove commas directly before a closing bracket |
| `repair.strategies.truncationClosure` | `true` | Close an unclosed string or container cut off by truncation |
| `repair.strategies.fieldCompletion` | `true` | Complete missing required fields with explicit `null` placeholders |
| `repair.maxSteps` | `8` | Strategy application budget (repair-loop passes, 1..64) |
| `diffMaxChars` | `200` | Cap on one logged diff fragment, in characters |
| `diffMaxEntries` | `50` | Cap on logged diff entries |
| `registerCommand` | `true` | Register the `/translate` command |
| `registerTool` | `true` | Register the `fix_json` tool |
| `rosettaDataPath` | *(none)* | Optional external rosetta data file (same shape as the bundled `lib/rosetta-data.json`); overrides the built-in mapping table |

Example override in your profile patch:

```yaml
- insert:
    - id: dsh-translate
      name: dsh-translate
      config:
        enabled: true
        repair:
          enabled: true
          toolNames: ['emit-json']
          strategies:
            escapeRepair: true
            trailingComma: true
            truncationClosure: true
            fieldCompletion: true
          maxSteps: 8
        diffMaxChars: 200
        diffMaxEntries: 50
        registerCommand: true
        registerTool: true
```

## Tools & surfaces

| Surface | Kind | Notes |
|---|---|---|
| `/translate` | command | `vendors`, `params`, or `<from> <to> [param]` pairwise mapping |
| `fix_json` | tool | `{ text, schema?, strategies? }` → `{ ok, repaired?, diff?, strategies, truncated, validated, error? }`; diff fragments are bounded and sanitized |
| post-execute repair | listener | Automatic for successful string results from string-rooted / `json`-rooted schemas (plus `repair.toolNames`); always calls `next()` unless it claims the call |

## Permissions & data

- **Permissions**: no network, no subprocess, no credentials — the plugin only consumes the official `commands` and `tools` services and appends to the session log.
- **Data**: repair never fabricates values; the only model-visible additions are the repaired canonical value and the `fix_json` diff. Session audit events (`translate/fix`) carry tool name, call id, strate