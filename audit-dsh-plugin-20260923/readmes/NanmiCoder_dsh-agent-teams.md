<p align="right">
  <strong>English</strong> · <a href="./README_ZH.md">简体中文</a>
</p>

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="dsh-agent-teams turns one DeepSeek Harness session into a coordinated multi-agent team">
</p>

<p align="center">
  <a href="https://dshfind.com/en/plugins/NanmiCoder/dsh-agent-teams?ref=badge"><img src="https://img.shields.io/badge/recommended%20by-dshfind-FFD700?style=flat-square" alt="Recommended by dshfind"></a>
  <a href="https://dshfind.com/en/plugins/NanmiCoder/dsh-agent-teams?ref=badge"><img src="https://dshfind.com/api/badge/NanmiCoder/dsh-agent-teams?lang=en" alt="dshfind score"></a>
  <a href="https://dshfind.com/en/plugins/NanmiCoder/dsh-agent-teams?ref=badge"><img src="https://dshfind.com/api/badge/NanmiCoder/dsh-agent-teams?metric=downloads&amp;lang=en" alt="dshfind downloads"></a>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@nanmicoder/dsh-agent-teams"><img src="https://img.shields.io/npm/v/@nanmicoder/dsh-agent-teams?style=flat-square&amp;color=5B4CF0" alt="npm version"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-0B7285?style=flat-square" alt="MIT license"></a>
  <a href="./cordis.patch.yml"><img src="https://img.shields.io/badge/DSH-Web%20%2B%20Headless-5B4CF0?style=flat-square" alt="DSH Web and Headless"></a>
</p>

## One prompt. A working team.

`dsh-agent-teams` turns the current DeepSeek Harness session into a captain that can assemble durable sub-agents, split a goal into dependency-aware tasks, and coordinate work through direct messages.

Ask in natural language. The plugin provides the team protocol, 14 coordination tools, persistent state, an automatic shared-task scheduler, and a live Web UI—without requiring a separate workflow engine.

<p align="center">
  <img src="./assets/ui.png" width="100%" alt="DeepSeek Harness conversation with the AgentTeams live activity panel, members, tasks, dependencies, and reports">
</p>

## Releases

[v0.1.20](./release-notes/v0.1.20.md) syncs the version references in this document with the npm `latest` channel. It changes no code and no behavior; the packaged artifact is identical to [v0.1.19](./release-notes/v0.1.19.md), which carries the substantive changes since the last documented release: member startup survives a host that disables or renames its delegation tools, automatic repair scope is derived from `requiredFix`, and captains gain `agent_teams_amend_task`. Recommended host: DeepSeek Harness `0.1.5-rc.1`; the three older supported host targets are retained.

## Why AgentTeams?

| Capability | What it changes |
| --- | --- |
| **Captain-led delegation** | The current session creates the team, assigns roles, and consolidates the final result. |
| **Durable members** | Members are continuable DSH sub-agents that can be woken for focused follow-up turns. |
| **Dependency-aware tasks** | Tasks move through explicit states and cannot be claimed before their dependencies finish. |
| **Automatic reuse and safe takeover** | Idle members claim the next ready task; reassignment revokes stale attempts before new work starts, and cold recovery retries stranded open attempts. |
| **Direct messaging** | Members send durable mailbox messages directly to teammates or the captain—no relay required. |
| **Live activity panel** | The Web UI combines segmented progress, a collapsible roster, and an interactive task DAG; running tasks show the member's model, and completed archives retain their full member and task history. |
| **Plan before execution** | Normal `/agent-teams` runs stage an unspawned roster and DAG first. The Web panel uses the host model catalog for member routes. Returning to chat stops the planning turn, asks what should change, and revises the same draft; discarding archives the draft, aborts the turn, and explicitly prevents automatic recreation. Only **Approve & Run** enables scheduling; each member starts with its first ready task. |
| **Quality gates** | Opt-in quality tasks support requirements → implementation → verification → review → integration contracts, automatic repair/re-review, and explicit resume. Scope control is a completion-time audit, not host write interception. See [docs/quality-gates.md](./docs/quality-gates.md). |

The conversation card and activity panel use Harness's official locale service. They follow live language changes between English and Simplified Chinese—including status labels, dynamic summaries, controls, archive markers, and accessibility text—without a page reload or a separate plugin setting.

## Install and choose versions

**Recommended pair: DeepSeek Harness `0.1.5-rc.1` + AgentTeams `0.1.20`. Harness remains a prerelease.**

| Use case | DeepSeek Harness | AgentTeams plugin |
| --- | --- | --- |
| **Recommended installation** | **`0.1.5-rc.1`** | **`0.1.20`** |
| Retaining an older RC | `0.1.2-rc.1` | `0.1.20` |
| Developer Alpha testing | `0.1.2-alpha.5` | `0.1.20` |
| Retaining an older Alpha | `0.1.2-alpha.2` | `0.1.20` |

### 1. Install DeepSeek Harness

```sh
npm install --global @deepseek-ai/dsh@0.1.5-rc.1
dsh --version
```

Skip this if you already run this version. Alpha is opt-in: select an exact Alpha version from the table and lock all host dependencies as described in the [maintenance guide](./docs/maintenance-workflow.md).

### 2. Install the AgentTeams plugin

Install into the `web` profile. Replace the profile name if needed:

```sh
dsh plugin --profile web add --save-exact @nanmicoder/dsh-agent-teams@0.1.20
```

**After installation, stop and restart Harness for that profile, then refresh the browser.**

The default npm `latest` tag points to `0.1.20`, so `dsh plugin --profile web add @nanmicoder/dsh-agent-teams` installs this version on a fresh profile. Use the exact-version command above to pin it. The recommended Harness version is `0.1.5-rc.1`; installing the plugin does not upgrade the host. See the [source installation guide](./docs/maintenance-workflow.md) and [release verification](./docs/releases/v0.1.19/README.md).

> Desktop users must check the app's embedded Harness core; upgrading the global CLI does not upgrade it. For older `0.1.0-*` / `0.1.1-*` or unlisted hosts, keep a working pair and follow the [older-version and diagnostic guide](./docs/maintenance-workflow.md).

See the full [compatibility matrix](./compatibility.json), [source installation and Alpha testing guide](./docs/maintenance-workflow.md), and [verification coverage and platform limits](./docs/maintenance-2026-09-06/release/README.md).

Then ask for a team directly:

> Use AgentTeams to review the commits after v0.5.3 from performance, security, and product perspectives. Return one consolidated report.

## How it works

1. For a request to use AgentTeams, the captain follows the core protocol already in its system instructions. It continues an existing team and uses `agent_teams_status` when current state needs checking. When no team exists, the goal becomes a staged plan for review.
2. The captain adds role-specific members backed by continuable sub-agents.
3. The goal becomes tasks with owners and explicit dependencies.
4. The shared scheduler uses real `running / idle / ready` state to atomically claim one ready task per idle member and wake it. An interrupted resident attempt stays parked and can resume through a direct message without losing its capability; after a cold process restart, the scheduler retries stranded open work with a fresh attempt.
5. Members update with the current `attempt_id`; reassignment or captain takeover revokes the old attempt and waits for the old worker to quiesce before a new attempt starts.
6. The captain presents the combined result, then archives the complete team record.

Team state is stored under `<workspace>/.agent-teams/`; the Web panel reads that disk truth and combines it with live sub-agent activity.

Member creation is zero-interaction by default: a member on the captain's current L