# AGENT-GUARD

[![CI](https://github.com/mokuyoaxis/agent-guard/actions/workflows/ci.yml/badge.svg)](https://github.com/mokuyoaxis/agent-guard/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/mokuyoaxis/agent-guard)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Source preview tags](https://img.shields.io/badge/Source-preview%20tags-5B6B7A)](https://github.com/mokuyoaxis/agent-guard/tags)

**Make destructive agent actions reversible by default.** · [简体中文](README.zh-CN.md)

Agent Guard is a reliability layer for coding agents. It makes supported
high-impact actions recoverable instead of permanently destructive, while
keeping routine work automatic.

- **Destructive file operations** can be relocated to `.agent-trash/` with a
  recovery manifest instead of being permanently deleted.
- **Destructive Git operations** can snapshot recoverable state before they
  overwrite the working tree.
- **Accidental outbound disclosure** of known credentials or host-identifying
  absolute paths can be checked through a cooperative text CLI. A caller that
  owns the emission can apply its redaction plan, escalate, or block.

The Core is harness-neutral and supports Python 3.9+ and Git. Automatic
interception still depends on whether the host exposes a compatible hook; a
Skill by itself does not intercept tool calls. The shared Core, Decision
Protocol, and Skills define the product; harness adapters are replaceable
integration bridges rather than the product boundary.

> **Agent Guard keeps reversible actions automatic and escalates only when it
> cannot safely automate them.** It is reliability infrastructure, not a
> security sandbox: it protects against mistakes, not a malicious agent with
> equal OS privileges.

## What it looks like

```text
rm -rf build/       → RELOCATE   # an in-scope tree moves to quarantine
rm -rf .            → BLOCK      # the workspace root is protected
git reset --hard    → SNAPSHOT   # snapshot first when Git state supports it
git push --force    → BLOCK      # remote history is not automated
```

These are illustrative verdicts for supported inputs, not commands to run or
proof that every harness intercepts them. Ignored, regenerable targets may be
`ALLOW`; a Git snapshot that cannot be made fails closed. When recovery or safe
rewriting is possible, the agent can keep working. Otherwise, the guard asks
the human or blocks the operation.

## Quick start with your coding agent

Keep a stable local checkout of this repository (skip the clone if you already
have one):

```sh
git clone https://github.com/mokuyoaxis/agent-guard.git
cd agent-guard
```

Python 3.9+ and Git are required for the Core; native interception depends on
the host's hook support. Then give your coding agent the following setup prompt
(replace the path with your checkout):

```text
Set up agent-guard from /absolute/path/to/agent-guard for this workspace.
First identify the current harness and its actual hook/skill capabilities;
read this README and the matching adapter README. Check Python and Git.
Install the relevant Skills, then configure a native shell hook only if this
harness supports one. Preserve existing settings and show me the proposed
diff before editing user-wide configuration or installing dependencies.
For Claude Code use adapters/claude/README.md; for Kimi Code use
adapters/kimi-code/README.md; for DSH use adapters/dsh/README.md.
For Codex or a host without a verified hook, set up Skill/CLI use and say
plainly that automatic interception is not enabled.
Verify a harmless command and pass a BLOCK-shaped command only as data to
check.py; never execute a destructive test command. Report what was actually
installed, what the host intercepted, and any unverified paths.
```

For manual setup and evidence limits, see the
[adapter matrix](docs/harness-capabilities.md) and the adapter README for your
host.

## Design principles

| Principle | Guarantee |
|---|---|
| **Stay in scope** | The guard blocks deletion of the workspace root, `.git`, and outside paths when the operation reaches it |
| **Make it recoverable** | Supported deletions relocate to `.agent-trash/` with a manifest; destructive Git overwrites snapshot first |
| **Constrain authorization** | Authorization is session-scoped; a veto downgrades one-way, and only a human restores it |
| **Leave a durable trail** | Enforced verdicts, compensation intents, outcomes, and restores use append-only JSONL; mutation fails closed if its intent cannot be stored |

One rule runs through all four: **uncertainty increases restriction.**

## How it decides

Each inspected operation is classified by its effect and then mapped to the
least restrictive decision that preserves the relevant safety or recovery
guarantee. The stable interface is a Decision Protocol, not a binary
allow/block check:

```
Effect → Classifier → Policy → Decision   ∈ { ALLOW, SANITIZE, RELOCATE,
                                            SNAPSHOT, ASK, BLOCK }
                                + ReasonCode   (stable, machine-readable)
                                + Explanation  (human-facing)
                                + RecoveryPlan (txids, strategy)
```

| Tier | Decisions | What the agent experiences |
|---|---|---|
| **SAFE** | `ALLOW` · `SANITIZE` · `RELOCATE` · `SNAPSHOT` | Runs silently; compensation is applied first where needed; recoverable mutations are restorable via txid. `SANITIZE` returns a plan for the *payload owner* to rewrite (not a command rewrite) |
| **AMBIGUOUS** | `ASK` | Single-execution authorization (`ASK_ONCE`) — e.g. compound shapes the guard cannot safely automate |
| **FORBIDDEN** | `BLOCK` | Refused with reason and remediation; never askable |

Precedence when several decisions meet in one operation, weakest to strongest:

```
ALLOW < SANITIZE < RELOCATE < SNAPSHOT < ASK < BLOCK
```

`SANITIZE` ranks *below* `ASK` deliberately: it is automatic (SAFE tier),
while `ASK` forfeits automation. A payload carrying both a sanitizable secret
and a shape that cannot be rewritten must `ASK` — you cannot silently proceed
when part of the emission is uninspectable.

True effect uncertainty (`$VAR` targets, `bash -c`, `find -delete`, stdin-fed
lists) stays on the BLOCK path: allowing it would forfeit the core guarantee.
Adapters map decisions onto their harness natively — DSH `PreToolDecision`,
Claude Code PreToolUse `ask`, or a deny carrying the explanation where no ask
exists.

## What Agent Guard includes

### `delete-guard`

Answers *"if this destroys something, can we come back?"* It runs before a
delete or destructive Git action when invoked through a supported adapter or
CLI, and compensates first when recovery is possible.

### `exfil-guard`

Answers *"if this leaves the machine, was it supposed to?"* Its cooperative
CLI checks text before an emission when the payload owner invokes it, returning
a redaction or escalation decision for supported patterns.

### `recovery-audit`

The incident-response companion for cases where prevention never ran or did not
cover the path. It establishes source precedence, distinguishes recovered bytes
from reconstructed behavior and known gaps, audits replay tooling, and keeps
landing, commit, push, and release as separate authorization gates.

`delete-guard` and `exfil-guard` are the two preventive guard branches;
`recovery-audit` handles evidence-led recovery after the fact.

## recovery-audit

Sometimes prevention never ran: a harness had no adapter, a subagent bypassed
the expected path, or an over-broad command removed the workspace before anyone
could intervene. The working tree may be gone while the coding agent's session
cache still preserves successful patches, file snapshots, tool results, diffs,
and command context.

`recovery-audit` turns those remnants, Git remotes/reflogs/stashes, editor or
tool caches, build artifacts, and project plans into an evidence