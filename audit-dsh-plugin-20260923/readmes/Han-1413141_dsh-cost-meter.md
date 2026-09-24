# dsh-cost-meter

**English** | [简体中文](README.zh-CN.md)

<div align="center">

**Session cost tracking plugin for the DeepSeek Harness web GUI (bilingual UI)**

Per-conversation cost · daily totals · OpenCode Go subscription quota display · budget with usage percentage · official account balance · custom provider balance · balance progress bar · history · peak/off-peak pricing hours display (peak hours UTC 01:00–04:00, 06:00–10:00; from Aug 23, 2026 weekends are billed at off-peak prices all day, shown as “Weekend — all off-peak”) · pre-switch popup & system-notification alerts for peak/off-peak changes (position / lead time / alert type configurable) · one-click price sync from the official docs · Codex-style token usage heat grid · multi-vendor model pricing (built-in 90+ model price catalog with auto-matching) · mainstream Coding Plan quota queries & display (Anthropic / Z.ai / MiniMax / Kimi / OpenRouter / SiliconFlow / CommandCode / SCNet / Volcano Ark / Qwen / Xiaomi MiMo) plan/API dual-track billing (subscription quota vs pay-as-you-go money separated, per-1% & full-window token/equivalent-cost estimates with daily/weekly/monthly curves) · · quota strip above the input box (budget / Go / coding-plan usage in one row, toggleable)

[![version](https://img.shields.io/badge/version-1.7.35-4176E6)](https://github.com/Han-1413141/dsh-cost-meter)

**v1.7.35** adds Bailian CLI quota support, full model names on hover, bounded decoding of bare gzip responses, and per-endpoint GLM quota diagnostics. See the [release notes](docs/release-notes/v1.7.35.md).

[![npm](https://img.shields.io/npm/v/dsh-cost-meter?label=npm)](https://www.npmjs.com/package/dsh-cost-meter)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![dsh](https://img.shields.io/badge/DeepSeek%20Harness-dsh--plugin-4176E6)](https://github.com/deepseek-ai/deepseek-harness)
[![awesome · DSH plugin](https://awesome-dsh-plugin.com/badge.svg)](https://awesome-dsh-plugin.com)
[![WhaleHarness audit](https://whaleharness.com/badge/Han-1413141/dsh-cost-meter/badge.svg)](https://whaleharness.com/audit-report.md)

</div>

---

![Promo art](docs/promo.en.png)

## Feature overview

| Feature | Location | Description |
|---|---|---|
| Per-model cost card | Sidebar / composer dock (optional) | Disabled by default; inline Top-N, Other totals, shares and optional tokens, Today / Last 90 days, remembered expansion and a Top-1 chip. See the [guide](docs/model-cost-card.md#english) |
| Per-conversation cost | Below the composer / session title bar | Live accumulated cost + input/cache/output tokens; the composer footer shows cache hit rate before Input (cache reads / all input, including cache writes); position configurable |
| Official balance | Sidebar top / Settings page (configurable) | Total / granted / topped-up balance, auto-refresh + manual refresh; optional three-segment progress bar (blue/orange/gray), whose today segment only counts official-channel spend (coding plans / custom providers excluded) |
| Custom provider balance | Sidebar / Settings page (configurable) | Configurable HTTP balance lookup (e.g. LiteLLM); bilingual labels, currency, extract rules (dot path / number / add / subtract / divide — use divide for NewApi-style quota endpoints, see [example](#custom-provider-balance-example-newapi-template)); collapsible panel alongside Coding Plan quotas |
| OpenCode Go quota | Sidebar / Settings / bottom-right dock (configurable) | Rolling-5h / weekly / monthly usage percent and reset times, each window toggleable independently, budget used % can show alongside; key auto-discovered (dedicated ref / official Go route apiKeyEnv / env / opencode login) or entered manually |
| Coding plan quotas | Sidebar / Settings page (per vendor) | Multi-vendor coding-plan quota queries (Anthropic Claude Pro/Max, Z.ai / Zhipu GLM Coding Plan, MiniMax Token Plan, Kimi Code weekly + 5-hour quotas with PAYG balance fallback when no subscription key, OpenRouter credits, SiliconFlow balance, CommandCode 5h/weekly windows + monthly credits balance, Xiaomi MiMo Token Plan plan/compensation credit windows + period-end reset + balance via console cookie); per-vendor enable switch, key, display position and refresh interval (sidebar card in the same box style as the Go quota; the collapsed rail shows percentages), official endpoints by default, with a [configurable trusted MiniMax origin](docs/minimax-quota-endpoint.md#english); neutral hints when no credentials/subscription; SCNet Token Plan supports [external console snapshots](docs/scnet-official-snapshot.md#english); without a valid snapshot, monthly usage is estimated from the local ledger via the official credits deduction table (no credentials needed) |
| Quota strip | Above the input box (toggle in Display settings) | One compact chip row for budget used % / the Go main window / each enabled coding-plan usage window (short label + mini progress bar, ≥80% warn, ≥100% over, hover for reset times); click any chip to refresh its data source (budget → state, Go → Go quota, vendor → all its windows); multiple windows of one vendor merge into a single segmented chip; a first-run guide card lets you decide whether to enable it; hides itself when there is no quota data |
| Click to refresh | Sidebar balance/quota boxes | Click the official balance / custom balance / coding-plan box (collapsed rail included) to fetch the latest data immediately; the box pulses while refreshing, failures keep the previous value and surface the reason in the hover tooltip; keyboard Enter/Space also triggers; a one-time guide card appears after the update |
| Simple sidebar display | Settings → Cost → Display | Optional, with a one-time choice after updating. Condenses cards and caps panel height at 38% of the viewport and 320 px, while preserving amounts, quotas, refresh actions and hover details. Turn off to restore your layout. [Guide](docs/sidebar-simple.md#english) |
| Today's cost | Sidebar bottom (above the settings button) | “Today ¥x”, hover for call count and token details |
| Budget box | Sidebar bottom (between the balance row and the settings button) | Rounded-square frame: budget, used %, progress bar, today's cost & share of budget, used/limit; ≥80% warning, ≥100% over-budget |
| Summary cards | Settings page | Today / this month / cumulative cost and call counts |
| Token usage stats | Settings page (Cost section) | All-time token totals (input/cache/output/calls) + a Codex-style 26-week daily usage heat grid that fills the settings width; hover a cell for that day's detail |
| Token Plan usage stats | Settings page (Usage) | Per enabled coding plan (incl. Go): per-1% quota and full-window token / equivalent-cost estimates for the current windows (sample delta / live ratio), plus daily/weekly/monthly usage curves; plan-channel amounts are equivalent-only and never touch real money (issue #64) |
| Today's sessions | Settings page | Per-session call count, input/cache/output tokens and cost |
| History | Settings page | Per-day totals; retention days configurable (default 180) |
| Pre-install history import | Automatic on first launch | After install/upgrade, the first launch automatically replays all host session logs to import conversations from before the plugin was installed (missing dates are rebuilt whole; existing dates only gain previously unknown sessions; idempotent and never double-counts live metering; costs priced at per-event historical rates); a manual re-run entry remains in Settings |
| Budget settings | Settings page, top | Limit, period (today / month / cumulative / custom date range), used % |
| Price table | Settings page | Per-model off-peak / peak prices (input/output shorthand supported; cache prices derived automatically); fully editable |
| Peak/off-peak hours display | Settings / budget / today | Shows UTC peak hours 01:00–04:00 and 06:00–10:00 with the current tier; from Aug 23, 2026 weekends (Sat & Sun, Beijing time) are billed 