<div align="center">

<h1>LeanToken</h1>

**Code intelligence for agents: find the code that matters and keep your context window and tokens lean.**

**Language:** English · [简体中文](docs/i18n/zh-CN/README.md) · [日本語](docs/i18n/ja-JP/README.md) · [한국어](docs/i18n/ko-KR/README.md)

- MCP Registry name: `mcp-name: io.github.morluto/leantoken`

<img src="assets/leantoken-hero-v3.jpg" alt="LeanToken narrowing a large codebase to the files and code an AI agent needs" width="100%">

[![npm](https://img.shields.io/npm/v/leantoken?logo=npm&label=npm)](https://www.npmjs.com/package/leantoken)
[![npm downloads](https://img.shields.io/npm/dm/leantoken?logo=npm&label=downloads)](https://www.npmjs.com/package/leantoken)
[![Rust 1.95+](https://img.shields.io/badge/Rust-1.95%2B-000000?logo=rust)](https://www.rust-lang.org/)
[![License: MIT OR Apache-2.0](https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-blue)](#license)

[Install](#quick-start) · [Why LeanToken](#why-leantoken) · [Tools](#available-tools) · [CLI](#cli-usage) · [How it works](#how-it-works) · [Docs](#documentation)

</div>

---

> **Measured token savings:** In a controlled 60-run study, LeanToken used
> 20.1% fewer model input tokens than the agent's built-in tools with limited
> repository exploration, and 37.6% fewer than those tools with broad
> exploration. See exactly
> how it was measured in the [measurement methodology](https://github.com/morluto/leantoken/blob/main/docs/measurement.md).

## Quick start

Add LeanToken to Claude Code, Cursor, OpenCode, Codex, Gemini CLI, or
Antigravity:

```bash
npx leantoken setup
```

<details>
<summary><strong>Setup behavior and safety</strong></summary>

Current releases stop setup before writing when `npx` resolves a stale
project-local or ancestor install, and point to
`npx leantoken@latest setup`. Older releases that predate this check can be
bootstrapped directly with that versioned command.

The interactive setup wizard preselects supported clients it detects; you can
change that selection before continuing. It then shows the exact configuration
paths and MCP launcher and asks for a separate final confirmation. Automation
never treats detection as consent. An npx-based setup pins the exact LeanToken
version that ran setup, so restarting a client cannot silently move to a newer
release.

Global setup never stores the repository where setup happened. OpenCode gets a
workspace-relative working directory; other supported clients launch LeanToken
from the workspace cwd selected by the host. If a host instead starts it from
the home directory or a filesystem root, LeanToken refuses to index that broad
root by default.

</details>

Restart or reload the configured clients, then verify the connection and first
retrieval from a repository:

```bash
npx leantoken doctor
```

Try a broad task such as: *Find the code related to request cancellation before
editing.* LeanToken helps the agent start with `leantoken.context`, while its
normal tools remain available for edits, builds, and tests.

Inspect LeanToken's observed repository-local token accounting:

```bash
npx leantoken savings
```

<table>
<tr>
<td width="33%" valign="top">
<strong>Local by default</strong><br><br>
Source is indexed on your machine in a local database. LeanToken is a read-only
discovery and retrieval layer.
</td>
<td width="33%" valign="top">
<strong>Explicit token budgets</strong><br><br>
Every response has an explicit token limit, so large files cannot take over the
request.
</td>
<td width="33%" valign="top">
<strong>Built for agent workflows</strong><br><br>
Find files, search code, inspect structure, read exact ranges, trace history,
query JSON, and track token usage through focused tools.
</td>
</tr>
</table>

<details>
<summary><strong>Advanced setup and version management</strong></summary>

To skip the wizard, select clients explicitly or configure all supported
clients:

```bash
npx leantoken setup --claude --codex --yes
npx leantoken setup --all --yes
```

For regular use, `--private-runtime` is the recommended launcher: it copies the
exact package-native executable into LeanToken's versioned application-data
directory so clients launch one verified process directly, without persistent
npm/Node wrappers. It remains opt-in so the zero-install path does not add an
application-data write. Preview its path and digest with `--dry-run`.

Automation never treats detection as consent: `--yes` requires explicit client
flags, `--all`, or `--refresh` for entries already managed by LeanToken. Preview
the same resolved plan without changing files:

```bash
npx leantoken setup --codex --cursor --dry-run
```

Setup adds the `leantoken` MCP entry plus a small owned discovery skill only in
the directories used by the selected hosts: Claude Code uses `~/.claude`, while
Codex and the other supported hosts use `~/.agents`. The skill advertises
routing metadata; it does not duplicate tool schemas, add rules, or install
shell hooks. Setup marks new MCP launchers as managed and refuses to replace a
same-name manual entry unless you review the dry-run and pass
`--force-unmanaged`. Remove the owned integration with:

```bash
npx leantoken remove
```

After private-runtime upgrades, inspect retained versions and preview a
reference-safe cleanup before applying it:

```bash
npx leantoken runtime list
npx leantoken runtime prune --dry-run
npx leantoken runtime prune --yes
```

Refresh only existing LeanToken MCP entries after explicitly choosing a new
version, or use an older version to roll back:

```bash
npx --yes leantoken@latest setup --refresh --yes
npx --yes leantoken@0.1.8 setup --refresh --yes --allow-outdated
```

</details>

## Common agent workflows

LeanToken works best as a small evidence loop rather than a one-shot repository
dump:

1. **Orient autonomous triage in one call.** Start an uncertain broad task with
   `context` and `plan_only: false`, then use the materialized evidence
   directly. Make at most one focused follow-up only when coverage identifies a
   concrete missing implementation or regression-test owner.
2. **Continue without resending source.** Pass the prior `receipt_id` on the
   next context call, or pass returned fragment hashes as `known_hashes`. The
   response reports exact and overlapping omissions instead of silently
   charging the same evidence again.
3. **Investigate an observed failure.** Use the `investigation` workflow and
   provide only directly observed `failure_traces`, paths, symbols, or test
   intent in `workflow_evidence`. Follow with exact `search`, `outline`, or
   `read` calls for the owners the evidence identifies.
4. **Review a change.** Use the `review` workflow with `base_revision` set to
   `BASE..HEAD` and `strict_changed_paths: true`. Request a `handoff` when
   another agent needs a compact manifest of selected hashes, changed paths,
   assumptions, and completed validations without copied source bodies.

This one-call contract is for autonomous repository triage, not a limit on
implementation agents. Human review and control-plane flows can still preview
expensive or high-risk retrieval with `plan_only: true` before materializing.
The [repeated multi-agent context suite](https://github.com/morluto/leantoken/blob/main/docs/measurement.md#repeated-multi-agent-context-suite)
found that an iterative LeanToken profile used 50.9% more total input than thin
native, while the frozen one-context-plus-optional-one-search profile saved
20.1% and had 15/20 path-set successes. Those results cover four pinned triage
tasks; they do not prove a universal implementation workflow.

Explicit focus constraints are contracts. When a request supplies
`focus_paths`, exact `focus_symbols`, and
`minimum_fragments_per_focus_path`, LeanToken generates candidates within the
documented per-file bounds and reports a coverage failure when distinct ranges
cannot satisfy the minimum. Explain-profile plans and materialized responses
also identify the bounded alloc