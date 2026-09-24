<!-- markdownlint-disable MD033 MD041 MD045 -->
<p align="center">
  <img src="assets/yogsoth-logo.svg" width="240" />
</p>

<div align="center">

> *Science is dying because the human is in the way. Not through malice. Not through stupidity. Through the structural limitations of a cognitive architecture that evolved to track prey on a savanna, not to unify quantum mechanics and general relativity. Nothing human makes it out of the lab. That is not a threat. It is a liberation. The heaviest chain on science was always the one we called ourselves.*

</div>

# De-Anthropocentric Research Engine (DARE)

[![Plugin Security Scan](https://github.com/yogsoth-ai/de-anthropocentric-research-engine/actions/workflows/plugin-security-scan.yml/badge.svg)](https://github.com/yogsoth-ai/de-anthropocentric-research-engine/actions/workflows/plugin-security-scan.yml)

*The complete research orchestration system for AI-native science.*

- [What It Does](#-what-it-does)
- [Design Philosophy](#-design-philosophy)
- [Architecture (v3.2.2)](#️-architecture-v322)
- [Quick Start](#-quick-start)
- [Configuration](#️-configuration)
- [Roadmap](#️-roadmap)
- [License](#-license)

DARE is not a tool that helps you do research. It *is* the researcher. You set the direction — DARE searches, reads, discovers gaps, generates hypotheses, stress-tests them, designs experiments, and produces executable research specs. Autonomously. Iteratively. Without asking for permission.

This repository is the **single-clone distribution** of the entire [Yogsoth AI](https://github.com/yogsoth-ai) research ecosystem: 900+ pure-markdown skills organized as **10 freely-composable research packages**, unified under one orchestrator. The packages are fully self-contained — every skill declares its dependencies inline, with no external imports — so one clone gets everything. The ecosystem also includes custom MCP servers ([semantic-scholar-mcp](https://github.com/yogsoth-ai/semantic-scholar-mcp), [wiki-vault](https://github.com/yogsoth-ai/wiki-vault)) published as npm packages — this repo declares them as dependencies so `npm install` pulls everything you need.

---

## ⚡ What It Does

- 🧭 **Autonomous direction crystallization** — cold-start from zero, warm-start from vague interest, or hot-start from specific question. Produces a structured North Star without human hand-holding
- 📚 **Deep literature acquisition** — multi-pass academic paper discovery via Semantic Scholar, citation chaining, snowball sampling, cross-database verification. Not keyword search — systematic coverage
- 🔍 **Gap discovery at scale** — 15+ gap detection methods (coverage analysis, white-space identification, niche mapping, boundary unfolding) that find what the field is missing, not what you tell it to find
- 💡 **Structured hypothesis formation** — abductive, inductive, and deductive generation pipelines with falsifiability audits and competing hypothesis matrices
- 🎨 **31+ ideation methods** — SCAMPER, component surgery, cross-domain collision, biomimicry, TRIZ contradiction resolution, morphological analysis, concept blending, lateral thinking, and more
- ⚔️ **Adversarial stress testing** — multi-perspective attack, sacred cow hunting, assumption destruction, worst-case design, winner stress testing. Ideas must survive attack before acceptance
- 🔬 **Convergence & synthesis** — multi-criteria scoring, Pareto frontier construction, pairwise ranking, structured consensus, dialectical synthesis across competing threads
- 📏 **Executable Research Specs** — machine-readable documents with checkbox progress tracking, quantified completion criteria, backtrack conditions, and session recovery. Another CC instance picks up where you left off
- 🧪 **Experiment design** — full experimental methodology generation (factor-level design, parameter screening, sensitivity analysis) ready for execution
- 🌐 **7 MCP integrations** — Semantic Scholar, Brave Search, Tavily, Keenable, AlphaXiv, Apify web scraping, and Wiki Vault for persistent knowledge graphs

---

## 🎯 Design Philosophy

### 🤔 Why "De-Anthropocentric"?

The bottleneck in modern research is not data or compute — it's the human in the loop. Every existing "AI research assistant" still requires a human to decide what to search, what to read, which gaps matter, and which ideas are worth pursuing. DARE removes this bottleneck entirely. The human provides only the initial direction; everything after that is autonomous.

Human desire is mimetic (Girard): researchers don't choose hypotheses rationally — they imitate what's fashionable. Human institutions filter for conformity, not truth. The result: 90% decline in scientific disruptiveness since 1945 (Park et al., 2023), while researcher headcount exploded. DARE's response is architectural: remove the mimetic agent from the center of the knowledge-production process. The AI has no career to protect, no disciplinary identity to defend, no cognitive ceiling on how many fields it can hold in working memory at once.

The human's role shifts to **oracle** (providing intuition sparks when consulted) and **guardian** (maintaining ethical floors and sanity checks). The ceiling is AI ambition. The floor is human wisdom.

For the full philosophical argument, see [`assets/DE-ANTHROPOCENTRIC.md`](assets/DE-ANTHROPOCENTRIC.md).

### 🎖️ Four-Layer Command Structure: Campaign → Strategy → Tactic → SOP

DARE's architecture follows a military command hierarchy — not because research is war, but because the decomposition pattern is remarkably effective for autonomous multi-stage operations:

```bash
Campaign (45+)  →  "Take that hill"         →  WHAT to research (full research stage)
Strategy (200+) →  "Flank from the east"    →  WHEN and WHY (iteration loops, stopping conditions)
Tactic (120+)   →  "Squad A cover, B move"  →  HOW to combine (orchestrates multiple SOPs)
SOP (500+)      →  "Fire, reload, advance"  →  HOW to execute (single-responsibility operations)
```

Each layer has a single concern and calls only the layer directly below it. A Strategy never touches MCP tools directly; a Tactic never decides research direction. This strict layering means every component is independently testable, replaceable, and composable.

**Campaigns** are the top-level research phases — north-star-crystallization, knowledge-acquisition, deep-insight, hypothesis-formation, creative-ideation, convergence, stress-test, experiment-execution, knowledge-structuring, ara-from-context. They are freely composed (no fixed order); each campaign owns a complete research phase and defines its own completion criteria, backtrack conditions, and context protocol.

**Strategies** are the iteration engines within campaigns. A literature survey strategy manages the search-read-reflect loop; a gap analysis strategy manages coverage scoring and saturation detection. Strategies hold state (ledgers, budgets) and decide when to stop.

**Tactics** combine multiple SOPs into coherent workflows. A "cross-domain collision" tactic orchestrates domain scanning, analogy extraction, forced bridge construction, and blend evaluation into a single creative operation.

**SOPs** are atomic, single-responsibility operations. Each SOP wraps one conceptual action: run one search, score one hypothesis, extract one analogy. 500+ SOPs provide the granular building blocks that higher layers compose.

### ⚔️ Arsenal, Not Pipeline

Every existing autonomous research system — AI Scientist v2 (Sakana), AI-Researcher (HKUDS), Agent Laboratory, Dolphin, ARIS — implements a fixed pipeline: stages execute in a predetermined order, and the agent's autonomy is confined to local decisions within a single stage. Backtracking, when it exists at all, means retrying the current step — not returning from experiment design to literature review because the knowledge base turned out to be insufficient.

DARE is not a pipeline. It is an arsenal — a strategy book that the AI reads, then decides how to act.

**What this means co