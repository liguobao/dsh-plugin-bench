# All in Luna

[简体中文](README.zh-CN.md)

<p align="center">
  <img src="docs/assets/brand/all-in-luna-mark.svg" width="112" alt="All in Luna mark" />
</p>

> **Stop running an entire project inside one AI conversation.**

Give All in Luna one big goal.

It turns the work into independent top-level tasks: **run what can run in parallel, wait only on real dependencies, keep each task's context separate, and bring the results back together.**

Each task can still use its own subagents, tools, Skills, or MCPs.

**Parallel across tasks. Recursive inside tasks.**

<p align="center">
  <img src="docs/assets/brand/hero-topology.svg" alt="All in Luna task topology" />
</p>

---

## Why does this exist?

Small AI coding tasks are easy.

The hard part looks more like this:

> “Refactor authentication end to end, including the backend, frontend, migration, tests, and documentation.”

At first, everything is fine.

Then the agent reads files, edits code, runs tests, starts subagents, handles failures, reads more files, and keeps pushing more execution detail back into the same conversation.

After enough turns, familiar problems appear:

- the context keeps growing;
- unrelated work starts contaminating other work;
- earlier constraints become easier to forget;
- one local blocker stalls the whole flow;
- subagent results become harder to manage;
- a new conversation has to reconstruct what really happened;
- the agent says “done,” but the outcome may not actually be complete.

**All in Luna starts from one simple idea: one conversation should not have to carry an entire project.**

<p align="center">
  <img src="docs/assets/brand/before-after.svg" alt="One giant context versus clear task lanes" />
</p>

---

## One more layer above subagents

A typical agent workflow looks like this:

```text
You
 │
 ▼
Main Agent
 ├─ subagent
 ├─ subagent
 └─ subagent
```

All in Luna adds a real **Top-level Task** layer above local workers:

```text
You
 │
 ▼
All in Luna
 │
 ├─ Top-level Task A
 │    ├─ local work
 │    └─ subagents / tools / Skills
 │
 ├─ Top-level Task B
 │    ├─ local work
 │    └─ subagents / tools / MCPs
 │
 └─ Top-level Task C
      └─ waits only when it actually depends on A
```

**A Top-level Task is not just another subagent.**

It is an independent work domain with its own goal, context, dependencies, working state, local execution process, and result boundary.

A subagent is a local worker a Task may use when that Task needs to split its own work further.

> **All in Luna does not replace subagents. It gives them a better place to live.**

---

# What you get

## 1. Real top-level tasks

A large goal can become independent work domains instead of temporary chat branches.

For example:

```text
Add billing to this app

├─ Billing backend
├─ Checkout UI
├─ Database migration
├─ Integration tests
└─ Documentation
```

Each task can move independently, wait on dependencies, produce results, and keep its own working context.

## 2. Parallel when possible

Independent work does not need to queue behind unrelated work.

```text
Billing backend       ● running
Checkout UI           ● running
Documentation         ● running
Database migration    ○ waiting for schema
Integration tests     ○ waiting for backend
```

**One blocked task doesn't freeze unrelated work.**

## 3. Separate working contexts

Backend debugging does not need to share one giant context with frontend changes, test logs, documentation, and release work.

Your main conversation should mostly see:

```text
✓ what is done
● what is running
○ what is waiting
! what needs your decision
```

File reads, terminal output, test logs, diffs, and implementation detail can stay with the Task that produced them.

**Your main conversation does not need to become the project's log file.**

## 4. Recursive local workers

A Top-level Task can still split into WorkUnits or use local subagents when it is complex on its own.

```text
Backend Task
 ├─ API
 ├─ database changes
 ├─ tests
 └─ migration checks
```

Local complexity stays local.

**Parallel across tasks. Recursive inside tasks.**

## 5. Resume instead of restarting

All in Luna persists run state, task state, dependencies, and results.

Long-running work does not have to remain attached to one ever-growing conversation.

```text
start
→ work
→ stop
→ come back
→ resume
```

Completed work does not have to be rediscovered from chat history.

## 6. Verify before “done”

An agent saying:

> “Done.”

is not the same as the task actually being complete.

All in Luna can check tests, builds, changed files, artifacts, and declared outputs before accepting a task as complete.

## 7. Bring your own workflow

All in Luna is not one fixed workflow.

Use the default delivery path for ordinary software work.

Use **GSD** inside a Task when you want a more explicit development workflow.

Connect **Research Routes** for research-oriented work.

Tasks can also use other Skills, MCPs, tools, and host capabilities.

**The Core runs complex work. It does not dictate how every task must think.**

---

# Example

Suppose you say:

> **“Refactor this application's authentication system, including backend, frontend, migration, and tests.”**

All in Luna can organize it as:

```text
Authentication refactor

├─ Task 1 — Auth backend
│    ├─ session/token logic
│    ├─ API
│    └─ backend tests
│
├─ Task 2 — Frontend auth flow
│    ├─ login
│    ├─ logout
│    └─ protected routes
│
├─ Task 3 — Migration
│    └─ waits for auth contract
│
└─ Task 4 — Integration
     └─ waits for backend + frontend
```

Task 1 and Task 2 can move at the same time.

Task 1 can still use its own subagents if needed.

Task 3 waits only for the result it actually depends on.

You do not have to follow the complete implementation history of all four tasks in one conversation.

---

# When should I use it?

All in Luna is a good fit for:

- large features;
- work spanning frontend / backend / tests / docs;
- major refactors;
- migrations;
- several outcomes that can move independently;
- long-running coding sessions;
- work where one blocker should not stop the whole project;
- tasks that need different tools, models, or workflows;
- work you want to resume instead of reconstructing from chat history.

If you are fixing one typo, explaining one function, changing one CSS rule, or doing another tiny linear task, using the current agent directly is usually faster.

**All in Luna solves the organization problem of complex work. It does not make simple work complicated.**

---

# Models & performance

<p align="center">
  <img src="docs/assets/brand/models-performance.svg" alt="Models and performance routing" />
</p>

## You do not have to configure anything

Most users do not need to choose a model policy first.

If you do not specify one, All in Luna uses resources available through the current environment, host, or deployment policy.

It does not require every user to use one fixed model or provider.

## You can take control when you want

Different kinds of work do not always deserve the same amount of expensive reasoning.

For example:

```text
Planning        → stronger reasoning
Implementation  → balanced
Mechanical work → fast / efficient
Verification    → strong / independent
```

> **Spend strong reasoning where it matters, not everywhere.**

All in Luna also separates the problem itself. Strong models can work on narrower, more stable objectives with less unrelated context and fewer cross-task switches.

**Less unrelated context. Less task switching. Less room for drift.**

Common ways to use the resource system include:

- **Balanced** — sensible defaults for most projects;
- **Quality first** — stronger reasoning for architecture, difficult debugging, risky refactors, and research;
- **Efficient** — reserve stronger reasoning for decomposition, hard blockers, synthesis, and final verification;
- **Single model** — keep the run on one explicitly selected model where possible.

These are usa