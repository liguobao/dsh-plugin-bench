<p align="center">
  <img src="./docs/images/dsh-crew-logo.png" alt="DSH Crew" width="120" />
</p>

<h1 align="center">DSH Crew</h1>

<p align="center">
  <strong>A <a href="https://github.com/deepseek-ai/deepseek-harness">DeepSeek Harness</a> plugin: dispatch work to DSH agents from Claude Code / Codex / Antigravity / Grok, without giving up the host's native subagent UI.</strong><br />
  <sub>Native Progress UI &bull; Tier Policy &amp; Escalation &bull; Dispatch Guardrails &bull; Jobs Board &bull; In-Host DSH Sessions &bull; Vision &amp; Image Gen (Native-First) &bull; One-Click Install</sub>
</p>

<p align="center">
  <sub>npm: <code>@zseven-w/dsh-crew</code> &middot; Current plugin release: <code>0.1.0-rc.10</code> &middot; Tested with DSH <code>0.1.1-rc.1</code></sub>
</p>

<p align="center">
  <a href="./README.md"><b>English</b></a> &middot; <a href="./README.zh.md">简体中文</a> &middot; <a href="./README.zh-TW.md">繁體中文</a> &middot; <a href="./README.ja.md">日本語</a> &middot; <a href="./README.ko.md">한국어</a> &middot; <a href="./README.fr.md">Français</a> &middot; <a href="./README.es.md">Español</a> &middot; <a href="./README.de.md">Deutsch</a> &middot; <a href="./README.pt.md">Português</a> &middot; <a href="./README.ru.md">Русский</a> &middot; <a href="./README.hi.md">हिन्दी</a> &middot; <a href="./README.tr.md">Türkçe</a> &middot; <a href="./README.th.md">ไทย</a> &middot; <a href="./README.vi.md">Tiếng Việt</a> &middot; <a href="./README.id.md">Bahasa Indonesia</a>
</p>

<p align="center">
  <a href="https://github.com/ZSeven-W/dsh-crew/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ZSeven-W/dsh-crew?color=64748b" alt="License" /></a>
</p>

<br />

<p align="center">
  <img src="./docs/images/dsh-crew-overview.png" alt="DSH Crew — settings page" width="100%" />
</p>
<p align="center"><sub>The DSH Crew settings page — host integrations, dispatch policy, execution and the multimodal bridge</sub></p>

## Why DSH Crew

DSH Crew is a plugin for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (DSH) — an open-source agent harness. It makes DSH agents dispatchable from Claude Code, Codex, Antigravity and Grok: the orchestrator keeps its own model, the work runs on a real DSH agent with that harness's tools, sandbox, presets and session history, and the host still shows it as a native subagent with live progress.

What runs the work is a DSH agent, not a bare model call. Tiers (`flash` / `pro`) select how much capability that agent gets from the harness's configured roster — DeepSeek V4 Flash and V4 Pro today — so a change of model in DSH needs no change here.

<table>
<tr>
<td width="50%">

### 🧵 Native Progress UI

Workers appear as regular subagents in Claude Code / Codex / Antigravity / Grok — dispatch count, running step, tool calls and token usage all show up in the host's own task panel, plus a claude-hud statusline segment: `⚙dsh 1▶pro 2m14s 21.7k/606 ✓3`.

</td>
<td width="50%">

### 🎚️ Tier Policy and Escalation

`flash` for mechanical work, `pro` for reasoning, `effort` from `off` to `max`. `tier_policy` can clamp every dispatch to one tier at the tool layer, and `escalate_on_failure` retries a failed flash run once on pro — based on evidence, not on guessing difficulty up front.

</td>
</tr>
<tr>
<td width="50%">

### 🏛️ In-Host DSH Sessions

With the bundle installed in a DSH profile, each worker is a first-class DSH session: visible in the Web UI, grouped by working directory, mounted with the Agent preset you choose per tier. Without DSH running, dispatch falls back to a standalone DSH runtime, so CI and headless environments still work.

</td>
<td width="50%">

### 👁️ Vision and Image Generation

DSH's models are text-only. `describe_image` now prefers DeepSeek's own VL model (`deepseek-v4-flash-vision-exp`) whenever a key is available, then falls back to the CLIs you already have — Claude, Codex, Grok, Antigravity — or any OpenAI-compatible API you configure. `generate_image` borrows the same CLIs' brush. Pasted images stay visible in the conversation and reach the model as text.

</td>
</tr>
<tr>
<td width="50%">

### 🛡️ Dispatch Guardrails

Every dispatch is checked before anything spawns. Worker→worker nesting is capped at origin-chain depth 3 and cycles are refused; a second worker on a workspace another job already holds is refused with the holder's info — never silently queued. Refusals are readable errors: wait or re-scope, don't bypass.

</td>
<td width="50%">

### 📋 Jobs Board

The DSH Crew panel doubles as a jobs board: every worker job — running or finished — is listed with tier, effort, live progress and tokens, held workspaces show their holders, and a job that vanishes mid-flight (e.g. a hub restart) is surfaced as an orphan ghost instead of disappearing silently.

</td>
</tr>
<tr>
<td width="50%">

### 🔌 Custom Providers

Bring your own endpoint (Base URL + API key + models) or a local command template. Each provider has a connectivity test that checks reachability and auth, then makes one real vision call so you find out now, not mid-task.

</td>
<td width="50%">

### 📦 One-Click Install

The settings page installs and updates the Claude Code plugin, the Codex role files and the Antigravity / Grok agents, skills and commands for you — marketplace registration, permission allowlist, HUD wiring, absolute paths rendered for this machine — and restores them just as easily. Every settings file is backed up first.

</td>
</tr>
</table>

## How it works

```
Claude Code / Codex / Antigravity / Grok (orchestrator, keeps its own model)
  └─ ds-flash / ds-pro  ← native subagent shell (progress shows in the host's task UI)
       └─ MCP: dsh_run_worker(tier, effort, cwd, worker=)
            ├─ worker="agy"/"grok" → that external CLI runs the task (explicit opt-in)
            ├─ hub reachable → session inside DSH (visible in the Web UI, grouped by cwd)
            └─ otherwise     → dsh-jsonrpc-agent runtime (worker.cordis.yml)
                 └─ DeepSeek V4 Flash / Pro (DSH SDK, event stream → progress and token stats)
```

## One run, two views

Dispatch fans out. Below, eighteen workers translate this README in parallel: the host counts them as its own subagents, while the harness runs them as real sessions.

<p align="center">
  <img src="./docs/images/dsh-crew-host.png" alt="Claude Code" width="100%" />
</p>
<p align="center"><sub>Claude Code sees dsh-crew workers as native subagents, with a statusline segment tracking running tiers, elapsed time and tokens.</sub></p>

<p align="center">
  <img src="./docs/images/dsh-crew-jobs.png" alt="DSH Crew" width="100%" />
</p>
<p align="center"><sub>The DSH Crew panel sees the same run from the harness side: which host dispatched each job, its tier and effort, live progress and token usage.</sub></p>

<p align="center"><sub>The panel is also the jobs board: running and finished jobs stay listed with tier, progress and tokens, held workspaces name their holders, and a job that vanishes mid-flight (a hub restart) surfaces as an orphan ghost instead of disappearing silently.</sub></p>

## Install

Install into a DSH profile from npm:

```bash
dsh plugin --profile web add @zseven-w/dsh-crew@latest
dsh web
```

Or, for local development straight from the source tree:

```bash
dsh plugin --profile web add link:/path/to/dsh-crew
dsh web
```

The `link:` protocol symlinks the profile dependency to this repository, so rebuilds are visible immediately.

### Configure DeepSeek credentials (standalone only)

In hub mode — the installation above — workers run inside the DSH instance and use the DeepSeek credentials it is already configured with. Nothing else to set up.

Only the standalone fallback needs a key of its own: dispatching from a host with no DSH instance running launches a worker runtime as a separate process. Obtain an API key from [platform.deepseek.com](https://platform.deepseek.com) and write it to `~/.config/dsh-crew/.env`:

```
DEEPSEEK_API