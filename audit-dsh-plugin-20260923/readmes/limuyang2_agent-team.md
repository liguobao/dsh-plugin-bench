# Agent Team for DeepSeek Harness

English | [简体中文](./README_CN.md)

![Agent Team — Independent Agents, Shared Workspace](./demo/github-banner.png)

[![npm version](https://img.shields.io/npm/v/@limuyang2/dsh-agent-team.svg)](https://www.npmjs.com/package/@limuyang2/dsh-agent-team)
[![license](https://img.shields.io/npm/l/@limuyang2/dsh-agent-team.svg)](https://www.npmjs.com/package/@limuyang2/dsh-agent-team)

Current release: `0.1.4`

Build teams of independent AI agents inside DeepSeek Harness. Mix models and providers, assign one Leader, and let every member work in its own conversation while sharing the same Workspace.

Agent Team does **not** turn members into subagents. Every member is an independent root agent with its own model, session, context, permissions, reasoning mode, and tool activity. Team tasks, messages, and the shared Workspace provide the collaboration layer.

![Agent Team workbench](./demo/4.png)

## Why Independent Agents Instead of One Overloaded Agent?

Agent Team is designed around a simple idea: **give specialized work to a specialized agent**.

A common parent/subagent workflow reuses or inherits much of the parent runtime configuration. That is convenient, but it can make every task carry the same expensive model, broad tool catalog, and growing context. A small commit-message task, for example, may still run through the same high-capability model used for architecture and implementation.

Agent Team lets every member have an explicit, focused configuration:

| Concern | Common parent/subagent setup | Agent Team |
| --- | --- | --- |
| Model | Often reuses the parent model or one shared model policy | Choose a different provider and model for every member |
| Skills and MCP | A broad catalog may be inherited or exposed everywhere | Give each role only the Skills and MCP Servers it needs |
| Context | Planning, execution, tool output, and results accumulate together | Every member has an isolated Session and context window |
| Cost | Simple work may still consume an expensive general model | Route routine work to smaller or specialized models |
| Permissions | One broad permission policy can spread across the workflow | Set least-privilege defaults and runtime permissions per member |

This separation keeps the Leader focused on planning and verification, keeps specialists focused on execution, reduces irrelevant tool choices, and prevents one agent's context from growing with every detail produced by the whole team. Members send tasks, progress, and results explicitly instead of sharing an ever-expanding conversation.

> Subagent behavior varies by framework. The comparison above describes the common parent-inherited pattern; Agent Team's advantage is that model, tools, permissions, and context isolation are explicit product-level choices for every member.

### Example: Use the Right Model for Each Job

Consider a software development team with three specialized members:

| Role | Model | Focused configuration |
| --- | --- | --- |
| Architecture Leader | GPT | Understand the requirement, design the solution, split work, coordinate members, and verify results |
| Coding Agent | GLM | Load coding Skills and development MCP tools, modify the Workspace, and run tests |
| Commit Assistant | DeepSeek Flash | Read Git status and diffs, then generate a Conventional Commit message with read-only permission |

The GPT Leader spends its context on decisions and verification instead of every implementation detail. GLM receives the codebase context and tools required for execution. DeepSeek Flash handles the narrow commit task quickly without paying for the Leader's higher-capability model or loading the coding agent's large tool catalog.

The collaboration flow is explicit:

```text
User goal → GPT Leader plans and assigns work
          → GLM Coding Agent implements and reports test results
          → GPT Leader verifies the result
          → DeepSeek Flash Commit Assistant summarizes the Git diff
```

## What You Can Do

- Create reusable assistants for planning, coding, testing, review, documentation, or any other role.
- Mix providers and models in one team—for example, a Codex Leader with GLM coding members.
- Create assistants manually or describe a role to the built-in **Team Agent Assistant**.
- Add the same assistant more than once; every selection becomes an independent team member.
- Watch all members side by side with streaming output, Markdown, Think blocks, and tool calls.
- Let the Leader create tasks, assign members, track progress, and collect results.
- Send messages directly to the Leader or, when enabled, to regular members.
- Change a member's permission preset and reasoning mode for the current session.
- Inspect loaded Skills, context usage, token statistics, and cache hit rate.
- Browse shared Workspace files and preview Git changes and diffs.
- Add or remove members, change the Leader, reset all contexts, or dissolve a team.

## Screenshots

### Create an Assistant by Conversation

Describe the role you need. The built-in assistant collects missing settings, prepares the long-term instructions, and creates the assistant only after your confirmation.

![Create an assistant by conversation](./demo/1.png)

### Reusable Assistant Library

Manage assistants under **Settings → Agent Team**. Each assistant can use a different provider, model, preset, default permission, reasoning mode, Skills, MCP Servers, and role instructions.

> **Skills and MCP scope:** Agent Team uses Skills and MCP Servers exposed through the standard DeepSeek Harness interfaces. This plugin does not provide installation, updates, or lifecycle management for Skills or MCP Servers. Install the appropriate Harness plugins to manage those resources first; Agent Team only lets an assistant select and use the resources already available in the active Profile.

![Assistant library](./demo/2.png)

### Build a Team

Select members, assign exactly one Leader, choose a Workspace, and decide whether direct communication with regular members is allowed.

![Build a team](./demo/3.png)

### Floating Team Launcher

A compact floating button opens the full-screen Team workbench without competing with sidebar extensions from other Harness clients. Hover over it or drag it to reveal the label. Drop it at either screen edge to collapse it toward that edge; the last position is remembered locally. Create teams and switch between them from the workbench navigator.

![Floating Team launcher](./demo/5.png)

## Requirements

- Node.js `22.19.0+` or `24.0.0+`
- DeepSeek Harness `0.1.1-rc.2`
- `pnpm` available on `PATH` (Harness uses it to manage Profile plugins)

Install pnpm if necessary:

```bash
npm install -g pnpm
```

## Installation

### DeepSeek Harness Web

Install Agent Team into the Harness `web` Profile:

```bash
npx @deepseek-ai/dsh plugin --profile web add @limuyang2/dsh-agent-team
```

Start Harness:

```bash
npx @deepseek-ai/dsh web
```

Open the URL printed by Harness, normally <http://127.0.0.1:3080/>. Restart Harness after installing or replacing the plugin.

### DeepSeek Harness Desktop

Install the exact Agent Team release into the Profile managed by DeepSeek Harness Desktop:

```bash
dsh plugin add --save-exact @limuyang2/dsh-agent-team@0.1.4
```

Quit and reopen DeepSeek Harness Desktop after the command completes. `--save-exact` keeps the Desktop Profile pinned to the tested plugin version instead of automatically moving to a newer release.

## Uninstallation

Stop Harness with `Ctrl+C`, then remove Agent Team from the `web` Profile:

```bash
npx @deepseek-ai/dsh plugin --profile web remove @limuyang2/dsh-agent-team
```

Restart Harness after the command completes. Removing the plugin does not modify DeepSeek Harness source code or delete files from your team Workspaces.

## Quick Start

### 1. Configure Models in Harness

Configure the providers, models, and credentials you want to use in Harness first. Agent Team reads the model catalog f