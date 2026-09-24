<div align="center">

# 🐳 dsh-plugin-guide
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-plugin-guide` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-plugin-guide)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-plugin-guide?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-plugin-guide?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-plugin-guide/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-plugin-guide)

**Everything you need to build [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) plugins.**

*Official docs archive · Cordis primer · community deep-dives · battle-tested pitfalls · agent skill · CLI toolchain*

> **Official repository.** This is the only official repository of dsh-plugin-guide, maintained by PerryLink. Same-name repositories under other accounts are not affiliated.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-plugin-guide.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-top-rated.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-plugin-guide/verify.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-plugin-guide/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-plugin-guide?label=version)](https://github.com/PerryLink/dsh-plugin-guide/releases)
[![npm version](https://img.shields.io/npm/v/dsh-plugin-guide)](https://www.npmjs.com/package/dsh-plugin-guide)
[![npm downloads](https://img.shields.io/npm/dm/dsh-plugin-guide)](https://www.npmjs.com/package/dsh-plugin-guide)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (re-synced 2026-09-18, `ddefc45`): the official-docs snapshot is refreshed to alpha.2, the checker now expects the four-clause peer range (`… || >=0.1.6-0 <0.2.0 || >=0.1.7-0 <0.2.0`) single-sourced from the scaffold templates, and a new red line fails `async apply` functions that register after their first `await`. Local gate chain green (40 tests, typecheck, `verify` dogfood); the compat job's real alpha.2 run lands with the next CI push. |
| Node | `^22.19.0 || >=24.0.0` (DeepSeek Harness runtime) |
| Platforms | All (plain ESM bundle; no native code, no network) |
| Model | Any (no model interaction) |

## What you get

`dsh-plugin-guide` is the DSH plugin-development knowledge base plus a CLI toolchain, packaged as one installable bundle. The knowledge base registers as the `dsh-plugin-guide` agent skill (visible in every session catalog, loading workflow steps, official docs, and community deep-dives on demand); the `dsh-plugin-dev` CLI adds three mechanical layers on top of it.

- **Plugin contract & hard rules** — effects/disposers, waterfall `next()`, model-visible ⟺ logged, Schemastery config.
- **Official docs archive** — a verbatim copy of the official repo docs (EN + ZH), byte-identical to upstream at the last verified snapshot.
- **Cordis primer** — the five concepts and the mechanism timeline (repository-plugin introduced 0809, removed 0811; the two install channels).
- **20+ real-world pitfalls** with root cause + fix (cordis dual copies, tsconfig trio, multi-frame zstd sessions, Windows junctions, stale npm `latest`, …).
- **Community deep-dives** — 114 community repositories archived (15 deep-dived), plus a full source index where every fact links to its origin.
- **CLI toolchain** — `dsh-plugin-dev new / check / verify`: scaffold, static-check, and pack-verify DSH plugins; every check links back to the skill section it enforces.

## Knowledge base

| Path | What it is |
|---|---|
| `SKILL.md` | The `dsh-plugin-guide` agent skill: hard rules + task-based development paths |
| `package.json` · `cordis.patch.yml` · `index.js` | The installable DSH bundle: `dsh.bundle.patch` manifest + entry point that registers the skill |
| `guide/plugin-dev-guide.md` | The complete development guide (10 chapters) |
| `guide/quick-reference.md` | One-page cheat sheet (5 languages) |
| `guide/links.md` | Curated URL index: official dev docs (site ↔ local copies) + community doc links |
| `references/official-docs/` | Verbatim copy of the official repo docs (EN + ZH) |
| `references/*.md` | Research reports: repo docs, website, Cordis, the paper, community ecosystem, 114-repo archive (15 deep-dived) |
| `scripts/` | Idempotent download scripts + integrity checker + topic snapshot generator |
| `bin/` · `src/cli/` · `dist/` | The `dsh-plugin-dev` CLI: scaffolder, checker, verifier (TypeScript, tsdown-bundled) |
| `templates/` | TS + JS scaffold skeletons: contract template, Config, tests, cordis.patch.yml, five-language READMEs |
| `downloads/` | Raw snapshots — generated by `scripts/`, not committed |

## CLI toolchain

The bundle ships the zero-runtime-dependency `dsh-plugin-dev` CLI (`bin/` → tsdown-bundled `dist/dsh-plugin-dev.js`). Each check cites the skill section it enforces, so an agent can keep auditing manually.

```sh
dsh-plugin-dev new <name> [--lang ts|js] [--dir <path>] [--force] [--git]
dsh-plugin-dev check [--cwd <dir>] [--json] [--strict]
dsh-plugin-dev verify [--cwd <dir>] [--dsh <bin>] [--pnpm <bin>]
```

| Subcommand | What it does |
|---|---|
| `new <name>` | Scaffolds a TS or JS plugin repo: `src/index.ts` contract template, Schemastery Config, tests, tsdown/vitest, commented `cordis.patch.yml`, five-language READMEs. Idempotent; refuses non-empty targets without `--force`. |
| `check` | Static checks: `cordis.patch.yml` validity, `package.json` metadata (`dsh.bundle.patch` pointer, peer deps, engines, files whitelist), five-language README consistency, engineering red-line patterns. Emits CI-consumable JSON. |
| `verify` | `pnpm pack`, then install/start/uninstall the bundle in a clean mkdtemp `DSH_HOME` profile (aligned with `verify:self-contained`). Failures report the log tail plus suggestions. |

### CLI configuration

The CLI has no hardcoded tunables — each is a flag or an environment variable.

| Tunable | Flag | Env | Default |
|---|---|---|---|
| Templates directory | — | `DSH_PLUGIN_DEV_TEMPLATES` | `<package>/templates` |
| dsh binary | `--dsh` | `DSH_PLUGIN_DEV_DSH` | `dsh` |
| pnpm binary | `--pnpm` | `DSH_PLUGIN_DEV_PNPM` | `pnpm` |
| Install/pack timeout | `--timeout` | `DSH_PLUGIN_DEV_TIMEOUT` | `300000` ms |
| Headless smoke timeout | `--smoke-timeout` | `DSH_PLUGIN_DEV_SMOKE_TIMEOUT` | `120000` ms |

### Upstream roadmap

`dsh-plugin-dev` is an upstream candidate for the official plugin-development CLI (planned item C12): the scaffolder/checker/verifier are the mechanical layers, while `SKILL.md` + `guide/` stay the cognitive layer.

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-plugin-guide#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-plugin-guide

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A3 'id: dsh-plugin-guide'
```

Then just ask your agent: *"Use the dsh-plugin-guide skill to build me a … plugin."*

Or drive the CLI directly:

```sh
npx dsh-plugin-guide new hello-plugin            # scaffold a TS plugin repo
npx dsh-plugin-guide check -