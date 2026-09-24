<div align="center">

# AItelier

**Structured-but-dynamic subagent workflows for AI agents — your agent delegates work to deterministic, fully-audited pipelines it can generate, run, and edit over MCP.**

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.12%2B-3776AB)
[![Engine: SkillFlow](https://img.shields.io/badge/engine-SkillFlow%20(MIT)-F59E0B)](https://github.com/linxuhao/SkillFlow)

</div>

AItelier makes multi-agent AI pipelines **deterministic and fully auditable** — define a pipeline (or have your agent generate one), run it, and inspect *why* it did everything it did. The whole surface is exposed over **MCP**, so any MCP-speaking agent can use AItelier as its workflow engine: delegate bulk work to cheap, deterministic pipelines and only decide at checkpoints (see [Use AItelier from another agent](#use-aitelier-from-another-agent-mcp)). Under it all is an open engine ([SkillFlow](https://github.com/linxuhao/SkillFlow), MIT, on PyPI as `skillflow-py`) plus a flagship software-delivery pipeline; the broader no-code **workflow platform** is on the [roadmap](#roadmap).

## Persistent project state, separate from workflow execution

AItelier also provides a **State DAG** for long-lived goals, revisioned acceptance
contracts, dependencies and evidence. SkillFlow continues to own workflow steps,
loops, retries and checkpoints; the driver chooses a ready goal and a workflow.
**A completed workflow produces a candidate, not a verified product capability.**

The MCP/internal-driver tools `state_graph_help`, `state_graph_read` and
`state_graph_write` expose the same typed contracts as `/api/state`. State data
reads require writer authorization. Existing DPE pipelines and task/project UI
remain compatible; legacy tasks are imported only explicitly and never inherit
verified status. See [architecture, usage, trust boundaries and rollout](docs/state-graph.md)
and the [offline real-engine demonstration](examples/state_graph_demo.py).
The authenticated `send_director_message`, `list_director_messages`,
`acknowledge_director_message`, and `resolve_director_message` State actions provide
project inboxes with durable delivery events; REST exposes the same closed v2
contract at `/api/state/director-messages/<action>`. The v2 lifecycle distinguishes
explicit-inbox `transient` deliveries from `standing` guidance that remains in a
bounded, redacted PostCompact recovery projection until resolved. Existing v1 rows
migrate as transient without losing their message, delivery, event or idempotency audit.
The [State Project frontend and migration preparation guide](docs/state-project-ui-migration.md)
covers project DAG browsing, exact-run graph versions, protected historical references
and held shadow migration rehearsal.
The [project-first dashboard guide](docs/project-dashboard-ux.md) covers the default State DAG workspace,
separate Runs/Pipelines navigation, readable node badges and actual run history.

### Wait for state changes and onboard another agent

Use `state_graph_read(action="wait_for_state_change", arguments={"project_id":
"my-project", "after": 0, "timeout_seconds": 30})` and persist the returned
`next_after` cursor. Matching durable events return immediately; unchanged state
waits without repeated model-driven queries. Workflow stops and pauses are
reconciled into State observations, with bounded recovery for missed notifications.
A timeout does not stop a worker, and completion never verifies a goal.

Agents can load the MCP prompt `state_graph_driver`, the resource
`aitelier://state/driver-guide`, or `driver_guide` from `state_graph_help`.
Each State project also has a revisioned `permanent`/`temporary` driver note:
`get_driver_note`, bounded/redacted `search_driver_note_history`,
`driver_note_history`, and CAS-protected
`update_driver_note` let different directors manage projects in parallel without
sharing note revisions or event cursors. `wait_for_state_change` keeps its
single-project compatibility defaults and adds `filter_mode="any"` plus
`note_after_revision` for OR-style handoff waits.
See the [agent driver guide](docs/state-agent-driver.md) for external evidence,
cursor scope, ownership and handoff rules.

The [2.0 release checklist](docs/release-2.0.md) separates implemented features
from distribution checks still required before a public release.

### Use State DAG without workflows

Your own director, subagents, CI or proof-checking harness can register an
external attempt, submit a scoped artifact/report and per-criterion evidence,
and verify a node without creating a SkillFlow Run. Workflow and external
attempts share the same acceptance and invalidation rules. External completion
is still only a candidate.

A dedicated authenticated, headless State HTTP/MCP server starts with
`python -m api.state_only --db /absolute/private/state.sqlite` and a configured
`AITELIER_STATE_TOKEN`; it does not import or start SkillFlow, a scheduler,
workspace manager or model registry. The package's install dependencies are not
yet split into a separate minimal wheel. See [the integration/standalone guide](docs/state-external-harness.md)
and [the real own-harness example](examples/external_harness_demo.py).

Design authors can use [lightweight design search and impact](docs/design-search-impact.md)
to find exact-version candidates, record direct conflicts and inspect affected
bindings. These read-only helpers reuse State revisions/baselines; they do not
introduce a solver, vector database or automatic acceptance.

## Why AItelier

Most "AI agent" tooling is built for demos, not trust. The tools that build software or automate a workflow for you are non-deterministic black boxes: you can't reproduce a run, audit *why* the agent did what it did, or insert a human approval where it matters. That's exactly the wall that stops agents from being deployed in anything serious — regulated industries, enterprise, anywhere "it usually works" isn't good enough.

AItelier is built on the opposite premise — that an autonomous pipeline should be **trustworthy by construction**:

- **Deterministic execution rules** — workflow graphs are traversed by the engine, not control flow improvised by an LLM. Their conditional outcomes may differ and their retry paths may contain cycles; they are not necessarily DAGs. Loops, gates, retries, and recovery are the engine's job. The separate project-state dependency graph is acyclic.
- **Minimal LLM surface (least privilege)** — each agent sees only the context it declares, and the [SkillFlow](https://github.com/linxuhao/SkillFlow) engine generates a constrained **write tool per declared output** (and gates reads to declared context) — so an agent *cannot* read or write a file outside its contract. Concretely in the software pipeline: the Researcher can only search the web; every other role can write only its own declared output (a design doc, a plan, a review verdict, or the project README) — and *only* the Implementer's outputs are code. The model makes the judgment calls; the framework and its generated tools do everything deterministic — *brain to brain, tools to tools*. It's also why cheap models suffice: small, focused, role-scoped context.
- **Fully traceable** — every run keeps an append-only audit trace that is *never deleted*: each step, prompt, model response, and tool call. "Why did this run do that?" is one query, not forensic archaeology.
- **Human-in-the-loop** — approval/reject checkpoints are first-class between stages; review and send work back with feedback at any point.
- **Adversarial quality** — every step is produced by a Green (Maker) agent and reviewed by a Red (Checker) agent before it advances.
- **Config-agnostic** — a pipeline can be *anything*. Nothing about the engine is hardcoded to one workflow; SkillFlow can even generate a new pipeline from a plain-language description.

**Where this sits.** Classic workflow engines are structured but *static*