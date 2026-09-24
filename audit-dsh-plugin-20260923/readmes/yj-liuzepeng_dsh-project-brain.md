# dsh-project-brain

**English** · [简体中文](./README.zh-CN.md)

[![Version](https://img.shields.io/badge/version-1.3.1-blue)](./CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D22.19-339933)](./package.json)
[![Status](https://img.shields.io/badge/status-stable-success)](./RELEASE_CHECKLIST.md)

**A persistent project intelligence and memory plugin for DSH.** It analyzes the active workspace, explains the architecture, preserves decisions and development history, and restores the right context in future sessions.

Instead of making every new conversation rediscover the repository, dsh-project-brain stores structured knowledge inside the project itself and keeps getting more useful as the project evolves.

> Current release: `1.3.1` — adds **import / export / local backup restore** (cross-machine sync). End-to-end 20/20 smoke suites + 46/46 host-acceptance pass; data format fully backward-compatible with v1.3.0.

**v1.3.1 新特性**：📦 **导入导出 / 备份恢复**
- Dashboard 顶部新增 **💾 备份 / 📥 恢复 / ↶ 回滚** 三个按钮（与项目名 + techStack chip 同一行）
- 一键把整个项目脑打成 zip（含 timeline + cache + manifest + sha256 校验）→ 跨机器传文件 → 在另一台机器一键还原
- 导入前自动预览影响清单（即将覆盖的脑 / 旧脑备份路径 / rootPath 改写）；主按钮文案「覆盖并恢复」明确提醒
- 每次导入/回滚前自动备份当前脑到 `.project-brain.backup-<ts>/`；可随时回滚到任一历史备份
- 4 个新 Tool：`project_export` / `project_import` / `project_rollback_backup` / `project_cleanup_backups`

[GitHub release](https://github.com/yj-liuzepeng/dsh-project-brain/releases/tag/v1.3.1) · [DSH community showcase](https://github.com/deepseek-ai/deepseek-harness/discussions/5121) · [MyDSH listing](https://mydsh.dev/plugin?repo=yj-liuzepeng%2Fdsh-project-brain)

## Preview

### Project Brain activation entry (before first scan)

![Initial activation screen showing the three core capabilities (read project / remember across sessions / continue from where you left off) and the Start Project Brain button on the current workspace path](https://raw.githubusercontent.com/yj-liuzepeng/dsh-project-brain/v1.3.1/docs/screenshots/01.png)

### Project card with detected stack and live status

![Project card showing project name, detected stack chips (GitHub Actions / Monorepo), description, last-updated timestamp, and a three-stat summary (pending TODOs / project memories / completed) with phase progress bar](https://raw.githubusercontent.com/yj-liuzepeng/dsh-project-brain/v1.3.1/docs/screenshots/02.png)

### Dashboard overview with SuggestionCard and Quick Actions

![Dashboard header (Dashboard · project overview), SuggestionCard with AI recommendation and confidence score, four Quick Actions (rescan / organize TODOs / organize memories / project overview), and the Overview tab showing detected tech stack / language usage / dev entry points](https://raw.githubusercontent.com/yj-liuzepeng/dsh-project-brain/v1.3.1/docs/screenshots/03.png)

### Architecture tab — lane-based layered overview

![Architecture tab with project positioning, architectural style tags, plugin-style layered architecture, and DSH LLM enhancement badge; layers shown as left-label + right-component lanes (interface / tools / storage / memory / build)](https://raw.githubusercontent.com/yj-liuzepeng/dsh-project-brain/v1.3.1/docs/screenshots/04.png)

### Architecture tab — expanded runtime path for a single layer

![Selecting the session-extraction-and-hybrid-retrieval layer reveals its runtime path: a horizontal numbered flow (memory subsystem → embedding → hybrid retrieval → config-gated vector lookup → Brain storage) with a step-by-step description, files, and risks](https://raw.githubusercontent.com/yj-liuzepeng/dsh-project-brain/v1.3.1/docs/screenshots/05.png)

### TODOs and development timeline

![Activity tab: completed TODOs on the left (real-time memory, session summary, cross-session continuation), and the timeline on the right showing memory-organize events, project_rescan events, and recent memory-add entries with timestamps](https://raw.githubusercontent.com/yj-liuzepeng/dsh-project-brain/v1.3.1/docs/screenshots/06.png)

### Project memories with type badges and importance stars

![Memories tab: Current Core (per-round injection) section with type chips (decision / bug / architecture / lesson / note), importance stars, summary line, date, and View Details button per card; dormant memories collapsible at the bottom](https://raw.githubusercontent.com/yj-liuzepeng/dsh-project-brain/v1.3.1/docs/screenshots/07.png)

### Settings — vector retrieval and Embedding config

![Settings tab · Retrieval and Embedding section: hybrid retrieval mode, enable vector switch, Embedding URL / model / API key input fields, vector dimension; top green banner reminds users that unsaved changes do not take effect](https://raw.githubusercontent.com/yj-liuzepeng/dsh-project-brain/v1.3.1/docs/screenshots/08.png)

### Settings — retrieval weights and probe button

![Settings tab · Retrieval weights section: keyword / vector / importance / confidence / recency weight inputs (0.15 / 0.25 / 0.3 / 0.1 / 0.2), each with a one-line hint describing what it does; small light-blue Test Vector Connection button probes the live embedding endpoint](https://raw.githubusercontent.com/yj-liuzepeng/dsh-project-brain/v1.3.1/docs/screenshots/09.png)

### Git history tab (VSCode-style)

![Git history tab: branch switcher (main, 32 commits, 1 other branch), HEAD hash, auto-refresh 30s toggle; commit timeline with graph dots, commit subject, short hash, author, relative time, and changed-file summary; branch chips on the right](https://raw.githubusercontent.com/yj-liuzepeng/dsh-project-brain/v1.3.1/docs/screenshots/10.png)

## Why use it?

AI coding sessions are usually short-lived, while real software projects are not. Important context gets scattered across conversations: why an architectural choice was made, which workaround fixed a production bug, what is currently in progress, and which files form the critical path.

dsh-project-brain turns that context into a local, workspace-scoped knowledge layer:

- **Understand a repository quickly** — detects languages, frameworks, tooling, entry points, manifests, README metadata, symbols, and imports.
- **Explain architecture, not just folders** — produces a report covering project purpose, architectural style, conceptual layers, component responsibilities, relationships, runtime flows, key files, reading order, and risks.
- **Reuse the active DSH model** — architecture analysis uses the provider/model already selected for the current DSH Session; no separate chat-model key is required.
- **Remember across conversations** — decisions, requirements, architecture notes, bugs, lessons, changes, TODOs, and timeline events persist in the workspace.
- **Restore context automatically** — a new Session receives high-value memories, active TODOs, and recent activity through the DSH system prompt.
- **Keep workspaces isolated** — the Host resolves the live Session workspace; one project's memory is never guessed from another project.
- **Work without embeddings** — local BM25 retrieval is the zero-configuration default. OpenAI-compatible embeddings are an optional semantic upgrade.
- **Stay usable when AI is unavailable** — architecture generation and memory retrieval have local fallback paths.

## How it works

```text
Active DSH Session
       │ trusted live Session cwd
       ▼
Workspace scanner ───────► project facts and source evidence
       │
       ├──► current DSH LLM ───► semantic architecture report
       │          │ unavailable / timeout / invalid output
       │          └────────────► local architecture fallback
       │
       ├──► .project-brain/ ───► memory, TODOs, timeline, architecture
       │
       ├──► context injector ──► next Session system prompt
       │
       └──► Connection RPC ────► Dashboard and TodoStrip
```

The browser-side UI cannot choose arbitrary filesystem paths. Runtime actions are resolved by the Host against the active DSH Session.

## Local pr