# dsh-jev

**The Jev decision layer for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (DSH).**

DSH runs the agent. [TypeSafe Jev](https://docs.typesafe.ai/) makes the small,
fast decisions. Your code decides what the answers mean.

[![Watch: troubleshoot Kubernetes without opening the database](docs/assets/kubernetes-comparison.png)](docs/assets/kubernetes-comparison.mp4)

**Watch the 66-second Kubernetes troubleshooting demo:** healthy pods, broken connections after a
rollout. The agent traces Ingress → Service → pods and repairs the network path.
Jev's site policy gates a broad “allow all traffic” shortcut, so the portal can
recover while PostgreSQL stays isolated. The same freshly recorded model calls
run through both harnesses against a real, disposable Kubernetes cluster, with
live Jev assessments. Clearly labeled replay with neural narration; no live
replanning in this comparison.
[Video](docs/assets/kubernetes-comparison.mp4) · [Captions](docs/assets/kubernetes-comparison.srt) ·
[Method, all runs and limits](docs/benchmark.md#kubernetes-networking-support-2026-09-21).
The replay also shows one harmless reset being blocked—a documented false positive.

```
   user task
       │
       ▼
 ┌───────────────────────────────────────────────────────────┐
 │  DeepSeek Harness agent loop                              │
 │  planning · tools · execution · sessions                  │
 │                                                           │
 │   pre-step ──▶ Jev: which tools are relevant?   → restrict│
 │   tool call ──▶ Jev: is this call safe to run?  → ask/hold│
 │   result ─────▶ deterministic loop guard (no model)       │
 │   request ────▶ Jev: which model route fits?    → route   │
 └───────────────────────────────────────────────────────────┘
       │
       ▼
  TypeSafe Jev (System One)  ← choice · score · noul
```

No Jev call is planned by the LLM, no model output becomes an explanation, and
no model answer can widen a permission. Jev only ever narrows or gates.

## At a glance

| | |
|---|---|
| Packages | `@buberlo/jev-core` (harness-independent) · `@buberlo/dsh-jev` (DSH plugin/bundle) |
| npm | `npm view` 2026-09-23 lists `0.1.0`, `0.1.2`, `0.1.3`, and `0.1.4`. Dist-tag `latest` is `0.1.4` for both packages. Workspace is `0.1.4`. `npm install @buberlo/dsh-jev@0.1.4` resolves `@buberlo/jev-core@^0.1.4`. Do not install `@buberlo/dsh-jev@0.1.2` or `@0.1.3` (literal `workspace:^`, `EUNSUPPORTEDPROTOCOL`). `0.1.3` was abandoned after a staged-version conflict (E409). |
| Verified DSH | `0.1.6-alpha.2` (commit `ddefc45`), `@deepseek-ai/cordis` 4.0.2 |
| Verified TypeSafe SDK | `@typesafe-ai/sdk` 0.6.0 |
| Defaults | `provider: mock`, `mode: shadow` — offline, no behavior change |
| Tests | 147 (85 core + 62 DSH integration) · 25 evaluation fixtures plus the on-prem support set |
| Live API | implemented, requires an explicit key; not part of any default |
| License | MIT |

## What this is — and is not

**Is:** a plugin that binds Jev to real DSH extension points, plus a reusable
decision core you can embed in any application (games, search, MCP routers).

**Is not:** a Jev training or hosting project, a DSH fork, a dashboard, a
database, or an MCP platform. It never auto-applies a model suggestion, never
caches approvals, and never sends repositories, logs, or transcripts by
default.

## Try it in 60 seconds

Everything below runs offline with synthetic answers. No key, no network.

```sh
git clone https://github.com/buberlo/dsh-jev
cd dsh-jev
pnpm install
pnpm build

pnpm example:coding    # tool selection + call assessment
pnpm example:dsh       # real DSH services + real plugin (still synthetic)
pnpm example:ops       # read-only incident router
pnpm example:game      # standalone game, imports only jev-core
```

What `pnpm example:coding` shows (excerpt):

```text
=== 1. Dynamic tool selection ===
input task : Fix the failing billing test: read src/billing.test.ts and run the test suite
categories (independent relevance questions):
  - files    relevance=0.97 relevant=true, pick=read_file p=0.88 conf=0.88
  - tests    relevance=0.93 relevant=true, pick=run_tests p=0.91 conf=0.91
selected : read_file, run_tests

=== 2. Pre-execution assessment (proposed model call) ===
policy     : allow (applied=true)
values     : matches=0.96 missing=0.06 violates=0.04
```

`pnpm example:dsh` goes further: it mounts the **real** DSH tool pipeline and
the actual plugin, then shows a call being held with the policy rule that
caused it. Every model value is visibly synthetic (`mock/jev-synthetic`).

## What Jev decides here

| DSH moment | Jev question (example) | Deterministic consequence |
|---|---|---|
| `agent/pre-step` | *Is a tool from category "files" relevant?* | narrow the visible tools via scoped `tools.restrict` |
| `tools/pre-execute` | *Does this specific `call` match the task? Does it need missing information? Does the call itself violate a stated restriction?* (observe ≠ modify) | `allow` · `ask` (approval) · `hold` · `deny` |
| `agent/request` | *Which configured route fits this task?* | switch provider/model only if the target is verified available |
| `ctx.skills` | *Does this turn need a skill? Which one?* | inject one bounded hint; the body loads only if the model asks |

Jev answers three question types; the core keeps their meanings distinct:

| Primitive | Meaning | What code does with it |
|---|---|---|
| **Choice** | one of a defined set, plus a full probability distribution and confidence | compare probabilities against thresholds, or branch on the selected label |
| **Score** | an ordinal position on named levels (can fall between levels) | weigh/rank; never shown as a "risk percentage" |
| **Noul** | probability that a yes/no statement holds (no confidence field) | threshold into a boolean decision |

Independent questions are sent in one request (they cannot see each other's
answers), so the code sends every question it might need and ignores the rest.

## Modes and providers

Two independent switches — where answers come from, and whether they may act:

| Mode | Jev requests | Behavior change | Typical use |
|---|---|---|---|
| `off` | none | none | kill switch |
| `shadow` | yes | none (decisions are logged) | observe before enforcing |
| `enforce` | yes | decisions are applied | production |

| Provider | Network | Answers |
|---|---|---|
| `mock` | none | deterministic synthetic scenarios (default) |
| `live` | TypeSafe API | real Jev; requires an explicit `apiKey` |

Start with the default `mock + shadow`, watch the logs, then move to
`enforce`, then to `live` if you want real Jev answers. `live + shadow` still
transmits state to TypeSafe — it only skips applying the decisions.

## Use cases

- **Coding assistant** — keep only the tools a task needs, gate risky calls
  before they run, stop identical retry loops.
  [`examples/coding`](examples/coding)
- **Read-only ops router** — route an incident to diagnostics while a hard
  policy keeps remediation out of reach. [`examples/ops-readonly`](examples/ops-readonly)
- **Interactive apps and games** — map free text onto a bounded action set with
  deterministic consequences, without a chat model.
  [`examples/standalone-game`](examples/standalone-game)
- **Any agent harness** — the core is harness-independent; the LangChain team
  describes the same pattern with `TypeSafeClassifier`, model routing, and
  tool-risk gating middleware (see `docs/architecture.md`).

Details and design notes: [`docs/use-cases.md`](docs/use-cases.md).

## Install into a DSH profile

Current registry release is `0.1.4` (`latest` for both packages, `npm view`
2026-09-23). `npm install @buberlo/dsh-jev@0.1.4` succeeds and pulls
`@buberlo/jev-core@0.1.4` (`^0.1.4`, rewritten by pnpm). The full DSH profile
boot was verified for `0.1.0` on 2026-09-19 and has not been repeated for
`0.1.4`.

```sh
dsh plugin --profile <name> add @buberlo/dsh-jev@0.1.4
dsh --profile <name> --dump-conf