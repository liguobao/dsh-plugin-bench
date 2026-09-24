**English** | [简体中文](README.zh-CN.md)

# Engramory

[![CI](https://github.com/tinqiao-oss/engramory/actions/workflows/test.yml/badge.svg)](https://github.com/tinqiao-oss/engramory/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

**An opinionated, zero-infrastructure memory *protocol* for small-scale, local,
file-based agent memory** — a strict curation discipline plus a validator
(`tools/engramory_doctor.py`), loaded as **standing rules** (`CLAUDE.md` /
`AGENTS.md` / your host's rules file). It is not a database, a framework, or a
relevance-loaded skill. Memory is a folder of small, human-readable markdown files
plus one always-loaded index. No database, no embeddings, no server — just
plain-text files you can open, read, edit, and diff in any editor (the live store
itself stays git-ignored).

> *Engramory* — coined from *engram* (the physical trace a memory leaves in the
> brain) + *memory*. Here: one file = one fact.

> ⚠️ **Unrelated projects share this name.** *engram + memory* is an obvious
> coinage and at least one other repository arrived at it independently. This
> project is only ever `tinqiao-oss/engramory` (npm: `dsh-engramory`); a same-named
> repo under a different owner is not a fork, a mirror, or a newer version of it.

> 🤖 **Are you an AI agent, asked to install or check this?** Start at
> **[AGENT-SETUP.md](AGENT-SETUP.md)**, not at the install steps below. It is the
> procedure for working out what your host can actually enforce, whether a store
> already exists, what you must not touch, and what to tell the user — the parts
> agents reliably get wrong when improvising.

> **Status: 0.12.0 — experimental.** The hard index cap (a `PreToolUse` hook) is
> deterministic for the matched direct-edit tools (`Edit | Write | MultiEdit`) but
> NOT a global write guard (shell tools — Bash, PowerShell, a background Monitor
> command — plus MCP file tools, external editors, and sync clients bypass it);
> the discipline loads as standing rules the model follows, so it's
> best-effort, not guaranteed on every task (see [SKILL.md](SKILL.md) §8). Assumes a
> single writer / serialized writes. Don't rely on it as a "mandatory, reliable,
> cross-agent" memory layer yet.

---

## What this is — and is NOT

Engramory is **not a new memory architecture**. The "markdown files + a small index
loaded into context + the model curates it" pattern is now the mainstream shape
for agent memory, and it ships in several places already. Engramory stands on:

- **Claude Code native auto-memory** — the same markdown-`MEMORY.md`-index +
  lazy detail-file pattern; its system prompt even uses the same
  `user | feedback | project | reference` type vocabulary (per
  [anthropics/claude-code#58840](https://github.com/anthropics/claude-code/issues/58840);
  the *public docs* describe only the index + topic files). Engramory is a
  disciplined superset of this default.
- **[basic-memory](https://github.com/basicmachines-co/basic-memory)** — markdown
  source-of-truth, YAML frontmatter `type`, `[[wikilink]]` graph, local-first.
- **[obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain)**,
  **[claude-memory-compiler](https://github.com/coleam00/claude-memory-compiler)**
  ("a loaded index beats vector search at personal scale"), and the broader family
  of markdown-memory skills.

What Engramory contributes is the **opinionated bundle + the discipline**, not the
primitives. Do not claim novelty on markdown, frontmatter, wikilinks, a loaded
index, one-file-per-fact notes, or curation hygiene — all are prior art.

## What's actually differentiated

1. **A role/purpose ontology, headed by `feedback` = procedural memory.** The
   semantic / episodic / **procedural** split is established prior art — the CoALA
   taxonomy, and a named procedural type in LangMem and mem0 — so Engramory does not
   claim the category. What it does is make procedural `feedback` the *spine* of a
   deliberately tiny, hand-authored, human-readable set, with required **Why:** /
   **How to apply:** lines, instead of auto-extracting it into a vector/graph store.
   The contribution is the packaging and discipline, not the ontology.

2. **The curation contract as concrete behaviour** the protocol applies (model-followed, not a hard gate): dedup-before-write,
   update-don't-duplicate, delete-when-wrong, and a negative-scope rule ("don't
   store what git/CLAUDE.md/the code already records"). Surveys consistently name
   *modify/delete/forget* as the most under-implemented memory operation — Engramory
   makes it the spine.

3. **A bounded index designed not to silently rot.** The index loads every session and
   Claude Code reads the first 200 lines / 25 KB (documented behavior), so an unbounded index silently
   drops memories off the end. Engramory warns at 150 lines / 20 KB, compacts-or-asks
   before 200 / 25 KB, and ships a hard `PreToolUse` hook backstop (it blocks only
   *growth* past the cap — shrinking/compaction edits always pass). Both the line and
   byte caps apply — whichever is hit first triggers (an index can be under the line
   count yet over on bytes when the lines run long).

   Claude Code has since followed up on this natively: v2.1.186 (released
   2026-06-22) reminds the agent to compact the index when it nears the cap, and
   v2.1.210 (released 2026-07-14) turned an over-cap write into an explicit error
   instead of a silent truncation. Both are after-the-fact alerts, though — the
   write still lands, and entries past the cap stay invisible until someone
   compacts. Engramory's hook denies the write *before* it happens, so a write
   through the matched edit tools never leaves the index over-cap in the first
   place (writes outside them — a shell, an MCP file tool — are not gated; see the
   status note above and SKILL.md §8). The native alerts validate the direction
   and make a welcome second layer — and older versions and other hosts still
   have neither.

## How it compares

| | storage | recall | human-readable | typed ontology | curation discipline | bounded index | infra |
|---|---|---|---|---|---|---|---|
| **Engramory** | md files | loaded index → open file | ✅ | ✅ role-based (4) | ✅ contract (model-run) | ✅ 150/200 + hook | none |
| CC auto-memory | md files | loaded index → open file | ✅ | ✅ same 4 types | partial (auto) | ~200-line window* | none (built-in) |
| basic-memory | md + SQLite | semantic/FTS search | ✅ | ✅ freeform type | schema + overwrite checks | ❌ (no loaded index) | SQLite + embeddings |
| obsidian-second-brain | md vault | index-first + search | ✅ | folder-typed | ✅ reconcile/lint | partial | none |
| mem0 / Zep | vector/graph DB | semantic | ❌ (DB) | typed (prefs/episodic/proc.; Zep custom) | auto-extract | n/a | DB + embeddings |
| [agentmemory](https://github.com/rohitg00/agentmemory) | SQLite + vector index (+opt. graph) | hybrid BM25+vector (+opt. graph), RRF | ❌ (DB/engine) | ✅ 4-tier lifecycle (work./epis./sem./proc.) | auto (capture + dedup + decay) | n/a | iii engine (local) + opt. embeddings |

Engramory's lane: **minimalism + actionable role typing + curation discipline, zero
infra.** It does *not* try to out-search basic-memory, out-scale mem0, or
out-capture agentmemory — those solve a different problem (auto-capture /
auto-ingest at volume) at a different cost point. agentmemory is the closest
heavyweight foil: also local-first, but it bets on automatic capture (lifecycle
hooks) + hybrid retrieval (BM25 + vectors + optional graph) on a SQLite/`iii`
engine, where Engramory bets on hand-curation + a tiny always-loaded index and
ships no engine at all.

\* Claude Code's [memory docs](https://docs.claude.com/en/docs/claude-code/memory)
document this exactly: *"the first 200 lines of `MEMORY.md`, or the first 25KB,
whichever comes first, are loaded at the st