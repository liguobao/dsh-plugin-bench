<!-- SkillHub is the live hosted product; this repository contains the open-source corpus,
     retrieval, evaluation, export, and plugin layer behind it. -->

<div align="center" id="readme-top">

<table width="100%" border="1" bordercolor="#d9d9d9" cellspacing="0" cellpadding="0">
<tr><td><img src="https://github.com/user-attachments/assets/2ef7e877-275d-4115-8ddf-f9b49de8ff5d" alt="SkillCorpus banner" width="100%"></td></tr>
</table>

<p align="center">
  <a href="https://arxiv.org/abs/2607.15557"><img src="https://img.shields.io/badge/arXiv-2607.15557-b31b1b?labelColor=gray&style=for-the-badge" alt="Paper"></a>
  <a href="https://huggingface.co/EverMind-AI"><img src="https://img.shields.io/badge/HuggingFace-EverMind-F5C842?labelColor=gray&style=for-the-badge&logo=huggingface&logoColor=white" alt="Hugging Face"></a>
  <a href="https://discord.gg/gYep5nQRZJ"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdiscord.com%2Fapi%2Fv10%2Finvites%2FgYep5nQRZJ%3Fwith_counts%3Dtrue&query=%24.approximate_presence_count&suffix=%20online&label=Discord&color=404EED&labelColor=gray&style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://github.com/EverMind-AI/EverOS/discussions/67"><img src="https://img.shields.io/badge/WeCom-EverMind_%E7%A4%BE%E5%8C%BA-07C160?labelColor=gray&style=for-the-badge&logo=wechat&logoColor=white" alt="WeCom"></a>
</p>

<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>


</div>

<br>

## What SkillCorpus gives you

SkillCorpus is EverMind's open-source pipeline for turning scattered `SKILL.md` files from public
repositories into reliable agent context. It aggregates sources, applies safety and license gates,
evaluates quality, and matches task-specific skills before the agent answers.

You can use the live [SkillHub](https://evermind.ai/skillhub) without cloning this repository. Clone
SkillCorpus when you want the open-source machinery behind that experience:

- **Build your own skill layer** — point the pipeline at your own source registry, apply the
  curation, safety, and license gates, and export a corpus for your agents.
- **Change the behavior** — modify the taxonomy, quality and dedup rules, retrieval recipe, export
  schema, evaluation suites, or host plugins.
- **Keep control of deployment** — self-host the released retrieval models and connect your own
  agent host instead of using the hosted SkillHub API.

The core code is Apache-2.0 licensed (`match/` and `evaluate/` are MIT); each skill retains its
upstream license. The public 1,000-skill demo, three agent benchmarks, and live SkillHub show the
result.

https://github.com/user-attachments/assets/4d9a3241-df13-4b20-9798-fb7920069995

<br>

## &#128293; Latest Updates

- **2026-09-17 · v0.4.0** Adds a **shared skills library** across all six hosts: they read one `~/.evermind-skillsearch/` directory and register their own, so a skill you have in one agent is available in the rest; skills retrieved from a catalog are **kept** instead of discarded at the end of the turn; and changes take effect **on the next turn, with no restart**. Raven and Hermes also gain `skills_dirs` / `SKILLSEARCH_SKILLS_DIRS`.
- **2026-09-02** Adds OpenClaw 2.0 support and smarter skill delivery: retrieve automatically on every query, or let the main agent call `skill_search` on demand.
- **2026-08-27** Supports multi-source retrieval across local skills, EverMind SkillHub, ClawHub, and skillhub.cn, with filtering, deduplication, and final 0–2 selection.
- **2026-08-26** Supports PathGuard placeholder resolution and host-aware paths for skill files and agent workspaces.
- **2026-08-25** Adds official SkillCorpus plugins for WorkBuddy, OpenClaw, Hermes, Raven, and DeepSeek Harness.

<br>

## Stronger agents, one turn at a time

At answer time, the practical difference is a retrieval layer: SkillHub selects vetted procedural
knowledge for the task and puts it into the agent's context.

<table width="100%">
<tr>
<th>Dimension</th>
<th>Without SkillCorpus</th>
<th>With SkillCorpus</th>
</tr>
<tr>
<td><strong>Context</strong></td>
<td>Model knowledge plus a manually maintained prompt.</td>
<td>Task-specific, license-audited <code>SKILL.md</code> retrieved automatically or on demand.</td>
</tr>
<tr>
<td><strong>Execution</strong></td>
<td>Generic workflows can miss exact steps, edge cases, or supporting scripts.</td>
<td>Procedures, references, and optional scripts arrive before execution.</td>
</tr>
<tr>
<td><strong>Integration</strong></td>
<td>Each host maintains its own collection of task instructions.</td>
<td>One curated skill layer serves OpenClaw, Hermes, Raven, WorkBuddy, DeepSeek Harness, and other hosts.</td>
</tr>
</table>

The result is the same agent with better task-specific procedures available at the moment it needs
them — stronger execution without asking users to memorise skill names or wire up tool calls.

<br>

## Results

Pass rate with no skills → with SkillCorpus, same harness, same backbone
([paper, Table 1](https://arxiv.org/abs/2607.15557)):

| Harness × backbone | SkillsBench | GDPVal | QwenClawBench |
|---|---|---|---|
| OpenClaw × Qwen3.5-27B | 8.8 → **13.0** | 81.2 → **83.1** | 65.2 → **66.7** |
| OpenClaw × Qwen3.5-397B | 11.1 → **16.9** | 82.2 → **84.0** | 65.7 → **67.0** |
| Raven × Qwen3.5-27B | 10.0 → **16.5** | 82.6 → **83.8** | 66.9 → **70.8** |
| Raven × Qwen3.5-397B | 9.2 → **22.6** | 84.0 → **85.2** | 68.8 → **73.2** |
| **Pooled ∆** | **+7.5**±2.3 (z=3.2) | **+1.51**±0.49 (z=3.1) | **+2.79**±0.70 (z=4.0) |

The gain is largest where the task needs procedural knowledge the model does not already have
(SkillsBench), and smallest on open-ended economic tasks it can already do (GDPVal).

<br>

## SkillHub integrations

SkillHub brings skill retrieval to the five agent platforms below. Choose a platform to open its
plugin guide:

<table width="100%">
<tr>
<td width="400" align="center"><a href="skillcorpus_plugin/engine-typescript/README.md"><img src="https://avatars.githubusercontent.com/u/148330874?s=200&amp;v=4" alt="DeepSeek Harness" width="72"><br><strong>DeepSeek Harness</strong></a></td>
<td width="400" align="center"><a href="skillcorpus_plugin/plugin-hermes/README.md"><img src="https://github.com/user-attachments/assets/477eebc4-e615-4425-921e-368d7667e491" alt="Hermes" width="72"><br><strong>Hermes</strong></a></td>
<td width="400" align="center"><img src="https://github.com/user-attachments/assets/01d948fe-1e2b-48e8-9b32-b8057cb3f336" alt="OpenClaw" width="72"><br><strong>OpenClaw</strong><br><a href="skillcorpus_plugin/plugin-openclaw/README.md">1.x</a> / <a href="skillcorpus_plugin/plugin-openclaw2/README.md">2.0</a></td>
<td width="400" align="center"><a href="skillcorpus_plugin/plugin-raven/README.md"><img src="https://github.com/user-attachments/assets/27e1ea63-69d4-48b3-a884-7f0355926907" alt="Raven" width="72"><br><strong>Raven</strong></a></td>
<td width="400" align="center"><a href="skillcorpus_plugin/plugin-workbuddy/README.md"><img src="https://github.com/user-attachments/assets/ab2157dc-90fc-4196-bbf3-87066820f7b4" alt="WorkBuddy" width="72"><br><strong>WorkBuddy</strong></a></td>
</tr>
</table>

Two modes, one setting. **On demand** — the default — gives the agent a `skill_search` tool and
lets it decide: a long task pays for retrieval at the step that needs it and nothing on the turns
that do not. **`mode: auto`** is the older behaviour: search every turn, before the model answers,
with no tool call and no skill names to memorise. They are exclusive; running both would search
twice for one turn.

OpenClaw ships as two packages, because 2.0 dropped the hook the 1.x plugin injects through:
`plugin-openclaw` for releases up to 2026.7.x, `plugin-openclaw2` for 2.0 (2026.8.1) and newer.
The packaged Raven plugin installs and its on-demand mode works today; `mode: auto` there will
claim the `skills` stage once Raven merges its upstream `context_segments` slot, and is