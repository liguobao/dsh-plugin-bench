<div align="center">

# 💰 dsh-budget
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-budget` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-budget)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-budget?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-budget?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-budget/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-budget)

**Cost governance for DeepSeek Harness: budgets, carbon, and latency in one panel.**

*Know what every session costs — before it costs you.*

> **Official repository.** This is the only official repository of dsh-budget, maintained by PerryLink. Same-name repositories under other accounts are not affiliated.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-budget.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-budget/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-budget/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-budget?label=version)](https://github.com/PerryLink/dsh-budget/releases)
[![npm version](https://img.shields.io/npm/v/dsh-budget)](https://www.npmjs.com/package/dsh-budget)
[![npm downloads](https://img.shields.io/npm/dm/dsh-budget)](https://www.npmjs.com/package/dsh-budget)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (GitHub tag, adapted 2026-09-18; peer range `>=0.1.2-rc.1 <0.2.0 || >=0.1.5-alpha.1 <0.2.0 || >=0.1.6-0 <0.2.0 || >=0.1.7-0 <0.2.0`): the alpha.2 catalog prices are built into the price table and unknown models surface as unpriced instead of a fabricated estimate; the audit gate keeps suppressing `budget/alert`/`budget/block` appends (fail-closed session event vocabulary). Verified 2026-09-18 by the two-ruler typecheck chain and the full local gate; the browser-panel items stay 人工·未测即未完成 (maintainer manual checklist). |

| Audit events | Written on harnesses before `0.1.2-rc.1`; suppressed with a logged degradation reason on `0.1.2-rc.1` and later (fail-closed session event vocabulary, no external registration surface) || Node | `^22.19.0 \|\| >=24.0.0` |
| Surfaces | Host + Web client (Settings budget tab); `/budget` command |

## What you get

`dsh-budget` turns the session event stream into a four-in-one cost governance loop:

- **Aggregated metering** — tokens (uncached input / output / cache read / cache write), estimated USD cost, and carbon footprint per model, session, and day, priced through a built-in USD-per-1M table merged with your `config.prices`.
- **Budget governance** — session/daily/monthly caps; a warn-ratio threshold alert (webhook POST + desktop-notification flag) and three over-limit policies: `alert` (notify only), `block` (short-circuit new model requests until the user lifts the block), `degrade` (block with corrective guidance naming the cheaper model from your `degradation` map).
- **Carbon & latency** — token→carbon bridge (tokens × kWh/token × PUE × regional grid intensity, ported from AI-Carbon-Footprint-Calculator) and per-model latency percentiles.
- **Surfaces** — the Settings budget tab (usage bars, per-day usage curve, model breakdown, alerts, cap editors, unblock buttons) and the `/budget` command (`/budget`, `/budget models`, `/budget unblock <scope>`).

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-budget#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-budget

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A2 'id: budget'
```

Then ask the agent: `/budget` — and watch the Settings tab fill in.

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-budget#main"` — the `prepare` script builds with production dependencies only.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-budget`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-budget-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-budget`.

> If pnpm reports `ERR_PNPM_IGNORED_BUILDS` for this package (esbuild's harmless platform-binary validation), add `allowBuilds: { esbuild: true }` to your `pnpm-workspace.yaml` — the `dsh` CLI prints the exact snippet.

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). `cordis.patch.yml` documents each key inline.

| Key | Default | Meaning |
|---|---|---|
| `prices` | `{}` | Per-model USD prices per 1M tokens, merged over the built-in table |
| `defaultPrice` | unpriced signal (`priced: false`, zero numbers) | Fallback for models absent from both tables: the default contributes 0 to accounting and surfaces as "unpriced"; set numbers with `priced: true` to price unknown models explicitly |
| `budgets.session` / `daily` / `monthly` | `10` / `50` / `500` | Budget caps in USD per scope; omit for unlimited |
| `warnRatio` | `0.8` | Alert once usage reaches this fraction of a cap (0..1) |
| `overLimit` | `alert` | `alert` / `block` / `degrade` after a cap is crossed |
| `degradation` | `{}` | Model id → cheaper model id of the same provider |
| `webhookUrl` | *(none)* | Optional webhook URL for threshold alerts (POST JSON) |
| `webhookTimeoutMs` | `5000` | Webhook request timeout |
| `alertsEnabled` | `true` | Master switch for threshold alerts |
| `alertCooldownMs` | `3600000` | Minimum ms between two alerts of the same scope |
| `desktopNotifications` | `false` | Browser desktop notifications while the tab is open |
| `refreshIntervalMs` | `5000` | Settings tab polling interval |
| `carbon.enabled` / `region` / `pue` / `energyKwhPerToken` | `true` / `global` / `1.58` / `0.000007` | Carbon bridge (regions: global, us, eu, china, india, uk, france, iceland) |
| `latency.enabled` / `windowSize` | `true` / `200` | Per-model latency percentiles and their window |
| `currency` | `{code: USD, rate: 1.0, decimals: 2}` | Display currency (costs are computed in USD) |
| `outputLanguage` | `en` | `/budget` output language: `en` / `zh` |
| `historyDays` | `30` | Per-day usage history kept in the panel snapshot |
| `persistence.enabled` / `intervalMs` | `true` / `10000` | Durable day/month persistence across restarts (storage domain); degrades to in-memory when the domain is absent |

## Tools & surfaces

| Surface | Kind | Notes |
|---|---|---|
| `/budget` | Command | Per-scope overview (usage, ratio, carbon, blocked state) |
| `/budget models` | Command | Per-model breakdown with latency percentiles |
| `/budget unblock <scope>` | Command | Lift a blocked scope (`session` / `daily` / `monthly`) |
| Settings → Plugins → Budget | Settings tab | Usage bars, per-day usage curve, model breakdown, alerts, cap editors, unblock buttons |
| `budget/status`, `budget/setSettings`, `budget/unblock` | Typert Remote | The client channel (the tab consumes these) |

## Permissions & data

- **Permissions**: `network:outbound` (the optional alert webhook only), `session:append` (audit events), `nat