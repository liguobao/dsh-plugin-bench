<div align="center">

<h1><img src="https://raw.githubusercontent.com/KCNyu/clawock/refs/heads/master/site/assets/logo-lockup.svg" alt="clawock" height="48"></h1>

### AI argues. Code settles. The losses stay on the page.

[![PyPI](https://img.shields.io/pypi/v/clawock?label=PYPI&style=flat-square&logo=pypi&logoColor=white&labelColor=252b35&color=4b91c8)](https://pypi.org/project/clawock/)
[![npm](https://img.shields.io/npm/v/clawock-dsh?label=NPM&style=flat-square&logo=npm&logoColor=white&labelColor=252b35&color=4b91c8)](https://www.npmjs.com/package/clawock-dsh)
[![Tests](https://img.shields.io/github/actions/workflow/status/KCNyu/clawock/ci.yml?label=TESTS&style=flat-square&logo=githubactions&logoColor=white&labelColor=252b35&color=738391)](https://github.com/KCNyu/clawock/actions/workflows/ci.yml)
[![Live Data](https://img.shields.io/github/actions/workflow/status/KCNyu/clawock/dashboard-artifact-gate.yml?label=DATA&style=flat-square&logo=githubactions&logoColor=white&labelColor=252b35&color=738391)](https://github.com/KCNyu/clawock/actions/workflows/dashboard-artifact-gate.yml)
[![Coverage](https://img.shields.io/endpoint?url=https%3A%2F%2Fkcnyu.github.io%2Fclawock%2Fassets%2Fdata%2Fcoverage.json&style=flat-square&logo=python&logoColor=white&labelColor=252b35)](https://github.com/KCNyu/clawock/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/LICENSE-MIT-aab5bf?style=flat-square&labelColor=252b35)](https://github.com/KCNyu/clawock/blob/master/LICENSE)

[**Live dashboard**](https://kcnyu.github.io/clawock/) &nbsp;·&nbsp; [**Daily briefs**](https://kcnyu.github.io/clawock/briefs.html) &nbsp;·&nbsp; [**Evidence**](https://kcnyu.github.io/clawock/evidence.html) &nbsp;·&nbsp; [**简体中文**](https://github.com/KCNyu/clawock/blob/master/README.zh.md)

<a href="https://kcnyu.github.io/clawock/">
  <img src="https://raw.githubusercontent.com/KCNyu/clawock/refs/heads/master/site/assets/social-card.png" alt="clawock — portable investment decision workflows for any external AI agent, proven on a live HK and US desk" width="820">
</a>

<sub><i>“The market doesn't care how confident the model was.”</i></sub>

<a href="https://kcnyu.github.io/clawock/"><img src="https://raw.githubusercontent.com/KCNyu/clawock/refs/heads/master/site/assets/dashboard.gif" alt="clawock dashboard cycling through its tabs" width="820"></a>

| **<!-- CW_M:days -->127<!-- /CW_M:days -->** | **<!-- CW_M:rows -->881<!-- /CW_M:rows -->** | **<!-- CW_M:settled -->144<!-- /CW_M:settled -->** | **43** | **5** | **0** |
|:---:|:---:|:---:|:---:|:---:|:---:|
| days live on a real HK + US account | decisions on the public ledger | episodes settled by code | data modules across 8 layers | agent harnesses, one contract | scores the model wrote for itself |

<sub>Real positions, real P&amp;L — <!-- CW_M:return_pct -->−17.30%<!-- /CW_M:return_pct --> since day one, published exactly as it is — graded in the open. Numbers and previews refresh weekly; the live dashboard updates through the trading day.</sub>

</div>

Every trading day, clawock turns raw market information into decisions that get graded:

- **Collect.** 43 fetch and compute modules across 8 layers: quotes, SEC and HKEX filings, capital flow, bilingual news, Reddit and influencer feeds, with multi-source fallback. Python fetches; the model only reads the assembled context.
- **Compute factors.** Quant factors, cross-sectional ranks, peer residuals and a trend × volatility leverage dial, all computed deterministically in Python.
- **Backtest.** A factor's clustered bootstrap interval has to clear 50% before it may influence a decision; the cross-sectional layer is pre-registered; the leverage dial is scored out of sample. What fails is published on the [evidence page](https://kcnyu.github.io/clawock/evidence.html).
- **Decide.** Four analyst lenses, a bull and a bear, three risk voices and a judge argue over the same context and write `plan.json`.
- **Settle.** Python settles every decision against real prices. The model never touches its own score, and every result lands on the public scorecard.

The whole pipeline plugs into the agent you already use: Claude Code, Codex, OpenClaw, DeepSeek Harness, or your own → [install and the full loop](#run-it-on-your-own-book)

---

## What this is

This started as one account, not a package. A multi-agent desk debates the
evidence on a real brokerage account with separate Hong Kong and US books and
proposes trades; the account owner still places the orders. What comes out of
that is the record: real positions, a growing decision history, and a public
scorecard the model has no say in — not a get-rich bot, and not a
copy-trading service.

clawock is the part of that desk pulled out to be reusable. Your runtime keeps
the model call, the conversation, memory, tools, permissions and credentials.
clawock adds the decision contract on top: certified evidence, a required
opposing case, checked money and FX arithmetic, and outcomes linked back to the
decision that caused them. It is files and a CLI, so switching harness leaves
the contract unchanged.
[`examples/`](https://github.com/KCNyu/clawock/blob/master/examples/README.md) runs the
same decision from a pure CLI, an OpenClaw skill, a Claude Code instruction, a
Codex AGENTS.md, and a DeepSeek Harness agent.

To try it without installing anything locally, open a Codespace and run
`examples/cli/minimal-run/run.sh`: a clean virtualenv, no credentials, no
broker, and the same script CI runs against every published wheel.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/KCNyu/clawock)

### What makes it different

- **A workflow plugin, not another agent or harness.** The runtime keeps its model, chat, memory, skills engine, tool loop and permissions; clawock owns only the decision contract, so it moves between runtimes unchanged.
- **The loop continues after the answer.** Evidence, the opposing case, thesis,
  decision, execution, and observed outcome share one lineage. Measured results
  can propose bounded parameter changes, but never silently rewrite strategy.
- **Real money, graded in public.** One live Hong Kong + US brokerage account, with a public scorecard that keeps every eligible result — the losses included, and the fact that the active calls haven't beaten buy-and-hold. Each published headline names the ledger slice, window and commit it was computed from, and `clawock scorecard-provenance --check` recomputes it from `memory/decisions.jsonl` — a re-graded row inside a published window shows up as a mismatch.
- **The model can't grade itself.** LLMs propose trades; Python settles them and computes the scorecard.
- **One thesis, one episode.** Repeated opinions on the same thesis count once. Each episode is settled from canonical vendor bars, with declared gap-fill rules when a session is missing.
- **The ledger has to reconcile.** A money-conservation check runs before every push; if cash, positions, and P&L don't balance, nothing is published.
- **Built to keep running.** Scheduled Hong Kong and US sessions produce the daily briefs and refresh the live dashboard through the trading day.

For the canonical EN/ZH rendering of every project term — composite, regime, DSR, CSCV, triple barrier, run card and the rest — see the [glossary](https://github.com/KCNyu/clawock/blob/master/docs/glossary.md).

## How it works

The product boundary is simple: the external agent reads and reasons; clawock
owns the portable decision workflow and the deterministic truth around it.

![clawock product architecture — external runtimes own models, conversation, memory and tools while the package supplies portable workflows, certified context, deterministic reconciliation, evaluation and bounded improvement](https://raw.githubusercontent.com/KCNyu/clawock/refs/heads/master/site/assets/product-architecture.svg)

The KCNyu deployment then applies that product boundary to one live portfolio.
This second di