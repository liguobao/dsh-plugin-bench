[![MCP Toplist](https://mcptoplist.com/badge/io.github.geml-spec%2Fgeml.svg)](https://mcptoplist.com/server/io.github.geml-spec%2Fgeml) [![Mentioned in Awesome](https://awesome.re/mentioned-badge.svg)](https://github.com/hashgraph-online/awesome-ai-plugins#development--workflow) 


<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo/geml-logo-dark.svg">
    <img src="docs/assets/logo/geml-logo-light.svg" alt="GEML" width="340">
  </picture>
</p>

# GEML — General Expressive Markup Language
[![npm](https://img.shields.io/npm/v/%40geml%2Fgeml?label=npm)](https://www.npmjs.com/package/@geml/geml) [![MCP](https://img.shields.io/badge/MCP-supported-blue.svg)](https://modelcontextprotocol.io) [![CI](https://github.com/geml-spec/geml/actions/workflows/ci.yml/badge.svg)](https://github.com/geml-spec/geml/actions/workflows/ci.yml) [![GEML check](https://github.com/geml-spec/geml/actions/workflows/geml-check.yml/badge.svg)](https://github.com/geml-spec/geml/actions/workflows/geml-check.yml) [![spec: 1.0](https://img.shields.io/badge/spec-1.0-brightgreen.svg)](spec/GEML-spec.md) [![code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE) [![spec license: CC BY 4.0](https://img.shields.io/badge/spec%20license-CC%20BY%204.0-lightgrey.svg)](spec/LICENSE-spec.md)

*English | [中文](README_CN.md)*

GEML is an **Agent-Native** fundamental markup format and protocol, designed for people and AI agents to read and write the same document.<br>
**One format, two readers.**
In agent-driven development and knowledge work, plain text and Markdown have no deterministic block boundaries: a program and a model trade the whole file in and the whole file back out — at best probing for it with line windows, and restating the original verbatim to rewrite it. Token cost grows with the length of the document, and the operation turns bloated. After a few rounds of rewriting, the copies excerpted elsewhere start to drift.

**You can start without changing a thing.** `geml list`, `geml find` and `geml get` address the Markdown you already have — nothing is converted, no new files, your `.md` stays `.md`:

```sh
geml list    README.md                          # every section, as an address
geml get     README.md '#key-features'          # read ONE section, not the file
geml set     README.md '#key-features' --body   # write one section back
geml replace README.md 'old text' 'new text'    # swap a string, told which block held it
```

Only that section enters the agent’s context — a couple of KB, not the whole ~48 KB file.

Need finer than a section — one block, one chart, one table? Let `.geml` stand in the middle ground: edit at that grain, and the `--to md` you ship never drifts from it.

**A block has a name; the things inside it have a coordinate.** A table's cell, a
`data` block's leaf, a key in `meta` — each has a coordinate the structure already
gives it, and `get` and `set` land on exactly that value.

```sh
geml get doc.geml '#fy[2]["Q1"]'                     # one cell
geml set doc.geml '#intake["fields"][1]["name"]'     # one leaf in the JSON
```

For people, it is plain text that reads clean; for agents, it is an addressable, verifiable, traceable, revertible **["Doc-as-a-Base"](docs/MANIFESTO.md)**.

---

**GEML is minimal.**
It is plain text — still clean with no renderer in sight;
one block syntax for the whole language;
addressable, verifiable, referenceable structure, natively.

Instead of a separate mini-syntax for each kind of content, GEML carries every kind in one container: the typed block. Code is a block. So are tables, diagrams, math, callouts, even metadata — and a run of prose can be one too (`=== text`), whenever you want it addressable. Extending it later is just as plain. The shape is the same every time, which makes the language easy enough to learn that it's hard to get wrong.

```
=== code {#hello lang=python}
print("hi")
===
```

```sh
geml get doc.geml '#hello'   # by name, just this block
```

Blocks have names so the verbs have somewhere to land — the full syntax is in
[the format in 1 minute](#one-minute).

**Contents:** [What it solves](#problems) · [Why now](#why-now) · [What's different](#whats-different) ·
[The format in 1 minute](#one-minute) · [A gift for programmers](#code-graph) ·
[Get hands-on](#hands-on) · [With an LLM](#with-an-llm) ·
[Maturity & versions](#maturity) · [The design](#challenge) · [Roadmap](#roadmap) · [Take part](#contributing) ·
[License](#license)

<a id="problems"></a>
## What it solves

### Problems solved

1. **Context load and token bloat**
   * **Status quo**: data formats like JSON/XML carry heavy wrapper tags and syntax symbols; Markdown lacks strict structural metadata and a reference mechanism.
   * **Approach**: tuned markup density and syntax overhead, reading and writing only the target block — context cost no longer grows with document length, keeping **agent reads and writes lightweight**.

2. **AST-level precision and parsing determinism**
   * **Status quo**: unstructured text degrades over multiple rounds of LLM reads and writes — broken formatting, semantic drift, parsing hallucinations.
   * **Approach**: a deterministic grammar that maps directly to an abstract syntax tree (AST), so programs and LLMs perform atomic block-level create/read/update/delete.

3. **Document copy fragmentation**
   * **Status quo**: multi-agent collaboration and shared pipelines pass content around by copy-paste, leaving multiple disconnected copies.
   * **Approach**: **Single Source of Truth** by design — standardized module references and data binding eliminate redundant copies and version divergence.

### Key features

#### 1. AST-level structured operations
* Uniform node definitions; a document parses directly into a typed document tree (AST).
* Agents pinpoint the target section, attribute or component; partial patches and idempotent updates replace whole-file rewrites. Writes land as byte splices with whole-document re-validation — the tree serves reading and validation, and every untouched byte is guaranteed unchanged.

#### 2. Low-token reads and writes
* What is saved is not markup characters — it is the part never read: `#id` hits one semantically complete block, and the rest never enters the context.
* For the same semantics, markedly lower prompt-token cost: better model throughput, lower inference cost.

#### 3. Single source of truth, modular references
* Native cross-document, cross-fragment component references.
* Change the source node once and every reference follows — no version skew.

#### 4. Robust two-way reads and writes
* One block shape for the whole language — easy to generate and hard to get wrong, a good match for mainstream LLM output distributions.
* A strict validator with precise error locations and actionable repair feedback.

### Comparison

| Dimension | Markdown | JSON / YAML | GEML |
| :--- | :--- | :--- | :--- |
| **Context cost (block-wise I/O)** | High (whole file in and out) | High (whole file + syntax noise) | **Minimal (only the target block)** |
| **Precise AST operations** | Weak (no strict semantic nodes) | Strong | **Strong (built for agent reads and writes)** |
| **Human readability** | High | Medium | **High** |
| **Single-source references** | Unsupported | Needs protocol extensions | **Native (modular embeds)** |
| **Write safety** | Weak | Medium | **Strong (a bad write is refused before landing + single-block revert)** |

---

<a id="why-now"></a>
## Why the LLM era needs a brand-new text format

Because **both the producer and the consumer of a document have changed**.

In traditional software engineering, a document was either a static explanation for people to read, or a serialized data file for programs.

Today, people and AI agents collaborate on the same document at high frequency. When the agent becomes the document's "second reader and co-author", the old balance breaks for good:

1. **Context is sca