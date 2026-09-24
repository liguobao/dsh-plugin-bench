<div align="center">

# 🎨 dsh-output-styles
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-output-styles` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-output-styles)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-output-styles?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-output-styles?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-output-styles/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-output-styles)

**Claude Code `outputStyles` for DeepSeek Harness** — switch the model's output style at runtime, per session, durably.

*`/style concise` — and every reply from now on is terse. `/style off` — back to the project default.*

> **Official repository.** This is the only official repository of dsh-output-styles, maintained by PerryLink. Same-name repositories under other accounts are not affiliated.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-output-styles.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-output-styles/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-output-styles/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-output-styles?label=version)](https://github.com/PerryLink/dsh-output-styles/releases)
[![npm version](https://img.shields.io/npm/v/dsh-output-styles)](https://www.npmjs.com/package/dsh-output-styles)
[![npm downloads](https://img.shields.io/npm/dm/dsh-output-styles)](https://www.npmjs.com/package/dsh-output-styles)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (adapted 2026-09-09): the session envelope keeps its ignorable field for stored-log read compatibility only - Session.append still cannot stamp it, so audit-gate behavior is unchanged. Verified 2026-09-11 against the dsh-v0.1.7-alpha.1 master checkout (full gate chain + profile install smoke). |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (host + web client) |
| Model | Any (system-prompt injection) |

## What you get

`dsh-output-styles` is the Claude Code `outputStyles` equivalent for DeepSeek Harness: a `/style` command that switches the model's output style at runtime, persisted per session, injected at every prompt assembly.

- **Style library** — one Markdown file per style (`styles/*.md`); frontmatter for metadata, body = the model directive. Six built-ins ship in the box (`concise`, `explanatory`, `formal`, `learning`, `proactive`, `step-by-step`), including Claude Code-parity `proactive` and `learning`.
- **`/style` command** — no argument lists styles (with descriptions) plus the current selection; `/style <name>` switches; `/style off` restores the project default.
- **Session-scoped persistence** — the choice lives in the `output_style` storage domain, keyed by sessionId, and survives restarts.
- **System-prompt injection** — a `systemPrompt.section()` contribution (order `sectionOrder`) injects the current session's style body at every assembly, truncated at a configurable budget.
- **Claude Code parity** — `keep-coding-instructions`, `force-for-plugin` (`force` alias), `outputStyles` JSON compatibility, layered `stylesDir` directories, hot reload, and a project-default fallback that is live-editable from the Web Plugins page.
- **Renderer registry (`output.render.*`)** — `ctx.outputRenderers` lets any plugin register a pure presenter, applied through the `output.render/before` waterfall; built-in renderers `concise` and `step-by-step`.
- **Per-session/per-tool rules** — `rules: [{ match: { tool: 'bash' }, style: 'concise' }]` name the renderer for matching requests; live-editable from the Web Plugins page.
- **`/transcript`** — render the current session to Markdown or sanitized HTML through the render pipeline; `--save <path>` writes the sanitized document to that workspace path after user approval. Every render keeps the original text beside the rendered one.

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-output-styles#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-output-styles

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A3 'id: output-styles'
```

## Demo

```
You > /style
      output style off
      concise — Terse, direct answers — minimal prose, no preamble. (Daily coding work, tool-heavy sessions, or when prompt length matters.)
      explanatory — Educational answers with short "Insights" that teach as you work. (Learning a codebase, onboarding, …)
      formal — Formal, precise prose with complete sentences and defined terms. (Reports, documentation, release notes, …)
      learning — Collaborative learn-by-doing mode with short "Insights" and small hands-on steps for the user. (Pairing, onboarding, …)
      proactive — Execute immediately, assume reasonable defaults, and prefer action over planning. (Routine multi-step work, …)
      step-by-step — Numbered reasoning steps with explicit intermediate results. (Debugging, design decisions, …)

You > /style concise
      switched to concise

You > 请只用一句话介绍你自己。
AI  > 我是运行在 DeepSeek Harness 插件化平台上、基于 deepseek-v4-pro 模型的 AI 编码代理。
```

## How it works

```mermaid
flowchart LR
    U[You type /style concise] --> C[command registry]
    C -->|command/run logged| L[(session log)]
    C -->|put {style, source}| D[(output_style domain)]
    D --> R[OutputStyleRuntime]
    R -->|body at every assembly| S[systemPrompt section order 90]
    S --> M[Model request]
    M -->|full system prompt| H[system/message logged]
```

Everything the model sees is reconstructable from the session log — no new session event type, no agent-loop changes. The style name comes from `command/run`, the exact injected text from `system/message`, and the provenance marker `{ kind: 'dsh-output-styles' }` rides in the domain record. Styles apply to the main conversation only; subagent sessions keep their own prompts (matching Claude Code).

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-output-styles#main"` — the `prepare` script builds with production dependencies only.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-output-styles`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-output-styles-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-output-styles`.

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). Invalid values fail the load.

`defaultStyle` and `rules` are declared `volatile()`, so on a host that composes the settings forms seam they are **live, Web-editable fields**: edit them under **Plugins → dsh-output-styles** in the Web UI and the running plugin adopts the new value without a remount. Every other field stays composition-only and needs a reload. A committed value is validated before it is applied — an invalid one is rejected and the running values are left unchanged.

| Key | Default | Web-editable | Meaning |
|---|---|---