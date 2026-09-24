<p align="center">
  <img src="assets/branding/dsh-banner.png" alt="DSH Automation" width="100%">
</p>

<div align="center">

  # DSH Automation

  **Run standalone coding tasks on a schedule in DeepSeek Harness**

  [简体中文](README.zh-CN.md) · [Changelog](CHANGELOG.md) · [Apache-2.0](LICENSE)

  [![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
  [![npm package](https://img.shields.io/npm/v/%40michengai%2Fdsh-automation.svg?label=npm%20package)](https://www.npmjs.com/package/@michengai/dsh-automation)
  [![npm downloads](https://img.shields.io/npm/dt/%40michengai%2Fdsh-automation.svg?label=npm%20downloads)](https://www.npmjs.com/package/@michengai/dsh-automation)
  [![DSH Web Plugin](https://img.shields.io/badge/DSH%20Web-Plugin-0f766e.svg)](https://github.com/MichengAI/dsh-automation)
  [![Node.js 22 or later](https://img.shields.io/badge/Node.js-22%20or%20later-339933.svg?logo=node.js&logoColor=white)](https://nodejs.org/)
</div>

> DSH Automation is a community-maintained DeepSeek Harness (DSH) plugin, not an official DeepSeek AI product.

## Features

Let DSH handle work on a schedule. Set up tasks in Settings or describe the timing and requirements in a conversation, then review each run.

- **Run once or repeat**: choose intervals, hourly, daily, weekly, monthly, or every N days.
- **Choose the working environment**: set the directory, model, skills, and permissions.
- **Adjust the schedule anytime**: create, pause, resume, run immediately, or delete tasks.
- **Review results**: browse task conversations by name and run time in the **Scheduled** tab, or filter run history in Settings.
- **Keep each run independent**: each run uses the saved task instructions and does not inherit the conversation that created it.

## Interface

Scheduled tasks live in the workspace **Scheduled** tab, next to **Tasks** and **Channels**:

![Scheduled sidebar](assets/screenshots/workspace-scheduled.png)

Open **Settings → Scheduled Tasks** to search, create, pause, and inspect rules:

![Scheduled tasks settings](assets/screenshots/settings-tasks.png)

Describe the job in chat. DSH handles approval according to the selected permission mode:

![Create a scheduled task from chat](assets/screenshots/chat-create.png)

![Official approval for automation_create](assets/screenshots/chat-approval.png)

After approval, the rule is saved and summarized in the conversation:

![Scheduled task created](assets/screenshots/chat-created.png)

Run history stays in Settings and can be filtered by day, week, month, task, or status:

![Run history](assets/screenshots/settings-runs.png)

## DSH product ecosystem

For a desktop workbench, download [DSH Codex Desktop](https://github.com/MichengAI/dsh-codex-desktop/releases). Existing [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) installations can add plugins as needed by following each project's README. Below are 11 first-party plugins; consult the corresponding desktop release notes and bundled catalog for what that version includes.

| Plugin | What you can do |
| --- | --- |
| [Codex UI](https://github.com/MichengAI/dsh-codex-ui) | Organize projects and conversations, search tasks, and navigate chat turns |
| [Agency Agents](https://github.com/MichengAI/dsh-agency-agents) | Choose and summon specialists for your task |
| [Skills Manager](https://github.com/MichengAI/dsh-skills-manager) | Find, enable, create, and import local skills |
| [Archive Manager](https://github.com/MichengAI/dsh-archive-manager) | Search, restore, or clean up archived conversations |
| [IM Connect](https://github.com/MichengAI/dsh-im-connect) | Send tasks and receive replies through messaging platforms |
| [Automation](https://github.com/MichengAI/dsh-automation) | Schedule tasks and review each run |
| [BTW](https://github.com/MichengAI/dsh-btw) | Ask side questions without interrupting the main task |
| [Simplify](https://github.com/MichengAI/dsh-simplify) | Use `/simplify` to improve code within your Git changes |
| [PUA](https://github.com/MichengAI/dsh-pua) | Guide the Agent to try new approaches after failures, investigate causes, and verify results before completion |
| [Code Review](https://github.com/MichengAI/dsh-code-review) | Use `/review` to request an independent Agent code review and receive the report in the current conversation |
| [Codex Pet](https://github.com/MichengAI/dsh-codex-pet) | View conversation notifications and respond to tool approvals and questions through a desktop pet |

## Prerequisites

- The current source uses DSH `0.1.7-rc.1` for development and real Host compatibility tests, and declares support through `0.1.7-rc.1`. Back up automation storage and sessions in the Profile before upgrading the Host. `0.1.7` writes V4 sessions, and V4 sessions cannot be read after downgrading.
- Official DSH peerDependencies are exactly `0.1.0-rc.8 || 0.1.1-rc.2 || 0.1.2-rc.1 || 0.1.5-rc.1 || 0.1.5-rc.2 || 0.1.7-rc.1`. The `0.1.6` line is absent because it will not get a release candidate; hosts still on `0.1.6-alpha.1` or `0.1.6-alpha.2` need `0.1.7-rc.1` for the next plugin release. `@deepseek-ai/dsh-agent-presets` is optional and stops at `0.1.5-rc.2`, because `0.1.7` renamed that package to `@deepseek-ai/dsh-agent-preset-registry` while keeping the `agentPresets` service. Development dependencies are pinned to `0.1.7-rc.1`. Use one consistent official package version within each Host.
- Other versions are outside the declared compatibility range. Installers may warn, and strict peer validation rejects them. Extend and pass the version matrix before adding a new rc.
- The Connection patch replaces the Web bundle's configured injection list with `[webServer, webRuntime]`; Loader still merges dependencies declared by the plugin source. Custom Hosts with additional configured injections must retain these two entries and their extra dependencies in a later Profile patch. This patch does not automatically merge other bundles' lists.
- A working DeepSeek Harness Web installation with `dsh` available in PowerShell.
- Examples use the `web` profile; replace it with the target profile.
- Source installation and development require Node.js 22.19+. npm installation does not require running `npm install` in an arbitrary directory.

## Installation

The installation commands below use the official npm registry.

### Ask an agent to install it (recommended)

Send the prompt below to any agent that can run terminal commands on your computer. Replace `web` with your actual profile. Once installed, use the plugin in DSH.

```text
Install the DSH plugin @michengai/dsh-automation into my local web profile by running: dsh plugin --profile web add @michengai/dsh-automation@latest --registry=https://registry.npmjs.org/. Then run dsh --profile web --dump-config, confirm the configuration includes dsh-automation, and explain how to reload DSH and start using the plugin.
```

### Install from npm

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
dsh plugin --profile web add @michengai/dsh-automation@latest --registry=https://registry.npmjs.org/
dsh --profile web --dump-config
```

Restart DSH Web and hard-refresh the browser. Pin a version with `@0.1.5` instead of `@latest` when needed.

## Updates

The settings title shows the installed version and a **Check for updates** button. When a newer release is available, **Update automatically** runs only when the DSH CLI or Desktop update service is available; otherwise, the dialog provides a profile-specific manual command to copy and run.

## Usage

Open **Settings → Scheduled Tasks**, then use the panel as follows:

| Goal | Action | Scope |
| --- | --- | --- |
| Create a rule | Select **New scheduled task**, then set name, schedule, prompt, workspace, model, skills, and permission. | Host-wide |
| Create from chat | Describe the schedule in any conversation, or select **Create in c