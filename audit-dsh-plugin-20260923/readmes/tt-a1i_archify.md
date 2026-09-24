<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/archify-lockup-dark.svg" />
    <img src="docs/assets/archify-lockup-light.svg" alt="Archify" width="440" height="121" />
  </picture>
</p>
<h3 align="center">Turn anything you want to understand, plan, or share into an interactive visual.</h3>

<p align="center"><img src="docs/assets/archify-readme-hero.png" alt="Archify — interactive diagrams" width="960" /></p>

<p align="center">Start with an idea, a question, or a plan. Describe it to your AI agent, and Archify turns it into an interactive HTML you can explore, customize, and share. From travel itineraries and learning maps to complex systems—make it your own.</p>

<p align="center">See what the community is creating—and imagine what you could make next.</p>

<p align="center">
  <a href="https://tt-a1i.github.io/archify/gallery.html"><strong>Live demos</strong></a> &nbsp;·&nbsp;
  <a href="#start"><strong>Get started</strong></a> &nbsp;·&nbsp;
  <a href="https://tt-a1i.github.io/archify/guide.html"><strong>Scenario guide</strong></a> &nbsp;·&nbsp;
  <a href="#community"><strong>Community</strong></a> &nbsp;·&nbsp;
  <a href="./README_ZH.md"><strong>简体中文</strong></a>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/31352?utm_source=repository-badge&amp;utm_medium=badge&amp;utm_campaign=badge-repository-31352" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/repositories/31352" alt="tt-a1i/archify | Trendshift" width="250" height="55" /></a>
</p>

<p align="center">
  <a href="https://github.com/tt-a1i/archify/stargazers"><img src="https://img.shields.io/github/stars/tt-a1i/archify?style=flat-square&amp;color=E5B650&amp;logo=github&amp;label=Stars" alt="GitHub stars" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e?style=flat-square" alt="MIT License" /></a>
  <a href="archify/SKILL.md"><img src="https://img.shields.io/badge/Agent-Skill-7C3AED?style=flat-square" alt="Agent Skill" /></a>
  <a href="CHANGELOG.md#unreleased"><img src="https://img.shields.io/badge/version-2.17.0--dev.1-0891b2?style=flat-square" alt="Development version 2.17.0-dev.1" /></a>
</p>

<p align="center">
  <a href="https://tt-a1i.github.io/archify/"><img src="https://img.shields.io/badge/Website-0891B2?style=for-the-badge" alt="Archify website" /></a>
  <a href="https://discord.gg/6xWMjgCeUq"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&amp;logo=discord&amp;logoColor=white" alt="Join Archify on Discord" /></a>
  <a href="#community"><img src="https://img.shields.io/badge/WeChat-07C160?style=for-the-badge&amp;logo=wechat&amp;logoColor=white" alt="Archify WeChat group" /></a>
  <a href="#community"><img src="https://img.shields.io/badge/QQ-1688D8?style=for-the-badge&amp;logo=qq&amp;logoColor=white" alt="Archify QQ group" /></a>
  <a href="https://x.com/t20000622yy"><img src="https://img.shields.io/badge/Creator_on_X-181717?style=for-the-badge&amp;logo=x&amp;logoColor=white" alt="Follow the creator on X" /></a>
</p>

<p align="center"><a href="#sponsors"><strong>❤️ Partners & sponsors: Kimi Work · Supercode · EverMind/Raven</strong></a></p>

## See Archify in action

<p align="center">
  <a href="https://tt-a1i.github.io/archify/gallery.html"><img src="docs/assets/archify-live-proof.gif" alt="Three verified Archify artifacts moving through Signal Flow, Blueprint, and Classic presets" width="960"/></a>
  <br/>
  <sub><strong>Three real generated artifacts.</strong> Signal Flow · Blueprint · Classic · <a href="https://tt-a1i.github.io/archify/gallery.html">open the interactive Proof Lab ↗</a></sub>
</p>

**Click the preview to open real interactive artifacts.** The GIF shows the motion; the HTML lets you explore it yourself.

<a id="start"></a>

### Install, then describe your idea

Works with Cursor, Claude Code, Codex CLI, and OpenCode. See installation options below for additional integrations.

```bash
npx skills add tt-a1i/archify -g
```

Send this to your agent:

```text
Use Archify to diagram a web request: Browser calls the API,
the API checks Redis, and a cache miss queries PostgreSQL and fills the cache.
```

Then continue: “Add authentication”, “Highlight the cache-miss path”, or “Switch to the light theme”.

**No repository is required:** start with a description, or ask your agent to read a repository for a source-backed architecture diagram.

[Choose your agent](https://tt-a1i.github.io/archify/start.html?agent=cursor&type=architecture) · [Installation details and update checks](#quick-start)

<a id="sponsors"></a>

## ❤️ Sponsors

<p align="center">
  <a href="https://www.kimi.ai/?aff=archify"><img src="docs/assets/sponsors/archify-kimi-work.png" alt="Archify × Kimi Work collaboration banner" width="800" /></a>
</p>

**Archify × Kimi Work.** Find Archify in the Kimi Work plugin store as **Interactive Architecture Diagram**. Describe your system in one sentence to create an interactive diagram. **[Try it in Kimi Work →](https://www.kimi.ai/?aff=archify)**

<table>
<tr>
  <td align="center" width="240"><a href="https://supercode.sh/?utm_source=archify"><img src="https://cdn.supercode.sh/sponsors/supercode-logo.png" alt="Supercode" width="200"/></a><br/><strong><a href="https://supercode.sh/?utm_source=archify">supercode.sh</a></strong></td>
<td><a href="https://supercode.sh/?utm_source=archify">Supercode</a> sponsors Archify and enhances Codex and Cursor with token optimization, curated Skills, and spec-driven development. Archify is featured as a <a href="https://supercode.sh/en/skills/tt-a1i/archify/archify">Supercode Editor’s Choice</a> skill.<br/><br/><a href="https://supercode.sh/en/skills/tt-a1i/archify/archify"><img src="https://supercode.sh/badges/editors-choice.svg" alt="Supercode Editor’s Choice — Archify" width="240" height="55"/></a></td>
</tr>
<tr><td align="center" width="240"><a href="https://github.com/EverMind-AI/Raven"><img src="docs/assets/sponsors/evermind-archify-raven.png" alt="Archify × Raven" width="200" /></a><br/><strong><a href="https://github.com/EverMind-AI">EverMind</a> · <a href="https://github.com/EverMind-AI/Raven">Raven</a></strong></td><td>EverMind sponsors Archify and builds memory infrastructure for agents. Its <a href="https://github.com/EverMind-AI/Raven"><strong>Raven</strong></a> harness supports Archify as a Skill for verified, interactive system maps.</td></tr>
</table>

> Want to sponsor Archify? [Contact us by email.](mailto:2801884530@qq.com)

## Show what matters

| Explain an agent workflow | Follow a cache miss | Explore service relationships |
|---|---|---|
| [![Agent workflow playing one authored chapter](docs/assets/archify-demo-story.png)](https://tt-a1i.github.io/archify/gallery/artifacts/agent-tool-call.workflow.html?theme=dark&present=1&play=1#view=happy-path) | [![Cache-miss sequence showing the Web App to Postgres route](docs/assets/archify-demo-route.png)](https://tt-a1i.github.io/archify/gallery/artifacts/cache-miss.sequence.html?theme=dark&present=1#route=web~db) | [![Production architecture comparing backend and database roles](docs/assets/archify-demo-lens.png)](https://tt-a1i.github.io/archify/gallery/artifacts/production-deployment.architecture.html?theme=dark&present=1#lens=backend~database) |
| Walk through the steps defined in the diagram. | Highlight the path from web app to database. | Focus on authored backend and database connections. |

The [Proof Lab](https://tt-a1i.github.io/archify/gallery.html) contains all 11 checked-in scenarios, their JSON sources, named views, and validation receipts.

### Understand a real repository

<sub>CODE → DIAGRAM · A source-backed system map</sub>

[![MCO runtime architecture generated from the public mco-org/mco repository](docs/assets/mco-runtime-share-card.png)](https://tt-a1i.github.io/archify/cases/mco-runtime.architecture.html?theme=dark&present=1#view=dispatch-path)

Archify traced [`