<div align="center">

<img src="docs/social-preview-distilly-v7.png" alt="Distilly — Distill how they think into Person Profiles for Agents" width="100%">

<br>

# 🧬 Distilly

**Formerly: Colleague Skill / colleague-skill.**

### Distill a person's experience, judgment, voice, and ways of working into a reusable Person Profile for AI agents and compatible bots.

**Messages · documents · interviews · public sources → Distilly → Person Profile → Agent / Bot**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)
[![Stars](https://img.shields.io/github/stars/titanwings/colleague-skill?style=social)](https://github.com/titanwings/distilly/stargazers)

[![Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2?logo=discord&logoColor=white)](https://discord.gg/NVX66RxWZv)

<br>

<table>
<tr><td align="left">

🧑‍💼 &nbsp;Your colleague quit, your mentor graduated, your teammate transferred — taking their whole playbook and context with them?<br>
💞 &nbsp;Your family, old friends, partner drifting apart — and you want to hold on to the way it felt to be with them?<br>
🌟 &nbsp;Your favorite author, idol, thinker you'll never meet — but you want to know what they'd say about your question?

</td></tr>
</table>

### ✨ One project, many kinds of people.

<br>

Distilly is the person-modeling layer for agents. It turns the materials you provide into a portable, source-grounded Person Profile built from observable experience, decision patterns, expression, and ways of working; it does not claim to clone the person behind them.

Colleagues · partners · family · old friends · idols · public figures · fictional characters — even yourself

**Source material + your description → a source-grounded Person Profile → your Agent or compatible Bot**

> A Person Profile is the reusable output. The current release packages each profile as an Agent Skill so supported hosts can install and invoke it. The canonical creator Skill is named `distilly`; install it in a `distilly` directory. The former name above remains for search continuity and project history.

<br>

[🆕 What Distilly does](#-what-distilly-does-today) · [📦 Data Sources](#-supported-data-sources) · [⚡ Install](#-install) · [🚀 Usage](#-usage) · [✨ Demo](#-demo) · [📝 Citation](#-citation) · [💬 Discord](https://discord.gg/NVX66RxWZv)

[**Chinese**](docs/lang/README_ZH.md) · [**Spanish**](docs/lang/README_ES.md) · [**German**](docs/lang/README_DE.md) · [**Japanese**](docs/lang/README_JA.md) · [**Russian**](docs/lang/README_RU.md) · [**Portuguese**](docs/lang/README_PT.md) · [**Korean**](docs/lang/README_KO.md)

</div>

---

<div align="center">

### 🎉 2026.08.13 Milestone — **the project has passed 20K ⭐!**

Massive thanks to everyone who starred — we'll keep shipping, keep distilling.

</div>

> 🧬 **2026.08.24 Update** — The creator is now named **Distilly** end to end and documents native local Skill discovery for Claude Code, Hermes, OpenClaw, Codex, DeepSeek Harness, Pi, Grok Build, and OpenCode. Grok Bot is listed separately as a saved-Skill workflow preview.

> 📝 **2026.06.01 Update** — **[The COLLEAGUE.SKILL technical report](https://arxiv.org/pdf/2605.31264) is now available**. The most rewarding part was not simply publishing a paper, but seeing the community grow the gallery to 215 skills contributed by 165 people, with more than 100,000 stars across the skill cards. The paper's Acknowledgements explicitly recognize every community contributor.

> 🗺️ **2026.04.13** — **The Distilly Roadmap is live!** What began as Colleague Skill is growing beyond colleagues: distill people into Skills that Agents can reuse. 👉 **[Full Roadmap](ROADMAP.md)** · **[💬 Discord](https://discord.gg/NVX66RxWZv)**

> 🌐 **2026.04.07** — Community gallery is live! Any skill / meta-skill can drive traffic directly to your own GitHub repo. No middleman. 👉 **[titanwings.github.io/colleague-skill-site](https://titanwings.github.io/colleague-skill-site/)**

<div align="center">

Created by [@titanwings](https://github.com/titanwings)

</div>

---

## 🆕 What Distilly does today

### 1️⃣ From Colleague Skill to Distilly

The project is no longer limited to the colleague scenario. Its `distilly` creator builds source-grounded Person Profiles for three person families with one workflow, then packages each profile as an Agent Skill.

### 2️⃣ Three character families

<table>
<thead>
<tr>
<th width="33%" align="center">🧑‍💼 colleague</th>
<th width="33%" align="center">💞 relationship</th>
<th width="33%" align="center">🌟 celebrity</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><sub>Coworkers · mentors · teammates · up/downstream partners</sub></td>
<td align="center"><sub>Exes · partners · parents · friends · close family</sub></td>
<td align="center"><sub>Public figures · creators · public voices · fictional characters</sub></td>
</tr>
<tr>
<td><sub>Builds a Work Skill + Persona from material-derived technical standards, workflows, expression, and workplace behavior. Supports Lark / DingTalk / Slack collection.</sub></td>
<td><sub>Organizes material-derived expression patterns, emotional triggers, conflict patterns, and repair patterns into a reusable Persona Skill.</sub></td>
<td><sub>Ships with a <b>six-dimension research toolchain</b> (subtitles → transcript cleanup → research merge → quality check) for organizing observable decisions, expression, and mental models.</sub></td>
</tr>
</tbody>
</table>

Each family has its own source-collection strategy, analysis dimensions, and Person Profile structure.

### 3️⃣ More Agent hosts

The old version only ran in Claude Code. Distilly now supports native local Skill discovery across eight agent hosts.

<table>
<tr>
<td align="center" width="25%"><a href="https://claude.ai/code"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/assets/hosts/claude-code-wordmark-dark.svg"><img src="docs/assets/hosts/claude-code-wordmark-light.svg" alt="Claude Code" height="28"></picture></a></td>
<td align="center" width="25%"><a href="https://github.com/NousResearch/hermes-agent"><img src="docs/assets/hosts/hermes-agent-wordmark.png" alt="Hermes Agent" height="32"></a></td>
<td align="center" width="25%"><a href="https://github.com/openclaw/openclaw"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/assets/hosts/openclaw-wordmark-dark.svg"><img src="docs/assets/hosts/openclaw-wordmark-light.svg" alt="OpenClaw" height="38"></picture></a></td>
<td align="center" width="25%"><a href="https://github.com/openai/codex" title="Codex"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/assets/hosts/codex-mark-dark.png"><img src="docs/assets/hosts/codex-mark-light.png" alt="Codex" height="64"></picture></a></td>
</tr>
<tr>
<td align="center" width="25%"><a href="https://github.com/deepseek-ai/deepseek-harness"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/assets/hosts/deepseek-wordmark-dark.svg"><img src="docs/assets/hosts/deepseek-wordmark-light.svg" alt="DeepSeek Harness" height="32"></picture></a></td>
<td align="center" width="25%"><a href="https://pi.dev/docs/latest/skills"><img src="docs/assets/hosts/pi-mark.svg" alt="Pi coding agent" height="46"></a></td>
<td align="center" width="25%"><a href="https://docs.x.ai/build/features/skills-plugins-marketplaces"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/assets/hosts/grok-build-mark-dark.png"><img src="docs/assets/hosts/grok-build-mark-light.png" alt="Grok Build" height="46"></picture></a></td>
<td align="center" width="25%"><a href="https://opencode.ai/docs/skills"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/assets/hosts/opencode-wordmark-dark.svg"><img src="docs/assets/hosts/opencode-wordmark-light.svg" alt="OpenCode" height="32"></p