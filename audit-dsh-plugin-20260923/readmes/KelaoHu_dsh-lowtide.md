<div align="center">

# dsh-lowtide

**Queue tasks when it's busy. They run on their own when it's cheap.**

<sub>Semi-auto or full-auto, off the model's peak hours and peak prices. A must-have plugin for DeepSeek Harness.</sub>

**English** | [简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-HK.md) | [العربية](./docs/README.ar.md) | [Deutsch](./docs/README.de.md) | [Español](./docs/README.es.md) | [Français](./docs/README.fr.md) | [Italiano](./docs/README.it.md) | [한국어](./docs/README.ko.md)

<img src="./assets/overview.png" alt="lowtide overview" width="100%">

</div>

---

![hero](./assets/screenshots/hero.png)

<p align="center"><i>Three tasks waiting in the queue, the price status glowing in the session header, auto-run when your window opens</i></p>

## Introduction

lowtide is a plugin for [DeepSeek Harness (dsh)](https://github.com/deepseek-ai/dsh). The problem it solves is plain and perfectly natural:

Usually, when you want an agent to do some work, you sit at the computer, send the agent an instruction, wait for the reply, and then review it by hand. But this workflow seems to forget that you have plenty of idle time — and a chance to dodge the peak/off-peak pricing that some models charge.

With lowtide installed, the day goes like this: whenever a job crosses your mind during the day, toss it in the queue, glance at it, release it. The tasks pile up until the time you set (say, after 7 PM — that's when DeepSeek is at valley pricing), then run by themselves. Next morning you open the report: keep what went well, send back what didn't.

That's all it is. But use it for a week and your working rhythm genuinely slows down — and don't forget, "time is money, efficiency is life"...

A few key capabilities:

- Four execution strategies: single, iterative, sampling, review — from "one pass is enough" to "run five candidates and I'll pick"
- 168 unit tests + 10 end-to-end specs, CI green across ubuntu / windows × node 22 / 24
- One build artifact serves both desktop and web — install once, works on both
- Off-peak execution lands in DeepSeek's valley hours: the same batch costs about half of what peak would

## A normal day with an agent might look like this…

**Ten minutes before clocking out.** You've finished reviewing code, so you file three tickets for tomorrow: a refactor (iterative, 3 rounds), a weekly report (single), and a design you're unsure about (sampling, 4 candidates). Release them all, shut down, leave. Tomorrow at your desk, the morning report says: the refactor's done, the report's drafted, and four candidate designs sit side by side, each with its cost written out.

**Friday night.** Queue a week's worth of chores in one go: dependency cleanup, missing tests, data scripts. Weekends are valley price around the clock. You go out; it works from home. Monday you check the report — retry what failed, merge what's good.

**A 10 AM brainwave.** You're mid-conversation with the agent about an urgent bug when you think "hey, update the docs too." The intercept card pops up: running now costs peak price, tonight it's about half — the difference is spelled out. Click "queue for off-peak"; your draft survives untouched, and you go back to the bug.

**An always-on server.** You've got a machine running dsh 24/7. Switch to L3 full-auto, then file tasks from anywhere through the API (`POST /ds-lowtide/tasks`). It runs them on schedule and writes the report. Nobody's watching, but the sandbox, the daily budget, and the file locks are all still there.

**Deliverables for a client.** Use the review strategy: run once, then automatically open an independent session that tears the result apart through your chosen focus (say, "hunt for data-source errors"). In the morning you don't get a bare result — you get a result plus a critical review.

**Living abroad.** You're in San Francisco; DeepSeek's peak is Beijing time, which for you lands in the evening and night before. Settings converts the official hours to your local clock, one click to adopt. You set windows by your own schedule, and the books always stay aligned with the official table.

## How lowtide works

```
① Intake             ② Adjudicate         ③ Execute               ④ Accept
Whenever you have    The queue dock        When the off-peak       When you're back:
a moment: one-click  groups tasks by       window opens: five      open the report —
from the intercept   workspace; triage    preflight gates pass,    results + diff
card, or file a  →   line by line:    →   then sandboxed runs →    + actual spend
ticket (4 strategies) ✓approve ⏸defer     one batch per window     + money saved
                     ✕drop / approve-all
```

A task's life: `pending-review → queued → preflight → running → done / failed / stale / timeout`, plus `deferred` (postponed) and `dropped` (soft-deleted, restorable).

Step two is where lowtide differs from a "fully automated script": **every task must be released by your hand before it runs** (in L2, you release the whole batch at once, 30 minutes before the window). The machine cannot move itself into the run queue. Execution is automated; decisions are not. That's why you can safely be absent.

## A tour of the lowtide interface

**The new-task modal.** Four strategies side by side, each with a plain-language hint; rounds, priority, and run mode ride along per task — no trip back to settings. Tasks land as "pending review". Nothing enters the queue without passing you.

![new-task-modal](./assets/screenshots/new-task-modal.png)

**Advanced options.** Model, reasoning effort, priority from 0 to 9, fresh session or continue-previous, and the locked-files list — all in one small pane. Locked files, briefly: anything on the list gets sha256-checked before execution, and if it doesn't match what you filed, the task goes stale and refuses to run. Otherwise the file you queued against could be rewritten by another task while waiting, and this one would blindly stomp on it.

![advanced-options](./assets/screenshots/advanced-options.png)

**Pick any model.** Batch runs default to the official `deepseek-flash` (DeepSeek-V4.1-Flash; the retired `deepseek-v4-flash` name still routes there at Flash prices), but each task can pick its own model — anything connected to your Harness is in the dropdown, grouped by provider. Private providers work too. Non-official models have no public price table, so the ledger honestly says "price unknown"; add a price override in settings if you want the bookkeeping exact.

![model-picker](./assets/screenshots/model-picker.png)

**The window editor.** Multi-segment, overnight, per-weekday — all fine. Underneath is a live 24-hour price band: red for peak, green for valley, and a marker showing where you are right now. Outside UTC+8, one click on "adopt official peak hours" converts Beijing time to your local clock.

![window-editor](./assets/screenshots/window-editor.png)

**The settings page.** Window hours, tasks per batch, per-task duration cap, concurrency, daily budget, report history, autonomy level, price overrides — all graphical, no config files. The official pricing rules (including the new all-weekend valley) are explained in human language on the same page.

![settings](./assets/screenshots/settings.png)

Three more pieces of UI appear in daily use: the **price pill** (session header — busy/idle, queue size; click it to edit windows), the **peak-hours intercept card** (type at peak, it appears; the price difference is spelled out; your draft survives), and the **execution report** (the morning briefing: savings first, anomalies pinned, candidates awaiting your pick, one-click Markdown copy).

## About lowtide workspaces

Every task runs inside a workspace. That single dropdown decides three things.

**Which files it can touch.** Tasks run in a sandbox whose boundary is the workspace directory. Pick wrong and at best it can't find the files; at worst it edits something it shouldn't.

**Who it queues with.** Tasks in the same wo