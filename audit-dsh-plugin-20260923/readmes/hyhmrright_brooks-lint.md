<p align="center">
  <img src="assets/logo.svg" alt="brooks-lint" width="200">
</p>

<h1 align="center">brooks-lint</h1>

<p align="center">
  <strong>AI code reviews grounded in twelve classic engineering books.<br>
  Consistent. Traceable. Actionable.</strong>
</p>

<p align="center">
  <strong>English</strong> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#the-six-decay-risks">The Six Decay Risks</a> •
  <a href="#what-it-looks-like">What It Looks Like</a> •
  <a href="#benchmark">Benchmark</a> •
  <a href="#installation">Installation</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.7.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-blueviolet.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Codex_CLI-Skill-orange.svg" alt="Codex CLI Skill">
  <img src="https://img.shields.io/github/stars/hyhmrright/brooks-lint?style=social" alt="GitHub Stars">
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/47738" target="_blank"><img src="https://trendshift.io/api/badge/trendshift/repositories/47738/daily?language=JavaScript" alt="#2 JavaScript Repository of the Day | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</p>

<p align="center">
  <img src="assets/banner-en.svg" alt="Your code → 12 classics → 12 decay risks → cited findings" width="900">
</p>

<p align="center">
  <a href="https://hyhmrright.github.io/brooks-lint/"><img src="assets/demo.gif" alt="brooks-lint reviewing code: a /brooks-review command produces a 28/100 health score and cited Symptom → Source → Consequence → Remedy findings" width="820"></a>
</p>

<p align="center">
  <strong><a href="https://hyhmrright.github.io/brooks-lint/">→ Visit the website</a></strong>
</p>

---

> *"The bearing of a child takes nine months, no matter how many women are assigned."*
> — Frederick Brooks, *The Mythical Man-Month* (1975)

**50 years later, Brooks was still right — and so were McConnell, Fowler, Martin, Hunt & Thomas, Evans, Ousterhout, Winters, Meszaros, Osherove, Feathers, and the Google Testing team.**

Most code quality tools count lines and cyclomatic complexity. **brooks-lint** goes deeper — it diagnoses your code against six decay risk dimensions synthesized from twelve classic engineering books, producing structured findings with book citations, severity labels, and concrete remedies every time.

For the full source-to-skill mapping, including exceptions and false-positive guards, see
[`skills/_shared/source-coverage.md`](skills/_shared/source-coverage.md).

## Quick Start

```bash
# Claude Code
/plugin marketplace add hyhmrright/brooks-lint
/plugin install brooks-lint@brooks-lint-marketplace

# Any other Agent Skills platform — Cursor · Codex · Gemini · Copilot · Windsurf · OpenCode · Kiro · Bob …
curl -fsSL https://raw.githubusercontent.com/hyhmrright/brooks-lint/main/scripts/install.sh | bash -s -- <platform>
```

Then just ask ("review this PR", "audit the architecture"), or run one of the six commands —
`/brooks-review`, `/brooks-audit`, `/brooks-debt`, `/brooks-test`, `/brooks-health`, `/brooks-sweep`
([what each one does](#slash-commands)).

Every finding comes back as **Symptom → Source → Consequence → Remedy** with a book citation and a
0–100 Health Score. Full install options (10 more platforms) and CI/CD setup are [below](#installation).

## The Twelve Books

| Book | Author | Contributes to |
|------|--------|----------------|
| *The Mythical Man-Month* (1975) | Frederick P. Brooks Jr. | R2, R4, R5 |
| *Code Complete* (1993, 2nd ed. 2004) | Steve McConnell | R1, R4 |
| *Refactoring* (1999, 2nd ed. 2018) | Martin Fowler | R1, R2, R3, R4, R6 |
| *Clean Architecture* (2017) | Robert C. Martin | R2, R5 |
| *The Pragmatic Programmer* (1999, 20th Anniv. 2019) | Andrew Hunt & David Thomas | R2, R3, R4, R5, T2, T3 |
| *Domain-Driven Design* (2003) | Eric Evans | R1, R3, R6 |
| *A Philosophy of Software Design* (2018) | John Ousterhout | R1, R4 |
| *Software Engineering at Google* (2020) | Winters, Manshreck & Wright | R2, R5 |
| *The Art of Unit Testing* (2009, 3rd ed. 2023) | Roy Osherove | T1, T2, T4, T5 |
| *How Google Tests Software* (2012) | Whittaker, Arbon & Carollo | T5, T6 |
| *Working Effectively with Legacy Code* (2004) | Michael Feathers | T4, T5, T6 |
| *xUnit Test Patterns* (2007) | Gerard Meszaros | T1, T2, T3, T4 |

## The Six Decay Risks

brooks-lint evaluates your code across **six production-code decay risks** and **six test-suite decay risks** synthesized from twelve classic engineering books:

| Decay Risk | Diagnostic Question | Sources |
|------------|---------------------|---------|
| 🧠 Cognitive Overload | How much mental effort to understand this? | Code Complete, Refactoring, DDD, Philosophy of SD |
| 🔗 Change Propagation | How many unrelated things break on one change? | Refactoring, Clean Architecture, Pragmatic, SE@Google |
| 📋 Knowledge Duplication | Is the same decision expressed in multiple places? | Pragmatic, Refactoring, DDD |
| 🌀 Accidental Complexity | Is the code more complex than the problem? | Refactoring, Code Complete, Brooks, Philosophy of SD |
| 🏗️ Dependency Disorder | Do dependencies flow in a consistent direction? | Clean Architecture, Brooks, Pragmatic, SE@Google |
| 🗺️ Domain Model Distortion | Does the code faithfully represent the domain? | DDD, Refactoring |

> Philosophy of SD = *A Philosophy of Software Design* (Ousterhout) · SE@Google = *Software Engineering at Google* (Winters et al.)

## What It Looks Like

Given this code:

```python
class UserService:
    def update_profile(self, user_id, name, email, avatar_url):
        user = self.db.query(f"SELECT * FROM users WHERE id = {user_id}")
        user['email'] = email
        ...
        if user['email'] != email:   # always False — silent bug
            self.smtp.send(...)
        points = user['login_count'] * 10 + 500
        self.db.execute(f"UPDATE loyalty SET points={points} WHERE user_id={user_id}")
```

brooks-lint produces:

---

**Health Score: 28/100**

*This method concentrates four unrelated business responsibilities into a single function, contains a logic bug that silently suppresses email change notifications, and is wide open to SQL injection.*

### 🔴 Change Propagation — Single Method Changes for Four Unrelated Business Reasons
**Symptom:** `update_profile` performs profile field updates, email change notifications, loyalty points recalculation, and cache invalidation all in one method body.
**Source:** Fowler — *Refactoring* — Divergent Change; Hunt & Thomas — *The Pragmatic Programmer* — Orthogonality
**Consequence:** Any change to the loyalty formula risks breaking email notifications and vice versa. Every edit carries regression risk across four unrelated domains simultaneously.
**Remedy:** Extract `NotificationService`, `LoyaltyService`, and `UserCacheInvalidator`. `UserService.update_profile` should orchestrate by calling each — it should hold no implementation logic itself.

### 🔴 Domain Model Distortion — Silent Logic Bug: Email Notification Never Fires
**Symptom:** `user['email'] = email` overwrites the old value before `if user['email'] != email` — the condition is always `False`. The notification is dead code.
**Source:** McConnell — *Code Complete* — Ch. 17: Unusual Control Structures
**Consequence:** Users are never notified when their email address changes. Silent data integrity failure — the system appears functional while violating a business rule.
**Remedy:** Capture `old_email = user['email']` before any mutation. Compare against `old_email`, not `user['email']`.

*(+ 6 more findings including SQL injectio