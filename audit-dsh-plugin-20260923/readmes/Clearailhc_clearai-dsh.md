<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="brand/logo-lockup-dark.png">
    <img src="brand/logo-lockup.png" alt="ClearAI" width="360">
  </picture>
</p>

<p align="center"><b>English</b> · <a href="README.zh-CN.md">中文</a></p>

**Your research, grown into an ontology.**

ClearAI is an **ontology discovery and exploration platform**, built on two core concepts:

- **Domain ontology** (what you get) — your project's own vocabulary, the knowledge entries established through the loop, and their graphs. At the end of a research session you hold a continuously growing knowledge structure, retrievable next round by concept.
- **Epistemic loop** (how you get it) — a disciplined seven-stage path: frame, hypothesize, plan, observe, verify, evaluate, record. Every edge is tested by evidence and independent evaluation.

> Other knowledge graphs pile up edges by extraction and assertion; here every edge has to be earned through the loop.

```bash
# Install (npm package, prebuilt — no build step, no allowBuilds prompt)
dsh plugin --profile web add clearai-dsh
```

Restart `dsh web`, then pick **ClearAI** in the preset picker at the top of a new session. That is the whole setup. [Full install notes ↓](#install-and-use)


<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/diagrams/ontology-hero-dark.png">
  <img src="docs/diagrams/ontology-hero.png" alt="The epistemic loop (left) growing a domain ontology (right)" width="1200">
</picture>

*Left: the Epistemic Loop — seven stages. Its emerald fact dot is also the first node of the domain ontology on the right. Right: the ontology graph — dark is a concept, light is a value form, emerald an instance; the instance carries two contradictory assertions — **the two readings are tinted amber**, marking that they do not agree. The system reports the conflict; retracting or keeping is a human decision.*

---

## What you get: a domain ontology

A **domain ontology** that grows as you research:

- **Vocabulary** — the language your project speaks: concepts, predicates, value forms, units. Conventions themselves carry no truth value; sentences written with them do.
- **Established entries** — knowledge that passed the loop: each with its boundary, support level, and evidence chain. Each entry states its boundary explicitly, so it can be cited safely.
- **Ontology graph and entity graph** — what your domain looks like (structure), and what you have actually verified (the state of play).
- **Conflict readings** — contradictory conclusions surface automatically; the system reports them, and retracting or keeping is your decision.

## How you get it: the Epistemic Loop

Most agent loops track one thing: whether the task is done. The Epistemic Loop also tracks **what makes a conclusion trustworthy**:

| | Task loop | Epistemic loop |
|---|---|---|
| Driving question | What next? | What do we know, and on what grounds? |
| Completion | The model declares it | The system computes it from delivered evidence |
| Verdict | Whoever did it, says so | Separated — above a level, the doer cannot judge themselves |
| Failure | Deleted, retried, forgotten | Kept: a refuted hypothesis is a result, not noise |
| What accumulates | A chat transcript | **An ontology**: every edge earned through the loop |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/diagrams/epistemic-loop-hero-dark.png">
  <img src="docs/diagrams/epistemic-loop-hero.png" alt="The Epistemic Loop" width="1000">
</picture>

*Inside the ring is the instrument's read-out: the L0–L4 axis, the **pre-registered** threshold as a dashed line, and five observations with error bars — the supported one filled, the inconclusive drawn as a dashed circle, the refuted left in place with a slash through it (nothing is deleted). The emerald dot at the opening is the one reading that crossed the threshold and settled as a fact.*

At runtime, the seven stages compress into four beats — plan, execute, observe, reflect. State is derived from the session record with no second store; the tools the model holds contain no field in which it could declare a step complete.

ClearAI does **not** claim recursive self-improvement. It provides the epistemic substrate a self-improving system would need. See [Positioning](docs/positioning.md) and the [OpenRSI survey](docs/research-openrsi.md).

---

## Install and use

**Recommended — install from npm:**

```bash
dsh plugin --profile web add clearai-dsh
```

This installs the prebuilt package from the npm registry. Nothing is compiled on your machine, so there is no `allowBuilds` grant to approve — the plugin is ready the moment the command returns.

**Also available — one-command installer:**

```bash
npx clearai-dsh install
```

Same install underneath; it resolves the DSH CLI from your PATH (or through npx), installs into the `web` profile, and reads the composed config back so you are not taking "success" on faith. Use this if you prefer a guided path, or `--lang zh|en` to force the installer's output language.

**Install from source (for development, not the normal path):**

```bash
dsh plugin --profile web add github:Clearailhc/clearai-dsh
```

Git fetches source rather than build artifacts, so pnpm ≥10 will refuse to run the `prepare` script until you add an `allowBuilds` entry to the profile's `pnpm-workspace.yaml`. That grant means *permission for this package's code to execute on your machine at install time* — grant it only if you have read the source, and pin a commit. If you just want to use ClearAI, use the npm install above.

The installer's output follows your system language (`--lang zh|en` overrides it, `doctor` / `seed` / `unseed` take the same flag). Its only runtime dependency is `zod`; the graph stack is bundled into the client half at build time.

Restart `dsh web` afterwards (`npx @deepseek-ai/dsh web`), then **create a session and switch to the `ClearAI` mode in the picker at the top**:

1. Open `dsh web` and click "New session";
2. Click the current mode name at the top (default: **Standard mode**) to open the preset list;
3. Pick **ClearAI** — its card reads "利用认识论循环构建可信本体。Build a trustworthy ontology through the epistemic loop.";
4. Just ask your question. Ordinary Q&A runs as usual; once you set a goal and register hypotheses, the system enters knowledge mode by itself: known facts come to you, gaps stay visible, and conclusions earn their place.

<picture>
  <img src="docs/shots/zh/jepa-ontology.png" alt="The knowledge graph in ClearAI mode" width="820">
</picture>

*The ontology graph in ClearAI mode — this real session grew 21 concepts and 9 predicates; the same ledger always yields the same picture. (UI shown is Chinese.)*

If pnpm is not on PATH: `npm install -g pnpm` (do not `corepack enable` — it installs a version forwarder that may download a pnpm it cannot launch).

From the repository:

```bash
npm test                       # 15 suites
node tools/build-package.mjs   # assemble dist/ from source
node tools/verify-package.mjs  # rebuild on the spot, byte-compare
node docs/diagrams/build-hero.mjs   # redraw the product hero (needs google-chrome)
```

`dist/` is generated and never committed. See [DSH integration](docs/dsh-integration.md).

---

## What it looks like

The middle column has two switchable views: **Deliverables** and **Ontology**. The right sidebar: **Worldlines** and **External Brain**.

**Ontology** — this view is your knowledge home. At the top, a **graph band**: the ontology graph (what your domain looks like) and the entity graph (what you have actually verified) toggle with one click; clicking a node or edge opens the **knowledge inspector** (definition / relations / assertions / evidence chain / history), and "filter by this" is an explicit action inside the detail view. Below that, the **ontology shelf**: established entries, each with assertion chips (click to see what the term means), boundary, and support level;