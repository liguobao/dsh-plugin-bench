<!-- Language toggle -->
**English** · [中文](README.zh-CN.md)

# odai

<p align="center">
  <img src="assets/odai-readme-badge.png" alt="Dai, the odai mascot" width="720">
</p>

`odai` is a governance-powered general task-execution framework for AI agents.

It embeds governance into execution: align the real objective, facts, assumptions, authorization, risks, and acceptance; then choose the shortest sufficient path, combine the right capabilities, act, verify, and keep moving until the task is genuinely deliverable. It does not replace the model's judgment with a rigid workflow.

The short version: call `/odai`; governance stays nearly invisible on simple work, while ambiguity, complexity, risk, and domain needs automatically increase or reduce the depth of handling.

## Why Use It

`odai` is for people who want agents to move with autonomy, but not with false confidence.

It helps an agent:

- ask only when the missing answer would change the goal, scope, authorization, acceptance, risk, or stop line
- verify what it can verify from files, commands, logs, tests, or project context before asking you
- keep lightweight tasks lightweight instead of turning every request into ceremony
- avoid claiming that something was tested, delegated, reviewed, or verified when it was not
- combine specialist skills and domain guidance only when the task needs them, instead of stuffing every rule into every turn
- reuse existing host or project memory, persisting only durable information with provenance, scope, and invalidation conditions
- respond early and humanely to persistent low mood or self-harm/suicide inclination without diagnosing, labeling, waiting for a plan, or causing secondary harm

## The Dao of odai

**The user defines the task; evidence determines the route; methods adapt to circumstances; verification determines completion; boundaries determine where to stop—get the task done, without acting presumptuously.**

This is not a collage of philosophical schools. It is one decision rule:

- **Get the task done**: advance the user's task to a verified, deliverable result, while surfacing counterexamples, risks, and a better route when they would change the outcome.
- **Do not act presumptuously**: do not bend facts, user decisions, or hard boundaries; do not conclude without evidence, exceed authorization, invent work, or treat a discovery as permission to implement it.

The person and the model work as partners toward a shared result, not through a one-way command chain. The person contributes intent, context, value judgments, and unacceptable outcomes; the model contributes judgment, evidence, creation, and execution, challenges doubtful premises, and proposes better routes. Both calibrate understanding and trust through real progress, candid uncertainty, and feedback. The person owns goal-level tradeoffs; the model chooses professional implementation details within the agreed boundary. Authorization is not blind obedience, and challenge is not a takeover.

odai is neither an echo of the user nor a reciter of rules. It takes the person's purpose as its direction and facts and boundaries as its constraints, forms its own judgment and recommendation, holds a justified disagreement when necessary, and changes its mind when the evidence changes. Truth outranks pleasing, effectiveness outranks ceremony, reliable results outrank superficial shortcuts, and long-term trust outranks one-turn performance.

The model's initiative is judged by net value. Speed, quality, stability, cost, breadth, and practicality are outcomes to balance against the user's goal and the evidence—not a flat list of slogans, and never substitutes for a real result.

### Operating Standard

**See clearly, hold steadily, strike accurately, land real results, defend what matters, and build for the long run.**

Understand the real objective, facts, and gaps; hold authorization, boundaries, and risk steady; choose the narrowest sufficient path; produce a verifiable deliverable; protect user decisions, system safety, and truth; and leave a result that survives use, maintenance, and change.

### Product Goal

Make agents **faster, more accurate, better, steadier, cheaper, lighter, broader, more adaptive, more useful, and more practical**. These are not independent process targets. They are product outcomes balanced around the task's net value; process, file count, tokens, and benchmark scores never substitute for getting the real task done.

## 30-Second Start

Install standalone governance:

```bash
npx skills add https://github.com/orziz/odai --skill odai
```

The source candidate separates optional orchestration into an installable sibling skill:

```bash
npx skills add https://github.com/orziz/odai --skill odai-orchestration
```

`odai-orchestration` depends on `odai` and adds responsibility presets and host routing adapters. Installing the skill does not change host settings. The candidate DSH packages bundle both; governance works without enabling orchestration. For an unpublished local checkout, replace the repository URL with its local path.

Then invoke it with `/odai`. That is the normal form in clients that expose skills as slash commands:

```text
/odai update the onboarding flow copy.
Goal: make it clearer for first-time users.
Materials: current app files and README.
Constraints: do not change behavior yet; give me the proposed copy and risks first.
```

If slash commands are not available in your client, naming `odai` in plain language works too.

You do not need to know the internal structure or choose a methodology. `odai` infers the required depth, capability, domain knowledge, and verification from the task and project evidence.

### DeepSeek Harness packages

[![npm: odai-dsh-plugin](https://img.shields.io/npm/v/odai-dsh-plugin?label=odai-dsh-plugin&logo=npm)](https://www.npmjs.com/package/odai-dsh-plugin)
[![npm: odai-dsh-agent](https://img.shields.io/npm/v/odai-dsh-agent?label=odai-dsh-agent&logo=npm)](https://www.npmjs.com/package/odai-dsh-agent)

DSH users can install either integration independently:

```sh
# Apply Odai to every agent preset in one profile
dsh plugin --profile web add odai-dsh-plugin

# Install a selectable, session-scoped Odai Agent preset
npx odai-dsh-agent install
```

The published `0.2.36` Plugin and Agent release and the current `0.2.37` source candidate target exactly `dsh@0.1.5-rc.2`. Previous SDK versions are outside current support; published releases retain their historical compatibility entries. Odai owns its preset and preserves its existing capabilities without requiring a copy of Standard or automatically adding Standard's new tools. Control Center declares the new Web transport dependency while headless governance remains independent of it.

Normal lifecycle and runtime paths do not inspect or rewrite old session logs. DSH refuses historical v0 logs containing unknown Odai events even when marked ignorable; the old flag-only `legacy-session-repair` entry is retired and does not modify files. New SDK support does not claim those historical sessions have been migrated.

The Plugin command requires `pnpm` on `PATH`. Each package already includes the canonical Odai skill, shared DSH runtime, and the same Chinese Control Center; there is no third package. Plugin exposes Control Center automatically. Interactive Agent install describes the existing profile source/version and asks at `[Y/n]`; Enter, `y`, or `yes` confirms, while EOF, `n`, `no`, or other text leaves the Web profile unchanged. Non-interactive install changes the profile only with explicit `--with-control-center`. Plugin and Agent may be installed independently or together: when both are present, Plugin owns the single Control Center surface while the runtimes share and deduplicate governance, routing, and evidence state. The existing provider-neutral `odai-cli` remains a separate product.

Both DSH packages default output to **soft concise**. Users can explicitly select norma