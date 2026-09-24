# 蒸留蔵 — distill-kura

**A long-term memory for agents that is distilled, not accumulated.**
Recall works by *meaning*, writing is gated by *evidence*, and one server can hold
several separate memories — one per agent mode — so switching mode switches what the
agent remembers.

Ships as a [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) plugin,
an MCP server for any other host, an HTTP service, and a Python library. Standard
library only; no vector database, no embeddings, no framework.

```
        ┌── recall ──────────────────────────────────────────────┐
        │  question → names a memory? → deterministic hit   ~2 ms│
        │      else → whole index in one prompt → picked slugs   │
        │           → walk [[links]] → the neighbourhood   ~0.4 s│
        └────────────────────────────────────────────────────────┘
        ┌── distil ──────────────────────────────────────────────┐
        │  journal → classed evidence → candidates → GATE        │
        │  → new? → composed → draft → judged → poured           │
        └────────────────────────────────────────────────────────┘
```

---

## Why this exists

Two failures kill an agent's long-term memory, and they kill it from opposite sides.

**Retrieval by keyword misses the thing you needed.** A question about *"SSD inference
chips"* shares no word with a memory titled *"running the 2.6T model off an SSD tier"* —
yet they are the same subject. Word search returns nothing; the agent answers from
nowhere. The fix here is not embeddings but *recognition*: the entire index (one line
per memory, written as a recognition trigger) goes into one prompt, and a small model
names what bears on the question. An index of ~500 memories is around 6k tokens — a
few percent of a modern context window, and it sits in the prefix cache.

**Writing everything poisons the store.** An agent asserts something; a naive distiller
records the assertion as a fact; the next agent reads it back as ground truth and
repeats it with more confidence. That loop is self-reinforcing, and prompt instructions
do not stop it — measured, not assumed. So the write path is gated by deterministic
Python: every candidate memory must carry quotes that exist *character-for-character*
in the raw material, tagged with where they came from.

| class | what it is | what it licenses |
|---|---|---|
| `[USER]` | the human's own words | "they decided", "they asked" |
| `[TOOL]` | machine output | **numbers — the only source** |
| `[ACT]` | a tool that was invoked | "this was done" |
| `[SELF]` | the agent's own prose | a judgement, in the first person, never a bare fact |

A quote that is not found verbatim is discarded. A candidate with no surviving quote is
thrown away. A number with no `[TOOL]` behind it is stripped. Text crediting the human
with a decision, when no `[USER]` quote survived, is refused at the last gate. Ideas are
welcome — they go to a seed file, never to the store, and graduate only when later
evidence confirms them.

---

## Tier zero: recognition before intelligence

The recall above is the right tool for a question that shares no words with its
memory. It is the wrong tool for a question that *names* what it wants — and in a
working session, most questions do. A blind 40-question benchmark on a live
317-memory store split exactly along that line: the direct questions needed no
intelligence at all, and everything else needed all of it.

So before the thinker runs, a deterministic recognizer gets one look. The design is
transposed from the n-gram embedding table inside Qwen3.8-Flash-Next — many hash
heads voting over one table, behind a gate — onto the index:

- **Five heads**, each an independent recognition channel: exact name; IDF-weighted
  word tokens (identifiers, ports, katakana runs); character 3-grams with
  **stop-grams** (a gram present in over a fifth of the store drowns in its own
  collisions, so it is dropped); character 2-grams; and the head of each body.
- **Coverage scoring** — each head's vote is normalized by what it could possibly
  have reached for *this* question, so one lucky rare gram cannot fake confidence.
- **An honesty gate** — a hit is returned only when the top score clears an absolute
  bar *and* beats the runner-up by margin. Anything less and the fast path says
  nothing; the question falls through to the thinker, unchanged.

Blind-tested — the examiner wrote the 40 questions from the index alone, never
seeing the implementation — against the live store over HTTP:

| question type | tier zero | thinker tier |
|---|---|---|
| direct (14) | **14/14, median 2.3 ms** | 14/14, ~900 ms |
| paraphrase (10) | silent → falls through | 10/10 |
| semantic bridge (10) | silent → falls through | 10/10 |
| not in the store (6) | **6/6 refused** | 0/6 refused |
| wrong answers, whole set | **0** | — |

What that buys:

- **The everyday case stops paying the intelligent price for a lookup.** Direct
  recall drops from ~900 ms to ~2 ms, and the fall-through tax on every other
  question is about 2 ms.
- **It knows what it does not know.** Zero wrong answers across the set is the
  gate working, not the heads being clever — everything uncertain goes to the
  model. On the six questions whose answers were *not* in the store, tier zero
  refused all six; the thinker tier answered something every time. Refusal is a
  feature this project keeps having to buy back.
- **A direct question now survives the thinker being down.** Recall used to
  degrade straight to word overlap; the named memory comes back regardless.
- **Every reply says which tier answered** — `how: "fastpath"`,
  `fastpath_verdict`, `fastpath_ms` — so a slow answer is never a mystery.

Configured under `[fastpath]` (`enabled`, on by default; `gate`), per-store
overridable like everything else. The row it will never win: a question that
shares no surface with its memory. That is the thinker's job, and the gate exists
to hand it over rather than guess.

---

## Quick start

```bash
git clone https://github.com/lna-lab/distill-kura && cd distill-kura
pip install -e .                       # or just run: python3 -m distill_kura.cli

cp kura.example.toml kura.toml         # edit: one model endpoint is enough to start
kura init main --path ~/kura/main      # create an empty store
kura serve                             # http://127.0.0.1:8085
```

```bash
curl -s -X POST localhost:8085/recall -H 'content-type: application/json' \
     -d '{"question":"what did we decide about the archive disk?","hops":1}'
```

Wear the index, so the agent always knows what is known:

```bash
kura weave                             # build the three-layer cloth
kura prefill                           # the block to put in the system prompt
```

Feed it your agent transcripts:

```bash
kura distill run      # drink a batch → candidates → gate → drafts
kura distill drafts   # look at what it wants to write
kura distill drain    # the scribe re-reads each draft cold: pour / fix / toss
kura distill night    # stay resident and do it whenever things go quiet
```

Nothing enters the store until `drain` (or a hand-run `pour`). Drafts carry their
evidence in an HTML comment, so you can always see *why* a memory exists.

---

## The resident map

Recall-by-tool answers *"what do you know about X?"* — but only once the agent has
decided to ask. It never answers the question the agent does not think to ask: **is
there anything here at all?** An agent that cannot see the map does not know what it is
missing, so it guesses, and a confident guess about your household is precisely the
failure this project exists to prevent.

So the index is also worn: a standing block in the system prompt, on every turn.

```bash
kura weave      # re-weave the index into the three-layer cloth
kura prefill    # print the block a host should inject
```

### Three layers, because detail only pays for recent things

A blind A/B test — 20 questions, fat index vs slimmed index, scored without k