<div align="center">

# dsh-plugin-shop

**The plugin shop for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)** — discover, install,
enable and update dsh plugins from a browsable, git-auditable catalog.

[![npm](https://img.shields.io/npm/v/dsh-plugin-shop?logo=npm&color=cb3837)](https://www.npmjs.com/package/dsh-plugin-shop)
[![plugins](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2FLivXue.github.io%2Fdsh-plugin-shop%2Fv1%2Findex.json&query=count&label=plugins&color=blue)](https://LivXue.github.io/dsh-plugin-shop/v1/index.json)
[![filtered](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2FLivXue.github.io%2Fdsh-plugin-shop%2Fv1%2Findex.json&query=rejected&label=filtered&color=orange)](https://LivXue.github.io/dsh-plugin-shop/v1/index.json)
[![license](https://img.shields.io/npm/l/dsh-plugin-shop?color=blue)](LICENSE)
[![plugin CI](https://github.com/LivXue/dsh-plugin-shop/actions/workflows/plugin.yml/badge.svg)](https://github.com/LivXue/dsh-plugin-shop/actions/workflows/plugin.yml)
[![catalog](https://img.shields.io/endpoint?url=https%3A%2F%2FLivXue.github.io%2Fdsh-plugin-shop%2Fv1%2Fbadge.json)](https://github.com/LivXue/dsh-plugin-shop/actions/workflows/daily.yml)

English | [中文](README.zh.md)

</div>

---

## 📦 Install the shop

Two tracks. They do the same thing; pick the one that matches who is reading.

### 🧑 For people

**Prerequisites:** Node.js. Running the harness itself needs no install — the
upstream-documented form is `npx -y @deepseek-ai/dsh web`. Plugin management
goes through `dsh plugin`, which spawns both the `dsh` command and `pnpm` —
install them once with `npm install -g @deepseek-ai/dsh pnpm` and verify with
`dsh --version` and `pnpm --version`.

```sh
# dsh on PATH (global install). Pin the version: pnpm 11 holds back very
# recent releases, so a bare `add dsh-plugin-shop` can hand you an older
# version for a while. This is the current release — refresh it with
# `npm view dsh-plugin-shop version`.
dsh plugin --profile web add dsh-plugin-shop@0.8.3
# or straight through npx, nothing installed:
npx -y @deepseek-ai/dsh plugin --profile web add dsh-plugin-shop@0.8.3
```

Replace `web` with your profile if you use another one. Restart `dsh` once — a newly
added bundle is not applied to a running process — then open

> **Settings → Plugins → Plugin shop**

### 🤖 For agents

Non-interactive. `--profile` is **mandatory**; without it `dsh plugin` exits with
`error: required option '--profile <name>' not specified`.

```sh
# 1. resolve a profile name ($DSH_HOME defaults to ~/.dsh; node_modules is not a profile)
ls -1 "${DSH_HOME:-$HOME/.dsh}/profiles" | grep -v '^node_modules$'

# 2. install — pin the version: it bypasses pnpm's release cooldown and
#    deterministic installs are the point of the agent path
dsh plugin --profile <profile> add dsh-plugin-shop@0.8.3

# 3. verify — a zero exit above only means pnpm resolved the package
dsh plugin --profile <profile> list --depth 0   # dsh-plugin-shop must appear

# 4. restart the profile; a new bundle is not hot-applied
dsh --profile <profile>
```

The same fact as step 3 lives in `$DSH_HOME/profiles/<profile>/package.json` under
`dsh.profile.bundles`, if you would rather read the manifest than parse CLI output.
Per-failure diagnostics are in the
[package README](packages/dsh-plugin-shop/README.md#failure-modes).

## 🖼️ Screenshots

<div align="center">
<img src="docs/images/shelf-light.png" alt="The plugin shop shelf inside dsh Settings" width="860">
</div>

<table>
<tr>
<td width="50%"><img src="docs/images/gate-light.png" alt="Installing an unreviewed plugin requires an explicit acknowledgement"></td>
<td width="50%"><img src="docs/images/shelf-dark.png" alt="The same shelf in the dark theme"></td>
</tr>
<tr>
<td align="center"><sub>Installing an unreviewed plugin requires an explicit acknowledgement</sub></td>
<td align="center"><sub>The same shelf in the dark theme</sub></td>
</tr>
</table>

## ✨ Highlights

- **🌐 Whole-registry harvest** — every npm package keyed `dsh-plugin` or
  `deepseek-harness`, plus every GitHub repository using them as topics. Nothing is
  submitted here; there is no queue to join.
- **🧹 Hard filtering** — every candidate is gated mechanically on every build, and
  one that fails becomes a named rejection carrying one of seventeen recorded reasons,
  in words its author can read. The `plugins` and `filtered` badges above count both
  sides, live.
- **🔌 Dependency check on your machine** — your installation resolves each recorded
  peer name against your own profile, the question dsh's loader asks at mount, so a
  card reads **Incompatible** only when the modules are really missing *here*.
- **🗓️ Daily rebuild** — committed to git, so every change is a reviewable diff. A
  new plugin lands the next morning; a repository that disappears drops out the same
  way.
- **🗂️ Seven categories** — an author who declares `dsh.catalog` picks their own; the
  rest are classified for them.

## 🗺️ How it fits together

**In this repository — the daily build.** Everything here is `registry/`.

```mermaid
flowchart TB
  subgraph HARVEST["1 · Harvest — the whole public registry, every day"]
    direction LR
    NPM(["npm packages<br/>keyword dsh-plugin<br/>keyword deepseek-harness"])
    GH(["GitHub repositories<br/>the same keywords,<br/>used as topics"])
  end

  subgraph GATE["2 · Gate — every candidate must clear all five, on every build"]
    direction LR
    G1["a plugin at all?<br/><br/>a dsh.bundle the<br/>loader can mount"]
    G2["auditable?<br/><br/>a license,<br/>a live repository"]
    G3["installable?<br/><br/>not deprecated on npm ·<br/>repo listings also need<br/>no build scripts and<br/>no workspace: deps"]
    G4["what it claims?<br/><br/>tarball integrity, publish time,<br/>not a near-miss of another name"]
    G5["anything to show?<br/><br/>a valid dsh.catalog,<br/>or an npm description"]
  end

  subgraph SHELVE["3 · Shelve — what the catalog records"]
    direction LR
    CAT["one of 7 categories"]
    PEER["the declared peer NAMES,<br/>never their version ranges"]
  end

  NPM --> G1
  GH --> G1
  G1 -.-> REJ
  G2 -.-> REJ
  G3 -.-> REJ
  G4 -.-> REJ
  G5 -.-> REJ
  REJ[["rejected — one author-readable reason per name"]]
  G5 ==>|"all five clear"| CAT
  PEER ==> PUB[["4 · Publish — content-addressed JSON, committed to git, then GitHub Pages and npm"]]
```

**On your machine — the npm package.** Everything here is `packages/dsh-plugin-shop/`.
The two halves share no code, only the schema.

```mermaid
flowchart LR
  CAT[["the catalog<br/>index.json + plugins.sha256.json"]]
  CAT ==> HOST["5 · Host half<br/>races every origin<br/>verifies sha256 · caches"]
  HOST ==> DEP{"6 · Dependency check<br/>resolve each recorded peer<br/>against YOUR profile"}
  DEP -->|"one or more absent"| BAD["Incompatible<br/>the card names<br/>what is missing"]
  DEP -->|"all resolve"| GOOD["installable"]
  BAD --> CLIENT["Client half — the Settings tab<br/>nine shop/* methods<br/>no network · no filesystem"]
  GOOD --> CLIENT
  CLIENT ==>|"dsh plugin add"| PROF[("your dsh profile")]
```

Two parts are worth naming, because they are the ones people expect to work
differently:

- **The gate rejects; it never silently drops.** Every candidate that fails becomes a
  named rejection with a reason, attached to the build.
- **The dependency check is not a catalog fact.** The build records only the peer
  *names* — never their version ranges, because nearly every dsh plugin declares
  `"*"` and the harness's own prereleases do not satisfy ordinary ranges, so checking
  them would accuse plugins that work. Whether a name resolves is decided by your
  installation, against your profile.

## ✅ What it is

| | |
|---|---|
| **Public and community-run** | Publishing to npm with the `dsh-plugin` or `deepseek-harness` keyword is all it takes to be discovered. Nothing is submitted to this project. |
| **Git-auditable** | Every daily catalog chan