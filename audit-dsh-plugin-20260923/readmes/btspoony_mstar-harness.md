<div align="center">

<img src="assets/logo.svg" alt="Morning Star Harness" width="96">

# [Morning Star](https://github.com/btspoony/mstar-harness)

Harness Workflow Engine · Agent Plugin

English / [中文](README_CN.md)

<a href="https://github.com/btspoony/mstar-harness">GitHub</a> · <a href="https://github.com/btspoony/mstar-harness/issues">Issues</a>

[![CI](https://img.shields.io/github/actions/workflow/status/btspoony/mstar-harness/ci.yml?branch=main&style=flat-square&label=CI&labelColor=black)](https://github.com/btspoony/mstar-harness/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-white?labelColor=black&style=flat-square)](LICENSE)
[![Version](https://img.shields.io/github/v/release/btspoony/mstar-harness?include_prereleases&sort=semver&label=version&style=flat-square&labelColor=black&color=c4f042)](https://github.com/btspoony/mstar-harness/releases)
[![Last commit](https://img.shields.io/github/last-commit/btspoony/mstar-harness?color=c4f042&labelColor=black&style=flat-square)](https://github.com/btspoony/mstar-harness/commits/main)
[![dshfind](https://dshfind.com/api/badge/btspoony/mstar-harness?lang=en)](https://dshfind.com/zh/plugins/btspoony/mstar-harness?ref=badge)
[![Greptile: The War on Bugs](https://www.greptile.com/badge.svg)](https://www.greptile.com/?utm_source=oss_badge&utm_medium=readme&utm_campaign=greptile_for_open_source)


[![npm: cli](https://img.shields.io/npm/dt/@mstar-harness/cli?style=flat-square&labelColor=black&color=c4f042&label=npm%3A%20cli)](https://www.npmjs.com/package/@mstar-harness/cli)
[![npm: dsh](https://img.shields.io/npm/dt/@mstar-harness/dsh?style=flat-square&labelColor=black&color=c4f042&label=npm%3A%20dsh)](https://www.npmjs.com/package/@mstar-harness/dsh)
[![npm: omp](https://img.shields.io/npm/dt/@mstar-harness/omp?style=flat-square&labelColor=black&color=c4f042&label=npm%3A%20omp)](https://www.npmjs.com/package/@mstar-harness/omp)
[![npm: opencode](https://img.shields.io/npm/dt/@mstar-harness/opencode?style=flat-square&labelColor=black&color=c4f042&label=npm%3A%20opencode)](https://www.npmjs.com/package/@mstar-harness/opencode)
</div>

**Morning Star / 晨星** is an Agent Plugin for harness engineering workflows: a TypeScript **Harness Workflow Engine** (`@mstar-harness/engine`) enforces deterministic workflow gates, while `mstar-*` judgment skills drive multi-agent code delivery.

- **Deterministic gates, enforced by a TS engine** — path/status/lease/dispatch/sdd/iteration/lint gates run in `@mstar-harness/engine`, not as prompt suggestions
- **Judgment stays in `mstar-*` skills** — skills remain the single source of truth (SSOT) for roles, gates, and workflow judgment
- **One engine across hosts** — the same engine + skills power dsh (DeepSeek Harness), omp, OpenCode, Cursor, Kimi Code, ZCode, and Codex
- **Agent Plugin packaging** — one-command install; portable across any Agent Plugins v1.0.0 client
- **Pluggable JSON persistence** — coordination docs (`status.json`, workflow snapshots, review envelopes) persist through an `ArtifactStore`; the default `FsStore` keeps the existing `.mstar/` paths, and integrations mount their own store via `MSTAR_STORE_MODULE` / `--store` / in-process `setArtifactStore`
- **Issue/catalog store vs execution JSON** — `{HARNESS_DIR}/store.db` (SQLite) is the issue and catalog authority after activation; `ArtifactStore` remains execution/review JSON (`status.json`, snapshots). The retired project registers are migration history with no write path. They are not the same store.
- **Recommended host** (best → usable): **dsh = omp ≥ ZCode = OpenCode = Cursor > Kimi > Codex**

**What ships**

| Component | What it is |
|-----------|------------|
| Harness Workflow Engine | `@mstar-harness/engine` — TS enforcement of deterministic workflow gates |
| mstar CLI | `@mstar-harness/cli` — installer bootstrap + `mstar` workflow verbs |
| `mstar-*` skills | Role, gate, and workflow judgment (single source of truth) |
| Host adapters | dsh, omp, OpenCode, Cursor, Kimi Code, ZCode, Codex |

Release notes: [CHANGELOG.md](CHANGELOG.md) / [CHANGELOG_CN.md](CHANGELOG_CN.md).

## Install

| Host | Command |
|------|---------|
| dsh (DeepSeek Harness) | `npx @mstar-harness/cli init --target dsh`<br>(one CLI command that runs two **independent** `dsh plugin --profile web add` installs:<br>`@mstar-harness/dsh` + `dsh-llm-fallbacks`; `--no-fallbacks` skips the latter)<br>or `dsh plugin --profile web add @mstar-harness/dsh`<br>+ `dsh plugin --profile web add dsh-llm-fallbacks` |
| omp | `npx @mstar-harness/cli init --target omp`<br>(links `~/.mstar/harness/packages/omp`)<br>or `omp plugin install @mstar-harness/omp` |
| OpenCode | `npx @mstar-harness/cli init --target opencode` |
| Cursor | `npx @mstar-harness/cli init --target cursor` |
| Kimi | Kimi TUI: `/plugins install https://github.com/btspoony/mstar-harness`<br>→ `/plugins reload` |
| ZCode | `npx @mstar-harness/cli init --target zcode`<br>then install **morning-star-harness** in ZCode → Settings → Plugin Management |
| Codex | `npx @mstar-harness/cli init --target codex`<br>then `codex plugin add morning-star-harness@mstar-repo` (repo-bundled marketplace) |
| Generic (Agent Plugins v1) | point any Agent Plugins v1.0.0 conformant client at this repo root<br>(`plugin.json` + `skills/` are the portable package) |

> CLI commands in this section run the published bin through its Bun shebang: `npx` / `bunx` / `npm i -g` all need **Bun >=1.4.0** on PATH. Node-only machine: `npm install @mstar-harness/cli`, then `node node_modules/@mstar-harness/cli/dist/mstar-harness.js <verb>` (see **Runtime floors**).

### Engine gate checks (Recommended)

```bash
npm i -g @mstar-harness/cli
```

Puts the `mstar-harness` binary (short alias `mstar`) on PATH, so the engine-check commands the skills cite (`mstar status validate`, `mstar dispatch validate`, `mstar iteration gate`, …) actually run.

`init` now auto-installs the matching-version CLI globally after a successful run — pass `--no-global-cli` to opt out.

Without a global install the harness still works and those checks stay advisory. Set `enforcement: hard` in an iteration compass to make dispatch preflights fail-fast.

> **Caution**: `mstar` is a short alias and a **shared bin namespace** — an unrelated third-party npm package named `mstar` claims the same command name. The alias exists only where `@mstar-harness/cli` is installed: bare `npx mstar …` without the package resolves via the registry to that other tool, and globally co-installing both packages silently overwrites the `mstar` shim (last install wins). The canonical invocation name stays `mstar-harness` — use the long name on any conflict.

### Verify

`npx @mstar-harness/cli doctor --target <opencode\|cursor\|codex\|zcode\|omp\|dsh>`.

Codex agent-link repair and named-role verification: [Codex installation](INSTALL.md#codex).

The repo ships a portable **Agent Plugins v1.0.0** manifest (`plugin.json`) at its root; `skills/` is the Agent Skills component — verify it with `npx @mstar-harness/cli plugin validate`.

Manual install / path layout: [`INSTALL.md`](INSTALL.md). CLI flags: the **`mstar-use-cli`** skill.

### Runtime floors (entrypoint, not “install both”)

The published CLI keeps a Bun shebang (`#!/usr/bin/env bun`). Normal launch of `mstar-harness` / the dist file uses **Bun >=1.4.0**. An explicit `node <CLI bundle>` uses **Node >=24.18.0**. `npx` / `bunx` fetch the package but still execute that same Bun-shebang bin, so they need **Bun >=1.4.0** on PATH as well — a package runner is not a runtime; on a Node-only machine install the package and run the bundle under Node (`node node_modules/@mstar-harness/cli/dist/mstar-harness.js <verb>`). Bun-hosted plugins need Bun; native Node entries need Node. Do not treat those floors as a demand to install both runtimes on every machine. This README does not prove packaged compatibility or store activation.

## Use

Three entry shapes: **without iteration*