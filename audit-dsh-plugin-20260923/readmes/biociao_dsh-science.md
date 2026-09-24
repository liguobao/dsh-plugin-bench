# dsh-science 
[![npm version](https://img.shields.io/npm/v/dsh-science)](https://www.npmjs.com/package/dsh-science)
[![license](https://img.shields.io/npm/l/dsh-science)](LICENSE)
[![node](https://img.shields.io/badge/node-%3E%3D18-339933)](package.json)
[![dsh-plugin topic](https://img.shields.io/badge/GitHub-topic%3A%20dsh--plugin-181717)](https://github.com/topics/dsh-plugin)
---
<img width="865" height="795" alt="Screenshot 2026-08-14 at 19 49 06" src="https://github.com/user-attachments/assets/b6ef210f-6081-42b7-91fd-484f554c955e" />

**A Claude Science–style research workbench for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) — for genomics / pathogens / human health / bioinformatics projects.**

> One-liner: **dsh-science** — Claude Science-style research workbench for DSH: ReAct research-loop engine (research_* tools), versioned artifacts with provenance (artifact_* tools), an SSH remote-compute engine (remote_* tools, mirroring Claude Science's Computer / Remote compute clusters), and 11 science skills for genomics / pathogens / bioinformatics.

- **ReAct research loop engine** — `research_init` / `research_state` / `research_hypothesis` / `research_experiment` / `research_findings` / `research_phase` / `research_review` / `research_report`, persisted in a `research-manifest.json` state machine (Question → Hypothesis → Experiment → Observe → Analyze → Conclude → Next Question).
- **Versioned artifacts with provenance** — `artifact_save` / `artifact_list` / `artifact_show` / `artifact_diff` / `artifact_verify` / `artifact_deprecate` / `artifact_reproduce`: every result saved as `artifacts/<name>/v<N>/` with per-file SHA-256, `artifact.json` provenance (command / inputs / environment / envFile) and an append-only `provenance.md`.
- **Remote compute engine (SSH / HPC clusters)** — 16 tools: `remote_host_add` / `remote_host_probe` / `remote_host_notes` / `remote_run` / `remote_status` / `remote_logs` / `remote_pull` / `remote_cancel` / `remote_exec` etc. Connect lab workstations or HPC clusters via `~/.ssh/config` aliases (nothing installed on the host, zero third-party deps). Long bioinformatics jobs run as detached processes on workstations or via `sbatch` on SLURM — they survive connection loss; submission asks for approval by default; `remote_status` batch-monitors and auto-transitions state (running → succeeded/failed/killed); `remote_pull` fetches outputs back (files over the size threshold stay on the host with their paths recorded).
- **Remote Hosts config UI (bundle/profile-level)** — a Settings > 远程主机 page (the analog of Claude Science's Settings > Compute > SSH hosts): list/add/probe/edit/remove hosts, plus each project's access allowlist and job summary. Host-side REST API (`webServer` route `/dsh-science/remote-hosts/*`, `engines/remote-hosts-ui.mjs`) + client bundle (`client/remote-hosts-ui/`, built by `scripts/build-client-bundle.mjs`) sharing the same data files as the remote engine. Requires a web-process restart to activate (see [docs/remote-hosts-ui.md](docs/remote-hosts-ui.md)).
- **Model Tier router (tiered, cross-provider)** — via the companion bundle [`dsh-model-tier`](packages/dsh-model-tier/): within one session, automatically routes auxiliary requests (session titles, compaction summaries) and subagent/background tasks to a **light tier**, keeps the main conversation on the **default tier**, and escalates complex work (deep subagent chains, very long inputs) to a **strong tier** — each tier may point at a **different provider** (e.g. strong GLM-5.3 / default deepseek-v4-flash / light minimax-M3), mirroring Claude Code's Opus/Sonnet/Haiku strategy. Built on DSH's native `agent/request` + `llm/stream` waterfall extension points; a no-op when the tier's provider is unregistered. Installed automatically with dsh-science, but also standalone-installable into any profile (`dsh plugin add dsh-model-tier`).
- **11 science skills** — research-loop, science-project-setup, artifact-provenance, scientific-reviewer, literature-connector, parallel-delegation, manuscript-writing, bioinformatics-toolkit, conda-environments, data-inventory, remote-compute.

All in-repo engine plugins are **zero-dependency** (Node built-ins + the system OpenSSH binaries, sharing `engines/core.mjs`) and register plain cordis tools; the companion `dsh-model-tier` router is likewise zero-dependency. Installable either as a profile bundle (`dsh plugin add`) or as an agent preset (`科学模式`).

### v0.2.0: Model Tier router (new, companion bundle)

Mirrors Claude Code's Opus/Sonnet/Haiku tiering: within one session, auxiliary requests (`purpose ∈ {session-title, compaction}`) and subagents (`session.meta.origin === 'subagent'`) are routed to the **light tier**; the main conversation keeps its own per-session model selection (never overridden); deep subagent chains (`delegationDepth ≥ subagentDepthStrong`) and very long inputs (`escalateOnChars`, opt-in) escalate to the **strong tier**. An optional LLM pre-classifier (`routing.classify`) grades each user prompt / subtask dispatch by complexity (light / default / strong) before routing. Each tier is `{provider, model, reasoningEffort?}` and may span providers.

Ships as the standalone bundle **[`dsh-model-tier`](packages/dsh-model-tier/)** — dsh-science depends on it and mounts it in its `cordis.patch.yml`, but it can equally be installed on its own into any profile (`dsh plugin add dsh-model-tier`):

```yaml
- id: model-tier
  name: dsh-model-tier
  config:
    tiers:
      strong: { provider: zai-coding-cn, model: glm-5.3 }
      default: { provider: deepseek-official, model: deepseek-v4-flash }
      light: { provider: opencode-go, model: minimax-m2.7 }
    routing:
      auxiliary: [session-title, compaction]
      subagents: light
      subagentDepthStrong: 3
```

- **Host plane** — mounted in the profile bundle (`cordis.patch.yml`), not the agent preset, so it applies to every session and subagent on the profile.
- **Safety rails** — no `tiers` configured → inert no-op; target provider unregistered → no routing; a failing light-tier call automatically falls back to the original route (auxiliary features never break).
- **Verified** — `node packages/dsh-model-tier/test/model-tier.test.mjs` (zero-dependency unit matrix) + `bash packages/dsh-model-tier/scripts/test-model-tier.sh` (E2E: light tier pointed at a local mock LLM; asserts the title request is actually routed).

### v0.2.0: Remote compute (new)

Mirrors Claude Science's **Remote compute clusters / Computer** capability, following its documented mechanism:

- **Host registration + read-only probe** — `remote_host_add` takes a `~/.ssh/config` alias (or `user@host`; ProxyJump etc. handled by OpenSSH), with optional port/identityFile overrides; probing records CPUs, memory, GPUs, CUDA driver, conda/module/Apptainer presence, scratch dirs, `sbatch` and SLURM partitions (`remote_host_probe` re-runs it). Host registry: `$DSH_HOME/remotes/hosts.json`.
- **Job submission** — `remote_run` copies script + inputs into `<scratch>/<jobId>/` (default `~/dsh-scratch`); workstations run it as a detached `nohup+setsid` process (connection-loss safe), SLURM clusters get `sbatch` (with `--time`); default job timeout 30 min; submission asks for approval by default (the analog of Claude Science's "Run this job on <host>?" card).
- **Monitoring & reaction** — `remote_status` batch-probes (ps / squeue+sacct / done+exitcode markers) and auto-transitions state; `remote_logs` tails logs; `remote_pull` fetches outputs and writes `pulled-manifest.json` (files > 100 MB stay on the host with recorded paths); `remote_cancel` kills (process group / scancel). Job registry: `<project>/.dsh/remotes/jobs.json`, persists across sessions.
- **Host Details document** — `remote_host_notes` maintains per-host notes (environment activation, partitions/account, conventions) that the model reads before submitting jobs.
- **Per-project access allowlist (allowed servers, is