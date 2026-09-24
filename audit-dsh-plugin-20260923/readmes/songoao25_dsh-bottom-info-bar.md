# Bottom Info Bar

<img src="assets/wechat-group.png" width="118" align="right" alt="WeChat group DeepThinking — scan to join">

**English** | [**中文**](README.zh-CN.md)

[![License: MIT](https://img.shields.io/github/license/songoao25/dsh-bottom-info-bar)](https://github.com/songoao25/dsh-bottom-info-bar/blob/main/LICENSE)
[![Release](https://img.shields.io/github/v/release/songoao25/dsh-bottom-info-bar)](https://github.com/songoao25/dsh-bottom-info-bar/releases)
[![Last commit](https://img.shields.io/github/last-commit/songoao25/dsh-bottom-info-bar)](https://github.com/songoao25/dsh-bottom-info-bar)
[![CI](https://img.shields.io/github/actions/workflow/status/songoao25/dsh-bottom-info-bar/ci.yml)](https://github.com/songoao25/dsh-bottom-info-bar/actions)

**A drop-in replacement for the stats row under the DeepSeek Harness composer.** Everything that row showed stays — turns and steps, LLM and tool time, cache hit rate, input/output tokens — and it adds the **provider and exact model**, your **real balance** (or subscription quota, or this month's bill), **peak/off-peak pricing** with a countdown to the next switch, and **what this conversation has cost so far**.

Install once, restart once, done. The billing mode is detected automatically, and every figure comes from a provider API — or is **explicitly labelled as an estimate**.

![Info bar in full view](assets/info-bar-full.webp)
![Info bar in compact view](assets/info-bar-compact.webp)

<sub>**Full** and **compact** view (English UI; labels follow DSH's language setting). Click the bar to switch.</sub>

> 💬 Questions or ideas? Scan the QR code to join our WeChat group **DeepThinking**. <sub>The code expires about 7 days after it is generated — if it has expired, open an issue and we will refresh it.</sub>

## At a glance

- **Three billing modes, auto-detected** — balance, subscription quota, or cloud bill. They replace each other and never overlap.
- **Real data, honestly labelled** — balances, quotas, plans and bills come from official provider APIs. The one figure that cannot (OpenAI has no public balance API) is derived from your spending rate and marked `(estimated)` in the bar.
- **Exactly what DSH shows** — the provider and model match DSH's model switcher, and newly published models are picked up automatically.
- **Peak / off-peak pricing** — both prices plus a countdown to the next switch (weekends count as off-peak all day).
- **Honest spend tracking** — this conversation (including subagents), today, last 30 days, and all time — persisted to disk, nothing lost on restart.
- **Native by design** — it replaces the native row instead of duplicating it; click to switch full/compact, and pick fields and colours on the plugin page.

## Requirements

- **[DeepSeek Harness](https://github.com/deepseek-ai)** with the **web** interface (`dsh web`). This plugin is web-only — the bar is a web UI component.
- **[pnpm](https://pnpm.io/)** — used by `dsh plugin` to manage profile packages.
- An API key for whichever provider you use, set in DSH under **Settings → Models**.

## Quick start

```bash
dsh plugin --profile web add dsh-bottom-info-bar
```

Then **restart `dsh web`** — plugins are composed when the host process starts, so a page refresh is not enough.

That is the whole setup: configure your provider's API key, restart, done. The plugin then shows up under **Plugins**, enabled:

![Plugins list with bottom-info-bar installed and enabled](assets/plugins-installed.webp)

<details>
<summary>Other ways to install (and which one to pick)</summary>

**Recommended: the npm command above.** It is the only install method with no build step: the update reminder hands you one command, and nothing has to be rebuilt afterwards — see [Updating](#updating).

**From a local checkout** (for development, or to run unreleased code):

```bash
git clone https://github.com/songoao25/dsh-bottom-info-bar.git
dsh plugin --profile web add /path/to/dsh-bottom-info-bar/plugin
```

This creates a `link:` install. It tracks your checkout rather than npm, so updates are `git pull` instead of a package install — see [Updating](#updating).

**One-command script** — clone and install in one step:

```bash
git clone https://github.com/songoao25/dsh-bottom-info-bar.git
cd dsh-bottom-info-bar
./install.sh                # installs into the "web" profile; --profile <name> to override
```

Like the local-checkout option, this produces a `link:` install.

Detailed instructions and troubleshooting: [docs/INSTALL.md](docs/INSTALL.md).
</details>

## Configuration

Everything is on the **plugin page** — **Plugins → bottom-info-bar** — not in DSH's global settings. Field switches, colours, custom text and the billing ledger all live there, and changes save as you make them.

![Plugin page: Info Bar settings — search, the two field groups, restore defaults, custom text and billing data](assets/plugin-page.webp)

<sub>**Info Bar** holds the search box, the two field groups, **Restore defaults** and **Custom text**; typing in the search box expands both groups. **Billing data** exports CSV/JSON or clears the ledger.</sub>

![Native information expanded: one switch and one colour per field](assets/field-config.webp)

<sub>**Native information** — the six fields DSH's own stats row already showed. Each row keeps its own switch and colour; the defaults match DSH.</sub>

![Plugin information expanded: the fields this plugin adds](assets/field-config-plugin.webp)

<sub>**Plugin information** — everything the bar adds: provider and model, subscriptions, spend, balance, peak/off-peak prices and quota. Switch a field off and the bar drops it.</sub>

## What it does not do

The boundaries are part of the design, and they are worth stating plainly:

- **It never passes a guess off as a fact.** Every figure comes from a provider API — or, in the one case where no API exists (OpenAI has no public balance endpoint), is computed from your spending rate and labelled `(estimated)` in the bar. When a number is simply unavailable, the bar says so instead of filling the gap.
- **It never updates itself.** The version reminder only tells you a newer version exists and prepares the command; nothing on your machine changes until you run it.
- **It never binds your ChatGPT account.** That belongs to the companion plugin [dsh-chatgpt-subscription](https://github.com/songoao25). This bar only reads the local token.
- **It never stores conversations.** The ledger records tokens, model, provider and cost — no prompts, no messages, no API keys.
- **It does not work outside the web interface.** There is no terminal or headless equivalent of the bar.

## Billing modes

The bar follows the active session in DSH and picks the display from the provider — no manual mode selection.

### Balance mode (DeepSeek, Kimi, OpenRouter, StepFun, Xiaomi MiMo, OpenAI reference)

Shows the **real balance** from the provider's `/user/balance` (or equivalent) API. It refetches the moment the bar opens, refreshes, or the provider changes, then polls every 60 seconds. The last known snapshot is kept on failure so the row never goes blank.

When the balance drops below ¥20, the amount and a `Low` label turn red.

### Subscription mode (ChatGPT / Codex, OpenCode Go, Zhipu, Xiaomi MiMo Token Plan, Command Code)

Shows **quota remaining per window** (5-hour / weekly / monthly, where remaining = 100 − used) and a **countdown to the next reset**. Quota and countdown always come from the same window, so they can never disagree.

- **ChatGPT / Codex** — decoded **locally** from `~/.codex/auth.json`, showing the real plan tier and expiry date (for example `ChatGPT · Plus | Expires 2026-09-16`). Zero network calls: the values come straight from OpenAI's own login token, never estimated. Not signed in → **Refresh failed** with a reauthorization hint. Binding, token refresh and the `openai-codex` model route belong to the companion plugin [dsh-chatgpt-subscription](https://github.com/songoao25) — 