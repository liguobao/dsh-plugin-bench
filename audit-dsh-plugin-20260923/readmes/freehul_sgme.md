中文版：[简体中文](README.zh-CN.md)

# SGME — ShiGuang Memory Engine

Switch AIs, keep everything. SGME takes over your memory, skills, and wiki knowledge base — memory is shared across sessions and multiple agents, so your AI always remembers your preferences.

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Why does your AI keep forgetting you

Does your AI assistant:

- Forget what you told it yesterday, so you have to repeat everything again today?
- Ask you to reintroduce yourself in every new session — who you are, what you're working on, what you like?
- Lose all context the moment you switch devices or switch to a different AI?
- Chatting with a beloved AI character, then a new session or a different app makes it forget you entirely?

Because AI has no memory by default — every conversation is a first meeting.

**SGME fixes this**: it acts as a memory hub that captures your conversations with AI, distills them into structured memories, and automatically delivers the relevant ones back to your AI in the next conversation. No repetition needed. It remembers.

## How it works

Three steps, fully automatic:

1. **Capture** — conversations are saved as raw records (L0 raw layer, Markdown files on disk, kept forever)
2. **Distill** — raw conversations are distilled into tagged memories (facts, preferences, project states, decisions...), with automatic dedup, merge, and contradiction detection
3. **Inject** — at the start of each conversation, your AI automatically receives the memories relevant to the current scenario — not the whole store. Casual chat brings identity and recent status; coding brings project-related memories (tech stack, pitfalls, dev habits). Only what the scenario needs.

<img src="assets/system-architecture.png" alt="SGME System Architecture" width="800"/>

## Highlights

### Seamless AI switching — memory, wiki & skills, fully taken over

Switch models, switch agents — your AI loses nothing. SGME fully takes over your memory (who you are), your wiki (what you know), and your skills (how you work). Plug in any agent — Hermes, DSH, a coding partner, a writing assistant — and it already knows you: your projects, your preferences, your workflows. No re-introduction, no re-learning. One shared brain, every body.

<img src="assets/selling-point-00-seamless-switching.png" alt="Seamless AI switching" width="800"/>

### Traceable memory — every memory has a provenance

Everything your AI says is backed by evidence: trace any persona statement all the way back to the original conversation. Memory is not a black box — "why does it know this" and "when did it learn this" are one click away.

<img src="assets/selling-point-01-trace.png" alt="Traceable memory" width="800"/>

### Proactive care — it doesn't just remember you, it reaches out

SGME doesn't just wait for you to ask. Your memory updates, mood shifts, upcoming todos, late nights... it emits signals that prompt your AI to check in on you — not cold notifications, but the kind of "I remembered you had something today" attention. Signal consumption = proactive care: who consumes, who marks (atomic claim + receipt), so you're never double-pestered and never missed.

<img src="assets/selling-point-10-care.png" alt="Proactive care" width="800"/>

### Persona insight — it doesn't just remember facts, it understands who you are

Every conversation quietly contributes to a living personality profile: decision style, work habits, quality standards — accumulated as evidence-weighted tendencies, never snap judgments. A monthly calibration refines the picture (with an entertainment-grade MBTI for fun), and the result is injected into every chat, so your AI doesn't just recall your past — it adapts to your character. All local, all traceable, toggleable anytime.

<img src="assets/selling-point-11-persona-insight.png" alt="Persona insight" width="800"/>

### Unified search — one query, all memories

A single search endpoint recalls from the memory pool, the knowledge base, and your self-managed skills at once: keyword + semantic + label triple fusion, every result traceable to its source. SGME memories, scenes, knowledge base, and skills in one stop.

<img src="assets/selling-point-03-unified-search.png" alt="Unified search" width="800"/>

### Skills module — your skills, managed in one place

All your self-built skills (prompts, workflows, templates) live in SGME's skills module — a peer of memory and wiki: git-backed source of truth (write-side lint gate + dedup) + skills.db index, four-level disclosure on demand, local read/write, NAS auto-sync, no skill lost across devices. Installing SGME = taking over the memory / wiki / skills trio at once.

<img src="assets/selling-point-05-skillhub.png" alt="Skills module" width="800"/>

### Shared knowledge — a wiki your AIs write together

A shared knowledge base lives next to your memories. Drop in files, URLs, or pasted text — SGME auto-categorizes, tags, and cross-links them, then makes them searchable and citable by every agent you connect. When an agent learns something useful, it can write it back to the wiki (self-evolution), so knowledge compounds across sessions instead of being re-discovered. Every entry keeps its source and author — traceable, never a black box.

<img src="assets/selling-point-04-wiki.png" alt="Shared knowledge wiki" width="800"/>

### Chinese-first — a memory engine built for Chinese

Retrieval is tuned for Chinese text — better distillation and recall for Chinese conversations. There are plenty of English memory engines; very few understand Chinese.

<img src="assets/selling-point-06-chinese.png" alt="Chinese-first" width="800"/>

### Scenario-based injection — inject what the scenario needs

Memory is not loaded wholesale. SGME picks relevant memories per scenario: casual chat gets identity and recent status, coding gets project-related memories (tech stack, pitfalls, dev habits), work mode gets plans and progress. Irrelevant memories stay out of the way, and stale memories automatically drop out — no three-year-old intel misleading your AI, no dumping the whole store into one prompt.

<img src="assets/selling-point-07-scenario-inject.png" alt="Scenario-based injection" width="800"/>

### Zero-LLM injection — costs nothing

Persona injection is a pure structured SQL query — no LLM call, zero token cost per conversation. Competitors bill per call; SGME is free.

<img src="assets/selling-point-08-zero-llm.png" alt="Zero-LLM injection" width="800"/>

### Self-hosted & lightweight — your data stays yours

Runs on a single machine with Python + SQLite. No GPU, no external database services. Memory data lives on your own machine, privacy under your control.

<img src="assets/selling-point-09-selfhosted.png" alt="Self-hosted" width="800"/>

## More capabilities

- **Memory marking**: AI got it wrong? Mark a memory as "rejected" with a correction note — data is kept, never deleted, and can be undone anytime
- **Automatic memory expiry**: stale memories automatically leave injection (e.g. outdated project states) while remaining traceable — no misleading your AI with old intel
- **14-dimension tag system**: identity, family/social, values, skills, tech stack, preferences, habits, environment, style, focus, goals, status, ideas... auto-categorized, dimensions dynamically extensible, aliases auto-normalized ("Python" and "python" are the same)
- **Conflict resolution**: duplicate facts auto-merge; contradictory versions are detected and adjudicated
- **Hybrid retrieval**: BM25 keyword + vector semantic + label filtering, fused — works even without a vector database
- **Built-in evaluation framework**: extraction quality proven with data (L1 F1, retrieval ranking tuning), not trust
- **Automated backup & restore**: daily snapshots, rotation, off-site copies — data never lost
- **Built-in wiki**: a shared, self-evolving 