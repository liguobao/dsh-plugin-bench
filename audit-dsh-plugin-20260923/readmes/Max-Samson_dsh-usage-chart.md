# dsh-usage-chart

> A usage, cost, and account-balance dashboard for DeepSeek Harness Web.

[![npm version](https://img.shields.io/npm/v/dsh-usage-chart)](https://www.npmjs.com/package/dsh-usage-chart)
[![CI](https://img.shields.io/github/actions/workflow/status/Max-Samson/dsh-usage-chart/ci.yml?branch=main)](https://github.com/Max-Samson/dsh-usage-chart/actions)
[![License](https://img.shields.io/github/license/Max-Samson/dsh-usage-chart)](./LICENSE)

[简体中文](./README_ZH.md) · [Report an issue](https://github.com/Max-Samson/dsh-usage-chart/issues) · [Changelog (EN)](./CHANGELOG.md) · [更新日志（中文）](./CHANGELOG_ZH.md)

Interface preview: light English on the left and dark Simplified Chinese on the right. Both variants follow the DSH theme and in-app language setting.

<table>
  <tr>
    <td width="50%"><img src="./docs/images/usage-panel-demo-en-lightv1.0.0.png" alt="Light-theme English usage-panel demo" /><br /><sub>Light theme · English</sub></td>
    <td width="50%"><img src="./docs/images/usage-panel-demo-zh-darkv1.0.0.png" alt="Dark-theme Simplified Chinese usage-panel demo" /><br /><sub>Dark theme · 简体中文</sub></td>
  </tr>
</table>

> Both screenshots use fictional demo data only. They contain no real session content, token counts, costs, balances, or API keys.

The plugin adds a compact indicator below the conversation composer. It shows input/output tokens, cache-hit ratio, estimated cost, active model, a multi-segment context-pressure bar (system/tools/messages breakdown, v1.1.0), and DeepSeek account balance. Click it to open a zero-dependency SVG dashboard with per-turn usage history — including a cost view (every bar shows its own cost value, not just the current round), a duration overlay, anomaly markers, an explainer tooltip (tokens + cost + model + billing tier + duration/TTFT/TPS + **user input source attribution: human/agent/continuation**, v1.1.0 + end reason), horizontally scrollable per-round bars (all rounds, fixed slim bar width, auto-scroll to latest), a dedicated **Context & Compaction Diagnostics section** (system/tools/messages token composition, compaction timeline, freed tokens, summarize cost, context occupancy suggestions, v1.1.0), a dismissible `≈ ¥/$0.00xx` badge on each assistant message, peak/off-peak tiered billing with a live red/green billing-tier tag in the panel (red = peak, green = off-peak, v1.0.1), and official dual-currency pricing (CNY from the Chinese pricing page, USD from the English pricing page — no FX conversion, v1.0.1).

```
▸ Input 12.4M · Output 86.2K · Hit 72% · Cost ≈$0.042 / ≈¥0.284 · demo-model · Balance --
```

Click ▸ to open the dashboard panel:

- **Session usage summary** — Input (uncached/cached), output, cache-hit percentage, and context occupancy (derived from official adapter `tokenUsage` / `contextPressure` projections).
- **Context breakdown & compaction diagnostics (v1.1.0)** — Official `contextBreakdown` projection breakdown (System prompt / Tools schema / Message history token counts and percentage with a 3-segment color bar, annotated as heuristic approximations); Host folds `compaction/*` events (which round was compacted, how many tokens were freed, model used, and summarize call cost); provides proactive suggestions (≥75% / ≥90% occupancy) to start a new session or reduce large file injections.
- **Cost estimation** — Estimated from official list prices (CNY/USD dual-currency per 1M tokens, peak/off-peak tiers) with verified source date; supports user override via `pricing.json`; unpriced models are explicitly tagged.
- **Session-cost aggregation (v1.1.7)** — Adds the host's per-round costs using each round's model and billing tier. While a new round is in progress, the indicator and panel share the fetched history plus a marked estimate for new tokens, then refresh the history after token updates pause. The model label follows the same current-history/live-node priority in both places.
- **DSH 0.1.2+ and themed docks (v1.1.7)** — Reads conversation nodes from the independent `chat` source on newer DSH versions, with a legacy session-snapshot fallback; keeps the expanded panel anchored when a theme creates a fixed-position containing block.
- **Peak / off-peak tiered billing (v1.0.1)** — Peak hours (Beijing time Monday–Friday 09:00–12:00 and 14:00–18:00, UTC 01:00–04:00 and 06:00–10:00) billed at 2× the off-peak rate; all other hours and weekends billed at off-peak rates; rounds bill automatically based on start time (or conservative peak if unknown); live red/green tag in the panel header.
- **Official dual-currency list pricing (v1.0.1)** — Builtin official CNY and USD prices directly used according to the active display currency — **no FX conversion applied to costs** (matching official billing); "Refresh rate" updates only the informational "1 USD ≈ X CNY" reference note.
- **Multi-currency display (v0.3 / v1.0.1)** — One-click toggle between USD and CNY (persisted in localStorage); indicator, panel, chart, and badges all follow.
- **Per-round usage & source attribution (v1.1.0)** — "Total / Composition / **Cost**" view modes; cost mode shows each bar's monetary amount; duration line overlay; anomaly marker chips on cost spikes; cache hit miniature ticks; hover explainer card with full round metrics + **user input source attribution: human/agent/continuation**; horizontal scroll for full session history.
- **Cost badge** — Dismissible `≈ ¥/$0.00xx` badge rendered at the bottom of each assistant message.
- **Multi-segment context pressure bar (v1.1.0)** — Slim bar in the composer dock indicating total context occupancy from green to red, segmented by System (blue), Tools (amber), and Messages (green) with hover percentages.
- **Account balance** — Real-time balance queried via official DeepSeek API (proxied securely through Host, API key never exposed to browser).
- **Bilingual (ZH / EN)** — Automatically follows DSH in-app language setting, with runtime switching between `zh` and `en`.

## Data sources

| Metric | Source | Accuracy |
|---|---|---|
| Token usage | DSH official adapter session projections (`tokenUsage` / `contextPressure`) | ✅ Official real-time data |
| Cost | Official list price (builtin + optional `pricing.json` override, CNY/USD dual-currency / 1M tokens, peak/off-peak tiers) × reported usage | ⚠️ Estimate, not invoice; resolved via Host `/pricing` snapshot |
| Display currency | Host `/meta` config; costs directly calculated in selected currency list price | ✅ Official dual-currency list price |
| Per-round history | Host session log fold (`/usage`): duration / TTFT / TPS / model attribution / **input source attribution** / end reason / per-round cost | ✅ Official event stream fold |
| Context & compaction | Official `contextBreakdown` / `contextPressure` projections + Host `compaction/*` event fold | ✅ Official projections + event fold |
| Balance | Official `GET https://api.deepseek.com/user/balance` | ✅ Official real-time data |
| Model name | Adapter request provenance / `request/context` | ✅ Official real-time data |

## Tech stack

- **Language**: TypeScript source, compiled to DSH loadable JavaScript bundles
- **Framework**: [Cordis](https://github.com/cordiverse/cordis) plugin model + React 18
- **Build**: esbuild (Host half = Node ESM; Client half = browser factory bundle matching DSH Web `PLATFORM_MODULES`)
- **Visualization**: Zero-dependency handcrafted SVG (matches platform rendering, minimal footprint, ultra-stable)

## Install

Prerequisites: **[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) ≥ 0.1.0-rc.6** · **Node.js ≥ 20** · **[pnpm](https://pnpm.io/install) on PATH** (`dsh plugin` forwards installs to pnpm).

> If you get `dsh: command not found` (or PowerShell `The term 'dsh' is not recognized…`),
> you ran `npx @deepseek-ai/dsh` transiently — see FAQ item 1 (install globally, or prefix commands with `npx --yes @deepseek-ai/dsh`).

### Option 1: npm registry (recommended, prebuilt — no build tooling needed)

```sh
