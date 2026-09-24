# Anchorlaw — Code Verification on DeepSeek Harness

**[English](README.md) | [中文](README_zh.md)**

> **"Any claim must have a verifiable practice anchor."**
>
> — First Law, Materialist Practice Theory

Anchorlaw is a **code verification toolchain for AI-assisted (vibe) coding**, maintained as a **DeepSeek Harness (DSH) host adaptation**: the `dsh/` subtree ships 11 protocol skills, 4 model tools, and the `anchorlaw` agent preset — install once, and every DSH session gets scan / report / noise-card / AI-context tooling. The underlying protocol (`spec/`, `python/`, `typescript/`) is language-neutral and drives the DSH tools. The Reasonix host format is **archived, not maintained** — see [Reasonix Version Archive](#reasonix-version-archive).

---

## Quick Start (DSH)

```powershell
# 1. install once (host-level default): preset + user skills + global tool mount
pwsh dsh/scripts/install.ps1
# 2. six-item self-check: toolchain / skill manifest / self-scan / installed artifacts / tool schemas / preset rows
pwsh dsh/scripts/selfcheck.ps1
# 3. open a NEW DSH session → 4 anchorlaw_* tools + 11 anchor-* skills in every session
```

Project-scoped skills need no installer: place them under `<projectRoot>/.dsh/skills/` (DSH's native project root, rank 100) and any preset discovers them. DSH has no project-level plugin/preset mechanism, so the `anchorlaw` preset and the 4 tools are host-level only.

> Tools appear in **new** sessions (session composition is fixed at creation). The global mount is gated by a tool-schema check (2026-08-13 incident guard) — a malformed schema can never be installed.

## What You Get (DSH)

### 4 model tools — global, every session

| Tool | What it does |
|------|--------------|
| `anchorlaw_scan` | Level-1 defensive-pattern scanner (P1-P6; `lang` cpp/go/java → annotation extraction) |
| `anchorlaw_report` | Health report (scan findings + noise backlog + verdict) |
| `anchorlaw_ai_context` | Noise cards + curriculum export for LLM context injection |
| `anchorlaw_status` | Toolchain versions + discovered `anchor-*` skills |

### 11 protocol skills (`anchor-*`, DSH format)

L0-L4 action skills + execution roles (scout/worker/judge), loaded per scenario; skill bodies live in `dsh/skills/` (single source of truth, protocol §14 is the host-neutral spec). Trigger index and tool-call conventions: `dsh/AGENTS.md`.

### anchorlaw agent preset

Judge-driven four-stage pipeline persona (protocol §15.4): input contract → implementation spec → plan → parallel implementation → delivery. Acceptance criteria first, 3-round hard stop, `confirmed` granted **only by the human**; scout/worker/judge delegated through isolated subagents.

---

## Protocol Core (language-neutral backend)

The protocol itself lives at the repo root and is host-neutral — the DSH tools drive its CLI:

| Component | Where | State |
|-----------|-------|-------|
| **Spec** | `spec/protocol-v0.23.md` | Language-agnostic code-verification protocol (current) |
| **Python** | `python/anchorlaw-scanner` + `python/anchorlaw` | Scanner (verified) + anchors/noise/CLI (experimental) — the DSH tool backend |
| **TypeScript** | `typescript/anchorlaw-scanner` | TS/JS scanner (in development) |

### Component Maturity

| Component | Python | TypeScript | Maturity |
|-----------|--------|-----------|----------|
| **Scanner** | ✅ [anchorlaw-scanner](python/anchorlaw-scanner/) | ✅ [anchorlaw-scanner](typescript/anchorlaw-scanner/) | **VERIFIED** — tested on real projects |
| **Anchors** | ✅ [anchorlaw](python/anchorlaw/) | — | **EXPERIMENTAL** — API stable, no efficacy data |
| **Source Provenance (v0.3/v0.7)** | ✅ `source` param + probe type (v0.7) | — | **SCOPED** — implemented in Python; 1 project (CoreSwap) produced sourced anchors |
| **Noise Cards** | ✅ [anchorlaw](python/anchorlaw/) | — | **UNVERIFIED** — schema defined, no accumulated data |
| **AI Context** | ✅ [anchorlaw](python/anchorlaw/) | — | **CONJECTURE** — format defined, no A/B test |
| **Degraded Verification (v0.3)** | — | — | **CONJECTURE** — modes defined, not exercised beyond the reference host |

> **Honesty notice**: Components marked EXPERIMENTAL, UNVERIFIED, or CONJECTURE are working hypotheses. Their value has not been demonstrated through practice. Use them to help us test the hypotheses — not because we claim they work.

### Changelog

> **v0.23 (2026-09-23):** DSH host-adaptation carrier migration — upstream DeepSeek Harness 0.1.7 replaced the agent-preset carrier: a preset is no longer a `$DSH_HOME/.agent-presets/<id>/` directory but a `@deepseek-ai/dsh-agent-preset` declaration row carried by a **bundle patch**, and nothing reads the legacy directory any more (sessions whose header recorded such a preset could no longer be resumed). The DSH adaptation (`dsh/`) therefore became a first-class bundle package; its preset's plugin row is addressed by **bare package subpath** (rows inside `config.plugins[]` are not path-anchored, and the preset subtree's `baseUrl` is the profile directory, not the bundle); and the 11 anchor-* skills install to the user-global root instead of being embedded in the preset. The project-level (Reasonix-style) install mode is **withdrawn** — DSH has no project-level plugin/preset mechanism, so a project-scoped install could deliver the skills but never the preset persona or the four tools; project-scoped skills remain available through DSH's own `<projectRoot>/.dsh/skills` root. The preset-row gate now walks the bundle-patch carrier and `config.plugins[]` (the previous walk missed 27 of 28 rows — the exact reason a green self-check coexisted with a failing resume). The protocol core is unchanged — this is §16 host-adaptation scope.
>
> **v0.22 (2026-09-15):** Verification temporality, criterion preconditions, equivalence tiers, process invariants — five clauses closing gaps practice had already paid for (CoreSwap #156/#160/#161/#162 + M11/M16): ① **§9.8 verification temporality** — a verification action's in-place side effects MUST carry an addressable inverse or an explicit irreversible declaration (registration only; automatic rollback is forbidden because failed-round evidence is the more valuable artifact); ② **criterion preconditions** — an acceptance criterion declares the external facts it depends on, and a lapsed premise **suspends** the criterion while never auto-changing any status; ③ **§9.7.1 equivalence tiers** — E1 same-carrier / E2 cross-carrier (compare only the mutually declared key set `S`) / E3 interleaving-unknown, plus the partial-equivalence honesty clause and an invalid-declaration list (named on its own axis, not reusing the §9.1 capability modes); ④ **§15.4 PI-1** — a halted pipeline is terminal and MUST NOT be silently inherited (PI-2 is registered unverified with its acyclicity premise stated); ⑤ **§14.7 reference integrity** — the protocol audits its own live citations at the decidable layer only. Evidence status is registered per clause in §8/§11 — most are `scoped` by design: the clause exists so hosts have one authoritative target to implement and to falsify.
>
> **v0.21 (2026-09-15):** DSH host-adaptation capability parity + fail-closed preset gate — the `anchorlaw` agent preset now tracks the upstream standard preset's row surface (`command-goal`, `tool-subagent-codex`, `tool-subagent-claude-code`, `tool-ralph`, `present`; the three optional external-agent/workflow rows stay `disabled: true` exactly as upstream ships them — enabling requires installing the matching Bundle). A composition `name:` that no longer resolves makes the whole preset fail to mount (sessions cannot be created/resumed), so preset-row resolvability is now a fail-closed self-check item (`dsh/tests/audit_preset_rows.mjs`, item 6) catching upstream renames/removals at maintenance time instead of at resume time; the outstanding rename (`dsh-workflow-worker-thread` → `dsh-workflow-ptc`) is closed. The protocol core is unchanged — this is §16 host-adaptation scope.
>
> **v0.20 (2026-0