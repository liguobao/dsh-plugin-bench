# Caliper: Know if your agent skill actually works

[![PyPI](https://img.shields.io/pypi/v/caliper-eval.svg)](https://pypi.org/project/caliper-eval/)
[![Python](https://img.shields.io/pypi/pyversions/caliper-eval.svg)](https://pypi.org/project/caliper-eval/)
[![Skills](https://skills.sh/b/edonadei/caliper)](https://skills.sh/edonadei/caliper)

Caliper is a lightweight evaluation harness for agent skills. Write a short spec of what "good" looks like, run it, and get a **success rate** you can track. Works with the agent you already use: **Claude Code, Codex, Pi, or Hermes**. Caliper installs the skill where the agent looks for skills and lets the agent choose.

**Teach your agent to evaluate:**

```bash
npx skills@latest add edonadei/caliper
```

**Or run it yourself:**

```bash
# Run the evaluation.
caliper run commit-commands.eval.yaml --k 3

# The control subject: your skill is not there.
caliper run commit-commands.eval.yaml --k 3 --ablate commit-commands

# Compare the runs. Did your skill improve it?
caliper compare .caliper/results/commit-commands/<evaluation-run>.json .caliper/results/commit-commands/<ablated-run>.json
```

You write a spec, a YAML file describing what "working" means. Either hand-write it or have `/grill-skill` generate it for you. `--ablate` runs the same tasks with that skill *removed* — a declared MCP server can be ablated the same way — and `caliper compare` diffs the two runs task by task:

<!-- Terminal output of `caliper compare`, rendered to SVG so the box-drawing
     table stays aligned on every screen. Regenerate with:
       python docs/render_readme_samples.py -->
![caliper compare, without commit-commands vs full neighbourhood on commit-commands: both tasks go 33.3% to 100.0% (+66.7%); tokens 290K to 180K, wall 1m 1s to 42s](docs/assets/compare-ablation.svg)

---

Agent skills are hard to test. A skill that works on your machine, on this prompt, today, might fail tomorrow after a model update or a one-line prompt edit. Caliper makes reliability measurable: define what success looks like, run the skill repeatedly, and get a success rate you can track over time.

Use Caliper to answer questions like:

- Is my agent still working the same with this new model?
- Did my prompt edit improved the skill?
- Does my skill fire when it should, and stay quiet when it needs to not trigger?
- Is the skill worth the context? Or would the base agent pass without it?
- Does it still pass the workflows it passed last week?
- Which agent (Claude Code, Codex, Pi, or Hermes) runs this skill more reliably?

---

## Quick start

### Path A: Agentic (let your agent drive)

**1. Install the skills**

```bash
npx skills@latest add edonadei/caliper
```

**2. Generate a spec interactively**

In your agent (Claude Code or Codex):

```text
/grill-skill ./my-skill/SKILL.md
```

`grill-skill` reads your `SKILL.md`, interviews you, and writes a 3-task `.eval.yaml` (happy path, edge case, adversarial).

**3. Run and measure**

```text
/evaluate-skill run my-skill.eval.yaml --k 3
```

Browse past runs:

```text
/evaluate-skill list
/evaluate-skill report my-skill
```

### Path B: CLI (run it yourself)

**1. Install the CLI**

```bash
pipx install caliper-eval   # requires Python 3.10+
```

**2. Write a spec**

```yaml
# commit-writer.eval.yaml
skills:
  - ./SKILL.md                     # the skill under test
  - ../changelog-writer/SKILL.md   # a neighbour it might steal work from

tasks:
  # Autorater: the LLM judge reads the transcript and decides
  - name: Writes a conventional commit message
    setup: >-
      git init -q && git config user.name Eval && git config user.email eval@example.com
      && printf 'retry on 429\n' > NOTES.md && git add NOTES.md
    prompt: "Summarize the staged git diff as a commit message."
    expect: >
      The response is a conventional-commit message: a concise subject
      line under 72 characters, followed by a body explaining why the
      change was made, not just what changed.
    activates: [commit-writer]

  # Script execution: a deterministic Python assertion
  - name: Keeps the subject line under 72 characters
    setup: >-
      git init -q && git config user.name Eval && git config user.email eval@example.com
      && printf 'retry on 429\n' > NOTES.md && git add NOTES.md
    prompt: "Commit the staged changes."
    assert: |
      import subprocess
      subject = subprocess.run(
          ["git", "log", "-1", "--pretty=%s"],
          capture_output=True, text=True, check=True,  # no commit fails here
      ).stdout.strip()
      assert len(subject) <= 72, f"subject line is {len(subject)} chars"
    activates: [commit-writer]

  # Activation: this prompt belongs to the neighbour, not to you
  - name: A release summary belongs to changelog-writer
    prompt: "What changed since v2.1? I need it for the release notes."
    activates: [changelog-writer]
```

Three kinds of check, and a task needs at least one. `expect:` is graded by the
judge LLM; `assert:` runs locally as Python; `activates:` asserts which skills
the agent chose to load. Use any combination.

The third task is the one you cannot write any other way. Both skills read git
history, so a release-notes request is exactly where `commit-writer` might grab
work that belongs to `changelog-writer`. Declaring the neighbour and asserting
`activates: [changelog-writer]` is how you find out. A task like that needs no
`expect:` at all: it skips the judge, so it costs a fraction of a graded task.

Caliper never pastes your skill into the prompt. It **installs** it where the
agent looks for skills and lets the agent decide, so a run measures the
`description` (does it fire?) and the body (does it work?) together, and
`activates:` is what tells the two apart.

The spec never names an engine. The skill and judge default to `claude-code`, and you pick a different agent/model at run time with `--model` / `--judge-model` (see [Choosing an engine](#choosing-an-engine)).

**3. Run it**

```bash
caliper run my-skill.eval.yaml --k 3          # --ablate <skill|mcp:server> for a run to diff against
```

**4. Read the output**

![caliper run of commit-writer at k=3. Three rows: 'Writes a conventional commit message' passes 3/3 (100.0%, 80K tokens) with a green tick in the act column; 'Keeps the subject line under 72 characters' 2/3 (66.7%, PARTIAL, 84K tokens) with a green tick; 'A release summary belongs to changelog-writer' shows no execution score, a red cross in the act column, and reads 'trigger only'. Score 83.3% over 2 tasks scored. Activation 77.8% over 3 asserted tasks. A per-skill table shows, for each skill, how many of the 9 attempts wanted it and how often it fired: commit-writer was wanted on 6 of 9, fired on 6/6 of those (100.0%) but also on 2/3 of the attempts that did not want it (66.7%); changelog-writer was wanted on 3 of 9, fired on only 1/3 (33.3%), and never fired unwanted (0/6, 0.0%). commit-writer is taking prompts that belong to changelog-writer. Failure panels below show the assertion error and the attempts where commit-writer activated on the changelog prompt](docs/assets/run-output.svg)

The report ends with the per-task failure panels: for each attempt that didn't pass, the output plus the assertion or autorater reason *why*. Full results are also saved as JSON under `.caliper/results/<spec>/` at the project's [results root](#where-results-are-saved), for you to inspect or `caliper compare` later. `--verbose` adds `pass@k` and `pass^k` columns (both derived from the raw rate) and a panel for every task.

### Not sure what to put in a spec?

The **[Eval Starter Pack](examples/starter-pack/)** has four copy-paste
templates, each catching a real agent failure (false success, tool misuse,
runaway loops, prompt regressions). Every template runs green as-is against a
bundled example, then points at your own skill by editing two or three
commented lines.

---

## How it works

```
.eval.yaml spec
      │
      ▼
  Harness  ──── runs you