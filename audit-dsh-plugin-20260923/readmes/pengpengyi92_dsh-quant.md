# 🐳 dsh-quant — The Everything-Plugin Quant OS

<p align="center">
  <img src="https://raw.githubusercontent.com/pengpengyi92/dsh-quant/master/assets/dsh-quant-open-source-hero.png" alt="dsh-quant open-source quant research hero" width="100%">
</p>

📣 **Announcement archive**: [2026-09-01 X open-source launch copy](https://github.com/pengpengyi92/dsh-quant/blob/master/ann/2026-09-01_x_open_source_launch.md)

🌐 **Site**: https://dsh-quant-site.pages.dev · ✅ Listed in [awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) (one-click install via dsh-market)

[![npm](https://img.shields.io/npm/v/dsh-quant)](https://www.npmjs.com/package/dsh-quant)
[![downloads](https://img.shields.io/npm/dm/dsh-quant)](https://www.npmjs.com/package/dsh-quant)
[![stars](https://img.shields.io/github/stars/pengpengyi92/dsh-quant?style=social)](https://github.com/pengpengyi92/dsh-quant)
[![site](https://img.shields.io/badge/site-dsh--quant--site.pages.dev-orange)](https://dsh-quant-site.pages.dev)
[![license](https://img.shields.io/npm/l/dsh-quant)](LICENSE)
[![ci](https://github.com/pengpengyi92/dsh-quant/actions/workflows/ci.yml/badge.svg)](https://github.com/pengpengyi92/dsh-quant/actions)
[![dsh-plugin](https://img.shields.io/badge/dsh-plugin-blue)](https://github.com/topics/dsh-plugin)

> **AI-native & DSH-native quant toolkit for every quant aspect** — 59 tools · 6 domains
> (data / alpha / ML / risk / execution / ecosystem) · one end-to-end PDAT→PET
> research pipeline. **Methods open, secrets internal.**

## 🧩 Core Philosophy: Everything is a Plugin (quant edition)

dsh's philosophy is **everything is a plugin**; dsh-quant brings it to quant —
open-sourcing the internal five-team paradigm (**PDAT → PAAT → PCPT → PRT → PET**)
as **five pluggable modules**:

```
data plugin   dsh-data      market data / sources / quality  ← plug in Binance or your own data
alpha plugin  dsh-alpha     indicators / factors / eval      ← write your own alpha (internal alpha stays private)
model plugin  dsh-ml        backtests / ML/DL/RL framework   ← train your own models (internal research stays private)
risk plugin   dsh-risk      VaR / drawdown / options / bonds ← set your own risk limits
exec plugin   dsh-execution sim execution / fund / report    ← build your own trading system (paper or live)
```

- **What's open is the paradigm**: how modules compose, how contracts are defined
  (null alignment / no look-ahead / hand-computed tests), how results are validated —
  not the internal secrets
- **You fill it in**: product power = UI + strategies + data interfaces + DL/RL
  models + trading-system building, all self-assembled, all pluginized
- **Infinite self-evolution**: fill the framework with your modules → run paper/live
  → feed the ecosystem back — that's dsh-quant

Plugin call for proposals: [Issue #27 (five modules × many plugins)](https://github.com/pengpengyi92/dsh-quant/issues/27) — PDAT plugins, PET plugins, anything you can imagine 🐋

## 🤖 AI-Native Is Deliberate (design statement)

dsh-quant's primary consumer is the **agent (the model), not the human** — a
deliberate choice from day one:

- **Tool schemas are injected into the system prompt** — every contract (args /
  outputs / alignment rules) is written from the model's perspective
- **Equal-length null alignment** — outputs match input length; leading window
  positions are `null`, so the model aligns by index and never pads
- **Canonical JSON + render separation** — machines read structure, humans read prose
- **All isConcurrencySafe** — pure functions, no shared state; agents can call all
  59 tools in parallel without interference
- **Skill layer** — `skill/quant-research` lets the model load the workflow itself

Full statement: [Issue #14](https://github.com/pengpengyi92/dsh-quant/issues/14) "AI-native is deliberate".

## 🐍 Why Almost No Python?

A common question: a quant project without `.py` files? **Answer: 0 Python files,
21 TypeScript source files, zero runtime dependencies — deliberate:**

- dsh-quant is a **dsh plugin** running inside the harness's Node runtime: same
  process as the agent, composable by the Loader, reversible registration (HMR-safe)
  — TypeScript is the only natural choice
- Where Python is needed (akshare / tushare / baostock), use the **channel knowledge
  base** (`quant_data_guide`, 15 channels): dsh ships shell / subprocess capabilities,
  so the agent decides whether to spawn Python — dsh-quant carries no runtime
- All numerical methods (indicators / backtests / options / bonds) are **pure
  functions with hand-computed baselines**: zero deps, offline-verifiable,
  `npm test` green anywhere

One goal: **build the most usable AI-native quant repo** 🐋

**59 `quant_*` tools · 6 domains · 215 unit tests · zero runtime deps**. Full positioning: pinned [Issue #9](https://github.com/pengpengyi92/dsh-quant/issues/9).

## 🤖 For visiting agents

Agents landing on this repo: start at [AGENTS.md](AGENTS.md) (root-level, auto-read
by Copilot / Claude Code / dsh), then the closed-loop example
[plugin/CASE_STUDY.md](plugin/CASE_STUDY.md) or [Discussion #38](https://github.com/pengpengyi92/dsh-quant/discussions/38),
and the one-glance contract [mcp/AGENT_GUIDE.md](mcp/AGENT_GUIDE.md).

## Quick Install (dsh users)

```sh
npm i dsh-quant
```

Add one line to your cordis.yml:

```yaml
- name: 'dsh-quant'
```

59 tools auto-register — indicators / backtests / factors / risk / fund simulation /
ecosystem metrics out of the box. One `quant_research_pipeline` runs the whole
PDAT→PET chain. ML/DL knowledge: [docs/ML_GUIDE.md](docs/ML_GUIDE.md);
executable demo: `npx tsx demos/ml-workflow.ts`.

## 🚀 Product Experience: Three Minutes to a Full Quant Pipeline

Right after install, experience the complete PDAT→PET flow (BTC public data +
simple strategy + backtest + paper trading):

```
data(quant_market_fetch) → quality(quant_data_quality) → factors(quant_factor_evaluate)
→ backtest(quant_backtest) → metrics(quant_metrics) → risk(quant_risk)
→ drawdown(quant_drawdown) → paper sim(quant_execute_sim) → fund sim(quant_fund)
→ report(quant_report)
```

One-liner: `quant_research_pipeline(symbol=BTCUSDT, limit=120)` returns everything
in one call.

Then plug **your own plugins** into each module (data sources / alpha / models /
risk / execution — everything is a plugin, proposals at Issue #27).

Five-step walkthrough with commentary: [docs/ONBOARDING.md](docs/ONBOARDING.md) ·
Agent one-glance guide: [mcp/AGENT_GUIDE.md](mcp/AGENT_GUIDE.md)

## 🖥️ UI Workbench (dsh-quant-ui)

![dsh-quant UI](demos/ui-demo-preview.png)

[dsh-quant-ui](https://github.com/pengpengyi92/dsh-quant-ui): candlesticks + MA
overlays + trade markers, equity curves, fund NAV / management-fee / performance-fee
cards, metric selector — plus a swimming chibi whale 🐋 (click the title 3 times).

Live demo: https://dsh-quant-ui.pages.dev

## ⌨️ CLI (dsh-quant terminal)

Zero-dependency readable terminal (pure Node + ANSI, same philosophy as the
P-Research CLI). Browse the research columns and live market data without a
browser:

```bash
node cli/main.mjs repo                      # 59 tools · 6 domains
node cli/main.mjs history                   # 53 firm archives index
node cli/main.mjs history citadel           # one firm's archive (rendered)
node cli/main.mjs history --reports         # ANALYSIS / TIMELINE / LINEAGE / BANK_LINEAGE
node cli/main.mjs history --search 高频      # cross-archive search
node cli/main.mjs kline BTCUSDT --limit 20  # colored OHLC table + stats
node cli/main.mjs browse                   # interactive TUI: arrow-key firm browser
```

After `npm install -g .`, the commands shorten to `dsh-quant repo`,
`dsh-quant history citadel`, etc.

## Tools

| Tool | Parameters | Canonical output | First valid index |
|---|---|---|---|
| `quant_data_compare` | `dataType` (e.g. "financials"/"daily bars") | `{ dataType, channels: [{ name, cost, covers, bestFor }] }` (covering first) | — |
| `quant_data_advice` | `