# 🤖 Codex Guard

![GitHub release (latest by SemVer)](https://img.shields.io/github/v/release/Akimiya-z/codex-guard)
![GitHub stars](https://img.shields.io/github/stars/Akimiya-z/codex-guard)
![License](https://img.shields.io/github/license/Akimiya-z/codex-guard)
![CI](https://github.com/Akimiya-z/codex-guard/actions/workflows/ci.yml/badge.svg)
![Docs](https://img.shields.io/badge/docs-akimiya--z.github.io%2Fcodex-guard-8b5cf6)
[![Marketplace](https://img.shields.io/badge/GitHub%20Actions%20Marketplace-Codex%20Guard%20PR%20Quality%20Gate-2088FF?logo=githubactions&logoColor=white)](https://github.com/marketplace/actions/codex-guard-pr-quality-gate)
[![Awesome · DSH plugin](https://awesome-dsh-plugin.com/badge.svg)](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin)

**Docs site:** <https://akimiya-z.github.io/codex-guard>

**An automatic quality gate for AI-generated pull requests.** Stop TODO leftovers,
leaked secrets, sloppy commits and red CI from reaching `main` — with zero review
bandwidth spent on the obvious stuff.

Works with **OpenAI Codex** (cloud & CLI), **Claude Code**, **Copilot**, and any
other agent that opens PRs against your repo.

> 🐕 **Dogfooding:** this repo gates its own AI-generated PRs. See a real failing
> example on [PR #6](https://github.com/Akimiya-z/codex-guard/pull/6) and the
> workflow behind it in `.github/workflows/codex-guard.yml`.

---

## Why

AI coding agents are great at writing code and terrible at cleaning up after
themselves. In practice, agent-written PRs tend to arrive with the same handful
of problems:

- `// TODO: handle this` comments that were never meant to stay
- Hardcoded API keys and connection strings copied from a chat transcript
- Commit trails like `WIP`, `fix stuff`, `more changes` — squashed versions of
  a messy session
- A green-looking PR that actually has failing CI on the head commit

You shouldn't need a human reviewer to catch those every single time. **Codex
Guard checks the boring, deterministic things automatically, and only on PRs
that look AI-generated** — so human attention goes where it matters.

## How it works

Codex Guard runs on `pull_request`, figures out whether the PR looks
agent-generated (via label, branch prefix, or title), and then:

| Check | What it flags |
| --- | --- |
| 🧹 TODO scan | `TODO` / `FIXME` / `XXX` / `HACK` / `WIP` markers on **added lines only** |
| 🔐 Secret scan | AWS (access + secret keys), GitHub, Google, OpenAI, Anthropic, Slack, Stripe, npm, SendGrid, Telegram, Azure connection strings, JWTs, hardcoded credentials, connection strings (values are redacted in reports) |
| 💬 Commit hygiene | Subjects that don't match conventional commits, empty subjects |
| 🧪 CI status | Failing status checks **or** check runs on the PR head commit |

Each finding is posted as a GitHub **check-run annotation at the exact file and
line**, plus a human-readable summary comment on the PR.

### Honest content-scan coverage

GitHub sometimes omits the textual patch for binary or very large files. Codex
Guard now distinguishes **no findings** from **not scanned**: every report shows
the number of eligible changed files whose patches were actually inspected. A
missing patch produces a neutral, non-blocking coverage warning with the
affected paths; the JSON and Action outputs carry the same information. The
warning also appears when GitHub's pull-request files API reaches its documented
3,000-file limit.

The output below comes from a real run on this repo
([PR #6](https://github.com/Akimiya-z/codex-guard/pull/6)) — a deliberate test
PR from a `codex/` branch that left a TODO, credential-shaped fixtures and two
sloppy commits. Secret-shaped values are redacted here just as they are in
current reports:

```text
## 🤖 Codex Guard

❌ **Checks failed — review the findings before merging.**

| Check | Result |
| --- | --- |
| TODO / FIXME scan | ⚠️ 2 |
| Secret scan | ⚠️ 3 |
| Commit hygiene | ⚠️ 2 |
| CI status | ✅ |

**Unfinished work**
- `scripts/sync.js:4` — `FIXME`: const aws = 'AKIA...MPLE'; // FIXME: move this to a secret store
- `scripts/sync.js:2` — `TODO`: // TODO: wire up real retry with exponential backoff.
**Potential leaked secrets**
- `scripts/sync.js:4` — AWS Access Key ID `AKIA...MPLE`
- `scripts/sync.js:5` — Connection string `post...prod`
- `scripts/sync.js:7` — OpenAI API Key `sk-p...6789`
**Commit hygiene**
- `7c84ae1` — _WIP stuff_ (by Akimiya-z)
- `1affcf8` — _tmp_ (by Akimiya-z)

> Detected as an AI-generated PR (branch prefix "codex/").
```

## Quick start

From the root of your Git repository:

```bash
npx --yes codex-guard init
git add .github/workflows/codex-guard.yml
git commit -m "ci: add Codex Guard"
```

The installer starts in **observe mode**: findings are annotated, but they do
not fail the workflow while you tune the policy. Three setup presets keep the
rollout explicit:

| Preset | Command | Behavior |
| --- | --- | --- |
| Observe | `npx --yes codex-guard init` | Report everything without blocking. |
| Balanced | `npx --yes codex-guard init --preset balanced` | Block secrets, commit hygiene, and red CI; warn on unfinished markers. |
| Strict | `npx --yes codex-guard init --preset strict` | Block every default finding. `--strict` remains an alias. |

Prefer to add it by hand? The generated workflow is:

```yaml
# Generated by codex-guard init
name: Codex Guard
on:
  pull_request:

permissions:
  contents: read
  statuses: read
  pull-requests: write
  checks: write

jobs:
  codex-guard:
    runs-on: ubuntu-latest
    steps:
      - uses: Akimiya-z/codex-guard@v1
        with:
          preset: 'observe'
```

That's it. Codex Guard now reports on matching PRs without blocking them.

> Upgrading an existing workflow? Add `statuses: read` to its `permissions`
> block. `checks: write` already includes read access for check runs. Without
> status access, Codex Guard reports incomplete CI visibility and returns a
> neutral result instead of claiming every check is green.

One-click from the [GitHub Actions Marketplace](https://github.com/marketplace/actions/codex-guard-pr-quality-gate).

### Turn on enforcement

After a few representative PRs, choose how strongly to enforce:

```yaml
- uses: Akimiya-z/codex-guard@v1
  with:
    preset: 'balanced' # or 'strict'
```

`balanced` warns on unfinished markers while blocking secrets, commit hygiene,
and red CI. `strict` blocks every default finding. For a custom mix, use
`fail-on` and the individual inputs. Then require the status check under
**Settings → Branches → Require status checks → `Codex Guard`**. A blocking
finding will prevent the PR from merging until it is resolved (or the PR is
marked with an `ignore` label — see "Opting out").

## Detecting agent PRs

By default Codex Guard **only gates PRs it believes were written by an agent**,
so human-authored PRs are never slowed down:

- **Label** matches one of `codex-generated`, `agentic`, `ai-generated`
- **Branch** starts with `codex/`, `copilot/`, `claude-auto`, `gh-codex/`
- **Title** contains `Generated by Codex`, `Generated by Claude`, `Generated by Copilot`

All of these are configurable — or set `gate-agents-only: false` to gate every PR.

### Opting out of a specific PR

Add a label named `codex-guard-ignore` (configurable) to a PR and Codex Guard
will pass it without running checks. Useful when a human has already reviewed
and accepted the changes.

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `preset` | _(empty)_ | Policy baseline: `observe`, `balanced`, or `strict`. Empty preserves the pre-preset behavior. Repository policy can override it. |
| `github-token` | `${{ github.token }}` | Token with write access to checks and PRs. |
| `gate-agents-only` | `true` | Only gate PRs detected as agent-generated. |
| `agent-labels` | `codex-generated,agentic,ai-generated` | Labels marking an agent PR. |
| `agent-branch-prefixes` | `codex/,copilot/,claude-auto,gh-codex/` | Branch prefixes marking an agent PR. |
| `agent-keyw