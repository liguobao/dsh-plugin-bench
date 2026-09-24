# causal-memory

> **An agent memory system with a causal core — and the only one that models inhibition.**
>
> Facts, temporal state, and `decision → outcome` causal edges on one SQLite store,
> powered by a hippocampus-style engine: typed spreading activation (excitatory
> *and* inhibitory), Hebbian co-occurrence reinforcement, Q-value dynamics, and
> immutable SWR consolidation. Agents recall *what* happened, *when* it was true,
> *why* it worked — and *what would happen if* they acted differently.

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Status: v0.9.3](https://img.shields.io/badge/status-v0.9.3--alpha-orange.svg)](#status)
[![Tests: 368](https://img.shields.io/badge/tests-368-brightgreen.svg)](#build--test)
[![Release: v0.9.3](https://img.shields.io/badge/release-v0.9.3-blue.svg)](https://github.com/JingxuanC/causal-memory/releases)
[![Hermes plugin](https://img.shields.io/badge/hermes-plugin-blue.svg)](hermes-plugin/)
[![DSH plugin](https://img.shields.io/badge/deepseek--harness-plugin-blue.svg)](dsh-plugin/)

**English** · [简体中文](README.zh-CN.md)

---

## Why

Every agent forgets *why* it made past decisions after a few context compactions.
It re-fixes the same bug the same wrong way, re-debates the same architecture
choice, relearns the same lesson.

This happens because **causal information is the most fragile type under text
compaction**. Real-LLM benchmark (grok-build's production compaction prompt):

| Compactions (k) | Textual recall | Causal-table recall |
|---|---|---|
| 1 | 100% | 100% |
| 2 | 85% | 100% |
| 3 | 55% | 100% |
| 5 | **45%** | **100%** |

The causal table survives because it lives **outside the agent's context window** —
compaction cannot touch it.

---

## Demo

**30-second single scene** — the agent is about to `git push --no-verify`;
`intervention_query` fires a DANGER chain citing the lesson it recorded last
time ("production login failed for 40 minutes; emergency rollback"):

<!-- GitHub's CSP (media-src) only allows GitHub-hosted media, so an
     external <video> never plays on the repo page. An animated GIF goes
     through the camo image proxy and plays inline. Click for the mp4. -->
[![30-second danger-warning demo](docs/demo/causal-memory-danger-30s.gif)](docs/demo/causal-memory-danger-30s.mp4)

[Download video](docs/demo/causal-memory-danger-30s.mp4) ·
[DANGER-scene screenshot](docs/demo/demo30_danger.png) ·
Regenerate: `scripts/capture_demo30.py` → `scripts/render_demo30.py`

A 21-second hands-on demo (real memory store, no mocks): pre-action warning
(`intervention_query` → DANGER chain) → experience recall (`search_causal`)
→ counterfactual comparison (`counterfactual_query`) → write loop
(`record_decision` → immediately searchable).

[![21-second demo](docs/demo/causal-memory-demo.gif)](docs/demo/causal-memory-demo.mp4)

[Download video](docs/demo/causal-memory-demo.mp4) ·
[Warning-scene screenshot](docs/demo/demo_intervention.png) ·
[Brand card](docs/demo/demo_card.png) ·
Regenerate: `scripts/render_demo.py`

---

## Benchmarks

### CausalEval — the causal memory benchmark (primary)

Most agent-memory benchmarks (LoCoMo, LongMemEval, Memora) test **fact recall**
("what is the user's preference"). causal-memory's differentiators — typed
causal edges, inhibition, intervention prediction, cross-task transfer — are
invisible on those suites. **CausalEval** measures them.

**Design: the causal graph is the answer key.** Typed DAGs are generated
deterministically; conversations are narrated from the graph; gold answers are
derived from graph structure — zero hand annotation, zero ambiguity.

**CausalEval v13 (soft supersession) — 140 questions, 20 graphs** (same LLM,
same judge; v12 baseline was 70q/10 graphs; mem0 comparison ran on the 70q
protocol):

| Capability | causal-memory | v12 (70q) | mem0 (70q) | What it tests |
|---|---|---|---|---|
| **C7 Update** | **100%** | 50% | 80% | Supersede old belief after falsification (soft `superseded_by` annotation) |
| C3 Counterfactual | **95%** | 90% | 80% | Choosing between alternatives with known outcomes |
| C2 Intervention | **75%** | 70% | 40% | Forward prediction: "if X again, what happens?" |
| C4 Inhibition | **80%** | 90% | 50% | Distinguishing root-cause fix vs blast-radius limiter (`prevented` edges) |
| C1 Attribution | 85% | 90% | 90% | Backward causal chain → root cause |
| C5 Temporal-causal | 90% | 100% | 90% | Ordering on a causal chain |
| C6 Lesson transfer | 20% | 20% | 30% | Cross-task analogy via meta edges (open limitation) |
| **Overall** | **78%** | 81% | 65% | |

**Key result: C7 update 50% → 100% (+50pp, 20/20 questions) and it holds at
doubled sample size.** Soft supersession annotates superseded edges
(`superseded_by`) instead of hiding them — the falsification signal reaches
the answer model while the old lesson stays retrievable for counterfactuals
(C3 unharmed at 95%). The C6 gap (20% vs mem0 30%) is the remaining open
limitation; C1/C4/C5 dips vs v12 are within re-distillation variance and
new-graph difficulty (v12 and v13 do not share a distilled corpus).

### Fact-recall benchmarks (not our strong suit)

On traditional fact-recall suites, causal-memory performs competitively but
**does not beat mem0** — this is expected, because fact recall is mem0's
specialty and not where causal-memory adds value.

| Benchmark | causal-memory | mem0 | Note |
|---|---|---|---|
| LoCoMo (strict judge) | 79.1% | 91.6% | mem0's home turf |
| LongMemEval-S (full pipeline, deepseek-chat) | **76.4%** @ 11.5K tok/q | 94.4% @ 6.8K tok/q (official) · 73.8% (ind. repro) | single-model stack vs platform stack; see docs/benchmarks/longmemeval.md |
| Memora MPA | 67.4% | 71.8% | −4.4pp |
| Compaction survival | 100% | 45% | External table = immune to compaction |
| Agent repeat-mistake | 33% | 67% | −34pp on trap-world |

### Capability tests (322 across the workspace)

These test capabilities that **no fact store (mem0, Zep, Letta) can offer**.

| Capability | What it proves | Tests |
|---|---|---|
| **Prevented-edge warning** | `prevented` edge spreads −0.3 activation (GABA analogue) | 2 |
| **Trace-cause attribution** | Backward CSR traversal finds root cause | 2 |
| **Multi-hop causal chain** | Forward K-hop spreading reaches 2-3 hop outcomes | 2 |
| **Inhibitory filtering** | Prevented outcomes appear as negative, not false positives | 1 |
| **Intervention comparison** | Same outcome has +0.9 for "skip tests" and −0.3 for "add tests" | 4 |
| **SWR consolidation** | LTP strengthens replayed edges, LTD weakens unvisited, GC forgets dormant | 5 |
| **Q-value dynamics** | Good decisions rank higher; Bellman propagates to parents | 3 |
| **Novelty entropy** | Diverse experience triggers consolidation; uniform does not | 3 |
| **Meta-edge mining** | Cross-session pattern discovery (similar_to / repeated) | 3 |
| **Hebbian co-occurrence** | Repeated co-activation strengthens connection | 3 |

---

## What makes it different

| Capability | causal-memory | mem0 | Zep | Letta | HeLa-Mem |
|---|---|---|---|---|---|
| Typed causal semantics (caused/enabled/prevented) | ✅ | ❌ | ❌ | ❌ | ❌ |
| **prevented negative spread (inhibitory)** | ✅ | ❌ | ❌ | ❌ | ❌ |
| Hebbian co-occurrence edges (excitatory) | ✅ | ❌ | ❌ | ❌ | ✅ |
| Immutable consolidation (delta + clone) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Q-value dynamic utility | ✅ | ❌ | ❌ | ❌ | ❌ |
| Forward simulation (intervention_query) | ✅ | ❌ | ❌ | ❌ | ❌ |
| SWR offline consolidation (LTP/LTD/GC) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Novelty-entropy consolidation trigger | ✅ | ❌ | ❌ | ❌ | ❌ |
| Meta-edge cross-session pattern mining | ✅ | ❌ | ❌ | ❌ | ❌ |
| Compaction survival evidence | ✅ +20.8pp | ❌ | ❌ | ❌ | ❌ |
| One graph unifying all memory types | ✅ | ❌ | ⚠️ | ❌ | ⚠️ |
| Write-time gatekeeping (raw → session_logs) | ✅ | ✅ | ❌ | ❌ | ❌ |
| Local ONNX embedding (offline) | ✅ | ✅ | ❌ | ❌ | ❌ |

**Core innovation: the excitatory/inhibitory duality.** HeLa-Mem (ACL 2026) builds
the excit