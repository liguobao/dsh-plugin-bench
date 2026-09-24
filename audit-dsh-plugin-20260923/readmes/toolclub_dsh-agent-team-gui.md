# dsh-agent-team-gui

[English](README.md) | [简体中文](README-zh.md)

[![CI](https://github.com/toolclub/dsh-agent-team-gui/actions/workflows/ci.yml/badge.svg)](https://github.com/toolclub/dsh-agent-team-gui/actions/workflows/ci.yml)
[![GitHub release](https://img.shields.io/github/v/release/toolclub/dsh-agent-team-gui?include_prereleases&style=flat-square)](https://github.com/toolclub/dsh-agent-team-gui/releases)
[![GitHub stars](https://img.shields.io/github/stars/toolclub/dsh-agent-team-gui?style=flat-square)](https://github.com/toolclub/dsh-agent-team-gui/stargazers)
[![MIT license](https://img.shields.io/github/license/toolclub/dsh-agent-team-gui?style=flat-square)](LICENSE)

**Give DeepSeek Harness a reusable team: one Agent plans, another implements, and a third reviews.**

Save the team once, choose a model for each member, and reuse it across projects and conversations.
Follow the plan, member outputs, retries, and provider-reported Token usage in one Run Center.
This is an unofficial community plugin for the **DeepSeek Harness Web profile**.

[Watch the 80-second UI guide](https://github.com/toolclub/dsh-agent-team-gui/blob/main/assets/promotion-walkthrough-zh.mp4) · [Install v1.3.0](#install) · [Run your first team](docs/first-team.md) ·
[Example recipe](examples/full-stack-delivery.recipe.json) ·
[Share a workflow](https://github.com/toolclub/dsh-agent-team-gui/discussions/1)

[![UI walkthrough: reusable team setup, run inspection, and recipes](https://raw.githubusercontent.com/toolclub/dsh-agent-team-gui/main/assets/promotion-walkthrough-preview.gif)](https://github.com/toolclub/dsh-agent-team-gui/blob/main/assets/promotion-walkthrough-zh.mp4)

*Screenshot-based UI guide with example data and Chinese synthetic narration. Displayed task results, timings, and Tokens are not a live-run benchmark. [Sources and captions](docs/promotion/demo-guide.md).*

If this is useful for your DSH workflow, [give the project a Star](https://github.com/toolclub/dsh-agent-team-gui)
and help another developer discover it.

## Why this plugin

A team is a reusable product object, not a one-off dispatch form. Create it once in **Settings →
Teams**, then use it across projects and conversations.

| Capability | User outcome |
| --- | --- |
| One model and tool policy per member | Combine a planner, implementer, reviewer, or specialist without forcing one route on everyone |
| Dynamic workflow planning by default | The active conversation's model assigns focused work and dependencies from the current request |
| Team / Solo / Inherited modes | Choose a durable conversation override, a project default, or a one-message exception without ambiguous switches |
| Bounded DAG, retries, quality gate, background work | Long work is observable, cancellable, finite, and restart-safe |
| Official provider Token usage | See input, cache-read, cache-write, and output Tokens with full/partial/unavailable coverage—never invented prices |
| Versions, recipes, and definition backup | Reproduce a team, share it without credentials, preview impact, and remap model routes before applying |

## Install

| Plugin release | DSH target | Upgrade guidance |
| --- | --- | --- |
| **1.3.0** | `>=0.1.5-rc.1 <0.1.6-0` | Recommended; selectable on-demand delegation and consistent mode boundaries |
| 1.2.0 | `>=0.1.5-rc.1 <0.1.6-0` | Failure diagnosis and bounded lead-driven continuation |
| 1.1.1 | `>=0.1.5-rc.1 <0.1.6-0` | Earlier workflow fixes; retries still replay the assignment |
| 1.1.0 | `>=0.1.5-rc.1 <0.1.6-0` | Initial 0.1.5 compatibility; upgrade the plugin to 1.3.0 |
| 1.0.1 | Verified with `0.1.1-rc.2` | Previous integration; upgrade both DSH and the plugin together |

The walkthrough has [English subtitles](https://github.com/toolclub/dsh-agent-team-gui/blob/main/docs/promotion/demo-captions.en.srt)
and [Chinese subtitles](https://github.com/toolclub/dsh-agent-team-gui/blob/main/docs/promotion/demo-captions.zh-CN.srt).
Load the SRT alongside the existing video in a compatible player; GitHub does not attach it automatically.

Upgrading DSH from 0.1.1? Use plugin **v1.3.0** for DSH **0.1.5**. This release fixes
`source.subscribe` during plugin loading, migrates reconnect and Session APIs, and keeps the existing
team definitions and run store. Restart DSH and refresh the browser after upgrading. The CLI may
report `0.1.5-rc.1` while its compatible internal packages resolve to `0.1.5-rc.2`.

Requirements: a working DeepSeek Harness **Web** profile, at least one configured provider/model,
Node.js `>=22.19.0 <23` or `>=24.0.0`, and pnpm. Declared DSH compatibility is
`>=0.1.5-rc.1 <0.1.6-0`; the v1.3.0 release was verified against DSH `0.1.5-rc.1`.

**Recommended: install the compiled release package.** It includes the built Host and client files,
so installation does not run this plugin's Git `prepare` build or require its `allowBuilds` entry.

```sh
dsh plugin --profile web add -w https://github.com/toolclub/dsh-agent-team-gui/releases/download/v1.3.0/dsh-agent-team-gui-1.3.0.tgz
dsh --profile web
```

Stop and restart an already-running DSH Web process after installing or upgrading. Then open
**Settings → Teams**. If a plugin marketplace chooses Git installation and fails, use the direct
release command above; see [installation troubleshooting](docs/first-team.md#installation-troubleshooting).

[Release notes and checksum](https://github.com/toolclub/dsh-agent-team-gui/releases/tag/v1.3.0) ·
[Git/source installation](#git-source-installation)

> [!TIP]
> If `dsh` is not on `PATH`, use the launcher that starts your working Harness installation.
> With npm, replace `dsh` with `npx @deepseek-ai/dsh@0.1.5-rc.1`; from a source checkout, replace
> it with `pnpm --dir /absolute/path/to/deepseek-harness dsh`. Keep the same launcher for installation
> and startup. New to Harness? Start with its [official setup guide](https://github.com/deepseek-ai/deepseek-harness#run).

Verify that both the `dsh-agent-team-gui` bundle and the `agent-team-gui` configuration row are present:

```sh
dsh --profile web --dump-config
```

## Run your first team

Use the included [full-stack delivery recipe](examples/full-stack-delivery.recipe.json), with a
planner, implementation engineer, and reviewer. You can bind all three to the same working model
for the first run; multiple providers are optional.

1. Download the recipe JSON. Open **Settings → Teams → Recipes & data** and choose **Choose recipe file**.
2. Map the placeholder routes to your configured provider/model routes, review the preview, and choose
   **Create a copy → Import reviewed recipe**. In **Member library**, confirm each member's exact model and tool access.
3. For this first walkthrough, set **Team usage → Host dispatches first**, **Dispatch policy → Run assigned work**, and member selection to
   **All members**, then save. The supplied recipe otherwise uses Smart/adaptive selection.
4. Select an empty scratch project, choose the imported team beside the composer, select **Select team for this conversation**, and send the
   [ready-to-copy task](docs/first-team.md#try-a-small-development-task): build and test a small to-do list.
5. Open **Team runs** to inspect the plan, outputs, review, and actual Token coverage. Check the delivered
   files and test results before treating the task as complete.

[Full walkthrough, expected results, and troubleshooting →](docs/first-team.md)

## Create your own team

In **Settings → Teams → Member library**, save each member's role, model, optional fallback, and tool policy.
In **Settings → Teams**, add those members and choose activation, member selection, and execution options.
Leave **Fixed order** off for dynamic planning, or enable it for a fixed serial sequence.
Choose **Team**, **Solo**, or **Inherited** beside the composer to control the current conversation.

![Choose Team, Solo, or Inherited beside the normal composer](assets/v0.5-composer-mode.png)

*UI example with demonstration data.*

## How or