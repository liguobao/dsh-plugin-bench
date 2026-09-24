<div align="center">

# oh-my-dsh

**Into the Unknown**

omdsh is a focused, keyboard-first DeepSeek coding agent built on the plugin architecture of [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) and inspired by the interaction quality of [oh-my-pi](https://github.com/can1357/oh-my-pi) and the original [Pi](https://github.com/earendil-works/pi) agent harness.

[![CI](https://github.com/agi-fans/oh-my-dsh/actions/workflows/ci.yml/badge.svg)](https://github.com/agi-fans/oh-my-dsh/actions/workflows/ci.yml) [![npm version](https://img.shields.io/npm/v/%40agi-fans%2Foh-my-dsh?style=flat-square&logo=npm)](https://www.npmjs.com/package/@agi-fans/oh-my-dsh) [![npm downloads](https://img.shields.io/npm/dm/%40agi-fans%2Foh-my-dsh?style=flat-square&logo=npm)](https://www.npmjs.com/package/@agi-fans/oh-my-dsh) [![Node.js ^22.19 or >=24](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&logo=node.js)](https://nodejs.org/) [![MIT License](https://img.shields.io/npm/l/%40agi-fans%2Foh-my-dsh?style=flat-square)](LICENSE)

[Documentation](https://omdsh.agi.fans/) · English · [简体中文](README.zh-CN.md)

</div>

![oh-my-dsh terminal interface](apps/site/public/screenshot.webp)

## Quick start

Requirements: Node.js 22.19 or later in the 22.x line, or Node.js 24 or newer, plus a DeepSeek API key for live model turns.

```sh
npm install --global @agi-fans/oh-my-dsh
omdsh
```

Run `/login` once inside omdsh to validate and save your DeepSeek API key, then start a conversation. To try it without a global installation, run `npx @agi-fans/oh-my-dsh`.

## Highlights

- **Durable conversations:** search, pin, rename, and resume sessions in `/sessions`; rewind, retry, compact, and export complete transcripts as Markdown or standalone HTML.
- **Three real session controls:** choose a Harness Agent preset (Standard, PTC, Minimal, or Cordis), Workflow (Default or Plan), and Access (Read only, Workspace write, or Full access). Each Agent preset owns its tool exposure; PTC uses the generated TypeScript SDK automatically.
- **Rich terminal input:** mention project files and other sessions with `@`, paste clipboard images, reuse persistent prompt history, edit multiline prompts externally, and retrieve queued follow-ups.
- **Readable tool activity:** follow streaming calls and live subagent progress, press Down on an empty composer then Enter (or use Alt+A directly) to select a child in the keyboard-driven Agent Hub, steer a continuable child from its transcript, inspect distinct Input and Output sections, expand long results, and keep domain-specific presentation owned by tool plugins.
- **Live operational context:** see Agent, Workflow, Access, model, reasoning effort, workspace, Git state, context pressure, tokens, TTFT, throughput, cache, timings, turns, and steps without leaving the composer; use `/context` for an inline projection-backed breakdown that remains in the transcript.
- **Responsive by design:** retain settled transcript layout, coalesce scroll updates, emit row-level terminal diffs, and preserve correct display-cell alignment for CJK text and emoji.

## Documentation

The full documentation is published at [omdsh.agi.fans](https://omdsh.agi.fans/), and the Markdown under `apps/site/content/` is its source of truth.

**Start here**

- [Tutorials](https://omdsh.agi.fans/docs/tutorials/) — complete a first task, give the agent precise context, guide queued work, recover long sessions, customize the environment, and write an installable plugin.
- [Commands](https://omdsh.agi.fans/docs/commands/) — every slash command with its arguments and aliases.
- [Keyboard and keys](https://omdsh.agi.fans/docs/keyboard/) — editing, transcript, overlay keys, and `keybindings.json`.

**Reference**

- [Sessions and history](https://omdsh.agi.fans/docs/sessions/) — durable logs, the Session Library, and the local data files.
- [Subagents and delegation](https://omdsh.agi.fans/docs/subagents/) — the three transports, the Agent Hub, steering, and background jobs.
- [Observability](https://omdsh.agi.fans/docs/observability/) — `/trajectory`, `/context`, `/diff`, `/tools`, and `/mcp`.
- [Settings](https://omdsh.agi.fans/docs/settings/) — appearance, motion, notifications, and the configurable status line.
- [Permissions and access](https://omdsh.agi.fans/docs/permissions/) — Access presets, sandbox, and approvals.
- [Command line](https://omdsh.agi.fans/docs/cli/) — flags, subcommands, and environment variables.
- [Tools](https://omdsh.agi.fans/docs/tools/) — what the model can use, grouped by capability.
- [Troubleshooting](https://omdsh.agi.fans/docs/troubleshooting/) — exit, color, scrollback, and boot failures.

**Extend and integrate**

- [Skills and MCP](https://omdsh.agi.fans/docs/skills-and-mcp/) — reusable instructions and external tools.
- [Language servers](https://omdsh.agi.fans/docs/language-servers/) — configure read-only code intelligence.
- [User plugins](https://omdsh.agi.fans/docs/plugins/) — install DSH bundles into the omdsh Profile with `omdsh plugin`.
- [Plugin internals](https://omdsh.agi.fans/docs/plugin-internals/) — the `ctx.tui` surface and the contribution layer.

**Internals**

- [Architecture](https://omdsh.agi.fans/docs/architecture/) — plugin boundaries and runtime data flow.
- [Performance](https://omdsh.agi.fans/docs/performance/) — benchmarks, methodology, and rendering optimizations.

[Report a bug or request a feature](https://github.com/agi-fans/oh-my-dsh/issues/new/choose) with a guided form for the version, environment, reproduction steps, and sanitized context.

## Why oh-my-dsh

DeepSeek Harness provides a capable agent runtime and a strong architectural idea: everything is a plugin. oh-my-dsh brings that runtime into a calm, keyboard-driven terminal experience without creating a second agent core or hiding Harness behind a parallel abstraction.

The TUI remains a presentation and interaction layer. Sessions, tools, permissions, models, Skills, MCP servers, commands, and telemetry come from Harness services and plugins; omdsh composes them into a terminal application and adds the interface behavior needed to use them comfortably. `/trajectory` opens a keyboard-driven event ledger with Turn/Step grouping, live following, search, folding, timing, token usage, tool payloads, results, and schemas. `/context` reads the same client-visible Harness projections as the status footer and distinguishes provider-anchored occupancy from heuristic prompt composition.

The project follows four principles:

- **Harness-native:** use published DeepSeek Harness packages as the source of truth for agent behavior, state, and lifecycle.
- **Real plugin boundaries:** create plugins for independently owned lifecycles and contribution points, not for every source file.
- **One terminal owner:** keep raw input, cursor state, viewport management, and atomic rendering inside the local TUI Provider.
- **Progressive disclosure:** keep the default view concise while making tools, telemetry, settings, and session detail discoverable on demand.

Reference checkouts under `refs/` remain read-only research material. Runtime code depends only on published packages and oh-my-dsh workspace packages.

## Architecture

```text
DeepSeek Harness plugins and services
                │
                ▼
  @agi-fans/dsh-tui — terminal capability seam
                │
                ▼
  @agi-fans/oh-my-dsh — boot and plugin composition
```

The TUI package is split into a service definition, local terminal Provider, session and interaction adapters, tool-presentation bridge, command contributions, and interactive Runner. This isolates terminal ownership from Harness domain state and exposes plugin seams only where a capability has an independent lifecycle or owner. See the [architecture overview](https://omdsh.agi.fans/docs/architecture/) for the current boundaries and data flow.

## Performance

Performance is part of the TUI archite