# dsh-cc

**English** | [简体中文](README.zh.md)

## Claude Code-style workflows. Your models. DeepSeek Harness.

`dsh-cc` turns [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) into a batteries-included coding environment for everyday development. Keep familiar project assets and interaction patterns while choosing the models, tools, permissions, and agent composition that fit your environment.

- **Reuse familiar workflows:** `.claude/agents`, `SKILL.md`, `CLAUDE.md`, hooks, permissions, slash commands, and resumable sessions.
- **Bring your own model strategy:** route aliases such as `sketch`, `draft`, `blueprint`, and `masterplan` to any provider/model pair supported by your dsh deployment.
- **Run a complete coding loop:** TUI, MCP, memory, subagents, background tasks, worktrees, structured output, deferred tool discovery, reversible tool-output compression (`context-crusher` + `context_retrieve`), and cost-gated compaction.
- **Stay composable:** install the experience through native dsh profiles and plugins instead of maintaining a permanent DeepSeek Harness fork.

> `dsh-cc` is not Claude Code and is not a wrapper around Claude Code. It implements familiar Claude Code-style workflows on the open, composable DeepSeek Harness runtime.

## Quick start

Install DeepSeek Harness and the `dsh-cc` launcher, then start coding:

```sh
npm install -g @deepseek-ai/dsh @dsh-cc/cli
dsh-cc
```

`dsh-cc` requires `dsh` **>= 0.1.5-rc.1**; the default `npm install -g @deepseek-ai/dsh` currently satisfies this (as of 2026-09-12), and the launcher enforces the floor at bootstrap.

Already have `dsh` **>= 0.1.5-rc.1**? Install only the launcher:

```sh
npm install -g @dsh-cc/cli
dsh-cc
```

### Upgrading

```sh
npm install -g @dsh-cc/cli@latest
dsh-cc
```

On the first launch after an upgrade, the launcher re-runs the profile's bundle install at the new version (recorded in `~/.dsh/profiles/tui/.dsh-cc-bootstrap.json`), so the profile converges automatically — no manual step. A failed reconcile (e.g. network, or the fresh release still inside npm/pnpm's minimum-release-age window) warns and boots anyway, retrying on the next launch. Dev-synced profiles (via `scripts/sync-local-profile.sh`) are never reconciled by the launcher; they follow the dev-restore flow instead.

The launcher creates and boots the CC-oriented `tui` profile. To compose the profile explicitly instead:

```sh
dsh plugin --profile tui add \
  @dsh-cc/bundle-permissions \
  @dsh-cc/bundle-shell \
  @dsh-cc/bundle-tui
dsh --profile tui
```

The same backend also works with the dsh web UI:

```sh
dsh plugin --profile web add \
  @dsh-cc/bundle-permissions \
  @dsh-cc/bundle-shell
dsh web
```

### Optional: official plugins

The bundles above are the whole quick start. Two optional official plugins — shipped through the repo's `dsh-cc` marketplace — add preconfigured subagent lanes:

- **`dsh-cc-agents`** — the `dsh-cc-agents:critic` (reasoning and plan review, `opus` alias) and `dsh-cc-agents:executor` (mechanical execution, `sonnet` alias) subagents, plus an orchestration routing skill (`data-analysis`) and optional serena code-intelligence hooks (gated on serena-onboarded repos).
- **`dsh-cc-shunt`** — PreToolUse gates that redirect bulk file reads and boilerplate generation to cheap-lane worker subagents, keeping large file corpora out of the main context (configure a `haiku` alias for real token savings).

Install them inside a session:

```text
/plugin marketplace add dsh-cc/dsh-cc
/plugin install dsh-cc-agents@dsh-cc
/plugin install dsh-cc-shunt@dsh-cc
```

`/plugin install` flips the `enabledPlugins` flag for you; restart the session so the new agents and hooks are picked up. To update later, re-pull the marketplace and then update the plugin: `/plugin marketplace update dsh-cc`, then `/plugin update <id>`. Each plugin's own README ([agents](packages/plugin/dsh-cc-agents/README.md), [shunt](packages/plugin/dsh-cc-shunt/README.md)) covers configuration and known limits.

## Why developers use dsh-cc

| Need | What dsh-cc provides |
| --- | --- |
| Keep project conventions | Loads Claude Code-style agents, skills, project memory, settings, hooks, and plugin commands |
| Mix fast and capable models | Maps stable aliases to deployment-controlled provider/model routes |
| Delegate larger tasks | Supports subagent dispatch, background work, task inspection, and resume-aware routing |
| Work safely in parallel | Adds permission rules, approval flows, worktree tools, and workspace boundaries |
| Avoid loading every tool up front | Provides deferred discovery through `ToolSearch` and MCP integration |
| Move between interfaces | Exposes the same CC-oriented backend through terminal and web profiles |

`dsh-cc` is developed with `dsh-cc` itself. The repository's current setup routes work across Kimi, GLM, and DeepSeek models; see [Dogfooding dsh-cc](#dogfooding-dsh-cc) for the concrete mapping.

## Compatibility at a glance

<!-- parity:matrix:start -->
| Category | Full | Partial | Missing | Non-goal |
| --- | --- | --- | --- | --- |
| Engine subsystems | 11 | 20 | 4 | 2 |
| Hook events | 12 | 5 | 4 | 0 |
| Command surface | 21 | 8 | 1 | 2 |
| Sessions and context | 0 | 1 | 1 | 0 |
| Memory and CLAUDE.md | 0 | 1 | 1 | 0 |
| Skills | 0 | 1 | 0 | 0 |
| Subagents | 0 | 2 | 0 | 0 |
| MCP | 2 | 1 | 0 | 0 |
| Plugins and marketplaces | 0 | 3 | 0 | 0 |
| Settings | 2 | 2 | 0 | 0 |
| Permissions | 0 | 1 | 0 | 0 |
| Models | 0 | 1 | 0 | 0 |
| Workspace | 0 | 4 | 0 | 0 |
| Interactive UX | 1 | 2 | 0 | 0 |

Statuses were verified against upstream documentation retrieved as of 2026-09-23 (freshness threshold: 120 days).

For the exact feature-by-feature status and known gaps, see the **[Claude Code parity matrix](docs/cc-parity-matrix.md)**.
<!-- parity:matrix:end -->

## Familiar coding-agent workflows

### Subagents

Project-local Claude Code-style agent definitions under `.claude/agents` can be discovered and dispatched by the CC preset.

```text
.claude/
  agents/
    reviewer.md
    debugger.md
```

Agent frontmatter can continue using familiar model aliases while dsh decides which provider/model actually serves the request.

### Skills

`SKILL.md`-based skills are discovered by the CC skill provider, including project-specific skills and bundled utility skills.

### Memory

The memory layer supports `CLAUDE.md`-style context plus a dedicated write channel for durable memories. Memory is isolated by workspace, with optional shared team memory, and background dream consolidation kicks in automatically when memory-index pressure builds up.

### MCP

The CC profile includes an MCP client with:

- tools;
- resources;
- prompts;
- OAuth 2.1 flows.

Use `/mcp` to inspect and manage MCP connections.

#### Optional: Serena code intelligence

When your MCP configuration connects a [Serena](https://github.com/oraios/serena) server, dsh-cc automatically takes advantage of it: the system prompt steers toward Serena's symbol tools for code questions, and the bundled `explore` subagent gains read-only symbol retrieval (`find_symbol`, `find_referencing_symbols`, `get_symbols_overview`). Serena is strictly optional — without it, sessions behave identically through the built-in Read/Grep tools, minus the steering hints.

Install Serena once so a local `serena` binary is on `PATH`:

```sh
uv tool install git+https://github.com/oraios/serena@v1.7.0
```

Then add it to `~/.dsh/.mcp.json` (or a project `.mcp.json`) using the local binary:

```json
{
  "mcpServers": {
    "serena": {
      "command": "serena",
      "args": ["start-mcp-server", "--context", "claude-code", "--project-from-cwd"]
    }
  }
}
```

Avoid launching it via `uvx --from git+…`: every server start would write `~/.cache/uv`, which the session sandbox denies.

`/doctor` reports the connection under the `mcp.serena` check.

### Hooks

Claude Code-style hooks can react to session, prompt, tool, permission, compaction, task, and subagent lif