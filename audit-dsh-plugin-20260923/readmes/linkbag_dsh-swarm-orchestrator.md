# dsh-swarm-orchestrator

[English](README.md) · [简体中文](https://github.com/linkbag/dsh-swarm-orchestrator/blob/main/docs/zh-CN.md)

Role-based AI swarms for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness). Give it a goal, get a team: an architect breaks the work into a task graph, parallel builders execute it, reviewers hold the line, and an integrator ships the result — while you watch the whole thing move on a live kanban board.

It runs **inside** your `dsh web` host. No daemon, no second process, no glue scripts. Task agents are ordinary DSH subagents with your tool access and your models; the orchestrator is just a well-behaved Cordis plugin.

It has already shipped real work: the first production run reverse-engineered a biotech research dashboard and rebuilt it as a **six-indication suite** (680 curated clinical trials across six cancers) in a single afternoon — five data-curation agents working in parallel, every deliverable machine-verified.

---

## At a glance

**dsh-swarm-orchestrator** turns one goal into a supervised agent team inside DeepSeek Harness: an architect reviews your plan into `PLAN.md`, parallel builders execute it as a task DAG, reviewers gate quality, an integrator ships. Every role runs a model you pin from your live catalog, every deliverable can be machine-verified, and the whole pipeline is visible on a live kanban + flow chart.

```text
        you ── "spawn a swarm: ⟨goal⟩"
         │
         ▼
   your chat agent            (free to plan/research on its own —
         │  swarm_dispatch     its plan becomes the proposal)
         ▼
  ┌─────────────────┐
  │ architect-review │  deep-reviews the proposal against the repo,
  │  → PLAN.md       │  consolidates parallel workstreams (evidence-checked)
  └────────┬────────┘
    ┌──────┼──────┐
    ▼      ▼      ▼
 builder builder builder    ▸ parallel wave — one model per role,
    │      │      │           fallback chains, exclusive write scopes
    ▼      ▼      ▼
 reviewer reviewer (human)   ▸ rejections loop back with feedback;
    └──────┼──────┘            `reviewGate: "human"` parks it on you
           ▼
       integrator             ▸ merges, verifies, ships
           ▼
       📄 run report          ▸ per-task summaries · models used · stats
```

## Example Kanban View (real-time workflow)

<img width="1045" height="507" alt="image" src="https://github.com/user-attachments/assets/ab727b4a-c75a-41fe-be3c-3f68e9499c88" />

## Optional hybrid workteam
<img width="1057" height="541" alt="image" src="https://github.com/user-attachments/assets/9259d6f0-ea08-4aaa-9a5b-8f0302a839b4" />

## Why not just ask one agent?

Because one agent serializes. Long research tasks queue behind quick edits, context fills up, quality drifts, and nothing checks the output but the same model that wrote it.

This plugin takes the coordination seriously so you don't have to:

- **Parallel by construction.** Tasks declare dependencies (`blockedBy`); everything independent runs at once, bounded by a concurrency cap that adapts when the provider struggles.
- **Every role gets its own model.** Pin DeepSeek, GLM, Kimi, Claude — any model configured in DSH — to any role, with an ordered fallback chain and a per-role reasoning-effort ladder. The picker reads your live model catalog, so new providers show up automatically.
- **Review before "done" means done.** Tasks tagged `reviewBy` are judged by a reviewer agent against the task brief; a rejection loops back to the builder with the feedback attached. Want the last word yourself? Set `reviewGate: "human"` and approve from the dashboard.
- **Failure is a state, not a mystery.** Provider timeouts, quota exhaustion, bad evidence — each is detected, reported plainly, and handled: retries with resume hints, run pause/resume instead of burn-down, automatic model rotation after repeated failures.
- **Scoped to where you are.** Each chat's Swarm tab shows the runs for that chat's workspace; a persisted switch reveals everything on the machine when you want the full picture.
- **One run per goal, reviewed before built.** Dispatching into a workspace with an active run raises a warning (or a block, your choice); and unless you opt out, an architect agent reviews the dispatcher's plan into PLAN.md before any builder starts.
- **Memory-safe concurrency.** Swarm agents run in-process on the DSH host, sharing its Node.js heap. A global cap (`maxTotalConcurrentAgents`, default 8) ensures concurrent runs from different workspaces share the agent budget — preventing the heap exhaustion that can crash the host when too many agents run simultaneously.
- **Every agent stays on the board.** Task agents cannot spawn hidden sub-agents of their own (`maxSubagentDepth`, default 1). Without that bound an agent could delegate to helpers the dispatcher cannot see or account for — not counted by the global cap, not tracked by the watchdog, not shown on the board, yet all sharing the host heap. Measured on a real machine: one task spawned 12 such hidden helpers while the board showed a single task.
- **Work outlives its agent.** Every task agent writes a small completion report as its final action. If the host restarts and kills an agent between finishing the work and being recorded, the dispatcher adopts the on-disk report instead of throwing the finished work away and re-running the task. A task can also never sit `dispatching` forever: `spawnTimeoutSeconds` arms a sliding no-progress window — it runs from creation, then every heartbeat re-arms it, so a working child is never killed for elapsed time while a child that never starts or goes silent is reclaimed (per-role override in the Roster).
- **The right effort for the right model.** Before a child is spawned, the pinned reasoning effort is validated against the deployment's declared model capabilities: a model that cannot accept the level has the pin stripped, and the candidate chain is never filtered — the `UNSUPPORTED_REASONING_EFFORT` crash that killed 6 tasks in one run cannot happen. If a pin still reaches a model that refuses it, the child dies fast with no output, and the dispatcher retries the *same* model at the next rung of the effort ladder (`max` → `high` → … → no pin) before any model rotation — without spending the task's retry budget. Reviewer pins are validated the same way.

> ⚠️ **Running multiple swarms from different workspaces in parallel**: this is supported and safe with the global cap. However, be mindful that each swarm agent is an in-process session on the host. We recommend **max 2 concurrent runs** with the default cap of 5 total agents. If you experience `ERR_CONNECTION_REFUSED` (host crash), lower `maxTotalConcurrentAgents` to 3 in the Runtime settings.

### Reliability notes (v0.5.8 – v0.6.17)

Diagnosed from 47 recorded runs / 184 task failures plus the incidents below, then fixed and regression-tested:

- **Evidence commands run under PowerShell** (bash elsewhere) from the workspace root, and the `evidence.commands` schema says so. Previously they were handed to `cmd.exe`, so a perfectly normal PowerShell gate (`if (Test-Path …) { exit 0 }`) failed the task — 32% of all recorded task failures. Prefer `evidence.files` where a file check can express the gate: it involves no shell at all.
- **`modlens` is denied to swarm roles** by default in the shipped roster guidance: it is an interactive tool that asks the user a question, and swarm children run non-interactively. Add it back per-role from the Roster if your deployment has a headless vision provider.
- **A task report that does not claim `"status": "completed"` is never adopted** — adoption cannot mask unfinished work.
- **An adopted report must also have been written by the live attempt.** `.dsh-swarm/task-<id>.json` is keyed by task id, not by run, so reusing an id silently shares the file across runs. A report older than the current attempt's `task/started` is now ignored (and logged) instead of being credited as t