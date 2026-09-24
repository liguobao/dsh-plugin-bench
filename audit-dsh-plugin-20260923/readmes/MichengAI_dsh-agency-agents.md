<div align="center">
  <img src="assets/branding/dsh-banner-en.webp" alt="DSH Agency Agents" width="100%">
</div>

<div align="center">

  # DSH Agency Agents

  **321 specialists · 5 built-in teams · Custom collaboration**

  [简体中文](README.zh-CN.md) · [Expert roster](#expert-roster) · [Installation](#installation) · [Changelog](CHANGELOG.md) · [Release notes](RELEASE_NOTES.md) · [Apache-2.0](LICENSE)

  [![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
  [![Bundled agents](https://img.shields.io/badge/Bundled%20agents-321-0f766e.svg)](#expert-roster)
  [![npm package](https://img.shields.io/npm/v/%40michengai%2Fdsh-agency-agents.svg?label=npm%20package)](https://www.npmjs.com/package/@michengai/dsh-agency-agents)
  [![npm downloads](https://img.shields.io/npm/dt/%40michengai%2Fdsh-agency-agents.svg?label=npm%20downloads)](https://www.npmjs.com/package/@michengai/dsh-agency-agents)
  [![DSH Web Plugin](https://img.shields.io/badge/DSH%20Web-Plugin-0f766e.svg)](https://github.com/MichengAI/dsh-agency-agents)
  [![DSH supported through 0.1.7-alpha.1](https://img.shields.io/badge/DSH-up%20to%200.1.7--alpha.1-2563eb.svg)](#prerequisites)
</div>

> DSH Agency Agents is a community-maintained DeepSeek Harness (DSH) plugin, not an official DeepSeek AI product.

## Features

Choose a specialist in DSH for code review, design, operations, or research. All 321 experts are bundled and ready to use after installation.

- **Find the right expert**: filter by category or search in **Settings → Experts**.
- **Enable the roles you need**: keep the picker focused by enabling or disabling experts.
- **Describe the task directly**: use `@` or the **Experts** picker, then write your complete request.
- **Get one final delivery**: experts provide specialist analysis and the parent conversation brings the results together. Experts cannot summon further experts.

## Expert teams

Manage teams in **Settings → Experts → Expert teams**, sharing the header, source/status filters, search, and card interactions with individual experts.

| Built-in team | Focus | Delivery |
| --- | --- | --- |
| Product Review Team | User value, experience, technical feasibility | Priorities and actions |
| Technical Review Team | Architecture, security, acceptance boundaries | Risks and acceptance checks |
| Content Planning Team | Angles, distribution strategy, fact checking | Topic options and content structure |
| Data Analysis Team | Metrics, data quality, business interpretation | Findings and validation steps |
| Research Team | Research scope, evidence, synthesis | Source-backed conclusions |

### Configure and use

1. Use a built-in team, copy it to customize, or create a team of 2–8 distinct experts. Up to 100 custom teams can be saved.
2. Set the name, description, tags, member duties, shared goal, constraints, delivery requirements, and 1–3 examples. Use, customize, or restore the coordinator template.
3. Confirm enabling required experts when enabling a team. Switch to Expert teams in the composer picker or select through `@`, then write the task. Selecting or adding an example never sends the message.
4. The current main conversation delegates, verifies evidence, handles disagreements, and delivers one result; no additional leader subagent is created. Ordinary mode runs up to four experts concurrently and preserves completed results if others fail.

### Automatic collaboration mode

| Host state | Behavior |
| --- | --- |
| Agent Team unsupported | Use ordinary subagents without recommending an unavailable feature. |
| Supported but disabled, or current-session tools unavailable | Recommend enabling Team while continuing to allow ordinary execution. |
| Services and current-session tools available | Use native Agent Team, shared tasks, and teammate messages; wait for actual results before summarizing. |

Explicit `maxDepth` uses ordinary mode to preserve depth limits. Native dispatch acceptance is not expert completion; partial startup failures do not automatically switch modes and duplicate work. Members inherit the main conversation's model selection; there is no per-expert model setting. Native model labels are provided by DSH and may display creation-time values.

### Tool interfaces

Retain `list_experts`, `summon_expert`, and `summon_experts`. Add `list_expert_teams`, `get_expert_team`, and `summon_expert_team`. The main conversation reads the enabled team's rules and duties before delegating the complete task, then verifies and summarizes actual member results.

### Drafts, language, and data

- System presets, member names, coordinator templates, UI, and runtime feedback support Chinese and English. Custom content remains unchanged, and language switches preserve unsaved drafts.
- Confirm team replacement or example insertion. If the draft changes during confirmation, stop insertion and retain the new text, attachments, and references.
- Team configuration lives in the host `agency-agents` settings namespace. Keep drafts on edit conflicts and review the latest configuration. Disabling or deleting teams does not disable experts or delete historical conversations.
- Experts cannot summon further experts or automatically add analysis rounds. Cancellation prevents queued starts; completed results and failures are reported separately.

> This README describes version 1.0.2; npm and GitHub Releases determine publication status. See the [changelog](CHANGELOG.md) for the full changes and [release notes](RELEASE_NOTES.md) for the bilingual release description. Upgrades retain expert settings. Back up settings before downgrading because older versions do not support teams.
## Screenshots

The screenshots below show the 1.0.0 interface in Chinese. Experts and expert teams share the same settings page.

Filter by category or search in **Settings → Experts**, then enable the experts you need:

![DSH Experts panel](https://raw.githubusercontent.com/MichengAI/dsh-agency-agents/5cdbd07fda18075eab186aa972b47ab01451d244/assets/screenshots/agent-roster.png)

Switch to **Expert teams** to browse the five built-in teams, filter by status, or create a custom team:

![Expert teams panel](https://raw.githubusercontent.com/MichengAI/dsh-agency-agents/5cdbd07fda18075eab186aa972b47ab01451d244/assets/screenshots/expert-teams.png)

Open team details to review its purpose, example tasks, and member responsibilities, then summon it or copy it for customization:

![Expert team details](https://raw.githubusercontent.com/MichengAI/dsh-agency-agents/5cdbd07fda18075eab186aa972b47ab01451d244/assets/screenshots/expert-team-details.png)

When the host supports Agent Team and the feature is enabled, view team members and shared tasks in the native panel:

![Native Agent Team panel](https://raw.githubusercontent.com/MichengAI/dsh-agency-agents/5cdbd07fda18075eab186aa972b47ab01451d244/assets/screenshots/agent-team-panel.png)

## DSH product ecosystem

For a desktop workbench, download [DSH Codex Desktop](https://github.com/MichengAI/dsh-codex-desktop/releases). Existing [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) installations can add plugins as needed by following each project's README. Below are 11 first-party plugins; consult the corresponding desktop release notes and bundled catalog for what that version includes.

| Plugin | What you can do |
| --- | --- |
| [Codex UI](https://github.com/MichengAI/dsh-codex-ui) | Organize projects and conversations, search tasks, and navigate chat turns |
| [Agency Agents](https://github.com/MichengAI/dsh-agency-agents) | Choose and summon specialists for your task |
| [Skills Manager](https://github.com/MichengAI/dsh-skills-manager) | Find, enable, create, and import local skills |
| [Archive Manager](https://github.com/MichengAI/dsh-archive-manager) | Search, restore, or clean up archived conversations |
| [IM Connect](https://github.com/MichengAI/dsh-im-connect) | Send tasks and receive replies through mes