# dsh-acp-interactive

[![npm](https://img.shields.io/npm/v/deepseekharness-acp-interactive)](https://www.npmjs.com/package/deepseekharness-acp-interactive)
[![CI](https://github.com/ClickPM/dsh-acp-interactive/actions/workflows/ci.yml/badge.svg)](https://github.com/ClickPM/dsh-acp-interactive/actions/workflows/ci.yml)
[![Registry auth check](https://github.com/ClickPM/dsh-acp-interactive/actions/workflows/registry-auth.yml/badge.svg)](https://github.com/ClickPM/dsh-acp-interactive/actions/workflows/registry-auth.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

English | [中文](README.zh.md)

Editor-facing Agent Client Protocol server over JSON-RPC stdio. It creates dsh agents on demand and projects their live session events into ACP message, thought, tool, permission, plan, title, usage, and command updates. Zed is the first compatibility target.

The package ships both the UI transport plugin and the `dsh-acp-interactive` executable. The transport contains no domain logic; the executable loads the complete Cordis composition bundled in `config/cordis.yml` — DeepSeek and user providers, the agent spine, model-generated session titles, file and filesystem-search tools, in-process subagents, shell, permissions, persistence, human commands, and the ACP transport — so ordinary users do not need a DeepSeek Harness source checkout. This UI bridge is separate from the upstream automation-only ACP transport.

`dsh-acp-interactive` is an independent, community-maintained project. It is not affiliated with or endorsed by DeepSeek or Zed Industries; it composes the published `@deepseek-ai/dsh-*` packages behind a reviewed editor profile and does not claim to be the official DeepSeek ACP agent.

## Quick start

```sh
npm install --global deepseekharness-acp-interactive
dsh-acp-interactive --setup
```

`--setup` stores `DEEPSEEK_API_KEY` through the Harness credential store without echoing it. Then register the installed command in Zed's `settings.json` (open via `Ctrl+Shift+P` / `Cmd+Shift+P` and type `zed: open settings`); on Windows use the absolute path printed by `where.exe dsh-acp-interactive` (using forward slashes `/` or double backslashes `\\`), on macOS / Linux use `which dsh-acp-interactive`:

```json
{
  "agent_servers": {
    "dsh-acp-interactive": {
      "type": "custom",
      "command": "C:/Users/you/AppData/Roaming/npm/dsh-acp-interactive.cmd",
      "args": []
    }
  }
}
```

After saving, open Zed's Agent panel (`Ctrl+?` / `Cmd+?`) and select `dsh-acp-interactive` from the dropdown list at the top. Zed starts the server with the workspace as cwd; JSONL sessions live under that workspace's `.sessions`, while every server process owns a separate in-memory SQLite session-query index, so several editor processes can share the JSONL source of truth without contending for the derived index.

Skipping `--setup` is fine: a thread opened without a stored key shows a `Configure DeepSeek API key` action that runs the same flow (see [Authentication](#authentication)); clients without terminal authentication receive its instructions as an agent-type method instead.

The published tarball already contains the built `lib/`; no build step runs at install time. Every published version corresponds to a `vX.Y.Z` tag and a [GitHub Release](https://github.com/ClickPM/dsh-acp-interactive/releases) whose assets include the tarball and its SHA-256 checksum, so an installation can be audited against the tagged source. Supported Zed versions and verification status are in the [Zed compatibility matrix](docs/compatibility.en.md); this release uses the stable ACP v1 schema from SDK `1.4.0` as its baseline.

## In Zed

![Zed agent panel running DeepSeek Harness Interactive next to the editor, with the model, reasoning-effort, and permission selectors in the composer](assets/zed-overview.png)

The `/` palette lists the human commands discovered from the composed Harness plugins; the permission and reasoning-effort selectors are ACP session configuration options backed by Harness permission presets and the selected model's advertised efforts.

![Slash command palette showing compact, feedback, goal, permission, and plan](assets/zed-commands.png)

![Permission preset selector (read-only, workspace-write, danger-full-access) and reasoning-effort selector (Default, Off, Low, High, Max)](assets/zed-controls.png)

### Authentication

Opening a thread without a stored key answers `session/new` with `auth_required`, so Zed shows the `Configure DeepSeek API key` action with the agent's own instructions. Clicking it runs `--setup` in a Zed terminal task; when that terminal exits, Zed retries `session/new` with the stored key.

![Zed's authentication panel: "Authenticate to DeepSeek Harness", a Configure DeepSeek API key button, and the message that DEEPSEEK_API_KEY is not configured](assets/zed-auth.png)

![After clicking: the thread shows "Authenticating to DeepSeek Harness…" while Zed runs the Configure DeepSeek API key terminal task](assets/zed-auth-terminal.png)

### Permissions

Tool calls run inside the Harness sandbox. Under the `read-only` preset a write is denied with the sandbox's escalation hint; the retried call arrives in Zed as an ACP permission request with `Allow once` / `Reject`, and the approved write and its read-back render as tool cards.

![A write denied under read-only, then the escalated write awaiting Allow once or Reject](assets/zed-permission.png)

![The approved write card with its content, the read-back, and the created file](assets/zed-edit-result.png)

## What's new in 1.3.0

Version `1.3.0` adds in-process subagents. The composed profile mounts the published `@deepseek-ai/dsh-subagent` registry with its `spawn` and `fork` backends and two delegation tools, `subagent` and `subagent_fork`: the model delegates a self-contained or conversation-seeded task and receives the child's final answer as the tool result. In Zed a delegation is one tool card — the child's own tool calls, replies, nested delegations, and settlement fold into a bounded transcript inside the card while it runs, and the parent's tool result settles it. Delegations wait in the foreground inside the parent's turn, children inherit the parent's sandbox with approval pinned to `never` and never raise an ACP permission request, and child sessions are not editor sessions. See the [In-Process Subagents Agent Note](docs/agent-notes/2026-09-10-in-process-subagents.md), and the [changelog](CHANGELOG.md) for earlier releases.

## Configuration

State lives in the dsh home — `$DSH_HOME`, or the current user's default `.dsh` directory — where `settings.yaml` holds providers and model catalogs and `.credentials.yaml` holds credentials. Pi Agent Desktop and Zed ACP can therefore share provider profiles, model catalogs, and credential references without copying API keys into Zed or `cordis.yml`; a profile's `apiKeyEnv` must match a key under `.credentials.yaml` `refs`, and the two remain separate processes with isolated sessions. Changes to `settings.yaml` refresh the provider directory through the existing settings and LLM-registry update path, and the bundled dormant `llm-pi-ai` mount registers every route under `llm-pi-ai.providers`.

At startup, Windows registers the native `pwsh` tool while Linux and macOS register `bash`; the model never receives both tool dialects. Stdout carries JSON-RPC frames only.

An explicitly configured image-capable model must declare its input modalities; without them the DeepSeek adapter treats the entry as text-only and the bridge rejects image admission before queuing the prompt:

```yaml
- id: deepseek-v4-flash-vision-exp
  inputModalities: [text, image]
```

Custom deployments may instead consume only the transport export and mount it in a dedicated ACP stdio composition, where `provider` and `model` select the initial route for new sessions without restricting the model selector:

```yaml
- id: settings
  name: '@deepseek-ai/d