<div align="center">
  🌏 <a href="./README.zh.md">中文</a> · <b>English</b>
</div>

<h1 align="center">Three-in-One Console · dsh-s-m-c-center</h1>

<div align="center">
  <b>One DeepSeek Harness (DSH) settings page for the agent's three kinds of tools —<br />skills, MCP servers and local CLIs — plus per-conversation skill injection.</b>
  <br /><br />
  <i>Skill linking · Session injection · Shadow catalog · Real MCP connections · CLI probes · Bilingual · Zero source patching</i>
  <br /><br />
  <a href="https://github.com/YpipaQ/dsh-s-m-c-center/releases"><img alt="release" src="https://img.shields.io/github/package-json/v/YpipaQ/dsh-s-m-c-center?style=flat-square&amp;label=release&amp;color=fe7d37&amp;labelColor=555" /></a>
  <a href="https://github.com/YpipaQ/dsh-s-m-c-center/stargazers"><img alt="stars" src="https://img.shields.io/github/stars/YpipaQ/dsh-s-m-c-center?style=flat-square&amp;label=stars&amp;color=f0a01e&amp;labelColor=555" /></a>
  <a href="https://github.com/YpipaQ/dsh-s-m-c-center/forks"><img alt="forks" src="https://img.shields.io/github/forks/YpipaQ/dsh-s-m-c-center?style=flat-square&amp;label=forks&amp;color=2b8df5&amp;labelColor=555" /></a>
  <a href="https://www.npmjs.com/package/dsh-s-m-c-center"><img alt="npm" src="https://img.shields.io/npm/v/dsh-s-m-c-center?style=flat-square&amp;label=npm&amp;color=cb3837&amp;labelColor=555" /></a>
  <a href="https://www.npmjs.com/package/dsh-s-m-c-center"><img alt="total downloads" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.npmjs.org%2Fdownloads%2Fpoint%2F2026-08-26%3A2030-01-01%2Fdsh-s-m-c-center&amp;query=%24.downloads&amp;label=total%20downloads&amp;style=flat-square&amp;color=2ea44f&amp;labelColor=555" /></a>
  <a href="./LICENSE"><img alt="license: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square&amp;labelColor=555" /></a>
  <a href="./package.json"><img alt="dsh" src="https://img.shields.io/badge/dsh-%3E%3D0.1.2--alpha.2-4d6bfe?style=flat-square&amp;labelColor=555" /></a>
  <a href="./package.json"><img alt="node" src="https://img.shields.io/node/v/dsh-s-m-c-center?style=flat-square&amp;labelColor=555" /></a>
  <br /><br />
  <a href="#-what-it-is">What it is</a> · <a href="#-screenshots">Screenshots</a> · <a href="#-features">Features</a> · <a href="#-two-channels-linking-vs-injection">Two channels</a> · <a href="#-two-tools-for-the-agent">Agent tools</a> · <a href="#-architecture">Architecture</a> · <a href="#-install">Install</a> · <a href="#-configuration">Configuration</a> · <a href="#-permissions-and-dependency-disclosure">Permissions</a> · <a href="#-development">Development</a> · <a href="#-license">License</a>
</div>

<br />

<div align="center">
  <a href="https://raw.githubusercontent.com/YpipaQ/dsh-s-m-c-center/main/docs/shots/shot-skills.png"><img src="https://raw.githubusercontent.com/YpipaQ/dsh-s-m-c-center/main/docs/shots/shot-skills.png" alt="Tool manager settings page: Skills tab" width="86%" /></a>
  <p><i>Settings → Web UI plugins → Tool manager: the unified store, skill linking and the session default, with one tab per tool family.</i></p>
</div>

> [!NOTE]
> **As of 0.1.2 the skill catalog is served by this plugin (shadow catalog)**: catalog membership follows the conversation's injection selection exactly; a catalog change publishes one replacement frame instead of re-appending every step; container directories (DESCRIPTION.md only) are injectable and loadable. Verified by a three-round external test run (16/16 pass).

## ✨ What it is

> Chinese name: **三合一工具台** (three-in-one console) ｜ UI entry: Settings → Web UI Plugins → Tool Manager ｜ Aliases: 工具管理, 工具中心, 技能管理, MCP 服务器管理, CLI 工具管理, Skills / MCP / CLI manager

A self-contained DSH web plugin: it adds one first-class **settings page** for the agent's **three kinds of tool** (skills / MCP servers / local CLI tools), plus a **per-conversation skill injection layer**; a guide tab explains how each of the three works and, at the bottom, hands everything back cleanly on uninstall.

| Capability | Native dsh web | With this plugin |
|---|---|---|
| Skill browsing / toggling | Edit skill directories by hand | One-click linking / unlinking in the settings page; canonical copies go into the store; `SKILL.md` is never touched |
| Per-conversation skill sets | — | Session default + sidebar panel + `skill_select`; each conversation stores only its difference from the default |
| Skill catalog (AI view) | Static directory scan | **Shadow catalog**: follows the conversation selection exactly, with one `smc-skill-index` index row |
| MCP servers | Hand-edit `mcp.json` | Form / JSON creation + one-off connection test + activate / archive switches |
| Local CLIs | — | Auto-discovery of skill-wrapped CLIs, system CLI registry, probes for installed / version / subcommands / API key |
| Intrusiveness | — | **Zero source changes**: one npm package + one profile bundle patch line |

| Tab | Manages | Under the hood |
|---|---|---|
| **Skills** | Browse / enable / disable / delete / import skills; the **session default** decides what a new conversation starts with | User level: canonical copies in `~/.dsh/S-M-C/skills` + directory junctions. Project level: frontmatter rewritten in place |
| **MCP servers** | Create / edit / test / activate / archive / delete MCP servers | Real `@deepseek-ai/dsh-mcp-client` connections (`mcp__<server>__<tool>`); archiving moves definitions into `S-M-C/mcp-archive.json` |
| **CLI tools** | Discover / probe local CLI tools; register system CLIs | Skill-embedded `scripts/run-cli` + `S-M-C/cli.json` |
| **Guide** | How each of the three kinds works, and what to do before uninstalling | Explanation lives here; the uninstall preparation sits at the bottom |

> Full documentation: [`docs/功能介绍.md`](./docs/功能介绍.md) and [`docs/架构.md`](./docs/架构.md) (Chinese).

## 📷 Screenshots

| | |
|---|---|
| **Conversation skills panel** ｜ adjust this conversation's injection from the sidebar | **MCP servers** ｜ real connections, one activate / archive switch each |
| <a href="https://raw.githubusercontent.com/YpipaQ/dsh-s-m-c-center/main/docs/shots/shot-session.png"><img src="https://raw.githubusercontent.com/YpipaQ/dsh-s-m-c-center/main/docs/shots/shot-session.png" alt="Sidebar conversation skills panel" width="98%" /></a> | <a href="https://raw.githubusercontent.com/YpipaQ/dsh-s-m-c-center/main/docs/shots/shot-mcp.png"><img src="https://raw.githubusercontent.com/YpipaQ/dsh-s-m-c-center/main/docs/shots/shot-mcp.png" alt="MCP servers tab" width="98%" /></a> |
| **CLI tools** ｜ discover / probe / register local CLIs | **Guide** ｜ how the three kinds work + uninstall escape hatch |
| <a href="https://raw.githubusercontent.com/YpipaQ/dsh-s-m-c-center/main/docs/shots/shot-cli.png"><img src="https://raw.githubusercontent.com/YpipaQ/dsh-s-m-c-center/main/docs/shots/shot-cli.png" alt="CLI tools tab" width="98%" /></a> | <a href="https://raw.githubusercontent.com/YpipaQ/dsh-s-m-c-center/main/docs/shots/shot-guide.png"><img src="https://raw.githubusercontent.com/YpipaQ/dsh-s-m-c-center/main/docs/shots/shot-guide.png" alt="Guide tab" width="98%" /></a> |

<p align="center"><i>Skill names, descriptions and MCP server details are redacted in the screenshots.</i></p>

## 💡 Features

- **Skills**: grouped by project / user level and by source (`.dsh/skills`, `.agents/skills`, `~/.dsh/skills`, `~/.agents/skills`). User-level skills are adopted into the **unified store** `~/.dsh/S-M-C/skills`; "enable" injects a directory junction in the skill root, "disable" removes it (`SKILL.md` is never touched). Project-level skills are managed in place through their frontmatter. Deletion is a two-step, physical delete — and it **only ever deletes the store's own canonical copy** (see below). Open a row for details (description / whenToUse / body); import by scanning any directory.
- **Session default and per-conversation injection**: the session default is what a brand-new conversation st