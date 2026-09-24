# iPolloWork

<p align="center">
  English · <a href="./docs/translations/README_ZH.md">简体中文</a> · <a href="./docs/translations/README_ZH_hk.md">繁體中文</a> · <a href="./docs/translations/README_JA.md">日本語</a>
</p>

<p align="center">
  <a href="https://github.com/Devin-AXIS/iPolloWork/releases/latest"><img src="https://img.shields.io/github/v/release/Devin-AXIS/iPolloWork?display_name=tag&amp;sort=semver" alt="Latest release" /></a>
  <a href="https://github.com/Devin-AXIS/iPolloWork/releases"><img src="https://img.shields.io/github/downloads/Devin-AXIS/iPolloWork/total" alt="GitHub downloads" /></a>
  <a href="https://github.com/Devin-AXIS/iPolloWork/stargazers"><img src="https://img.shields.io/github/stars/Devin-AXIS/iPolloWork?style=flat" alt="GitHub stars" /></a>
  <a href="https://x.com/iPolloWork"><img src="https://img.shields.io/badge/X%20Global-%40iPolloWork%20%C2%B7%207.9K%20followers-000000?logo=x&amp;logoColor=white" alt="Follow iPolloWork on X" /></a>
  <a href="https://x.com/iPolloCN"><img src="https://img.shields.io/badge/X%20%E4%B8%AD%E6%96%87-%40iPolloCN%20%C2%B7%203.4K%20followers-000000?logo=x&amp;logoColor=white" alt="Follow iPolloCN on X" /></a>
  <a href="https://www.bestpractices.dev/projects/14127"><img src="https://www.bestpractices.dev/projects/14127/badge" alt="OpenSSF Best Practices" /></a>
  <a href="https://www.cloudflare.com/startups/"><img src="https://img.shields.io/badge/Cloudflare-for%20Startups-F38020?logo=cloudflare&amp;logoColor=white" alt="Cloudflare for Startups" /></a>
  <a href="https://github.com/opea-project"><img src="https://img.shields.io/badge/OPEA-Open%20Platform%20for%20Enterprise%20AI-ff7a00" alt="OPEA: Open Platform for Enterprise AI" /></a>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/88012?utm_source=trendshift-badge&amp;utm_medium=badge&amp;utm_campaign=badge-trendshift-88012"><img src="https://trendshift.io/api/badge/trendshift/repositories/88012/daily?language=TypeScript" alt="#22 TypeScript Repository Of The Day | Trendshift" width="250" height="55" /></a>
  <a href="https://trendshift.io/repositories/88012?utm_source=trendshift-badge&amp;utm_medium=badge&amp;utm_campaign=badge-trendshift-88012"><img src="https://trendshift.io/api/badge/trendshift/repositories/88012/weekly?language=TypeScript" alt="#24 TypeScript Repository Of The Week | Trendshift" width="250" height="55" /></a>
</p>

**The enterprise-grade, local-first Agent Workbench for people and agent teams—one workspace for multiple agent engines, one unified system for plugins and Skills, multi-agent projects and tasks, and editable creation across code, documents, presentations, websites, design, and video.**

https://github.com/user-attachments/assets/201b561a-22ec-4c8e-a4e8-f34172cf0aa3

iPolloWork is the unified workspace layer for the next agent-native way of working. It does not split projects or extensions by runtime: teams coordinate agents, tasks, schedules, plugins, Skills, tools, execution, and editable outputs from one control surface. Describe the outcome; agents plan and execute; your team reviews progress, approves actions, and keeps editing the result in the same place.

iPolloWork is not positioned as a replacement for a single coding agent. It connects [Codex](https://github.com/openai/codex), [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness), OpenCode, and future agent runtimes through explicit compatibility boundaries while preserving the native strengths of each ecosystem. Coding is only the starting point: when the output is a deck, web page, visual design, or video, it remains editable instead of becoming a finished file or a chat transcript.

<div align="center">
  <h3>Join the official iPolloWork WeChat community</h3>
  <p>Scan with WeChat to join the official group for product updates and community discussions.</p>
  <img src="./docs/assets/ipollowork-official-wechat-group.jpg" alt="QR code for the official iPolloWork WeChat community" width="220" />
</div>

## What makes it different

- **One workbench across agent engines** — use Codex, DeepSeek Harness, OpenCode, and future runtimes without rebuilding the project experience around each engine.
- **One global extension system** — install, enable, update, and uninstall portable plugins, Skills, agents, commands, services, and authorization once; optional engine-native bindings stay behind the same lifecycle.
- **Project-native human-agent collaboration** — give people and agents one shared project view for responsibilities, tasks, schedules, execution health, and results instead of scattering work across isolated chats.
- **One editable production loop** — move from code to documents, websites, presentations, design, and video while keeping text, images, layouts, timelines, and scenes editable after generation.
- **Local and enterprise control** — run locally, bring your own model or provider, review permissions and execution, and connect organization services only when a team needs them.

## Agent runtime compatibility

OpenCode is the default local execution runtime today. [DeepSeek Harness (DSH)](https://github.com/deepseek-ai/deepseek-harness) is integrated as an optional peer runtime and subagent delegation target, while [Codex](https://github.com/openai/codex) connects through the [`ipollowork-ui-mcp`](https://www.npmjs.com/package/ipollowork-ui-mcp) control surface. MCP is the integration protocol for that path, not another agent engine alongside Codex, DSH, and OpenCode. These paths share the workbench without pretending that every runtime has the same native capabilities.

The collaboration model keeps iPolloWork as the project workspace: a task can delegate bounded work to DSH subagents when useful, then bring structured progress and results back into the same project. Each runtime retains its own agents, Skills, plugins, and execution model.

### Run iPolloWork creative plugins directly in DeepSeek Harness

DeepSeek Harness users can install iPolloWork's native Design, PPT, and Video views into the DSH Web UI and start them from any project directory:

<p>
  <a href="https://www.npmjs.com/package/deepseek-idesign"><img src="https://img.shields.io/npm/v/deepseek-idesign?label=DeepSeek%20Design&amp;logo=npm&amp;color=CB3837" alt="deepseek-idesign npm version" /></a>
  <a href="https://www.npmjs.com/package/deepseek-ivideo"><img src="https://img.shields.io/npm/v/deepseek-ivideo?label=DeepSeek%20Video&amp;logo=npm&amp;color=CB3837" alt="deepseek-ivideo npm version" /></a>
</p>

```bash
npx @deepseek-ai/dsh plugin --profile web add deepseek-idesign deepseek-ippt deepseek-ivideo
npx @deepseek-ai/dsh web
```

Open [http://127.0.0.1:3080](http://127.0.0.1:3080), start a conversation, and choose **Design**, **PPT**, or **Video**. If the `dsh` command is already installed, replace `npx @deepseek-ai/dsh` with `dsh`. DeepSeek Harness is currently a developer preview, so plugin compatibility follows its active release line.

## Install iPolloWork

### Download the desktop app

Official installers are published on [GitHub Releases](https://github.com/Devin-AXIS/iPolloWork/releases). If you prefer a manual download, choose the file that matches both your operating system and CPU:

| System | CPU | Installer to use |
| --- | --- | --- |
| macOS | Apple Silicon (M-series) | `ipollowork-mac-arm64-<version>.dmg` |
| macOS | Intel | `ipollowork-mac-x64-<version>.dmg` |
| Windows | Intel/AMD 64-bit | `ipollowork-win-x64-<version>.exe` |
| Windows | ARM64 | `ipollowork-win-arm64-<version>.exe` |
| Linux | Intel/AMD 64-bit | `ipollowork-linux-x64-<version>.AppImage` |
| Linux | ARM64 | `ipollowork-linux-arm64-<version>.AppImage` |

The macOS `.zip` and Linux `.tar.gz` files are portable/update artifacts; most users should choose `.dmg`, `.exe`, or `.AppImage`. If the Releases page does not yet contain an installer for your system, run or package the app from source below.

Installation after downloading:

- **macOS:** open the `