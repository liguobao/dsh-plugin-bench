# dsh-rigorquant

**English** | [简体中文](README.zh-CN.md)

<p align="center">
  <img src="docs/figs/edgesworth-box.png" alt="Edgeworth box with contract curve and Pareto optimum" width="70%">

</p>
<p align="center"><sub>
  <a href="docs/figs/edgesworth-box.png">Edgeworth box</a> — hand-drawn in
  <a href="https://en.wikibooks.org/wiki/LaTeX/PGF/TikZ">TikZ</a>, no AI-generated imagery
</sub></p>

Unattended-within-a-session, long-running **empirical/computational mathematics
research** for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)
— economics, finance, portfolio construction/optimization, simulation,
computational econ/finance.

RigorQuant is an agent preset + bundled skills that turns one DSH session into a
context-isolated multi-agent research lab:

- **Parallel explorers** propose candidate methods (`subagent_explorer`, blank
  context).
- An **OffGridThinker** (`subagent_offgrid`) works off the grid when a route
  must be isolated: raw model intelligence plus compute tools (sympy, numpy,
  mpmath, Lean checkers) — no web, no literature, no other agents' results.
- A **ground-truth track** re-derives the analytic closed forms, invariants, and
  bounds for simplified cases — twice, by different means (two independent
  `subagent_double_checker` calls).
- An **adversary** eliminates routes by counterexample only.
- A **four-part check battery** (closed-form equality, exact invariants,
  analytic bounds, statistical hardening) runs BEFORE numerical implementation.
- **A meta-validator** (`rq_check.py`) refuses a PASS whose evidence is missing:
  empty stage outputs, an empty `derivations/`, a registry with no
  audit-referenced passed route, or deliverables that do not compile. Its
  evidence checks read the audit record, not `study.json` — a study may not
  vouch for itself.
- **Fixed-seed + LLN** conventions for stochastic work.
- A **jacobian MCP escalation lane** (opt-in; Lean as a manual external lane)
  settles proof-critical claims before implementation.
- **PASS → auto-implement and proceed; BLOCKED → 3 rounds of the same gap →
  strongest derivation + exact gap; BUDGET → 5 rounds → checkpoint + report.**

The operating pattern adapts Shanmu Jin's Crouzeix-conjecture run
([prompt](https://github.com/jinshanmu/CrouzeixConjecture/blob/main/crouzeix_conjecture_prompt.txt),
[Lean audit](https://github.com/jinshanmu/CrouzeixConjecture/tree/main/Lean))
and Terence Tao's blueprint/equational-theories projects to numerical work.
Full design record: [docs/architecture.md](docs/architecture.md).

**"Unattended", precisely:** the framework runs unattended within one live
session. Crossing a session boundary disarms the goal; one human turn
("continue") re-arms it. It does not continue autonomously across restarts.

## The research team — and how it works

Eight roles around one hub, each a separate tool with its own powers and limits.
The Orchestrator is the only role that sees every report; the separation is
enforced by the composition, so **the producer never checks its own work** — an
idea dies only on a concrete counterexample, never on style or vibes.

<img src="docs/figs/avatar-orchestrator.png" align="left" width="200" alt="Orchestrator">

**Orchestrator** · `root persona` — fans out the work, synthesizes, and writes the state. Bound by four rules: producer ≠ checker, counterexample-only elimination, seeds always recorded, no handwaved load-bearing claims.

<br clear="left">


<img src="docs/figs/avatar-explorer.png" align="left" width="200" alt="Explorer">

**Explorer** · `subagent_explorer` — blank-context and divergent. Proposes lemmas, equations, constructions, and candidate methods with exact statements. Status reports are rejected.

<br clear="left">


<img src="docs/figs/avatar-offgrid.png" align="left" width="200" alt="OffGridThinker">

**OffGridThinker** · `subagent_offgrid` — the off-grid lane. Raw model intelligence plus the pinned compute lane (sympy, numpy, mpmath, cvxpy, hypothesis, jax; Lean checkers when provisioned) — and nothing else: no web, no skills, no delegation, no other agents' results. Its own agent, not an Explorer variant: isolation is the identity.

<br clear="left">


<img src="docs/figs/avatar-doublechecker.png" align="left" width="200" alt="DoubleChecker">

**DoubleChecker** · `subagent_double_checker` — blind (no web, no skills, no delegation, no drafts). Re-derives the load-bearing claims from first principles, twice by different means.

<br clear="left">


<img src="docs/figs/avatar-adversary.png" align="left" width="200" alt="Adversary">

**Adversary** · `subagent_adversary` — runs the check group and hunts counterexamples. Ends in a verdict: `PASS` or `NEEDS-EDITS`.

<br clear="left">


<img src="docs/figs/avatar-literature.png" align="left" width="200" alt="Literature">

**Literature** · `subagent_lit_line` · `_adversary` — a walled citation-graph sweep, then an independent adversary re-retrieves each claim and certifies it's real **and** current.

<br clear="left">


<img src="docs/figs/avatar-validator.png" align="left" width="200" alt="Validator">

**Validator** · `rq_check.py` + schemas — refuses a `PASS` with missing evidence. Reads the audit record, never the study's own claims — a study cannot vouch for itself.

<br clear="left">


<img src="docs/figs/avatar-document-adversary.png" align="left" width="200" alt="Document adversary">

**Document adversary** · `subagent_document_adversary` — an independent agent that audits each finished deliverable for **self-completeness** (the thing 90% of AI-generated writing drops): every jargon term, symbol, and abbreviation the document uses must be defined in the artifact itself or the audience spec's symbol registry. Returns `VERDICT: PASS` / `VERDICT: NEEDS-EDITS`; a `NEEDS-EDITS` is a blocking gap the validator refuses a `PASS` without.

<br clear="left">

### The team, live — the activity view

The plugin ships a **live activity panel** (the `rq-activity` host half, the
`shell.overlay` floater in the browser half): while a RigorQuant session runs,
a pill appears vertically centered on the main window's right edge (it follows
the conversation column, so the workspace rail and right-docked panels stay
clear), expanding into a panel that shows, for the **current session's lab
only** (never other sessions, and only while the current session is a
RigorQuant one), the
**five-move stage** the run is on, a hub-and-spoke role map (the Orchestrator
at the hub, every role it can delegate to as a spoke), a
working/idle roster with
their `docs/figs/` portraits, each role's last action, and a newest-first
activity feed. It is pure observation — it reads the events the core already
publishes and serves a JSON snapshot + portraits over
`/plugins/dsh-rigorquant/...`, and it changes no tool, route, or model. Colors
are `--dsw-alias` tokens, so it follows the shell's own light/dark theme.

<p align="center">
  <img src="docs/figs/agent-team-activity.svg" width="52%" alt="RigorQuant agent team activity view — team summary, segmented progress, member roster, and task dependency graph">
</p>

The picture above is the reader-safe rendering of the same design (the live
panel is only visible in a running web session) — adapted from the live
activity panel of [dsh-agent-teams](https://github.com/NanmiCoder/dsh-agent-teams)
— the picture in
[its README](https://github.com/NanmiCoder/dsh-agent-teams/blob/main/assets/ui.png)
— showing RigorQuant's own eight roles at a fan-out moment. The panel SVG is
generated from [`docs/figs/agent-team-activity.js`](docs/figs/agent-team-activity.js).

> **Attribution.** The activity-panel design is adapted from
> [dsh-agent-teams](https://github.com/NanmiCoder/dsh-agent-teams) by
> [NanmiCoder](https://github.com/NanmiCoder) (程序员阿江 / Relakkes) —
> Copyright (c) 2026, MIT License. The role portraits are this repo's own
> `docs/figs/` assets. The header banner is likewise reworked from the
> upstream hero graphic.

**The loop, in