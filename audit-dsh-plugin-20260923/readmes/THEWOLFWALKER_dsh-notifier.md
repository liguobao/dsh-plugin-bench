# dsh-notifier

> **Your agent, in your pocket.** — 通知、审批、遥控，全在你的手机里。

> **Maintenance notice (维护公告)**: until **2026-10-01**, the author is taking exams and cannot promptly maintain the project or review PRs/issues — replies will be delayed. Apologies for the inconvenience; outstanding items will be picked up after that. 至 **2026-10-01** 前作者因考试无法及时维护与查看 PR/Issue，回复会延迟，非常抱歉。

**English** · [**简体中文**](README.zh-CN.md)

![DSH](https://img.shields.io/badge/DSH-DeepSeek%20Harness-1F6FEB?style=flat-square)
![Node.js](https://img.shields.io/badge/Node.js-22%2B-339933?style=flat-square&logo=node.js&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ESM-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Cordis](https://img.shields.io/badge/Cordis-plugin-FF6B6B?style=flat-square)
![Zero deps](https://img.shields.io/badge/zero%20deps-000000?style=flat-square)
![Bilingual](https://img.shields.io/badge/bilingual-EN%2F%E7%AE%80%E4%BD%93-00A98F?style=flat-square)
![Channels](https://img.shields.io/badge/channels-27-00B4D8?style=flat-square)

![npm version](https://img.shields.io/npm/v/dsh-notifier?style=flat-square&logo=npm&logoColor=white)
![tests](https://img.shields.io/badge/tests-1616-brightgreen?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square)
![awesome-dsh-plugin](https://img.shields.io/badge/awesome--dsh--plugin-listed-00B4D8?style=flat-square)
![omdsh workshop](https://img.shields.io/badge/omdsh-workshop-7C3AED?style=flat-square)
[![dshfind](https://dshfind.com/api/badge/THEWOLFWALKER/dsh-notifier?lang=en)](https://dshfind.com/en/plugins/THEWOLFWALKER/dsh-notifier?ref=badge)
[![dshfind downloads](https://dshfind.com/api/badge/THEWOLFWALKER/dsh-notifier?metric=downloads&lang=en)](https://dshfind.com/en/plugins/THEWOLFWALKER/dsh-notifier?ref=badge)
[![dshfind plugin card](https://dshfind.com/api/card/THEWOLFWALKER/dsh-notifier?lang=en)](https://dshfind.com/en/plugins/THEWOLFWALKER/dsh-notifier?ref=badge)

![never miss](https://img.shields.io/badge/never%20miss-a%20turn-00BFFF?style=flat-square)
![silence](https://img.shields.io/badge/silence%20never-approves-9C27B0?style=flat-square)
![push](https://img.shields.io/badge/push%20it-real%20good-FF4081?style=flat-square)

Package metadata: `dsh-notifier@0.10.2` · 1616 automated contract tests (1616 pass) · MIT licensed.

Bring your [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) agent to the places you already use. dsh-notifier puts one minimal `notify()` API in front of 27 channels, then adds phone-friendly approvals, questions, session controls, and a calm local console — with no second runtime to deploy.

[Get started](docs/guide.md) · [Upgrade guide](docs/upgrade-guide.en.md) · [Plugin integration](PLUGINS.md)

Your agent and the harness itself both push through it: session events (`turn/end` · `approval/asked` · `agent/error`) auto-notify, the model calls a `notify` tool directly, and six inbound channels carry approvals, conversations, and multiple-choice questions (`ask_user`) back from your phone. Decisions are single-use and fail-closed — unknown sources and QQ GROUP control are rejected by default. Long tasks send heartbeats and stall alerts with a one-click stop button; identity is runtime pairing codes and bindings, not YAML strings — all with zero runtime dependencies.

## How it works

```
DSH agent ──notify() tool─────────┐
                                  ├─▶ notifier core ─▶ 27 channels (IM webhooks / push apps / China apps)
DSH session events ──auto push────┘   level routing · tiered retries · segmentation · anti-disturb · ledger
                                      heartbeat ⏱ / stall ⚠ (v0.5) ──▶ cards with a ⏹ stop button
your phone ──6 inbound channels───▶   remote approval (buttons · reply 1/2) · remote conversation (followup/inject/steer) · remote questions (option cards + custom/skip aux buttons, v0.8)
```

Every message resolves through one chain — level (`timeSensitive` / `active` / `passive`) → routing (multi-agent matrix) → channel adapter (`resolve(cfg)` + `send(msg)`). Two trigger lines feed it: the harness auto-pushes session events (debounced, deduped), and the model calls the `notify` tool. Six inbound channels ride the same core in reverse for approvals and conversation — and since v0.5 the outbound line reports back too: long-running turns send heartbeats, silent turns raise stall alerts, and Telegram/Feishu notifications carry a one-click stop action.

## Web admin console

The console is enabled by default and binds loopback only (mobile-friendly since v0.5). Zero-config onboarding: no YAML needed after install — open the exact `http://127.0.0.1:<port>/#token=...` link printed by the startup line (port conflicts fall back to a free port automatically; the token lives only in the URL fragment and is printed once). The in-page unlock gate verifies silently, then a first-visit wizard walks you through: pick a notification channel → fill in credentials → receive a real test notification on your phone. Remote reply, approvals, and member pairing can be configured later; bindings and sessions stay behind an explicit advanced-settings toggle.

| Page | What it shows |
|---|---|
| **Home** | link status & next actions, outbound/inbound channel health matrix, pending questions, audit stream; a three-step setup wizard when nothing is configured yet |
| **Channels** | outbound-first credential forms (masked `***`; untouched `***` fields are never submitted), instant real test send, QR authorization |
| **Members** (v0.7.0) | identity bindings (roles / labels / pairing time), pairing codes, pending-binding confirmations |
| **Notifications** (v0.4.0) | live SSE event stream, system-notification preferences, event log |
| **Bindings** (advanced) | agent × channel checkbox grid, per-channel default agent |
| **Sessions** (advanced) | per-session outbound resolution with override editing |

> **Outbound config is "view-hot, delivery-cold"** (G-14, W12): saving an **outbound** channel in the admin console reflects in the UI immediately, and the channel card shows a **"重启后生效" (takes effect after restart)** badge — the delivery layer (outbound router/channel instances) only merges runtime config (YAML ⊕ store) at the **next plugin startup**; inbound credentials likewise reconnect at next startup. Test send is exempt: it runs against the latest merged config instantly, no restart needed.

### What it looks like

| Zero-config onboarding wizard | Channel setup (configured + collapsible groups) |
|---|---|
| ![First-visit onboarding wizard](docs/screenshots/fresh-wizard-desktop.png) | ![Channel setup](docs/screenshots/configured-channels-desktop.png) |

| In-page unlock gate (silent token check) | Mobile layouts |
|---|---|
| ![Unlock gate](docs/screenshots/gate-unlock.png) | ![Mobile · channels](docs/screenshots/configured-channels-mobile.png) · ![Mobile · wizard](docs/screenshots/fresh-wizard-mobile.png) |

Screenshots captured from the loopback console (blue-white theme, aligned with the DeepSeek Harness design tokens). The console binds loopback only and is mobile-friendly from v0.5.

## Quick start

```bash
dsh plugin add dsh-notifier --profile <profile-name>
```

> `--profile` is required (DSH 0.1.0-rc.6+): plugin installs target a named profile — use the one you run (e.g. `web`).

No YAML needed. Restart DSH, then open the full link printed by the `Web 管理台已就绪` startup line (looks like `http://127.0.0.1:<port>/#token=...`):

1. The token in the link verifies silently and the first-visit wizard opens;
2. Pick a channel your phone already has (Bark / Telegram / Feishu / DingTalk …) and fill in its credentials;
3. Hit "save & send test notification" — **once your phone buzzes, setup is done**.

That's it. `turn/end`, `approval/asked`, and `agent/error` events now reach every configured channel, and the model can push on its own with `notify({ message, channel, title })`. Long tasks send he