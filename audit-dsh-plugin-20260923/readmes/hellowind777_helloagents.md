<div align="center">
  <img src="./readme_images/01-hero-banner.svg" alt="HelloAGENTS" width="800">
</div>

# HelloAGENTS

<div align="center">

**A workflow layer for AI coding CLIs: skills, project knowledge, delivery checks, safer config writes, and resumable execution.**

[![Version](https://img.shields.io/badge/version-3.1.9-orange.svg)](./package.json)
[![npm](https://img.shields.io/npm/v/helloagents.svg)](https://www.npmjs.com/package/helloagents)
[![Node](https://img.shields.io/badge/node-%3E%3D18-339933.svg)](./package.json)
[![Skills](https://img.shields.io/badge/skills-14-6366f1.svg)](./skills)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](./LICENSE.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/hellowind777/helloagents/issues)
[![LINUX DO](https://img.shields.io/badge/LINUX_DO-recognized-0A84FF?logo=linux&logoColor=white)](https://linux.do)

</div>

<p align="center">
  <a href="./README.md"><img src="https://img.shields.io/badge/English-blue?style=for-the-badge" alt="English"></a>
  <a href="./README_CN.md"><img src="https://img.shields.io/badge/简体中文-blue?style=for-the-badge" alt="简体中文"></a>
</p>
---

> [!IMPORTANT]
> Looking for `v2.x`? The old Python line now lives in [helloagents-archive](https://github.com/hellowind777/helloagents-archive). The `v3` line is a full rewrite based on Node.js, Markdown rules, skills, and small runtime scripts.

> 🏅 This project is linked & recognized by the [LINUX DO](https://linux.do) community.

## Contents

- [What HelloAGENTS Does](#what-helloagents-does)
- [Core Features](#core-features)
- [Quick Start](#quick-start)
- [CLI Management](#cli-management)
- [Commands in Chat](#commands-in-chat)
- [Project Knowledge Base](#project-knowledge-base)
- [Workflow and Delivery](#workflow-and-delivery)
- [Configuration](#configuration)
- [How Each CLI Is Integrated](#how-each-cli-is-integrated)
- [Verification](#verification)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## What HelloAGENTS Does

AI coding CLIs can move fast, but they can also stop at advice, skip checks, lose project context, shift responsibility when tasks get hard, or report completion before the work is really done.

HelloAGENTS adds a workflow layer on top of Claude Code, Gemini CLI, Grok Build, Cursor, and Codex CLI. It anchors the agent as a capable executor, blocks responsibility-shifting patterns, helps the agent choose the right path, use task-specific quality skills, keep a project knowledge base, and verify work before delivery.

<table>
<tr>
<td width="50%" valign="top" align="center">

**Without HelloAGENTS**

<img src="./readme_images/08-demo-snake-without-helloagents.png" alt="Without HelloAGENTS" width="520">

</td>
<td width="50%" valign="top" align="center">

**With HelloAGENTS**

<img src="./readme_images/07-demo-snake-with-helloagents.png" alt="With HelloAGENTS" width="520">

</td>
</tr>
</table>

| Problem | Without HelloAGENTS | With HelloAGENTS |
|---------|---------------------|------------------|
| Stops too early | Ends with suggestions | Continues into build, verify, and closeout |
| Shifts responsibility | Refuses hard tasks, suggests other tools | Exhausts alternative paths, stays on task |
| Quality is inconsistent | Depends on each prompt | 14 quality skills activate by task type |
| Context is scattered | Plans live in chat history | Project knowledge and plan files stay on disk |
| Completion is vague | Natural language says “done” | Delivery checks use state, evidence, and verification |
| Config writes are risky | CLI files can drift | Install, update, cleanup, and doctor flows check managed files |

## Core Features

### 1) 14 built-in workflow skills

HelloAGENTS ships 14 built-in skills. They are loaded only when the current stage needs them, so simple tasks stay light while complex work gets stricter checks.

| Skill | Focus |
|-------|-------|
| `hello-ui` | UI planning, design contracts, implementation mapping, visual validation |
| `hello-api` | API design, validation, error format, compatibility |
| `hello-security` | auth, secrets, permissions, injection risks |
| `hello-test` | TDD, coverage, edge cases, test structure |
| `qa-review` | unified quality review, verification commands, blocking fixes, delivery evidence, closeout |
| `helloagents` | command routing, workflow stage rules, project knowledge, and state coordination |
| `hello-errors` | error handling, logs, retry and recovery behavior |
| `hello-perf` | performance, caching, query and rendering risks |
| `hello-data` | database, migrations, transactions, indexes |
| `hello-arch` | architecture, boundaries, code size, maintainability |
| `hello-debug` | bug diagnosis and escalation when stuck |
| `hello-subagent` | subagent delegation and result integration |
| `hello-write` | documentation, reports, and written deliverables |
| `hello-reflect` | reusable lessons and knowledge updates |

All UI work first follows the shared UI quality baseline.
In host global mode, in initialized projects, or in explicit UI workflows, `hello-ui` adds deeper design-contract execution, design-system mapping, and visual validation on top of that baseline.
When visual evidence is required, HelloAGENTS records it in the current session `artifacts/visual.json`.

### 2) Commands for different work styles

Commands run inside the AI CLI chat with a `~` prefix. The command skill is read directly; unrelated skills are not loaded unless the workflow needs them.

| Command | Purpose |
|---------|---------|
| `~ask` | Interactive clarification: Q&A to pin down goals, direction, scope, and constraints; does not write files |
| `~auto` | Chooses the main path and keeps going until delivery or a real blocker |
| `~plan` | Requirements, solution design, task breakdown, and plan package |
| `~build` | Implementation from the current request or an existing plan |
| `~prd` | Modern product requirements document through guided dimension-by-dimension exploration |
| `~loop` | Long-running entry; in Codex it prefers `/goal -> ~auto -> ~qa` |
| `~init` | Initialize the project workflow and sync project knowledge |
| `~test` | Write tests for a target module or recent change |
| `~qa` | Run the unified quality loop: review, verification commands, fixes, and closeout |
| `~commit` | Generate a conventional commit message and sync knowledge |
| `~clean` | Archive finished plans and clean temporary runtime files |
| `~help` | Show commands and current settings |

Compatibility aliases:

- `~do` → `~build`
- `~design` → `~plan`
- `~review` → `~qa`
- `~idea` → `~ask` (deprecated)

Use `~ask` for clarifying requirements, comparing approaches, weighing value, and scoping — pure conversation, no files created.

### 3) Project knowledge base

HelloAGENTS can create and maintain a project knowledge base under `.helloagents/`.

The knowledge base helps future turns understand the repo without re-discovering the same facts. It can store:

| File or directory | Purpose |
|-------------------|---------|
| `context.md` | project overview, stack, architecture, module index |
| `guidelines.md` | non-obvious coding conventions inferred from the repo |
| `verify.yaml` | verification commands such as lint, test, build |
| `CHANGELOG.md` | project-level change history |
| `DESIGN.md` | stable UI design contract when the project has UI work |
| `modules/*.md` | module-specific notes and lessons |
| `plans/<feature>/` | active plan packages |
| `archive/` | archived plan packages |

`~init` initializes the project workflow: it writes the project-level full carrier marker, prepares project state, and creates or updates the knowledge base.

### 4) Structured plan packages

Complex work can be stored as plan packages instead of a single paragraph in chat.

For `~plan`, HelloAGENTS uses:

- `requirements.md`
- `plan.md`
- `tasks.md`
- `contract.json`

For `~prd`, HelloAGENTS also creates PRD files suc