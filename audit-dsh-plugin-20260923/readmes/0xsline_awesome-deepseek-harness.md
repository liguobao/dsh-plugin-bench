<p align="center">
 <a href="README.md">English</a>&nbsp;&nbsp;|&nbsp;&nbsp;
 <a href="README.zh-CN.md">简体中文</a>
</p>

<br>

<div align="center">
 <img width="640" src="assets/banner.jpg" alt="Awesome DeepSeek Harness">
</div>

# Awesome DeepSeek Harness [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

<!-- BANNER: luminous DeepSeek whale with agent-orchestration harness (1280×480) -->

<p align="center">
 <a href="#install">Install</a>&nbsp;&nbsp;&nbsp;
 <a href="contributing.md">Contribution guide</a>&nbsp;&nbsp;&nbsp;
 <a href="https://deepseekdocs.com/">DeepSeek Docs</a>&nbsp;&nbsp;&nbsp;
 <a href="https://github.com/topics/dsh-plugin">Public plugin topic</a>&nbsp;&nbsp;&nbsp;
 <a href="https://github.com/dsh-external/issues">Issues</a>&nbsp;&nbsp;&nbsp;
 <a href="CATALOG.md">完整目录</a>&nbsp;&nbsp;&nbsp;
</p>

<br>

<p align="center">
 <b>Curated DeepSeek Harness (DSH) ecosystem: plugins, tools &amp; infrastructure. Sources: dsh-external/hub catalog and the public GitHub dsh-plugin topic.</b><br>
</p>

<br>
> Note: the GitHub [`dsh-plugin` topic](https://github.com/topics/dsh-plugin) is public; some `dsh-external` repository links may still require org access.

## Contents

- [Install](#install)
- [Core & Bundles](#core--bundles)
- [Agents & Orchestration](#agents--orchestration)
- [Context & Search](#context--search)
- [Memory & Knowledge](#memory--knowledge)
- [Input & Editing](#input--editing)
- [UI, Themes & Interaction](#ui-themes--interaction)
- [Dashboards & Session UX](#dashboards--session-ux)
- [IDE & Clients](#ide--clients)
- [Browser & Remote](#browser--remote)
- [Models & Inference](#models--inference)
- [Git & Engineering](#git--engineering)
- [Security & Governance](#security--governance)
- [Output & Deliverables](#output--deliverables)
- [Office & Documents](#office--documents)
- [Notifications & Channels](#notifications--channels)
- [Fun & Lifestyle](#fun--lifestyle)
- [Plugin Ecosystem & Development](#plugin-ecosystem--development)
- [Runtime & Operations](#runtime--operations)
- [Domain & Specialist Skills](#domain--specialist-skills)
- [Tools & Utilities](#tools--utilities)
- [Related](#related)
- [Thanks](#thanks)

## Install

Install the official runtime with Node.js:

```sh
npx @deepseek-ai/dsh web
```

Install an external profile bundle with pnpm on your `PATH`:

```sh
dsh plugin --profile web add "github:owner/repo#ref"
```

`dsh plugin` forwards package operations to pnpm, so npm, Git/GitHub, local path, `file:` and `link:` package specs are supported. Only packages declaring `dsh.bundle.patch` become active profile layers; plain dependencies remain installed but inactive. Restart `dsh --profile web` after installing or updating a bundle.

The former `&path:` sub-path and Repository Plugin installation forms are not part of the current official bundle flow; use an installable package that declares `dsh.bundle.patch`.

Management panel: Settings → Plugins.

## Core & Bundles

- [DeepSeek Harness Ultimate](https://github.com/18126295767-cell/deepseek-harness-ultimate) - Community-maintained reproducible profile installer: deduplicated defaults across coding, workflow, reliability and productivity; full commit-SHA pins, permissive-license audit, pre/post dependency checks, optional sensitive integrations, and beginner guides in 20 languages for Windows, macOS and Linux.
- [dsh-deepresearch](https://github.com/dsh-external/dsh-deepresearch) - DeepResearch plugin (cordis).
- [dsh-plan-execute](https://github.com/dsh-external/dsh-plan-execute) - Dual-model plan/execute routing: planner model thinks, executor model acts.
- [dsh-toolkit](https://github.com/dsh-external/dsh-toolkit) - Zero-dependency tool suite (calculator/csv/diff/encoding/json/markdown/regex/time).
- [dsh-deep-research](https://github.com/dsh-external/dsh-deep-research) - Adaptive deep-research orchestrator (workflow engine).
- [dsh-101](https://github.com/dsh-external/dsh-101) - DSH documentation reading mode.
- [dsh-client-ui-plan-execute](https://github.com/dsh-external/dsh-client-ui-plan-execute) - Web Settings row for plan/execute model routing.
- [dsh_workflow](https://github.com/dsh-external/dsh_workflow) - Dynamic workflow for DSH (placeholder).
- [dsh-equip-engine](https://github.com/wuykjl/dsh-equip-engine) - Task-driven plugin equip engine: dual retrieval (curated rules + LLM semantic), combo scoring (synergy/conflict/cost/trust), conflict detection and install-command export.
- [dsh-claude-move](https://github.com/PerryLink/dsh-claude-move) - Four-source migration wizard: move Claude Code, Codex, OpenCode and Hermes sessions, memories, skills, instructions and slash commands into DSH (approval-gated, idempotent, resumable sessions).
- [dsh-skill-mover](https://github.com/mjylfz/dsh-skill-mover) - One-click skill migration into DSH: scans 14 agent platforms (Cursor, Claude Code, Codex, Hermes, Trae, Qoder...) plus the shared ~/.agents layer, merges same-name skills, dedupes symlinks and rolls back safely.
- [gewu-tools](https://github.com/nyantused-cpun/gewu-tools) - Model-agnostic visual-inspection pipeline for text-only agents: page-by-page HTML screenshots plus a ready-made vision-subagent briefing contract (gewu_prep), then source-code truth verification of every finding (gewu_locate); validated on mimo-v2.5 & qwen3.7-plus.
- [dsh-plugin-hub](https://github.com/Noob-stupid/dsh-plugin-hub) - DSH plugin manager & marketplace: one-click enable/disable, multi-source market, static index (500+ plugins / 300 skills), skill install/disable, suite one-click assembly, one-click framework upgrade (online install + auto-rollback).
- [dsh-gsd-bundle](https://github.com/jaaty/dsh-gsd-bundle) - Git Ship Done (opengsd-core) reimplemented as host-plane Cordis plugins: replaces the default agent loop with a spec/discuss/plan/execute/verify/ship phase loop.

## Agents & Orchestration

- [NanmiCoder/dsh-agent-teams](https://github.com/NanmiCoder/dsh-agent-teams) - Multi-agent team orchestration: captain-style session with durable sub-agent teams, role assignment, and coordinated task execution.
- [dsh-todo-guard](https://github.com/a903067276-rgb/dsh-todo-guard) - Reliable todo panel that survives restarts (official panel only re-renders on write — fixed via projection pre-warm) with three-state completion verification: evidence exists → verified, fake evidence → blocked, no evidence → unverified badge; settings toggle to fall back to official behavior.
- [fakechris/dsh-track](https://github.com/fakechris/dsh-track) - Embedded task-management engine for DSH: decision-point protocol, idea capture wall, Linear-shaped issue store with an evidence-driven lifecycle.
- [dsh-dual-model-eval](https://github.com/huangdaxianer/dsh-dual-model-eval) - Runs one coding prompt across multiple configured models in isolated Git worktrees, streams side-by-side tool traces and results, and commits the candidate the user adopts for later rounds.
- [dsh-agent-arena](https://github.com/LeemanCheung/dsh-agent-arena) - Compares coding agents in isolated Git worktrees with deterministic validation, scoring, and explicit winner application.
- [xiehuan123/coding-coach](https://github.com/xiehuan123/coding-coach) - Coding Coach: 35-skill bundle plus a full agent preset for non-developers (8-stage idea-to-launch pipeline; engineering/product/UI skills).
- [dsh-collaboration](https://github.com/Socialist-Sister/dsh-collaboration) - Multi-agent collaboration suite: user-configured specialist roster, persistent on-demand dispatch (team_call/team_message/team_status/team_close), clone instances, star-topology relay, model comparison and a multimodal vision bridge.
- [dsh-plans](https://github.com/Optim-Agent/dsh-plans) - Planning-first agent preset: research repository changes into traceable Markdown plans, refine them through reviewer/criticizer subagent rounds, then execute as a DSH goal with a verifier checklist.
- [dsh-agent-team-gui](https://github.com/toolclub/dsh-agent-team-gu