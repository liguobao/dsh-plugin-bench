<div align="right">

[English](README.md) · [中文](README-zh.md)

</div>

<h1 align="center">flow-comet</h1>

<p align="center">
  <strong>An automated execution engine that turns AI coding discipline into a verifiable state machine — for the flow-kit 9-stage workflow, built for Claude Code, Codex, and DeepSeek Harness.</strong>
  <br />
  <em>For AI coding workflows — deterministic state machine · protocol-driven · guard-validated · subagent-isolated</em>
</p>

<p align="center">
  <a href="#quick-start"><img src="https://img.shields.io/badge/Quick_Start-4CAF50?style=for-the-badge" alt="Quick Start" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License" /></a>
</p>

<p align="center">
  <a href="https://claude.ai/code"><img src="https://img.shields.io/badge/Claude_Code-D97757?style=flat&logo=claude&logoColor=white" alt="Claude Code" /></a>
  <a href="https://github.com/openai/codex"><img src="https://img.shields.io/badge/Codex-10A37F?style=flat&logoColor=white" alt="Codex" /></a>
  <a href="https://github.com/deepseek-ai/deepseek-harness"><img src="https://img.shields.io/badge/DeepSeek_Harness-4D6BFE?style=flat&logoColor=white" alt="DeepSeek Harness" /></a>
  <a href="https://github.com/rihebty/flow-kit"><img src="https://img.shields.io/badge/flow--kit-4CAF50?style=flat" alt="flow-kit" /></a>
  <a href="https://github.com/rpamis/comet"><img src="https://img.shields.io/badge/comet-4CAF50?style=flat" alt="comet" /></a>
</p>

<p align="center">
  <a href="https://nodejs.org"><img src="https://img.shields.io/badge/Node.js_%E2%89%A518-339933?style=flat&logo=node.js&logoColor=white" alt="Node.js 18+" /></a>
  <a href="https://github.com/baobaolaodie/flow-comet/actions"><img src="https://img.shields.io/github/actions/workflow/status/baobaolaodie/flow-comet/ci.yml?style=flat" alt="CI" /></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-1.5.1-blue.svg" alt="Version" /></a>
</p>

---

## Why

If you use skill-based disciplines like [superpowers](https://github.com/obra/superpowers), [OpenSpec](https://github.com/Fission-AI/OpenSpec), or [GSD](https://github.com/open-gsd/gsd-core), you know the pain: discipline relies on the model's compliance, and progress lives in chat history. flow-comet turns the flow-kit 9-stage process (CHANGE → REQUIREMENT → DESIGN → TASK → DEV → TEST → REVIEW → INTEGRATION → ARCHIVE) from a discipline-dependent manual flow into a **verifiable deterministic state machine**:

- **Automated routing** — scripts manage stage transitions, guard validations, and hook-based write interception
- **Protocol-driven** — the built-in 8-node protocol is the default workflow; custom protocols composed from any installed skill run on the same engine (see [Custom Protocols](docs/PROTOCOL.md))
- **Three defense layers** — physical write interception (hook), coordinator prohibition, and exit takeover detection
- **Subagent-isolated execution** — implementation work is delegated to fresh-context subagents with a verifiable Return Contract
- **File-as-truth recovery** — state is derived from `.specs/` artifacts, so recovery never depends on conversation history

## Quick Start

Requires [Claude Code](https://claude.ai/code), [Codex](https://github.com/openai/codex), or [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (dsh) and [flow-kit](https://github.com/rihebty/flow-kit) in the target project (see [Installation](docs/INSTALLATION.md)).

```bash
# 1. Install the CLI globally (Node.js 18+)
npm install -g flow-comet

# 2. Install flow-comet into your project, from the project directory
cd <your project>
fcomet init
```

The package ships two command names pointing at the same installer — `fcomet` (primary) and `flow-comet` (alias). The `init` token is optional whenever another argument expresses the intent (`fcomet --target <dir>` is equivalent to `fcomet init --target <dir>`), and `--target <dir>` is optional too (default: the current working directory); run with no arguments at all, the command prints its usage and exits non-zero instead of installing. `fcomet --version` prints the version of the installed CLI. Re-running the same command updates an existing install and is idempotent.

On an interactive terminal, the first run prompts for the platform with a direction-key multi-select (arrow keys + space to toggle, Enter to confirm; the default is Claude Code) — `@clack/prompts` is the primary path, with an automatic readline number/comma multi-select fallback when the dependency is not installed, offline, or stdin has no raw mode (`FLOW_COMET_FORCE_READLINE=1` forces the fallback for testing); for a non-interactive pick, add `--platform codex` / `--platform dsh` / `--platform claude-code,dsh` (comma-separated) / `--platform all`.

**Updating**: a global package upgrade does not touch projects that are already installed — re-run `fcomet init` in each project to pick up the new files. And because an npm install has no git history to derive a development marker from, the version marker it writes (`<project>/.claude/skills/flow-comet/INSTALLED_VERSION` for Claude Code, `.agents/skills/…` for Codex, `.dsh/skills/…` for dsh) is the release version shipped inside the package; the `<release>-<n>-g<hash>` form appears only for installs run from a repository clone that has git and tags.

By default the installer targets Claude Code (unchanged behavior). For Codex: `fcomet init --platform codex` — skills install to `.agents/skills/` (auto-discovered), orchestration rules are injected into an `AGENTS.md` managed block, and the write-guard hook intercepts Bash write commands via Codex's PreToolUse (trust the hook on first use: `/hooks`). For DeepSeek Harness: `fcomet init --platform dsh` — skills install to `.dsh/skills/flow-comet` (auto-discovered at rank 100, no restart), orchestration rules are injected into an `AGENTS.md` managed block, and a thin bridge loader is mounted globally in `$DSH_HOME` (see [Installation → Option D](docs/INSTALLATION.md#option-d--deepseek-harness-dsh-platform)). When run on an interactive terminal (TTY) without `--platform`, the installer prompts for the target platform with a multi-select (pre-checked from existing traces — default Claude Code — press Enter to accept); without a TTY (CI/scripts) existing `.claude/` / `.codex/` / `.dsh/` in the target project is detected, falling back to Claude Code.

The installer also ensures `flow-kit` in the target project: when missing it clones the upstream and checks out the locked snapshot `9b5dda7`; an existing upstream clone is only inspected (current HEAD vs the locked snapshot is reported, read-only); a same-name non-clone directory is skipped with guidance; a network failure warns and continues; purge never touches it.

The same installer also runs straight from a repository clone, with no global package — that is the path this repository's own workflow and its distribution to other projects use (Option B in the installation guide):

```bash
cd <flow-comet repo>
node scripts/prepare-env.mjs --target <absolute path to your project>
```

For DeepSeek Harness (dsh), install through the same installer — a dedicated dsh platform descriptor, with no separate plugin bundle:

```bash
cd <your project>
fcomet init --platform dsh
```

This installs the skill tree project-locally at `<project>/.dsh/skills/flow-comet` (dsh auto-discovers skills there at rank 100 without a restart — projects without that directory cannot see the skill, which makes activation naturally project-level), injects the orchestration rules into an `AGENTS.md` managed block (non-destructive merge), and mounts a thin bridge loader globally at `$DSH_HOME/plugins/dsh-flow-comet-bridge.mjs` with a managed block in `$DSH_HOME/cordis.patch.yml` (read-merge-write, preserves existing blocks such as dsh-skin, effective for all profiles). The bridge intercepts write tools via dsh's `tools/pre-execute` event. Interception only ap