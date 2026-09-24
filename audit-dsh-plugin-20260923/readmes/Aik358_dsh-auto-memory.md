# 无问自忆 · 记忆不断线

**dsh-auto-memory** — *She remembers, unbidden.*

> **EN** Now, across windows, too. Context that survives windows, sessions, and tools
> **中文** 该想起的，自己浮现。跨窗口 · 跨会话 · 跨工具，记忆不断线

<p align="center">
  <a href="https://htmlpreview.github.io/?https://github.com/Aik358/dsh-auto-memory/blob/preview/docs/landing/index.html"><strong>🌐 Landing page (full feature tour · data flow · papers · screenshots)</strong></a>
</p>

<p align="center">
  <a href="docs/screenshots/promo/promo-0-banner-v4.png"><img width="820" alt="dsh-auto-memory hero: she remembers, unbidden" src="docs/screenshots/promo/promo-0-banner-v4.png"></a>
</p>

<p align="center">
  <a href="docs/screenshots/promo/promo-0-banner-v4.png"><img width="130" alt="hero" src="docs/screenshots/promo/promo-0-banner-v4.png"></a>
  <a href="docs/screenshots/promo/promo-1b-auto-recall.png"><img width="130" alt="auto recall" src="docs/screenshots/promo/promo-1b-auto-recall.png"></a>
  <a href="docs/screenshots/promo/promo-2-tour.png"><img width="130" alt="welcome tour" src="docs/screenshots/promo/promo-2-tour.png"></a>
  <a href="docs/screenshots/promo/promo-3-recall.png"><img width="130" alt="recall & crystallization" src="docs/screenshots/promo/promo-3-recall.png"></a>
  <a href="docs/screenshots/promo/promo-4-unattended.png"><img width="130" alt="unattended mode" src="docs/screenshots/promo/promo-4-unattended.png"></a>
  <a href="docs/screenshots/promo/promo-5-external.png"><img width="130" alt="external memory inheritance" src="docs/screenshots/promo/promo-5-external.png"></a>
  <a href="docs/screenshots/promo/promo-6-greeting.png"><img width="130" alt="scheduled greetings" src="docs/screenshots/promo/promo-6-greeting.png"></a>
</p>
<p align="center"><sub>Promo gallery · seven frames · click any thumbnail to view full size</sub></p>

<details>
<summary><b>Promo gallery, frame by frame</b> (expand and flip through)</summary>

#### Frame 1 · Hero — She remembers, unbidden

<p align="center"><img width="720" alt="hero" src="docs/screenshots/promo/promo-1-hero.png"></p>

#### Frame 2 · Auto Recall — A semantic model matches it and injects it before you ask

<p align="center"><img width="720" alt="auto recall" src="docs/screenshots/promo/promo-1b-auto-recall.png"></p>

#### Frame 3 · Welcome Tour — Every feature, explained and toggled on the spot

<p align="center"><img width="720" alt="welcome tour" src="docs/screenshots/promo/promo-2-tour.png"></p>

#### Frame 4 · Recall & Crystallization — Conversation condenses into skills, traceably

<p align="center"><img width="720" alt="recall" src="docs/screenshots/promo/promo-3-recall.png"></p>

#### Frame 5 · Unattended Mode — Runs all night, zero small talk, zero interruptions

<p align="center"><img width="720" alt="unattended" src="docs/screenshots/promo/promo-4-unattended.png"></p>

#### Frame 6 · External Memory Inheritance — Your other AIs feed her memory too

<p align="center"><img width="720" alt="external" src="docs/screenshots/promo/promo-5-external.png"></p>

#### Frame 7 · Scheduled Greetings — Every day remembered

<p align="center"><img width="720" alt="greeting" src="docs/screenshots/promo/promo-6-greeting.png"></p>

</details>

<p align="center">
  <a href="./README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-switch-lightgrey?style=for-the-badge"></a>
  <a href="./README.md"><img alt="English" src="https://img.shields.io/badge/English-current-blue?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@a9i5k4/dsh-auto-memory"><img alt="npm" src="https://img.shields.io/npm/v/@a9i5k4/dsh-auto-memory"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/License-BSD--3--Clause-yellow.svg"></a>
  <img alt="Runtime dependencies" src="https://img.shields.io/badge/runtime%20deps-0-brightgreen">
  <img alt="Platform" src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey">
</p>

<p align="center">
  <code>pnpm add @a9i5k4/dsh-auto-memory@latest</code>
</p>

<p align="center">
  <a href="docs/USER-GUIDE.en.md"><strong>📖 User guide</strong></a> ·
  <a href="docs/USER-GUIDE.zh-CN.md"><strong>📖 用户手册</strong></a> ·
  <a href="CHANGELOG.md">Changelog</a> ·
  <a href="https://htmlpreview.github.io/?https://github.com/Aik358/dsh-auto-memory/blob/main/docs/CONTRIBUTORS.html">Contributors &amp; Sponsors</a> ·
  <a href="https://qm.qq.com/q/v7Asxn6vPa">QQ group</a>
</p>

---

## The burned book keeps no book report

Everyone who does real work with AI knows the moment: halfway through, the context window fills, and she "forgets". Not for lack of intelligence — her thinking was compressed into a summary, like burning a whole book and keeping one line of book report. Why that fix failed, why that path dead-ended — all in the fire.

dsh-auto-memory never believed it had to be this way. She keeps memory outside the window: what should resurface, resurfaces unbidden; and everything she recalls has provenance — checkable, editable, deletable.

Now we push this route to its last missing piece — when the context fills, she no longer compresses herself. She **closes a notebook filled with margin notes and opens a new page**. The notebook stays within reach.

**Compression distorts, closed windows reset, tool switches zero out — starting from here, none of that holds.**

---

## Highlights in 30 seconds

| | |
|---|---|
| **Proactive recall, zero instructions** | Memory is never fetched by the model — the host watches context and recalls automatically, injected at a fixed boundary, prefix-cache friendly |
| **Three-layer memory engine** | User rules → project notes → daily logs; injected + on-demand recall |
| **Memory writes itself** | A subagent quietly evaluates every turn and files topic-grouped entries — you never "remember to log" |
| **Every activation is auditable** | Each recall decision carries a full evidence chain, gradeable in the Recall review tab; skills crystallize from cross-session evidence |
| **Proactive reminders** | The AI spots deadlines and promises in conversation, files them into the calendar and reminds you later |
| **Everything is a switch** | Welcome tour + settings page, every feature individually toggleable (incl. unattended mode) |
| **External memory inheritance** | Memories from WorkBuddy / CodeBuddy / Claude Code / Codex are scanned, importable, per-source managed |
| **Production-grade hygiene** | Write gate (mojibake/stutter/JSON-injection blocking) + dirty-token scanner + credentials never enter prompts |
| **Astra-style context management** | A filling context no longer collapses into one summary — four-part handoff notes carry work across windows, full history stays searchable, the agent retrieves on demand (on by default, threshold 0.75) |
| **No cross-talk between workspaces** | Open several workspaces or sessions at once and each keeps its own recall decisions and index cache. Clicking into one never disturbs the one that's running |
| **Model-agnostic** | No vendor lock, no tier lock: any model on DSH works out of the box — lexical 0GB floor, built-in ~130MB semantic tier, advanced 563MB |
| **Portable memory** | Everything lives on your own disk; memories scan in from other AI tools, every entry has an evidence chain — auditable, deletable. Memory belongs to you, not to any vendor |

---

## Four things we poured our heart into

Four features in this plugin were raised one by one, by hand; everything else — calendar, search, the mind map, unattended mode, memory hygiene — grows around them.

### The first · She takes notes, and she says welcome back

The earliest version of this plugin learned two small things: after every conversation, it wrote down what was worth keeping, unprompted; and when you returned from time away, or in the morning, afternoon, and late-night hours, it greeted you in a fitting tone. Simple — but these two acts set her character: memory is not a database, a greeting i