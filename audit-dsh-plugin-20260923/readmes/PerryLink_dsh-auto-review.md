<div align="center">

# 🤖 dsh-auto-review
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-auto-review)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-auto-review?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-auto-review?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-auto-review/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-auto-review)

**Second-model AI approval for DeepSeek Harness — a read-only reviewer subagent decides allow/deny on the approval chain, fail-closed by default.**

*When an action crosses the sandbox boundary, a second model reads the evidence and returns a verdict with a reason — so humans approve nothing while nothing unsafe slips through.*

> **Official repository.** This is the only official repository of dsh-auto-review, maintained by PerryLink. Same-name repositories under other accounts are not affiliated.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-auto-review.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-auto-review/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-auto-review/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-auto-review?label=version)](https://github.com/PerryLink/dsh-auto-review/releases)
[![npm version](https://img.shields.io/npm/v/dsh-auto-review)](https://www.npmjs.com/package/dsh-auto-review)
[![npm downloads](https://img.shields.io/npm/dm/dsh-auto-review)](https://www.npmjs.com/package/dsh-auto-review)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (verified 2026-09-22). Dual-line npm support: dev pins and runtime deps `0.1.7-alpha.2`, peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0` — the plugin code feature-detects the published host lines and each line runs the full gate chain; the runtime dependency pins follow the host line so a profile install never shadows the host's own tree. `pnpm-workspace.yaml` pins the whole `@deepseek-ai/dsh-*` graph to that line, because `autoInstallPeers` otherwise fills the frozen `dsh-agent-spine-demo` subgraph's `^0.1.1-rc.2` peers with previews that lack the exports the 0.1.7 packages import. On the alpha.2 line the eval fixtures pin `deepseek-flash` (the removed `deepseek-v4-flash` id is gone from `eval/`). |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | All (host answerer; optional Web review panel via the session-projection capability) |
| Model | Any (the reviewer inherits the session agent's route; `reviewerModel` overrides) |

## What you get

`dsh-auto-review` puts a second model on the `approval/request` answerer chain:

1. **Official seam** — an answerer that claims only the requests it owns (`ai` policy) and delegates everything else via `next()`; the human approval flow is never short-circuited.
2. **Read-only reviewer subagent** — a one-shot fork with a `read`/`glob`/`grep` tool allow-list returns a structured verdict `{ decision, reason, riskLevel }`. Reviewer asks are recognized by identity and delegated; `maxDepth` + the allow-list keep the reviewer non-delegating.
3. **Fail closed** — reviewer crash, timeout, or schema mismatch resolves through `fallbackPolicy` (default `rejected`); a deny verdict feeds its reason back to the calling model.
4. **Config-driven routing** — per-tool policies (`ai`/`human`/`never`) plus regex risk rules, all changeable from cordis.yml.
5. **Deny reasons reach the model** — the reviewer's reason is injected into the denied tool result (callId-linked); fallback and `never`-policy rejections inject auditable markers too (`[auto-review]` / `[auto-review-fallback]` / `[auto-review-never]`).
6. **Full audit trail** — log-only `autoReview/verdict` + `autoReview/rejection` session events (envelope `ignorable: true`) plus an optional invariant companion enforcing marker ⟺ event.
7. **Safety knobs** — a rejection circuit breaker (3 consecutive denials, or 6 of the last 10 verdicts, per turn), a risk-level policy, a one-shot `/auto-review approve` override, and a `never`-policy hard disable that explains itself to the model.
8. **Optional reviewer context** — a bounded compact transcript (`contextBudget`) plus a Codex-style Markdown ruling policy (`reviewerPolicyText`).

Every decision reconstructs from the session log: `approval/asked` → `autoReview/verdict` (or `autoReview/rejection`) → `approval/decided`.

## Why a second model instead of rules?

Pattern-based auto-approvers decide before dispatch, with no evidence. `dsh-auto-review` gives the decision to a **reviewer subagent** that reads the actual workspace (through its read-only tool face), the already-streamed tool-call arguments (sensitive values redacted), the request reason, and your risk rules — then returns a structured verdict. A deny verdict feeds its **reason back to the calling model**, so the agent learns why instead of retrying blindly.

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-auto-review#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-auto-review

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A4 'id: auto-review'
```

Out of the box the shipped patch AI-reviews `bash` and `write`; every other tool (including `edit` — in-place modification) delegates to the human chain. Add `edit: ai` explicitly if you accept in-place edits without a human in the loop.

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-auto-review#main"` — the isolated `prepare` build needs the single `allowBuilds: { esbuild: true }` key the `dsh` CLI prints for `dsh-auto-review`.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-auto-review`.
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-auto-review` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-auto-review-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-auto-review` (or remove the row from the profile patch).
- **native build scripts**: when `dsh plugin add` stops at `ERR_PNPM_IGNORED_BUILDS` for `koffi` / `node-pty` (pulled in by the eval harness), run `pnpm approve-builds` to approve those build scripts.

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). An id-targeted override replaces the whole row — restate every key you need.

| Key | Default | Meaning |
|---|---|---|
| `enableByDefault` | `true` | Sessions start with auto-review enabled; `/auto-review on\|off` writes a durable override that beats this |
| `toolsPolicy.default` | `human` | Policy for unlisted tools (delegate to the human answerer) |
| `toolsPolicy.overrides` | `{}` | Per-tool policy: `ai` / `human` / `never` |
| `riskRules` | `[]` | `{pattern, policy, field?}` matched before the tool table; `field` selects `reason` (default), `toolName`, or `arguments` |
| `reviewerProvider` | `fork` | Subagent provider for th