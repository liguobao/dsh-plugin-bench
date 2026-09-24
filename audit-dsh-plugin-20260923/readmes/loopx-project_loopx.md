<div align="center">

<h1 align="center">LoopX</h1>

**Give your agents a goal. Keep the work moving.**

The open, local-first control plane for long-horizon agents and personal agent teams.<br>
<sub>Keep goals, decisions and evidence across sessions. Work with Codex, Claude Code, DeepSeek Harness and other supported runtimes.</sub>

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE) [![Release](https://img.shields.io/github/v/release/loopx-project/loopx?filter=v*&display_name=tag)](https://github.com/loopx-project/loopx/releases/latest) [![Discord](https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white)](https://discord.gg/XmGgQyCFZd)

[Get started](#try-loopx) · [Workspace](#meet-the-personal-agent-workspace) · [LHTB results](#lhtb-results) · [Docs](https://loopx-project.github.io/loopx/docs/) · [简体中文](README.zh-CN.md)

**[LHTB](https://zli12321.github.io/LHTB/index.html) · 46 tasks · GPT-5.6 Sol:** LoopX 1.0.3 Heartbeat reaches **0.4948 mean reward** — **+17.3% vs Plain Codex**, **+10.6% vs native Codex Goal**.<br>
<sub><a href="#lhtb-results">Results and pass rates ↓</a></sub>

</div>

---

**More verified work. Less human attention.** LoopX gives agents durable goals,
bounded continuation, peer ownership and recoverable handoffs. Your runtime
provides the model and tools; LoopX keeps track of what to do next, what is
accepted, and when to ask you.

<a id="learn-loopx"></a>

| What you want to do | Start here |
| --- | --- |
| Keep a coding or research agent working across sessions | [Install and connect](#try-loopx) |
| Manage personal projects, schedules and decisions in one place | [Personal Agent Workspace](#meet-the-personal-agent-workspace) |
| Let agents collaborate and deliver verifiable results | [Agent collaboration guide](docs/product/use-cases/cross-runtime/README.md) |

## Meet the Personal Agent Workspace

Keep long-horizon goals in one local-first workspace. Goals, attention,
conversations, tasks, files, schedules, and recovery stay durable across days,
restarts, and harnesses. Reopen a project, inspect the previous turn’s state
and evidence, and continue the next permitted action.

<a href="docs/assets/personal-workspace/loopx-dashboard-launch.mp4">
  <img src="docs/assets/personal-workspace/workspace-1.0.webp" alt="LoopX Workspace: owner decisions, Agent tasks, scheduled watches and completed work" width="960">
</a>

LoopX 1.0 brings these long-horizon control states into the Personal Workspace. It gives you one place to:

- see what needs you, what is running, what is being watched, and what is
  scheduled or stopped;
- configure Goal capabilities, distinguish machine defaults from Goal overrides,
  and preview changes before applying them;
- steer a live turn, queue a message, or use the async inbox from a connected
  Lark conversation with explicit Goal/Agent/session routing;
- inspect deliverable files, periodic reports, and their supporting evidence;
- continue across Codex, Claude Code, direct-model, and other registered Agent
  sessions without losing Goal state or evidence;
- review protected changes through typed preview, explicit confirmation, and
  receipts while LoopX state—not the browser—remains authoritative.

For Manager group conversations, LoopX keeps message visibility separate from
Turn authority; see the bilingual [Lark Manager context and authority
contract](docs/reference/protocols/lark-manager-context-authority-v0.md).

```bash
loopx dashboard
```

`loopx dashboard` is the supported browser/PWA launch path. You can also download
native desktop previews from the [1.0 release](https://github.com/loopx-project/loopx/releases/tag/v1.0.0);
they reuse the same loopback services and Goal state. Apple Silicon macOS supports
signed App updates that pair the shell with its bundled runtime, plus repair and
recovery. Python 3.11+ is required; the App is ad-hoc signed, not notarized.
Windows preview installers currently use manual updates and a separately installed CLI.
[Desktop installation, updates, and source development](apps/desktop/loopx-control-plane/README.md).

<details>
<summary>Capability settings and reproducible workspace scenarios</summary>

<img src="docs/assets/personal-workspace/capability-1.0.webp" alt="Real Workspace recording: configure child-task capacity and allowed responsibility domains" width="960">

From a source checkout, run `python -m demo.workspace serve` to explore a community
event, a home-energy comparison, and a neighborhood website release. Each has four
work roles, 18 tasks, two decisions, and two watches. The screenshot above comes
from this reproducible workspace. [Scenarios and replay instructions](demo/workspace/README.md).

</details>

[Watch the full 32-second walkthrough](docs/assets/personal-workspace/loopx-dashboard-launch.mp4)
· [Read the workspace guide](docs/guides/personal-workspace-user-guide.md)
· [Try the five-minute tour](docs/guides/personal-workspace-trial-guide.md)

<a id="how-it-works"></a>

## Why LoopX

An agent can finish a task in one session. Long-running work is harder:
objectives change, owner decisions appear, evidence goes stale, agents hand work
to peers, and a scheduler can keep spending after no useful transition remains.
Chat memory and a timer are not enough to govern that.

LoopX keeps the durable control state in one compact layer:

```text
objective / issue / project
   │
   ▼
LoopX state: objective + gates + todos + scope + evidence + quota
   │
   ├─ human judgment needed? ── yes ─▶ ask a concrete question and wait
   │
   ├─ safe fallback available? ──────▶ run one bounded agent slice
   │
   ▼
Codex / Claude Code / Cursor / shell agent executes one turn
   │
   ▼
write evidence + handoff + next todo ─▶ quota decides the next tick
```

Agent runtimes execute the work. LoopX governs the state that lets engineering,
research, discovery, and operations loops continue across runs. It is not
another agent framework or a provider-specific orchestration runtime.

![LoopX control-plane board](docs/assets/control-plane-board.svg)

A useful mental model is an
**[agent-native Kanban for long-running work](docs/development/control-plane-course/00-concept-primer.md)**.
Cards carry identity, authority, evidence, and continuation. Moves are validated
operators such as claim, gate, monitor, and writeback. The board is a
projection; LoopX state remains the source of truth.

Registered agents are peers. Claims, leases, task boundaries, capabilities, and
typed continuation decide who acts next; no durable leader identity is
required.

LoopX is useful when you run:

- multi-day engineering, research, benchmark, or experiment objectives;
- issue and PR loops that must preserve scope, evidence, and review state;
- recurring heartbeat or monitor work;
- projects with owner, safety, publication, or private-data gates;
- peer-agent teams where ownership, leases, and handoff matter;
- creator, research, or operations workflows whose progress must remain
  legible to a non-engineering operator.

LoopX is not an autonomous production controller. Dangerous permissions,
publishing, production writes, and final ownership stay with the human.

### Personal Agents, Teams, and Self-Improving Workflows

[Meta Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)
and [Grok Bot](https://x.ai/news/introducing-grok-bot) make persistent personal
agents and delegated work a familiar product idea. LoopX approaches that space
as an open, provider-neutral control plane for agents you already run—not as a
hosted replacement for either product.

- **Personal agent:** use the shipped Workspace and connected Lark surfaces to
  inspect goals, steer work and resolve decisions. The
  [persistent steward and semantic handoff RFC](docs/architecture/rfcs/capable-manager-semantic-handoff-v0.md)
  extends this toward one capable front door for a team; the complete journey
  remains under qualification.
- **Agent team:** s