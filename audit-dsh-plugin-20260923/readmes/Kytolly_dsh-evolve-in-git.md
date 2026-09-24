# dsh-evolve-in-git

<p align="center">
  <a href="https://github.com/Kytolly/dsh-evolve-in-git"><img src="https://img.shields.io/badge/DeepSeek%20Harness-plugin-4D6BFE" alt="DeepSeek Harness plugin"></a>
  <img src="https://img.shields.io/badge/version-0.6.3-4D6BFE" alt="version 0.6.3">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license MIT">
</p>

<p align="center">
  <a href="./README.md">English</a> · <a href="./README.zh-CN.md">中文</a>
</p>

Git-backed long-term memory and evolution plugin for DeepSeek Harness.

## Contents

- [What it does](#what-it-does)
- [Install](#install)
- [Usage](#usage)
- [Architecture](#architecture)
- [Data layout](#data-layout)
- [Config](#config)
- [Harness entry points](#harness-entry-points)
- [Browser half](#browser-half)
- [Development](#development)
- [Delivery notes](#delivery-notes)
- [License](#license)

## What it does

This plugin treats a user-chosen or preconfigured Git repository as the memory store.
It can write session notes, branch-specific records, and reusable skill drafts into that repo, then commit them as ordinary Git history.

## Install

```sh
# example: install into the web profile
 dsh plugin --profile web add github:Kytolly/dsh-evolve-in-git
```

The bundle inserts one `dsh-evolve-in-git` row with the plugin defaults.
Later profile patches can override `repoPath`, `repoUrl`, `auth`, and the storage roots.

## Usage

### Natural language

You do not need to remember tool names — describe the outcome and the model
selects the right `evolve_*` / `memory_*` tool:

| You say (or similar) | The model uses |
| --- | --- |
| "Remember: whenever X happens, do Y" | `evolve_remember` / `memory_save` |
| "Any memory about the deploy flow?" | `evolve_recall` / `memory_search` |
| "Read my recent memory history" | `evolve_timeline` |
| "Turn this warning into a reusable skill" | `evolve_skill_draft` → `evolve_skill_promote` |
| "What is the memory repo's current state?" | `evolve_status` / `evolve_branches` |
| "Undo the last memory commit" | `evolve_rollback` |

### Commands (`/evolve`)

For explicit, deterministic control, type `/evolve <subcommand>`:

```sh
/evolve remember warning "pitfall" :: <content>
/evolve search deploy
/evolve skill list
/evolve skill promote evolve-process
/evolve status
/evolve help
```

The full command reference is under [Harness entry points](#harness-entry-points).

## Architecture

The package is split into a **framework-free core** and a thin **DSH adapter**:

- `src/core.ts` (`GitMemoryCore`) is the portability boundary. It depends only on
  Node built-ins and sibling core modules — never on `@deepseek-ai/*` — and
  resolves config from the on-disk file over the host-provided base.
- `src/index.ts` (`GitEvolutionService`) is the adapter: it registers Cordis
  tools, the `/evolve` command, the system-prompt section, the skill provider,
  and the config-file route, then maps every surface onto `GitMemoryCore`.

| Module | Responsibility |
| --- | --- |
| `src/git.ts` | Spawns `git`: clone/open, status, branch ops, push/fetch, commit, `git mv`, conflicts, rollback. |
| `src/memory.ts` + `src/memory-index.ts` | Markdown+YAML-frontmatter scanning, a metadata index cache (HEAD + mtime signature), budgeted recall, timeline. |
| `src/update.ts` | Versioned update: a new active record plus `supersedes`/`supersededBy`; the old file is never deleted. |
| `src/forget.ts` | Soft-delete (move to `archiveRoot`) and restore. |
| `src/privacy.ts` | Sensitive-content detection, sensitivity classification, redaction, export filtering. |
| `src/skill.ts` | `drafts/` ↔ `enabled/` skill discovery; promote/demote via `git mv`; bundled-skill sync. |
| `src/strategy.ts` | Slug/sanitize, draft generation from a memory, evolution suggestion, preview. |
| `src/harness.ts` | `/evolve` command normalization/parsing plus help/usage/safety text. |
| `src/config.ts` + `src/defaults.ts` | Config-file read/write/merge and the plugin defaults. |
| `src/invariant.ts` | No-op invariant companion (the source of truth is the configured Git repo). |
| `src/loopback.ts` + `src/config-route.ts` | Loopback-only `/api/evolve-git/config` route for the config-file editor. |
| `src/client/` | Browser settings section (`evolve-git` slot) and config-file editor. |

## Data layout

- **Memory** — `<repo>/<memoryRoot>/<kind>/<timestamp>-<slug>-<id>.md`, one
  Markdown file per record with YAML frontmatter (`kind`, `title`, `branch`,
  `source`, `tags`, `createdAt`, `id`, `updatedAt`, `status`, `supersedes`,
  `supersededBy`, `expiresAt`, `sensitivity`) followed by the body.
- **Skills** — `<repo>/<skillsRoot>/drafts/<name>/SKILL.md` (promotable) and
  `<repo>/<skillsRoot>/enabled/<name>/SKILL.md` (discoverable). Promotion is a
  `git mv` between the two, never a copy, so it stays reversible and in history.
- **Archive** — `<repo>/<archiveRoot>/…` (same relative layout as memory);
  `evolve_forget` moves records here so they leave recall/timeline but stay
  recoverable. `archiveRoot` must remain outside `memoryRoot`.

## Config

> **Web settings UI (v0.1.4+).** The plugin ships a browser half that registers a
> first-level **Settings → 演进记忆** section on the web profile's Settings page
> (via the `settings.section` slot). The form uses a `SettingsScope` adapter that
> reads and writes the per-user config file directly through the loopback-only
> `/api/evolve-git/config` route, so what the form shows is exactly what takes
> effect (defaults overlaid by the file) and saving writes the file immediately.
> Nested `auth` is written as one merged object, and the `auth.token` field is
> write-only (secret, redacted from read-back). Requires the profile to be
> restarted after install so the client manifest is rescanned.

- `repoPath` - the local Git checkout that stores memory and skills. Defaults to `~/.dsh-evolve-in-git/remote-memory`.
- `repoUrl` - the remote memory repository. **No personal default ships with the plugin**: the built-in default is the placeholder `https://github.com/<your-github-username>/<your-memory-repo>.git`, so configure your own repository (see "Per-user config file" below).
- `auth` - Git auth settings for private access. The default profile is SSH-first and token-capable.
- `memoryRoot` - where memory records are written, default `.dsh-evolve/memory`.
- `skillsRoot` - where skill drafts are written, default `.dsh-evolve/skills`.
- `defaultBranch` - branch to evolve from when creating new branches, default `main`.
- `remoteName` - remote to fetch and push, default `origin`.
- `autoCommit` - whether writes auto-commit, default `true`.
- `archiveRoot` - where `evolve_forget` moves records, default `.dsh-evolve/archive`.
- `recallTopK` - maximum results `evolve_recall` returns, default `10`.
- `recallMinScore` - minimum relevance score to keep, default `0`.
- `recallMaxChars` - cumulative character budget for returned recall content, default `8000`.
- `privacyMode` - write-path privacy gate for sensitive content, default `ask`. `block` rejects the write when sensitive content is detected; `redact` stores the redacted content (never the plaintext); `ask` stores the content as-is and marks its `sensitivity` so it can be reviewed/confirmed.
- `digestEnabled` - whether to inject the session-start `persona`+`warning` digest, default `true`.
- `digestMaxRecords` - maximum `persona`/`warning` records in the session-start digest, default `5`.
- `digestMaxChars` - maximum characters of the session-start digest, default `2000`.

### Auth

- `auth.mode: "ssh"` - use `ssh` or a custom `sshCommand`.
- `auth.mode: "token"` - use `token` or a token from `tokenEnv` and a GitHub-style `Authorization` header.

### Privacy write gate

Every memory write passes through the privacy gate (emails, phones, ID cards,
credit cards, AWS keys, GitHub tokens, private keys, and `password:`-style
secrets). `privacyMode` controls the response:

- `block` - reject the write when sensitive content is detected.
- `re