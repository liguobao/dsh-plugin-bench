# dsh-trading

A trading **research** workbench built as plugins for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (`dsh`). No fork, no patched core — just a bundle you stack on the stock `web` or `headless` profile.

> **Status: early scaffold.** dsh itself is in developer preview and moves fast; expect breaking changes on both sides.

## The workbench

Under `dsh web` with the optional shell frame, the app becomes chart-first: a
persistent, live chart column on the left, the conversation on the right.

```
┌──┬────────────────────────────────────┬─────────────────────────┐
│  │  CC.BTCUSDT   1m 5m [15m] 1h 1d    │  ⌄ Market Analyst       │
│▸ │  ┌──────────────────────────────┐  │                         │
│  │  │        ╱╲    ╱╲              │  │  MU is coiling under    │
│s │  │  ╱╲   ╱  ╲__╱  ╲_ ── 118,400 │  │  118.4k; the 15m ADX …  │
│e │  │ ╱  ╲_╱          ╲ ── 116,900 │  │                         │
│s │  │▁▂▃▁▂▄▃▁▂▃▅▂▁▃▂▁▄▃▁▂▃         │  │  ▸ annotate_chart       │
│s │  └──────────────────────────────┘  │    ✎ 6 marks — Show     │
│  │  ● live · 15m · 5:05:10 PM   📌    │                         │
└──┴────────────────────────────────────┴─────────────────────────┘
   rail        the chart you drive          the agent you talk to
```

The column is **yours**: type a symbol, pick a timeframe, and it fetches over a
loopback channel without going through the model at all. It also **follows the
conversation** — when the agent charts something, the column loads that
instrument *live* rather than mirroring the agent's frozen snapshot. Touching
the chart at all — a symbol, a timeframe — **pins** it, and a 📌 chip says so;
from then on the agent's drawings arrive as a **Show** offer on a pill instead
of taking the chart out from under you. Click the chip to start following
again.

Drawings work the same way in both directions. `annotate_chart` levels, zones
and paths land on the live column; the *prose* half of the same analysis —
the level table, the bull/bear scenario cards — stays in chat, where reading
text belongs. And the loop closes: the panel publishes what it is showing back
to the host, so the agent can read your chart (`get_chart_view`, plus a
one-line context injection each turn) instead of asking you to screenshot it.

## Demo

![The chart column is pinned to Micron while the agent's marks are for Bitcoin, so nothing lands; a pill offers them, and one click loads that chart with its six marks](media/workbench-preview.gif)

The column is pinned to Micron. The agent's six marks are for Bitcoin — a
different instrument, so the predicate refuses the merge and **nothing lands
on the wrong chart**. They are offered on a pill instead; one click loads that
chart with its marks. The clock in the top-right corner is a live feed off a
local OpenD, ticking through the whole clip.

▶ **[Watch the full 90-second demo with narration](https://www.youtube.com/watch?v=ULeROBoBGTc)** —
the loop above is one beat of it. The full cut also walks the shell, the
symbol box and the timeframe row, the agent drawing on the live column, and
the per-turn context line that lets it read your chart without asking for a
screenshot.

None of it is a mockup: the footage is 1920x1080 Playwright captures of a real
session against a live Futu OpenD, and the chart keeps ticking through every
shot.

<details>
<summary>The earlier v0.2 demo — chart cards in the chat feed</summary>

▶ **[80-second demo with narration on YouTube](https://www.youtube.com/watch?v=9KLpy-jPtKY)**

Recorded before the chart-first shell existed, and still exactly how the `web`
surface behaves *without* `@dsh-trading/client-frame`: the agent answers with
an interactive chart card, chips draw indicator panes from the exact per-bar
series the model read, and `annotate_chart` puts levels on the chart through a
trust gate — mandatory provenance, prices validated against the real candle
window.

[![Interactive chart cards in dsh web: chips toggle indicator panes drawn from the model's own numbers; annotate_chart draws provenance-gated levels](media/demo-preview.gif)](https://www.youtube.com/watch?v=9KLpy-jPtKY)

</details>

## Design

Eight packages, one direction of dependency:

```
@dsh-trading/tool-market      model-facing tools (list_symbols, get_ohlcv,
                              market_snapshot, annotate_chart, render_chart)
                              + the indicator library
        │  consumes
        ▼
@dsh-trading/market-data      the seam: ctx.marketData — typed candle/symbol interface
        ▲  implements
        │
@dsh-trading/provider-csv     reference provider: local CSV files
@dsh-trading/provider-futu    live provider: HK / US / A-share equities and
                              24/7 crypto pairs, from a local Futu OpenD

@dsh-trading/risk-guard       independent: refuses execution-shaped tool names
                              from any plugin, at dsh's tools/pre-execute gate

@dsh-trading/verdict          the evaluation harness: audit_backtest validates
                              fills against real candles, runs a seeded
                              random baseline and sample-size power check;
                              lint_strategy_code hunts lookahead leaks.
                              Verdicts may honestly be NOT PROVEN.

@dsh-trading/client-chart     web-only cards + the persistent chart column and
                              the loopback channel that feeds it; host-side,
                              the get_chart_view tool and the per-turn
                              context line that let the agent read that column
        │  fills the chart seat of
        ▼
@dsh-trading/client-frame     web-only: the shell frame. Replaces dsh's stock
                              three-column layout row with a chart-first one —
                              sidebar | chart | conversation | details,
                              70/30 by default with the sidebar railed — and
                              declares the `trading.chart` seat
```

- **`market-data`** defines the seam and nothing else (its only peer is cordis). Every consumer talks to `ctx.marketData`; every data source hides behind `MarketDataProvider`.
- **`provider-csv`** is the *bring-your-own-data* template: ~100 lines, local `<root>/<symbol>/<timeframe>.csv` files. Copy it to put ClickHouse, a broker API, or CCXT behind the same interface — tools upstream never change.
- **`provider-futu`** is that template filled in against a real broker gateway: HK / US / A-share equities and crypto pairs (`CC.BTCUSDT`), the last being the only instrument that keeps moving at 3am, which makes it the honest way to check that "live" is live. It reads `Qot_GetKL` rather than `Qot_RequestHistoryKL` on purpose: GetKL rides the subscription quota and serves the most recent bars (≤1000), while RequestHistoryKL spends a scarce historical quota OpenD rations by account assets. The trade is stated in the provider's own `description` and honoured in its behaviour — `start` / `end` **filter** the fetched window, they do not seek, so a query for an older range returns honestly empty rather than quietly wrong. See [Live data](#live-data-futu-opend) for setup; note that OpenD is an account-bound personal gateway, which is a licensing fact, not a configuration one.

  `futu-api` is a **peer** dependency, deliberately unpinned. The SDK's version is coupled to the OpenD *you* have installed, not to this package, and Futu states outright that its package versions follow its own scheme rather than semver — so no range expresses "compatible" and the two must be aligned by hand. Install the `futu-api` matching your OpenD (`10.9.x` SDK for a `10.9.x` OpenD). The provider checks this itself at connect, via `GetGlobalState`, and logs a warning naming both versions if the protocol lines differ — a skew otherwise surfaces as a rejected handshake or an empty decode, with nothing to point at.
- **`tool-market`** registers read-only a