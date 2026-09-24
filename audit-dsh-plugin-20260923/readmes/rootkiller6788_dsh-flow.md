# dsh-flow

[中文](./README_CN.md) · **English**

What stalls long or complex work is usually not "not enough tools". It is that the executor cannot be swapped, the state has no source of truth, and the boundaries have no assertions — a task that has run for hours crashes once and cannot say how far it got; changing how work is executed means changing the core, and so does adding a kind of team source.

dsh-flow solves all three at the level of **kernel shape**: `rules/` is a pure core (no IO, no `ctx`), execution and sources are **declared seams**, and `kernel.js` is the single composition root that decides which implementation this deployment attaches.

It and [dsh-agent-teams](https://github.com/NanmiCoder/dsh-agent-teams) are **two kernel shapes**: the same capability surface, the opposite internal shape. That opposition is where this document starts.

![Agent canvas: requirement timeline + team hierarchy + artwork inspector](assets/1.png)

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-0B7285?style=flat-square" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Node.js-%3E%3D22.19.0-3c873a?style=flat-square" alt="Node.js >= 22.19.0">
  <img src="https://img.shields.io/badge/DSH-web%20profile-5B4CF0?style=flat-square" alt="DSH web profile">
  <img src="https://img.shields.io/badge/runtime%20deps-0-2ea44f?style=flat-square" alt="zero runtime dependencies">
  <img src="https://img.shields.io/badge/build%20step-none-f0ad4e?style=flat-square" alt="no build step">
</p>

## Two kernel shapes

In the host's own words, the difference is **whether a plugin divides its own internals into services**. The host frames this as "everything is a plugin" and "Plugins, not loop changes", which in code comes down to the `core` / `seam` split:

| Usual phrasing | The host's own terms | The evidence |
| --- | --- | --- |
| **microkernel** | Keep `core` as small as possible and hang every capability off a **declared seam**; new behaviour goes on an extension point rather than into `core` | dsh-flow: a `rules/` pure core (no IO, no `ctx`) + three services + one composition root |
| **monolithic kernel** | No seam; the capabilities all live inside `core` | dsh-agent-teams: `src/` is one flat plane (17 TS modules + 13 under `client/`), importing each other freely, with no mechanism asserting module boundaries |

A seam comprises three roles — **Service Definition / Provider / Consumer** — and is only complete with all three. In dsh-flow they line up plainly: `runner/interface.js` is the definition, `manual.js` and `subagents.js` are the two Providers, and `tools/` is the Consumer.

**Both are DSH plugins**, and both attach to seams the host provides — the difference is whether the plugin has seams of its own. Once the functionality is split into core and seam, "add another way to execute" is adding a Provider and "add another kind of team source" is one `register()` call; on a flat `src/`, that work is changing the core.

So this is an **opposition, not an absorption**: the capability surfaces can be aligned (the 13 tools map one to one to `agent_teams_*`, and the 31 differential checks in `pnpm test:diff` guard that line), but the two kernel shapes cannot give the same set of guarantees.

### What it is like to use

| | dsh-flow | dsh-agent-teams |
| --- | --- | --- |
| Install | Clone it and it runs, **nothing to install** | Pulls a whole dependency tree (24 peers, including React 18) |
| Host upgrade | Declares no host version; probes capabilities at runtime and takes a fallback branch when it cannot | Pins 4 host versions in its peers; outside those it will not work |
| Change one canvas line | Save → **refresh the page** (0 builds, 0 restarts) | Rebuild the client bundle → **restart the host** |
| Stop execution, keep the view | `runner: manual` — look and edit, nothing runs | No equivalent switch |
| How a task's attempts went | Click a task row for the **attempt timeline**: how each attempt ended, which was rolled back | A monotonic attempt counter that cannot say how any one ended |
| Unreadable lines | Go into the **import report**, listed with **line numbers** on the canvas | — |
| Teams that cannot reach the canvas | Counted in the toolbar; they do not vanish silently | — |
| Approving a plan | Edit and approve directly on the canvas, through the same validation `flow_edit_plan` / `flow_approve` use | Panel editing |
| The canvas | Session timeline and team hierarchy **in one figure** (the team nests under the requirement turns) | A team tree panel |
| Uninstalling the other plugin | Everything keeps working — there was never a second record | — |

What you can "feel" in the table above all comes from the architecture: **a change takes effect on refresh** because canvas modules are served over HTTP individually (`src/**` invalidated by mtime + ETag revalidation), with no bundle step; **`runner: manual` exists** because execution is a seam, fixed at composition time; and **uninstalling the other plugin changes nothing** because team records are this plugin's own append-only log, with the other plugin only an entry in the source registry. Changing `client.js` (the tab registration layer) still requires a host restart on both sides — that layer really does go into the host's client bundle.

### Measurements

All of these are this repository's own numbers, reproducible with one command:

| Item | Number |
| --- | --- |
| Cost of the plugin on the host's startup path (`import './index.js'`) | **4.3 ms** |
| Composition root assembly (`import './kernel.js'`, cold) | 33 ms |
| A change to `src/canvas/**` taking effect | **0 builds, 0 restarts** |
| Canvas first paint | 41 requests / 449 KB; every request afterwards revalidates by ETag, so unchanged files are a 304 |
| The layer-boundary gate (107 modules parsed + 7 layers asserted + serve allowlist) | 4.0 s |
| All 434 tests | 1.1 s |

### Why there is no "N times faster" here

A cross-implementation performance comparison requires **both sides to run on this machine**. dsh-agent-teams' full pipeline does not: it has no `node_modules` and no `lib/` (its published artifact), and its `snapshot.ts` imports host runtime packages directly (`@deepseek-ai/dsh-llm`, `@deepseek-ai/dsh-agent`). Replacing those with stubs and then timing measures the stubs, not it. Its state-reading layer (`src/state.ts`) depends only on Node builtins and could in principle run directly under Node 24, but that is another repository's code, and running it needs your explicit consent.

So any "N times faster" in this repository would be invented. What can be given is the kind of difference above — **confirmable without running anything** — plus my own reproducible measurements.

## Long-running work

The longer it runs, the more two things matter: a crash that cannot say how far it got, and a state that forks without telling you.

- **The source of truth is an append-only `events.jsonl`; `state.json` is only one reading of it.** When the two disagree the log wins, and the disagreement is judged an error by `teamDiffEvents` rather than quietly smoothed over — reconciliation **refuses** a difference it cannot express instead of picking a winner. The longer it runs the likelier state forks, and silently picking a winner is how errors accumulate.
- **How many times a task was tried, how each ended, which was rolled back** — click a task row for the **attempt timeline**. This information exists only at the protocol layer: a monotonic attempt counter cannot say how any single attempt ended.
- **A line that cannot be read never stops parsing**, but it does go into the import report, listed on the canvas with its **line number** (kind / member / line / reason). The line number is the only thing that makes a file that ran itself damaged fixable.
- **If it runs away you can keep the view and stop the work**: `runner: manual` lets you look and edit while nothing executes. This is a **composition-time