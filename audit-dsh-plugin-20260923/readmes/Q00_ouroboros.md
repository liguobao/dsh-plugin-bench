<!-- mcp-name: io.github.Q00/ouroboros -->
<p align="right">
  <strong>English</strong> | <a href="./README.ko.md">한국어</a> | <a href="./README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <br/>
  ◯ ─────────── ◯
  <br/><br/>
  <img src="./docs/images/ouroboros.png" width="420" alt="Ouroboros">
  <br/><br/>
  <strong>O U R O B O R O S</strong>
  <br/><br/>
  ◯ ─────────── ◯
  <br/>
</p>


<p align="center">
  <strong>It gets smarter on its own. We just hold the line.</strong>
  <br/>
  <sub>Skip the prompt engineering. The agent runs, fails, and gets smarter every generation. The grading command and expected result never make it into the success contract we hand it.</sub>
  <br/>
  <sub>The <strong>Agent OS</strong> for replayable AI coding workflows</sub>
</p>

<p align="center">
  <a href="https://github.com/Q00/ouroboros"><img src="https://img.shields.io/github/stars/Q00/ouroboros?color=yellow&logo=github&label=stars" alt="GitHub stars"></a>
  <a href="https://pypi.org/project/ouroboros-ai/"><img src="https://img.shields.io/pypi/v/ouroboros-ai?color=blue" alt="PyPI"></a>
  <a href="https://github.com/Q00/ouroboros/actions/workflows/test.yml"><img src="https://img.shields.io/github/actions/workflow/status/Q00/ouroboros/test.yml?branch=main" alt="Tests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>
  <a href="https://github.com/sponsors/Q00"><img src="https://img.shields.io/github/sponsors/Q00?logo=githubsponsors&color=EA4AAA&label=sponsors" alt="GitHub Sponsors"></a>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/26008?utm_source=repository-badge&utm_medium=badge&utm_campaign=badge-repository-26008" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/repositories/26008" alt="Q00%2Fouroboros | Trendshift" width="250" height="55"/></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="#why-ouroboros">Why</a> ·
  <a href="#what-you-get">Results</a> ·
  <a href="#the-loop">How It Works</a> ·
  <a href="#commands">Commands</a> ·
  <a href="#from-wonder-to-ontology">Philosophy</a> ·
  <a href="https://ouroboros.page/learn/en/">Guide</a>
</p>

```bash
# macOS / Linux / WSL 2
curl -fsSL https://raw.githubusercontent.com/Q00/ouroboros/main/scripts/install.sh | OUROBOROS_INSTALL_REF=readme-hero bash
```

```powershell
# Windows (PowerShell) — no Python needed; installs Git and uv for you
irm https://raw.githubusercontent.com/Q00/ouroboros/main/scripts/install.ps1 | iex
```

<p align="center"><sub>One command installs it. Then run <code>ooo setup</code> once inside your coding agent — details in <a href="#quick-start">Quick Start</a>.</sub></p>

<p align="center"><sub><b>Separate runs, separate hosts. Different tasks on purpose — the engine is what is shared, not the prompt</b></sub></p>

<table align="center">
<tr>
<td align="center" width="33%"><img src="./docs/images/ooo-interview.gif" width="300" alt="Terminal recording of the ouroboros CLI interview reporting an ambiguity score"><br><sub><b>Terminal CLI</b> — a task-management CLI: <code>ouroboros init start</code> asking about ordering and scope, then reporting an ambiguity score</sub></td>
<td align="center" width="33%"><img src="./docs/images/host-codex.gif" width="300" alt="Screen recording of the ChatGPT app calling Ouroboros as an integration"><br><sub><b>ChatGPT (Codex)</b> — called as an integration, on a video-publishing harness: the interview, its advisory lanes, and the ambiguity ledger</sub></td>
<td align="center" width="33%"><img src="./docs/images/host-claude.gif" width="300" alt="Screen recording of Claude Code running six Ouroboros interview advisory lanes in parallel"><br><sub><b>Claude Code</b> — a YouTube automation task, with the six advisory lanes running in parallel before the interview submits</sub></td>
</tr>
<tr>
<td align="center" width="33%"><img src="./docs/images/host-hermes.gif" width="300" alt="Screen recording of a Discord bot running the Ouroboros interview and reporting a final ambiguity of 0.15"><br><sub><b>Hermes (Discord)</b> — a kart-racing game, run as a chat bot, ending at <code>Final ambiguity: 0.15</code></sub></td>
<td align="center" width="33%"><img src="./docs/images/host-dsh.gif" width="300" alt="Screen recording of DeepSeek Harness calling the Ouroboros interview tool and submitting advisory fan-out results"><br><sub><b>DeepSeek Harness</b> — an OSS-trend outreach script, driven from a dsh chat: <code>mcp__ouroboros__ouroboros_interview</code> turn by turn, fan-out results submitted between rounds</sub></td>
<td align="center" width="33%"><img src="./docs/images/host-kiro.gif" width="300" alt="10x screen recording of Kiro CLI running an Ouroboros interview"><br><sub><b>Kiro</b> — the Kiro CLI running the Ouroboros interview flow, turning a vague request into a structured, testable Seed</sub></td>
</tr>
</table>

**Turn a vague idea into a verified, working codebase -- across Claude Code, Codex CLI, OpenCode, Hermes, Gemini, Kiro, Copilot, Pi, OMP, Zcode, Goose, GJC, Antigravity, and Grok.**

Ouroboros is an **Agent OS** for AI coding: a local-first runtime layer that
turns non-deterministic agent work into a replayable, observable, policy-bound
execution contract. It replaces ad-hoc prompting with a structured
specification-first workflow: interview, crystallize, execute, evaluate,
evolve.

---

## The Ouroboros Agent OS Stack

Like any OS, Ouroboros is split into a stable **OS layer** of primitives, an
**application layer** of domain workflows, and a **shell** that humans actually
sit in front of. Three repos, one stack:

| Layer | Repo | Role | What it gives you |
| :--- | :--- | :--- | :--- |
| **Shell** (terminal client) | [`Ouro-labs/ourocode`](https://github.com/Ouro-labs/ourocode) | Native terminal UI for running `ooo` workflows across Claude / Codex / Gemini CLIs in one session | TUI, wonderTool decision pickers, MCP pane state, command discovery |
| **Apps** (domain workflows) | [`Ouro-labs/ouroboros-plugins`](https://github.com/Ouro-labs/ouroboros-plugins) | UserLevel plugin contract — composes core primitives into installable domain programs (PR ops, Jira sync, incidents, releases) | Plugin manifest, scoped permissions, audit/provenance, reference plugins |
| **OS** (this repo) | [`Q00/ouroboros`](https://github.com/Q00/ouroboros) | Agent OS core — Seed, Ledger, Runtime, MCP, safety boundaries | `ooo` commands, spec-first workflow engine, multi-runtime adapter |

**How they connect:**

```
  ourocode  ──►  ooo / ouroboros-plugins  ──►  ouroboros core (Seed · Ledger · MCP · Runtime)
   shell             user-level apps                        kernel
```

- The **kernel** (`ouroboros`) owns the contract: every action becomes a
  Seed-bound, ledger-recorded, replayable event — regardless of which LLM
  executes it.
- **Plugins** (`ouroboros-plugins`) declare scoped capabilities against that
  contract, so domain workflows (review a PR, triage a Linear ticket, run a
  release) stay auditable and policy-bound instead of being one-off prompts.
- **Ourocode** is the terminal shell: it surfaces MCP state, interview
  questions, and wonderTool decisions as first-class TUI elements, so you can
  drive the OS without leaving the keyboard or switching between CLIs.

Use `ouroboros` alone with any supported CLI, layer plugins on for domain
workflows, or install `ourocode` when you want a unified terminal cockpit.

> **Disclaimer.** The Ouroboros project and community are **not affiliated with
> any cryptocurrency, token, memecoin, or trading community** — including, but
> not limited to, any "ouroboros" tickers on pump.fun or other launchpads. This
> is an open-source developer tool. We do not issue, endorse, or hold any
> coins. Any token claiming association with this project is unauthorized.

> **Naming note.** A separate, unaffiliated open-source project also uses the
> name "Ouroboros" — Anton Razzhigaev's self-mod