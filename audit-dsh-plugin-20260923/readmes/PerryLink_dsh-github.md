<div align="center">

# dsh-github
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-github)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-github?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-github?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-github/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-github)

**GitHub PRs, reviews, issues, and CI for DeepSeek Harness — every write gated by human approval, token never logged.**

*Create, review, merge, and search GitHub from the agent, with a CI composite action, polling review bot, and status-check gate.*

> **Official repository.** This is the only official repository of dsh-github, maintained by PerryLink. Same-name repositories under other accounts are not affiliated.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-github.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-github/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-github/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-github?label=version)](https://github.com/PerryLink/dsh-github/releases)
[![npm version](https://img.shields.io/npm/v/%40perrylink%2Fdsh-github)](https://www.npmjs.com/package/@perrylink/dsh-github)
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add @perrylink/dsh-github` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![npm downloads](https://img.shields.io/npm/dm/%40perrylink%2Fdsh-github)](https://www.npmjs.com/package/@perrylink/dsh-github)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## 📚 Table of contents

- [Compatibility](#compatibility)
- [What you get](#what-you-get)
- [Quick start](#quick-start)
- [Install & uninstall](#install--uninstall)
- [Configuration](#configuration)
- [Tools & surfaces](#tools--surfaces)
- [Architecture](#architecture)
- [Permissions & data](#permissions--data)
- [Security boundaries](#security-boundaries)
- [Known limitations](#known-limitations)
- [Development](#development)
- [Repository layout](#repository-layout)
- [Topics](#topics)
- [Contributors](#contributors)
- [PerryLink DSH Plugin Family](#perrylink-dsh-plugin-family)
- [License](#license)

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (compat declared for `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0`; 0.1.2-rc.1 adapted 2026-09-09): the review job is owned by a bare `SessionId` and a notice source is the plugin-owned kind `dsh-github` (the host's `Agent \| SessionId` union and its catch-all `kind: 'plugin'` are both gone); the settings card registers on the **Plugins page** (Official group, `plugins.item` slot) and renders from the owner form `dsh-client-ui-plugin-manager` supplies, instead of binding the removed `ctx.settingsScope`; the CI driver auto-approves through the official `ctx.approval.setPolicy` policy seam; the review bot polls as a `ctx.jobs` background job with a timer fallback. Upgraded 2026-09-22 to `0.1.7-alpha.1` (typecheck + typecheck:ci + 185 unit tests green). |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | All (host plugin; outbound network to GitHub) |
| Model | Any (static review is deterministic; `reviewMode: "model"` is optional) |

## What you get

`dsh-github` fills the GitHub gap between `dsh` and tools like Claude Code and Codex: your agent can read, review, open, update, and merge pull requests, read repository metadata and files, comment on and close issues, and search — while a human approves every write and the token stays secret.

- **15 tools** — `pr_create`, `pr_merge`, `pr_update`, `gh_review`, `review_post`, `gh_issue`, `issue_open`, `issue_comment`, `issue_close`, `gh_search`, `gh_repo`, `gh_file`, `gh_repo_search`, `gh_checks`, all canonical JSON via `defineTool`, plus the one-shot `ci_run` when `ci.enabled` is on.
- **4 command families** — `/pr create`, `/review` (start/stop/post), `/issue open`, and `/ci` (`scan`/`status`/`start`/`stop`/`run <pr>`, registered under `ci.enabled`).
- **Full PR lifecycle** — create → review → update (title/body/state/base) → merge (merge/squash/rebase, optional head-branch delete).
- **Inline reviews** — `review_post` posts one summary comment or line-anchored review comments against the PR head commit.
- **Approval-gated writes** — every GitHub write goes through `ctx.approval` (default `ask`, fail-closed); approval reasons preview titles, body sizes, and comment overrides.
- **Token secrecy** — credentials seam → environment → `gh` CLI, resolved per operation, never in logs, events, renders, or errors.
- **Background review jobs** — `/review` runs on `ctx.jobs` with the host's own `job_list` / `job_output` / `job_kill` surface.
- **Resilience** — 429 retry with `Retry-After`/`x-ratelimit-reset` backoff; read tools are concurrency-safe; all calls honor cancellation.
- **CI surface** — the one-shot `ci_run` tool, a polling review bot, and a status-check gate (composite action `action.yml`).

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-github#main"

# or from npm (published releases)
dsh plugin --profile web add @perrylink/dsh-github

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A3 'id: dsh-github'
```

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-github#main"` — the `prepare` script builds with production dependencies only.
- **npm channel** (published releases): `dsh plugin --profile web add @perrylink/dsh-github`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./perrylink-dsh-github-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove @perrylink/dsh-github` (or remove the row from the profile patch).

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). An id-targeted override replaces the whole row — restate every key you need. `cordis.patch.yml` documents each key inline. In the GUI, the **Plugins page settings card** (Official group) reads `tokenRef` from the entry's own configuration form — the `0.1.7-alpha.1` host removed the `ctx.settingsScope` binding and the namespace-registration seam behind it, so the card no longer owns a settings namespace. The GitHub token is not a configuration field at all: the card reports whether the referenced credential is set and writes it through the credentials file, which is where the host half resolves it.

| Key | Default | Meaning |
|---|---|---|
| `tokenSource` | `auto` | `auto` (credentials → env → gh) or one of `credentials` / `env` / `gh` |
| `tokenRef` | `GITHUB_TOKEN` | Credential-seam reference / environment-variable name |
| `defaultOwnerRepo` | — | Fallback `owner/repo` when a call names none and git has no origin |
| `autoCommit` | `false` | Whether `/pr create` may instruct the model to commit+push first |
| `maxDiffChars` | `8000` | Character cap for PR diffs read into reviews |
| `renderExcerptChars` | `2000` | Character cap for the diff excerpt rendered into tool output |
| `maxComments` | `20` | Cap for PR comments listed by `gh_