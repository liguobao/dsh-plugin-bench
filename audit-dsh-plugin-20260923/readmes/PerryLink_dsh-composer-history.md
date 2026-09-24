<div align="center">

# ⌨️ dsh-composer-history
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-composer-history` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-composer-history)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-composer-history?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-composer-history?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-composer-history/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-composer-history)

**Terminal-style input history for the DeepSeek Harness Web GUI composer.**

*Press ↑ like it's in a terminal — and keep your half-typed draft safe.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-composer-history.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-top-rated.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-composer-history/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-composer-history/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-composer-history?label=version)](https://github.com/PerryLink/dsh-composer-history/releases)
[![npm version](https://img.shields.io/npm/v/dsh-composer-history)](https://www.npmjs.com/package/dsh-composer-history)
[![npm downloads](https://img.shields.io/npm/dm/dsh-composer-history)](https://www.npmjs.com/package/dsh-composer-history)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (verified 2026-09-22: dual typecheck rulers + 294 tests; client peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0`). On this line the settings seam is the profile entry's own live `Config` form — the removed `ctx.settings.register` / `SettingsProvider` family and the client `ctx.settingsScope` service are both gone, so every tunable now travels through `ctx.configForms`. On the 0.1.6+ lines `SessionListState.current` is gone — the current session is derived from the retention facts, so history injection / the snippet library keep working. |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | Web GUI only (client plugin; browser-local storage; no network, no native code) |
| Model | Any (no model requests — pure UI behavior) |

The browser half rides the published client packages (`dsh-client-ui-conversation`, `dsh-client-ui-input-trigger`, `dsh-client-ui-settings`) and the cordis `Context`; it no longer depends on the removed `dsh-client-runtime` package, so the client surface also lines up with `0.1.2-rc.1` hosts.
Interception anchors on the web composer's DOM: the contenteditable surface `div[data-composer-input]` inside `[data-input-scroll]` (the Lexical composer shipped since 0.1.2-alpha.5 / 0.1.2-rc.1), with the legacy textarea composer inside `[data-input-scroll]` (harness lines up to 0.1.1-rc.2) still matched; textareas elsewhere pass through. The compat workflow's jsdom web-behavior smoke asserts this identity/text/caret face against the packed bundle.
0.1.2-rc.1 (adapted 2026-09-04): the session envelope keeps its ignorable field for stored-log read compatibility only - Session.append still cannot stamp it, so audit-gate behavior is unchanged. Verified 2026-09-06 against the dsh-v0.1.7-alpha.1 master checkout (full gate chain + profile install smoke).
0.1.5-rc.1 (adapted 2026-09-10): dependency pins move to the published 0.1.5-rc.1 line; no seam change affects this plugin's behavior.
0.1.5-rc.2 (adapted 2026-09-11): dependency pins move to the published 0.1.5-rc.2 line; no seam change affects this plugin's behavior.
0.1.7-alpha.1 (adapted 2026-09-22): the settings seam is replaced on both halves. The host half no longer registers a `composer-history` namespace through the removed `ctx.settings.register(ns, schema, { base })` — on this line a plugin's durable settings surface IS its own live `Config`: every tunable is declared `.volatile()`, the profile entry id (`composer-history`, the bundle patch's row id) names the form, and `apply` claims the generated-form presentation (`ctx.settings.configure({ auto: true }, ctx.fiber)`, effect-owned so a reload re-registers cleanly). The browser half reads the same entry through `ctx.configForms.get('composer-history')` instead of the removed `ctx.settingsScope.bind({ namespace })`; the snapshot/subscribe shape is unchanged, so the wiring still reinstalls on every committed change. Editable surface is preserved, not widened: every field the old namespace exposed is volatile, and no new field became editable. An existing `settings.yaml` section named `composer-history` is migrated into the profile entry of the same id by the host itself.

## What you get

`dsh-composer-history` puts a terminal's input history into the DeepSeek Harness Web GUI composer:

1. **Edge-first arrow recall** — bare ↑/↓ move the caret first; history recall triggers only when the caret sits on the first/last line. The first recall stashes `{draft, caret}`, and reaching the newest entry again (or pressing `Esc`) restores both exactly — never cleared.
2. **Persisted history** — every sent message is appended to a bounded browser-local store, so recall survives page reloads and reaches across sessions.
3. **Reverse search** — `Ctrl+R` (configurable) opens a query overlay over merged history, snippets, and templates.
4. **Smart input layer** — `/save`/`/load` snippets, prompt templates with `{{workspace}}`/`{{session}}`/`{{draft}}` variables, and browser-local reuse insights.
5. **Sliding-context aware** — compaction summaries join recall and search as `[compacted] …` entries, and a transient notice announces each compaction with a one-click `/compact` fill.
6. **Versioned JSON backup** — export/import all four libraries (history, snippets, templates, insights) as one schema-versioned document; download or copy on export, file pick or paste on import.

Pure UI behavior: no session events, no agent-loop changes, no model requests. Recalled text only enters the ordinary composer draft; it reaches the model only if *you* press Enter.

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-composer-history#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-composer-history

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A3 'id: composer-history'
```

## Install & uninstall

The npm package ships the built bundles; a source checkout must be built first (`pnpm run build`) — the client-package check refuses to boot against an unbuilt bundle.

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-composer-history#main"`.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-composer-history`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-composer-history-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-composer-history` (or remove the row from the profile patch).

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml and the entry's settings form; the profile patch is the persisted