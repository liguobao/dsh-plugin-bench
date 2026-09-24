<p align="center">
  <img src="assets/euthyna.png" width="150" alt="euthyna logo">
</p>

<h1 align="center">euthyna</h1>

> **εὔθυνα** — in classical Athens, the audit every outgoing official had to submit.
> You did not get to simply walk away from office. You handed over your accounts and they
> were examined. Pass, and you left with your standing intact. Fail, and you faced trial.

<p align="center">
  <a href="https://github.com/slow-stack/euthyna/actions/workflows/ci.yml"><img src="https://github.com/slow-stack/euthyna/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://www.npmjs.com/package/euthyna"><img src="https://img.shields.io/npm/v/euthyna?style=flat&color=007EC6" alt="npm version"></a>
  <a href="https://www.npmjs.com/package/euthyna"><img src="https://img.shields.io/npm/dm/euthyna?style=flat&color=007EC6" alt="npm downloads"></a>
  <a href="https://www.npmjs.com/package/euthyna"><img src="https://img.shields.io/npm/l/euthyna?style=flat&color=007EC6" alt="license: Apache-2.0"></a>
  <a href="https://search.sigstore.dev/?logIndex=2915999059"><img src="https://img.shields.io/badge/npm%20provenance-verified-007EC6?style=flat" alt="npm provenance verified"></a>
  <a href="https://www.skills.sh/slow-stack/euthyna"><img src="https://skills.sh/b/slow-stack/euthyna.svg" alt="Agent skills installs"></a>
  <a href="https://awesome-dsh-plugin.com/p/slow-stack/euthyna/"><img src="https://img.shields.io/badge/DSH%20plugin-listed-blue" alt="Listed in the awesome-dsh-plugin catalog"></a>
</p>

**euthyna is a code security audit framework for AI coding agents.** It is not another
scanner. It does two things: it **produces the facts an agent cannot compute by reading
code**, and it **forces every security claim the agent makes through gates before it
counts as a finding**.

---

## 📖 The problem, in plain words

When an AI coding agent touches security, it fails in two specific ways:

1. **It reports things that are not real.** Code that *looks* dangerous gets called a
   vulnerability, without tracing the data. In validation runs on real codebases — a
   JavaScript one and a Python one — the pattern-matched "vulnerabilities" were mostly
   false: **5 out of 5** refuted at the gates on the first run; **2 out of 3** refuted,
   the third unresolved (INCONCLUSIVE, supply-chain-dependent) on the second. See the
   [case studies](https://github.com/slow-stack/euthyna/blob/main/docs/case-study-crewai.md)
   ([Python/crewAI](https://github.com/slow-stack/euthyna/blob/main/docs/case-study-crewai.md),
   [JavaScript/axe-core](https://github.com/slow-stack/euthyna/blob/main/docs/case-study-axe-core.md)).
2. **Its reassurances cannot be checked.** "I'm done." "The tests cover this." "It's
   safe now." These are assertions. You cannot tell a done-claim from a done-deal.

Neither is fixed by telling the agent to be more careful. euthyna changes the handshake
between you and the agent:

> **The agent saying "I'm done" does not count. The accounts get handed over, and the
> gates decide.**

---

## ⚖️ The two things it does

### 1. It measures what a model cannot

Three fact producers — a zero-dependency Node CLI:

- **`history`** — for every line a change deletes, it attributes the line to a commit
  and classifies that commit from its message, its own diff, and the deleted line's
  content (a deleted `if (!authorized)` is flagged even under a "tweaks" subject). By
  default the attribution traces the commit that *first introduced* the content with
  `git log -S` (`--no-origins` falls back to blame's "last touched", which is faster
  but mis-attributes a security line later moved by a formatting commit). If the
  deleted code came from a security fix, that is flagged. This is git archaeology no
  model can do from reading a diff.
- **`coverage`** — was this symbol *ever actually invoked* by a test? It has exactly two
  answers: never invoked (established), or entered but that proves nothing about any
  specific call site (unknown). **It never reports "executed"** — V8 coverage marks
  unreachable code as covered, and "line covered → call ran" is wrong in exactly the
  direction an audit cannot afford. The reasoning is in
  [`docs/fact-contract.md`](https://github.com/slow-stack/euthyna/blob/main/docs/fact-contract.md) §6.2.
- **`deps`** — what version is a dependency *actually* pinned to? It reads the lockfile
  (package-lock.json / Cargo.lock / go.mod) and reports the resolved versions, or that a
  dependency is absent from the tree entirely. This is the fact that resolves
  supply-chain claims ("the app uses a vulnerable version of X"): the version-to-CVE
  mapping is left to the adjudication layer, exactly as the fact contract requires. See
  [`docs/fact-contract.md`](https://github.com/slow-stack/euthyna/blob/main/docs/fact-contract.md) §6.3.

### 2. It gates what the agent claims

The [skill](https://github.com/slow-stack/euthyna/tree/main/.agents/skills/euthyna/) is the audit discipline itself, as loadable
Markdown. Every security claim must pass six gates — reachability, trust boundary, real
impact, and their counterparts. A claim that cannot produce evidence is **downgraded to
an observation**, not reported as a finding. "I'm done" becomes a package: claims,
evidence, and the commands that reproduce both.

The gates are not only prose. `euthyna gate <report>` reads an adjudication report and
mechanically checks every finding against its verdict — evidence down to `path:L123`, a
reproduce command, an impact statement, consistent gate statuses — and downgrades
whatever does not measure up. `--verify` re-runs the reproduce commands: `git` commands
by default, interpreter commands (`node`/`npm`/`python`) only with the explicit
`--allow-exec`, because an interpreter command from a report is arbitrary code and the
flag is the caller vouching for that report.

---

## 🖥️ Which tools it works in, and how to install

**Prerequisite for everything**: Node >= 20 and git. There is nothing else to install —
the project is deliberately zero-dependency.

| Host | The skill (audit discipline) | The CLI (fact producers) |
|---|---|---|
| **DSH** | `dsh plugin --profile web add euthyna` — the npm package mounts its own skill; or copy `.agents/skills/euthyna/` into `~/.agents/skills/` (user-wide) or `<project>/.agents/skills/`. Markdown hot-reloads; no restart needed. | `npm install -g euthyna` — runs in any terminal |
| **Claude Code** | `/plugin marketplace add slow-stack/euthyna` then `/plugin install euthyna@euthyna`, or copy `.agents/skills/euthyna/` into `~/.claude/skills/` | Same |
| **Codex** | The same Markdown layer works; packaging goes through Codex's plugin/marketplace format | Same |
| **Hermes** | Copy the same folder into `~/.hermes/skills/` under a category folder, or install from a repo with `hermes skills install` — and for the slash command, install the repo as a plugin (see below) | Same |
| **OpenCode** | Copy the same folder into `~/.agents/skills/` or `~/.config/opencode/skills/` (OpenCode loads both; unknown frontmatter fields are ignored). For a `/euthyna` slash command, copy `.opencode/commands/euthyna.md` into `~/.config/opencode/commands/` — it is a prompt template that tells the model to run the CLI | Same |
| **OpenClaw** | Copy the same folder into `~/.agents/skills/` (or `<workspace>/.agents/skills/`) — OpenClaw exposes every `user-invocable` skill as a slash command natively, so `/euthyna` works with no extra file. Published on ClawHub as [`@modusensus/euthyna`](https://clawhub.ai/modusensus/skills/euthyna) (zh) and [`@modusensus/euthyna-en`](https://clawhub.ai/modusensus/skills/euthyna-en) (en): `clawhub install modusensus/euthyna` | Same |
| **GitHub Copilot** | Copy the same folder into `.github/skills/` (project), `~/.copilot/skills/` or `~/.agents/skills/` (personal) — Copilot reads all three. For a `/euthyna` prompt, copy `.github/prompts/euthyna.prompt.md` into the same-named folder of your repo or profile. `gh skill`