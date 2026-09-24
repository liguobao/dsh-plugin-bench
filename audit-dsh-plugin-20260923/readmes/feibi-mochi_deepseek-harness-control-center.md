# DeepSeek Harness Control Center

[![npm version](https://img.shields.io/npm/v/deepseek-harness-wallet?label=npm&color=5965d8)](https://www.npmjs.com/package/deepseek-harness-wallet)
[![GitHub release](https://img.shields.io/github/v/release/feibi-mochi/deepseek-harness-control-center?label=release&color=5965d8)](https://github.com/feibi-mochi/deepseek-harness-control-center/releases)
[![CI](https://github.com/feibi-mochi/deepseek-harness-control-center/actions/workflows/validate.yml/badge.svg)](https://github.com/feibi-mochi/deepseek-harness-control-center/actions/workflows/validate.yml)
[![DeepSeek Harness](https://img.shields.io/badge/DeepSeek%20Harness-0.1.5--alpha.1-4aa3ff)](https://github.com/deepseek-ai/DeepSeek-Harness)
[![License: MIT](https://img.shields.io/badge/license-MIT-3b7a57)](./LICENSE)

**DeepSeek Harness monitoring, alerts, recharge, and session control center.**

`Balance ¥5.89 · Session ¥0.72 · Official 18.8M | Third-party 800K · ↗ Recharge`

[English](./README.md) · [简体中文](https://github.com/feibi-mochi/deepseek-harness-control-center/blob/main/docs/i18n/README.zh-CN.md) · [Install](#install) · [Compatibility](#browser-desktop-and-os-compatibility) · [Changelog](./CHANGELOG.md)

> A local-first companion that keeps account status, per-conversation usage, completion reminders, official recharge, flexible layout, and host-gated session controls beside the DSH composer.

> **Version:** v0.3.13.

> If DeepSeek Harness Control Center helps you, please consider leaving a ⭐ Star. Thank you!

## What it does

The wallet UI is currently primarily Chinese and does not yet follow the host language setting (#32). DeepSeek balances come from the official API; cost accounting is a local estimate.

```
余额 ¥5.89 · 本场 ¥0.72 · 官 18.8M | 三方 800K · ↗充
```

- **Official DeepSeek** — live balance (60s global refresh with fast boot retries), an estimated current-session cost (not an official bill) locked to the price active for each usage event, including the 2026-08-17 peak/off-peak rollout, and token breakdown.
- **Vision model accounting** — `deepseek-v4-flash-vision-exp` is priced like V4 Flash; image tokens reported by the Harness are included with text tokens.
- **v4 peak/off-peak ring clock** — a resident 24-hour sidebar footer widget for `v4-flash`, `v4-pro`, and `v4-flash-vision-exp`. Weekday peak windows are 09:00–12:00 and 14:00–18:00 Beijing time. After Friday 18:00 the card previews “weekend all-day off-peak”; Saturday and Sunday name the current all-day off-peak rule; Monday before 09:00 shows the time remaining to enter peak. Optional notifications treat Friday 18:00 through Monday 09:00 as one continuous off-peak period.
- **Official pricing sync** — periodically checks the official DeepSeek pricing page and applies only a fully validated table. Network failures retain the last validated rule (or the built-in rule before the first successful sync); an unrecognized page structure is marked for review instead of silently changing billing.
- **Z.ai Coding Plan quotas** — a generic official-plan adapter monitors configured Global and China plans without exposing credentials. It separates the 5-hour model-token window from monthly MCP-tool usage, leads with quota remaining from 100% down while keeping usage as secondary context, retains the last successful snapshot on failure, and never converts subscription quota into CNY balance.
- **Provider-aware composer surfaces** — the chip and sidebar clock follow the session's selected provider/model. Z.ai—including transparent `vision-toolkit-` variants—replaces DeepSeek balance, recharge, and peak pricing with plan-window summaries; unrelated providers show only their own session tokens, and DeepSeek V4 restores the wallet and peak clock.
- **Local usage ledger (up to 365 days / 20,000 events)** — Wallet settings keeps the heatmap visible, while compact wallet panels keep it collapsible. Stable request identities are deduplicated, official cost is locked at usage time, official and third-party data stay separate, and prompts or responses are never stored. Collection begins after upgrading to v0.3.2; older aggregate counters have no trustworthy dates and are not backfilled.
- **Third-party total** — current-session tokens (input / cache read / output) remain available with zero configuration.
- **Custom third-party pricing** — enter an exact Provider/model route, currency, and base per-million input/cache-read/cache-write/output rates, then optionally add multiple IANA-timezone, weekday, and cross-midnight pricing windows. Current-session and 365-day ledger costs are recalculated locally by occurrence time and clearly labeled as user-defined estimates, never as provider balances or invoices.
- **Provider classification** — observed wrapper routes appear in the settings page; opted-in routes join the official token/cost bucket for subsequent calls and are priced with the official table. Existing history is not retroactively reclassified.
- **Click the chip** to open the detail panel: correctly formatted per-currency balances, cost and token splits, a freely editable low-balance threshold for the active account and currency (two decimals, persisted per account; alerts never mix currencies), manual refresh, and a jump to the official recharge page (first click shows the domain for confirmation — anti-phishing).
- **Move, dock, and scale** — drag the chip freely, preview nearby snap targets, use compact horizontal or vertical layouts, adjust its scale from the control panel, and show official or third-party data independently. The peak clock background can be explicitly set to transparent (solid on hover) or solid; there is no automatic mode. The choices are remembered locally.
- **Composer-label controls and skin compatibility** — independently show/hide the composer label or reduce it to the primary remaining value (DeepSeek balance, Z.ai five-hour quota) without disabling reminders, settings, plan monitoring, or history. The standard chip also resists broad skin button rules and aligns with maid-atelier's 38px navy-and-gold composer toolbar.
- **Floating window mode** — detach the detail panel into a draggable window with a remembered position, or minimize it directly to a freely movable dot; the dot turns red below the threshold.
- **Completion reminders** — optionally notify when a conversation finishes, with persistent or timed modes, queueing and deduplication for simultaneous completions, cross-tab coordination, and an in-page fallback when system notifications are unavailable.
- **Low-balance alert** — below the threshold the chip turns red with a breathing animation and fires one desktop notification; it resets automatically once the balance recovers.
- **Theme-native UI** — uses DSH `--dsw-alias-*` variables with safe fallback colors, so light and dark themes both render correctly; the panel closes when you click outside and flips open-direction near screen edges.
- **Clear current-session wallet data** — one button clears only the open conversation's token/cost records; it does not delete the conversation, and every other conversation is untouched. Historical ledger clearing is a separate action.

## Multi-account

- Open the wallet panel → **Account Management（账户管理）** to add accounts (name + API key), switch the active one, or remove them.
- Adding the first account attempts to synchronize its key with the host credential store. It activates only if that write succeeds; a refused write retains the saved account without marking it active for billing.
- Switching prompts a confirmation because it changes **LLM billing** for subsequent requests: the switch writes the account key into the credentials seam (`credentials.set('DEEPSEEK_API_KEY', ...)`), and since the llm-deepseek provider route resolves that reference per request, the very next LLM call is billed with the new account — no restart needed.
- Account keys are encrypted at rest in `$DSH_HOME/storages/accounts.json`: Windows uses