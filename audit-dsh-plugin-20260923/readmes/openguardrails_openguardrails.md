<div align="center">

# OpenGuardrails

**The vendor-neutral protocol for AI agent safety & security — and the neutral benchmark that ranks the vendors.**

Integrate safety & security once, enforce it across every agent and LLM — instead of wiring every vendor to every tool by hand.

Apache-2.0 · [openguardrails.com](https://openguardrails.com)

</div>

---

This monorepo is the home of the **OpenGuardrails (OGR) specification and its
reference integrations**. The specification is the normative contract every
integration and detector speaks; the integrations, benchmark, examples, skill,
and website live alongside it so changes can be reviewed and tested together.

OGR is **not a guardrail product**: it defines the wire and referees the
leaderboard. Vendors compete on detection quality behind a common plug; users
get one way to configure and compose safety & security across every agent they
run.

- We define the **wire** — the layer model, events, verdicts, composition,
  taxonomy.
- We **referee** the benchmark.
- We do **not** build detection capability — vendors compete behind the contract.

## The layer model: OGR beside OSI

**This is the protocol's foundational concept.** OGR is to agent traffic what
the layered network model is to packets — and it is built the way a firewall
is: an integration sees **one event at a time**, the way a firewall sees one
IP packet, and the runtime reassembles everything above it and reads
everything below it out of the payload.

| # | OGR layer | Network analogue | One unit is |
|---|---|---|---|
| **L6** | **Session** | — *(this domain's own layer)* | one conversation |
| **L5** | **Turn** | — *(this domain's own layer)* | one instruction → quiescence |
| **L4** | **Step** | transport | one model call: request + response, paired by `step_id` |
| **L3** | **Event** | **network — the packet** | one `GuardEvent`, half a step — **the only layer on the wire** |
| **L2** | **Call** | link | one tool call the model asked for |
| **L1** | **Exec** | physical | one real execution on a machine — *named by the model, not carried by the contract* |

Like a packet, an event is a **header** — `kind` (`step/request` \|
`step/response`), `step_id`, and the identity four-tuple `agent_id ·
agent_type · agent_workspace · agent_user` (OGR's answer to the firewall's
5-tuple) — plus a **payload**: the raw provider body. Everything above L3 is
**derived server-side** (sessions by conversation-prefix chaining, turns by
instruction boundaries and idle timeout — a firewall does not ask packets
which connection they belong to); everything below is parsed from the payload
(calls) or inferred (exec: no sensor observes it, and the gap between what a
call claims and what an exec does is precisely what agent security is about).

Two honest notes on the analogy. OGR follows the *pragmatic* TCP/IP cut — a
layer earns its place with its own unit, mechanism, and question — not OSI's
seven: above transport, networking has only "application", but agent traffic
*is* a dialogue with stable structure, so Turn and Session are this domain's
own layers, defined here rather than mapped onto OSI's vestigial
session/presentation layers. And the **agent is an endpoint, not a layer** —
it persists with zero traffic, sessions belong to it the way TCP connections
belong to a host, and it is addressed by the four-tuple every event carries.
Beside the stack sits the entity axis every firewall has: tenant (the API
key), **workspace** = security zone (one zone, one policy set), **agent** =
host, discovered from traffic into an inventory.

Each event gets a **verdict at the moment the integration can still refuse
it** — the request before the model sees it, the response before the agent
acts on it:

```
  your own agent · harness plugins        gateway integrations
  (two POSTs at the loop's seams)         (an LLM proxy: Higress, …)
        │                                       │
        │   raw provider bodies + step_id       │
        ▼                                       ▼
   ┌───────────────────────────────────────────────┐
   │  OGR core contract                            │
   │  GuardEvent · Verdict ·                       │
   │  composition · taxonomy                       │
   └───────────────────────────────────────────────┘
                       ▲
                       │
                detector plugins
               (config rules OR model/classifier)
```

### The same six layers, in five other vocabularies

Agent harnesses already have words for this traffic. They line up:

| # | OGR | Network (OSI / TCP-IP) | OTel GenAI | OpenAI Agents SDK | Claude Agent SDK | LangGraph |
|---|---|---|---|---|---|---|
| **L6** | **Session** — one conversation | *no OSI layer* — the firewall's session table, idle aging | `gen_ai.conversation.id` *(no span)* | `Session` / `SQLiteSession` id; a trace's `group_id` | the session — `session_id`, `resume`, `fork` | the **thread** — `thread_id` + checkpointer |
| **L5** | **Turn** — one instruction → quiescence | *no OSI layer* — a flow's FIN / RST / timeout | `invoke_agent` span | one `Runner.run()` — one trace | one `query()` prompt, up to its `ResultMessage` | one `invoke()` / `stream()` on the graph |
| **L4** | **Step** — one model call | **transport** (OSI L4) | the inference span, `chat {model}` | `generation_span` / `response_span` — *their* "turn" | one loop round trip — *their* "turn" (`max_turns`) | one model-node execution (`before_model` → `after_model`) |
| **L3** | **Event** — half a step, **the wire unit** | **network** (OSI L3) — the packet | that span's start / end | that span's start / end | `AssistantMessage` out; tool results ride the **next** `UserMessage` | the two moments around the chat model's `invoke()` |
| **L2** | **Call** — one tool call | **data link** (OSI L2) | `execute_tool` span | `function_span` | a `tool_use` block; `PreToolUse` is its gate | a `ToolNode` call; `wrap_tool_call` is its gate |
| **L1** | **Exec** — one real execution | **physical** (OSI L1) | — | — | what `Bash` / `Edit` actually did on the host | what the tool function actually did |
| — | **Agent** *(entity, off the stack)* | host / endpoint | `gen_ai.agent.id` / `.name` | the `Agent` object (`agent_span`); a handoff switches it | the agent, and each subagent | the compiled graph |
| — | **Workspace** · **Tenant** | security zone · administrative boundary | *(`deployment.environment.name`)* | — | — | — |

**The numbers line up through L4 on purpose.** Exec/call/event/step sit on
physical/link/network/transport, and the packet is L3 in both columns. Above
transport the columns part: networking has only "application", because network
applications share no structure — agent traffic *is* a dialogue with stable
structure, so **turn and session are this domain's own L5 and L6**, not OSI's
session and presentation layers (the two practice discarded).

⚠️ **"Turn" means this stack's STEP in two of the three SDKs.** In both the
OpenAI Agents SDK and the Claude Agent SDK a *turn* is one iteration of the
agent loop — one model call plus the tool runs it triggers — and that is what
`max_turns` counts. An OGR **turn** is the user-instruction episode that
*contains* those iterations: one `Runner.run()`, one `query()` prompt, one
graph `invoke()`. Same word, one layer apart. (The OpenAI Agents SDK
documentation uses both senses: `max_turns` counts loop iterations, while "a
single logical turn in a chat conversation" is one `Runner.run()` — an OGR
turn.)

The full mapping — including what to send as `session_hint`, why an SDK *hook*
(`PreToolUse`, `wrap_tool_call`) is an enforcement point where a tracing span
is not, and how a handoff moves the entity axis rather than the stack — is in
[Overview § The layer model in harness vocabularies](specification/overview.md#the-layer-model-in-harness-vocabularies-non-normative).

Normative text: [Overview § The layer model](specification/overview.md).

## Integrate your agent in five minutes

T