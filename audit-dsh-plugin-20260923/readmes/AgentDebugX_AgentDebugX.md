<div align="center">

<img src="docs/assets/logo.png" alt="AgentDebugX logo" width="360">

# AgentDebugX

**A local-first debugging framework for agentic AI systems: diagnose failures, attribute root causes, recover with evidence, and validate fixes through reruns.**

<a href="https://www.agentdebugx.com"><img src="https://img.shields.io/badge/WEBSITE-208B57?style=for-the-badge&logo=googlechrome&logoColor=white" alt="AgentDebugX website"></a>
<a href="https://docs.agentdebugx.com/"><img src="https://img.shields.io/badge/DOCS-176B45?style=for-the-badge&logo=materialformkdocs&logoColor=white" alt="AgentDebugX documentation"></a>
<a href="https://github.com/AgentDebugX/AgentDebugX"><img src="https://img.shields.io/badge/GITHUB-24292F?style=for-the-badge&logo=github&logoColor=white" alt="AgentDebugX GitHub repository"></a>
<a href="https://youtu.be/ztni6w0o_l8"><img src="https://img.shields.io/badge/DEMO_VIDEO-EA4335?style=for-the-badge&logo=youtube&logoColor=white" alt="AgentDebugX demo video"></a>

[![PyPI](https://img.shields.io/badge/pip-agentdebugx-3775A9)](https://pypi.org/project/agentdebugx/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](pyproject.toml)
[![GitHub Stars](https://img.shields.io/github/stars/AgentDebugX/AgentDebugX?style=flat&logo=github&label=Stars)](https://github.com/AgentDebugX/AgentDebugX/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/AgentDebugX/AgentDebugX?style=flat&logo=github&label=Forks)](https://github.com/AgentDebugX/AgentDebugX/forks)


</div>

---

AgentDebugX turns failed agent runs into structured, auditable debugging
artifacts. It ingests a live or exported trajectory, detects visible failure
signals, attributes them to responsible steps or agents, proposes recovery
actions, and prepares controlled reruns so fixes can be validated instead of
guessed.

The project is designed for researchers and engineers building complex LLM
agents: multi-agent systems, tool-using agents, computer-use agents, benchmark
runners, and local agent development workflows. AgentDebugX is local-first by
default: traces stay on your machine, sharing is opt-in, and recovery proposals
carry explicit policy and approval metadata into the Rerun boundary.

## 📰 News

- 🔌 **2026-08-25** — Released
  [`dsh-agentdebugx` v0.1.0](https://www.npmjs.com/package/dsh-agentdebugx),
  the AgentDebugX plugin for DeepSeek Harness.
- 📄 **2026-07-31** — Released
  [CUADebug](https://arxiv.org/abs/2608.02643), our framework for diagnosing
  and repairing computer-use agent failures.
- 📄 **2026-07-21** — Released the
  [AgentDebugX paper](https://arxiv.org/abs/2607.18754), presenting our
  open-source toolkit for failure observability, attribution, recovery, and
  rerun in LLM agents.
- 📦 **2026-05-16** — Released AgentDebugX on
  [PyPI](https://pypi.org/project/agentdebugx/).
- 📄 **2025-09-29** — Released
  [Where LLM Agents Fail and How They Can Learn From Failures](https://arxiv.org/abs/2509.25370),
  introducing AgentErrorTaxonomy, AgentErrorBench, and AgentDebug.

## System Overview

<p align="center">
  <img src="docs/assets/overview.png" alt="AgentDebugX system overview" width="900">
</p>

AgentDebugX follows the two-stage loop used by the project paper:

```text
Diagnose = Detect -> Attribute -> Recover
Rerun    = checkpoint -> retry directive -> branch execution -> evaluation
```

`Diagnose` explains what failed and why. `Rerun` tests whether the proposed
recovery actually improves the agent behavior.

## Why AgentDebugX

Tracing tools show what happened. AgentDebugX focuses on the debugging step that
usually comes next:

- Which earlier decision caused the visible failure?
- Which agent, tool call, memory read, handoff, or GUI action was responsible?
- What evidence supports that diagnosis?
- What concrete recovery should be tried?
- Did the rerun branch improve the outcome?

The output is a portable diagnostic report that can be inspected in a local UI,
used by a CLI workflow, stored in an Error Hub bundle, or invoked from an
agentic skill.

## Core Capabilities

- **Portable trace schema**: framework-agnostic trajectory, event, finding, and
  diagnostic report models.
- **Ingest adapters**: normalize raw JSON, LangGraph, CrewAI, OpenAI Agents SDK,
  OpenTelemetry, GAIA/Open Deep Research, OSWorld, and other exported traces.
- **Detect**: deterministic analyzers, manifest-backed rule packs, LLM judge
  mode, GUI-aware signals, and taxonomy induction support.
- **Attribute**: heuristic attribution, all-at-once analysis, step-by-step
  localization, binary search, counterfactual attribution, MOE localization,
  and DeepDebug.
- **Recover**: Reflexion, CRITIC, Self-Refine, AutoManual, DeepDebug recovery,
  and saga rollback style strategies.
- **Rerun**: three explicit modes for plan/export only, labeled simulation, or
  observed execution in an application-owned process or persistent HTTP runner.
- **Local inspection UI**: no-build FastAPI dashboard for traces, reports,
  before/after CUA visuals, debugger discussions, saved cases, debug branches,
  and rerun-from-event workflows.
- **Error Hub**: scrubbed, shareable failure bundles for regression tests,
  benchmark corpora, and team debugging memory.
- **Agent integrations**: generate host-runtime assets such as debugging skills
  for external agent tools.

## Install

```bash
pip install agentdebugx
```

Optional extras:

```bash
pip install "agentdebugx[ui]"             # local FastAPI dashboard
pip install "agentdebugx[langgraph]"      # LangGraph adapter
pip install "agentdebugx[crewai]"         # CrewAI adapter
pip install "agentdebugx[openai-agents]"  # OpenAI Agents SDK adapter
pip install "agentdebugx[otel]"           # OpenTelemetry ingest
pip install "agentdebugx[gui]"            # screenshot decoding for GUI RCA
pip install "agentdebugx[all]"            # all optional integrations
```

Computer-use / OSWorld GUI root-cause analysis (`agentdebug.gui`) ships with the
core install and needs no extra. The `gui` extra only adds `pillow`, which the
RCA tools use to decode screenshots. Two heavier layers of the same package sit
behind their own extras: `gui-memory` for the lesson/episodic memory stack, and
`gui-app` for the provider adapters, the batch pipeline (`python -m
agentdebug.gui`) and the Streamlit annotation app.

The package is installed as `agentdebugx` and imported as `agentdebug`:

```python
import agentdebug
```

## Claude Code and Codex Plugins

AgentDebugX ships native plugins for Claude Code and Codex so an agent can
debug its own session. The plugin bundles capture hooks and the AgentDebug
skill, which keeps two boundaries explicit:

- **Capture is automatic** once a project opts in. Sessions are normalized into
  AgentDebugX trajectories locally and silently.
- **Diagnosis is explicit.** Ask AgentDebug in-session and the skill diagnoses
  that exact captured trajectory with `agentdebug run --current --profile deep`.
  Re-running or repairing the agent's work stays a separately authorized step.

Follow the [capture quickstart](CAPTURE_QUICKSTART.md) to install a plugin,
enable project capture, diagnose a session, and turn capture off again.

The plugin bundles live in this repository:

| Plugin | Bundle | Documentation |
| --- | --- | --- |
| Claude Code | `integrations/claude-code/plugins/agentdebug` | [Claude Code plugin](integrations/claude-code/README.md) |
| Codex | `integrations/codex/plugins/agentdebug` | [Codex plugin](integrations/codex/README.md) |

Each plugin's documentation covers its hooks, install scope, the capture
consent step, and lazy session creation. See
[`src/agentdebug/capture/README.md`](src/agentdebug/capture/README.md) for the
stored `.agentdebug/` layout and
[`src/agentdebug/workbench/README.md`](src/agentdebug/workbench/README.md) for
`agentdebug run` profiles and run manifests.

## DeepSeek Harness Plugin

AgentDebugX is also available as 