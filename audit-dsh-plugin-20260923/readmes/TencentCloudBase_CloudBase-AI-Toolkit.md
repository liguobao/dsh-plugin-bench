<div align="center">

<img src="https://raw.githubusercontent.com/TencentCloudBase/CloudBase-AI-Toolkit/main/mcp/icon.png" width="96" height="96" alt="CloudBase AI Toolkit" />

# CloudBase AI Toolkit

**AI writes the code. CloudBase runs the backend.**

The CloudBase integration layer for AI coding tools: Plugin installs the stack, Skills steer how code is written, MCP operates databases, functions, storage, and deploys from chat.

**English** · [简体中文](./README.zh-CN.md) · [Docs][docs] · [Changelog][changelog] · [Issues][github-issues-link]

[![][npm-version-shield]][npm-link]
[![][npm-downloads-shield]][npm-link]
[![][github-stars-shield]][github-stars-link]
[![][github-forks-shield]][github-forks-link]
[![][github-issues-shield]][github-issues-link]
![][github-license-shield]
![][github-contributors-shield]
[![][cnb-shield]][cnb-link]
[![][deepwiki-shield]][deepwiki-link]

</div>

## Recent updates

**v2.34.x** (2026-09)

- i18n / IDE: full tool-copy localization with an instance-level `lang`, plus `auth` `site` / `region` params so international-site login and region routing resolve correctly
- Cloud API: `callCloudApi` service allowlist widened to 57 with built-in version mapping (multi-version services such as `tke` / `mongodb` / `vod` require an explicit `version`)
- Deploy / Env: new `appBuild` tool with hosting build neutralization; `queryEnv` reports the region actually applied and `domains` honors a passed envId
- Skills / Docs: skill fallback reads now point at the official distribution repo with a references address list; SDK-first database decision gate for cloudrun; site doc links moved to the current Markdown addresses; post-deployment share offered after delivery in the expert packs and the deploy skills (opt-in, redacted, at most once)
- Deploy / Apps: the cloud upload channel now completes end to end (`deployApp` accepts the timestamp `getUploadUrl` returns, `getBuildLog` accepts the build ID a deploy returns), and gateway route creation verifies the upstream exists before writing
- Skills / Context: new PostgreSQL access-pattern best-practices skill (batching, indexes, RLS role gating, launch capacity); `searchKnowledgeBase`'s inline skill / OpenAPI catalogs now load on demand, cutting the 43-tool surface by 9.1% on every `tools/list`
- Runtime / Hosting: CloudRun Function mode must not bind `PORT` (the function framework does) and gets a credential decision gate naming `CLOUDBASE_APIKEY`; hosting paths and prefixes are normalized so a leading slash can no longer read as an empty directory
- Connectors: the international-site WorkBuddy connector (`cloudbase-intl`) is built from the same `config/source/**` corpus as the domestic one — remote `streamableHttp` with standard MCP OAuth instead of local stdio, with China-site hosts rewritten to their international equivalents

**v2.33.x** (2026-09)

- Functions / Apps: custom container-image deploy for cloud functions with async status query; cloud upload channel (`getUploadUrl` + `deployApp` cosTimestamp)
- Env binding: `cloudbaserc.json` as field-level fallback for envId / region / site (literal + `{{env.KEY}}`)
- Errors / Skills: centralized error guidance by structured `Code`; virtual-pay reference; CodeBuddy IDE MCP upgrade skill; WorkBuddy experts
- Cloud API / Deploy: `callCloudApi` opens monitor & postgres services; declarative deploy with `deployPlan` / `deployApply`; `cloud-api-operations` skill

[Releases][changelog] · [Star][github-stars-link] · Watch → Releases

## What it is

AI IDEs (Cursor, Claude Code, Codex, CodeBuddy, and others) are strong at generating code. What usually blocks you is the backend: schemas, permissions, functions, storage, environments, and release.

[CloudBase](https://docs.cloudbase.net/) is Tencent Cloud’s AI-native all-in-one backend (database, storage, auth, cloud functions, Cloud Run, and more). This repo is the Toolkit that connects that backend to AI tools:

| Piece | Role |
|------|------|
| **Plugin** | Installs MCP Server, Agent Skills, and Hooks together—less per-IDE wiring |
| **Agent Skills** | Scenario skills (Web / Mini Program / database / auth / functions, etc.) toward workable CloudBase practice |
| **MCP** | Login, query and change data, manage functions and hosting, read logs—from the conversation |

This repository ships the npm package `@cloudbase/cloudbase-mcp`, Skills, and AI plugins.

You still need your own CloudBase environment, and you should confirm sensitive actions the AI proposes. The Toolkit provides capability and path—not judgment.

### Related repositories

Publishing and sync repos live under [TencentCloudBase](https://github.com/TencentCloudBase). Directly related to this Toolkit:

| Repository | Contents | Typical entry |
|------|------|----------|
| [CloudBase-AI-Toolkit](https://github.com/TencentCloudBase/CloudBase-AI-Toolkit) (this repo) | MCP Server source; marketplace source for Claude Code / Codex | `npx @cloudbase/cloudbase-mcp@latest` |
| [dsh-plugin](./dsh-plugin) | DeepSeek Harness plugin (`@cloudbase/dsh-plugin`): MCP bridge + DB/Storage/Auth panel | `dsh plugin add @cloudbase/dsh-plugin` |
| [cloudbase-plugin](https://github.com/TencentCloudBase/cloudbase-plugin) | Open Plugin Spec publish repo (CI-synced): MCP + Skills + Hooks | `npx plugins add TencentCloudBase/cloudbase-plugin` · CNB fallback: `npx plugins add https://cnb.cool/tencent/cloud/cloudbase/cloudbase-plugin.git` |
| [cloudbase-sites-plugin](https://github.com/TencentCloudBase/cloudbase-sites-plugin) | Sites plugin: Vite Web create & deploy | `npx plugins add TencentCloudBase/cloudbase-sites-plugin` · CNB: `https://cnb.cool/tencent/cloud/cloudbase/cloudbase-sites-plugin.git` |
| [cloudbase-skills](https://github.com/TencentCloudBase/cloudbase-skills) | Agent Skills collection | `npx skills add TencentCloudBase/cloudbase-skills` · CNB: `https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills.git` |
| [skills](https://github.com/TencentCloudBase/skills) | Per-skill install catalog (also on [skills.sh](https://skills.sh)) | `npx skills add tencentcloudbase/skills --skill <name>` |
| [awesome-cloudbase-examples](https://github.com/TencentCloudBase/awesome-cloudbase-examples) | CloudBase examples and case studies | Browse / clone examples |
| [OpenVibeCoding](https://github.com/TencentCloudBase/OpenVibeCoding) | Vibecoding template on CloudBase | Use as a project starter |

Prefer Plugin for the full stack; Skills alone when you only need knowledge constraints. For marketplace IDEs use this repo—do not also run `npx plugins add` on the same tool.

## Quick start

### Fastest way to get started

Copy this AI prompt into your AI IDE. The agent reads `skill.md` and completes the setup:

```
Set up CloudBase for me:
1. Open https://docs.cloudbase.net/skill.md and complete the setup following its instructions.
2. Tell me when you're done, and suggest the most relevant next step.
```

<details>
<summary>Pick one default path for your tool (Plugin / CLI / MCP)</summary>

| Your tool | Suggested path |
|----------|----------|
| Claude Code / Codex (native marketplace) | Add this repo as marketplace, then install the `cloudbase` plugin ([plugin docs](https://docs.cloudbase.net/ai/cloudbase-ai-toolkit/ai-agent-plugins)) |
| Open Plugin Spec tools | `npx plugins add TencentCloudBase/cloudbase-plugin` |
| Prefer one CLI for many tools | [CloudBase AI CLI](https://docs.cloudbase.net/cli-v1/ai/introduce): `npm i -g @cloudbase/cli && tcb ai` |
| CodeBuddy / WorkBuddy / ZCode / Kimi (built-in) | Use the IDE's built-in CloudBase plugin or connector; for CodeBuddy you can also [install via plugin marketplace](https://docs.cloudbase.net/ai/cloudbase-ai-toolkit/ide-setup/codebuddy) |
| Other MCP-capable IDEs | MCP config only (below) |

#### Plugin

```bash
npx plugins add TencentCloudBase/cloudbase-plugin
```

Details and IDE differences: [AI plugin docs](https://docs.cloudbase.net/ai/cloudbase-ai-toolkit/ai-agent-plugins).

#### MCP only

```json
{
  "mcpS