<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/banner-dark.svg">
  <img src="./assets/banner-light.svg" alt="task-coordinator" width="600">
</picture>

**Codex-style cross-task coordination · a supervisor plugin for DeepSeek Harness**

[![DSH 0.1.2-rc.1 verified](https://img.shields.io/badge/DSH-0.1.2--rc.1%20verified-16A34A?style=for-the-badge)](docs/PROTOCOL.md)
[![Node.js](https://img.shields.io/badge/Node.js-%5E22.19%20%7C%20%3E%3D24-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)](package.json)
[![155 unit tests](https://img.shields.io/badge/tests-155%20unit-0EA5E9?style=for-the-badge)](test/smoke.test.mjs)
[![MIT](https://img.shields.io/badge/license-MIT-7C3AED?style=for-the-badge)](LICENSE)

[What is this](#what-is-this) · [Screenshots](#screenshots) · [Quick start](#quick-start) · [Tools](#the-eleven-tools) · [Architecture](docs/ARCHITECTURE.md) · [Host contract](docs/PROTOCOL.md) · [Web bridge (zh)](docs/WEB-BRIDGE.md) · [Changelog](CHANGELOG.md) · [Chinese](README.zh-CN.md)

</div>

---

## What is this

**Once installed, you just say what should run in parallel — the `task_*` tools handle every step of the orchestration:**

```text
Split this into three tasks and run them in parallel: A researches the approach,
B builds the prototype, C runs the tests. Summarize for me when they finish.
```

What happens behind the scenes: you (plain language) → supervisor session → decomposition analysis → **an approval card you confirm** → batch-spawned task sessions → each task reports its result back when done → the supervisor summarizes. You never watch a single step in between, but the decision points stay in your hands.

- This is a DSH plugin: **any top-level session** can discover tasks, read progress, spawn tasks and deliver instructions;
- Spawned tasks **appear in the GUI session list immediately** (the same `api-session/added` event the sidebar consumes);
- Every cross-task message is stamped with a `coordinator` source — visible and attributable in the target session's transcript;
- One prerequisite: **DSH Desktop is installed and starts** (the plugin never launches the host for you).

> 📌 Host contract verified on **DSH 0.1.2-alpha.1**; every capability passed real-host end-to-end testing after restart (criteria in [Host contract](docs/PROTOCOL.md)).

## Screenshots

<table>
  <tr>
    <td><img src="./assets/shot-1.png" alt="task-coordinator in the DSH Desktop GUI (1/4)" width="420"></td>
    <td><img src="./assets/shot-2.png" alt="task-coordinator in the DSH Desktop GUI (2/4)" width="420"></td>
  </tr>
  <tr>
    <td><img src="./assets/shot-3.png" alt="task-coordinator in the DSH Desktop GUI (3/4)" width="420"></td>
    <td><img src="./assets/shot-4.png" alt="task-coordinator in the DSH Desktop GUI (4/4)" width="420"></td>
  </tr>
</table>

<sub><i>Live GUI captures — the same four shots are declared in <code>screenshots.json</code> for the dsh-market detail view.</i></sub>

## Quick start

### Prerequisites

- DSH Desktop (contract verified on 0.1.2-alpha.1);
- Node.js `^22.19.0 || >=24` (the host runtime usually satisfies this already);
- PowerShell (the deploy script is `.ps1`).

### Install (one command)

> 🛒 **Listed on [awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) (Workflow & Automation)** — with the in-app [dsh-market](https://github.com/dsh-market/dsh-market) plugin browser, search “task-coordinator” and install/upgrade with one click. The git-clone route below is the no-market equivalent.

```powershell
git clone https://github.com/Kayungko/dsh-plugin-task-coordinator.git
cd dsh-plugin-task-coordinator
pwsh install.ps1 -Source .
```

The script does three things: copies the plugin into the profile's `node_modules/` (no `pnpm install`, the lockfile stays untouched), registers the dependency + bundle in the profile manifest, and updates `.package-map.json` — **everything is backed up first** into `backups/<timestamp>/`.

**Restart DSH Desktop** afterwards — any session can then use the eleven tools and the `/tasks` command.

> 💡 `install.ps1` defaults `-Source` to `$PSScriptRoot/plugin` (workspace layout); when running from the plugin repo itself, **pass `-Source .` explicitly**.
> Re-running is safe: file copies are idempotent and manifest registration de-duplicates.

### Verify

After the restart, send this to any session:

`List the currently visible tasks`

It calls `task_list` and returns the task list (an empty list is a valid answer) — the tools are mounted ✅

Uninstall: `pwsh install.ps1 -Source . -Uninstall` (also takes effect after restart).

## Directing the supervisor (prompting that actually works)

The model only coordinates when it can map your words to the tools. Vague prompts like "you may use the /task plugin whenever you want" are discretionary — sessions tend to default to working solo (field-verified failure mode). Two rules:

1. **Name the tools, use imperative mood.** Example: "Split the remaining work with `task_spawn_batch` into parallel sub-task sessions (give them a team name); collect results with `task_wait`. Don't do everything in this session."
2. **In /goal mode the coordination mandate must live inside the goal objective** — every continuation round re-anchors on that text alone. Recommended objective:

> As the supervisor session, take over the remaining development: ① splittable work MUST be dispatched to parallel sub-task sessions via task_spawn_batch (attach a team name) — do not do everything yourself; ② collect results with task_wait and integrate them; ③ sub-task sessions may further parallelize with their own subagents; ④ push to remote main at every milestone.

Loose wordings ("/task plugin", "coordinate things") are recognized too — the bundled skill carries an alias table and the tool descriptions carry trigger context since 0.9.0 — but the imperative template above is the reliable form, especially for goal objectives.

## The eleven tools

| Tool | Purpose |
|---|---|
| `task_list` | List coordination-visible tasks with stable session ids, status, titles, todo/goal progress; filterable by `team`; `ungrouped: true` (0.19.0) lists only sessions belonging to NO workspace — the remediation view for the ungrouped bucket, paired with `task_workspace` and the registry's `expectedWorkspace` |
| `task_progress` | Read one task in depth: live/cold state, queued messages, conversation tail, todos, goal |
| `task_send` | Deliver a visible follow-up prompt (`mode: queue` or `steer`; `reference` links an earlier instruction); returns a `messageId` plus a `queueDepth` receipt `{nextTurn, nextStep}` (post-send; one next-turn message is consumed per round, so depth N ≈ N rounds before it is read) |
| `task_spawn` | Create + name + kick off a brand-new task (title follows the `MMDD｜type｜topic` rule; groupable via `team`); returns a `correlationId`; appends the report-back convention by default; optional `externalRef` (0.25.0) carries a free-form external caller reference for cross-agent correspondence (e.g. a Codex conversation dispatching through the task bridge — trimmed, ≤200 chars, stored durably in the spawn registry and echoed on the receipt / `task_list` rows / `task_progress`, never parsed); **workspace placement fallback chain** (0.19.0): exact-match attachment (0.12.0) → subdirectory attaches to the NEAREST ancestor workspace with the session cwd normalized to the workspace root (default `ancestor` policy, stated in both the receipt and the kickoff) → git worktrees deliberately stay ungrouped to preserve isolation (strong warning) → every ungrouped landing carries a warning + remediation hint; receipts always report `workspace` ({id,title} | null) and the `placement` enum; optional `provider`+`model` (+`reasoningEffort`) select the child's LLM route, installed before the kickoff (0.13.0); omitted, the spawn falls back to the plugin's configured default route (Settings → 任务编排, 0.18.0), then the host defau