<div align="center">
  <a href="https://aidea-labs.com/open/projects/mcp-for-stata">
    <img src="assets/mcp-for-stata-stata-ai-data-analysis.jpg" alt="MCP-for-Stata (Stata-MCP): let Claude Code, Codex, and other AI agents run local Stata for regression analysis and empirical research" width="300"/>
  </a>
</div>

# MCP-for-Stata (Stata-MCP): Run Stata with ANY Agent

MCP-for-Stata is an safety first open-source MCP server and CLI tool with Skills lets any AI agent you use invoke local Stata on your device for regression analysis, econometrics, paper replication, and empirical research. It provides command guards, resource monitoring, automatic log capture, and cross-platform client installation, while you retain control of your data and Stata license.

Turn Claude Code, Codex, and other AI agents into an on-demand research assistant.

> Stata is a registered trademark of StataCorp LLC. This project is an independent community-developed tool and is not affiliated with, endorsed by, or sponsored by StataCorp LLC.

[![en](https://img.shields.io/badge/lang-English-red.svg)](README.md)
[![cn](https://img.shields.io/badge/语言-中文-yellow.svg)](README.zh-CN.md)
[![fr](https://img.shields.io/badge/langue-Français-blue.svg)](README.fr.md)
[![es](https://img.shields.io/badge/idioma-Español-green.svg)](README.es.md)
[![Publish to PyPI](https://github.com/SepineTam/mcp-for-stata/actions/workflows/python-package.yml/badge.svg)](https://github.com/SepineTam/mcp-for-stata/actions/workflows/python-package.yml)
[![PyPI version](https://img.shields.io/pypi/v/stata-mcp.svg)](https://pypi.org/project/stata-mcp/)
[![PyPI Downloads](https://static.pepy.tech/badge/stata-mcp)](https://pepy.tech/projects/stata-mcp)
[![License: AGPL 3.0](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](LICENSE)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/14255/badge)](https://www.bestpractices.dev/projects/14255)
[![Issue](https://img.shields.io/badge/Issue-report-green.svg)](https://github.com/sepinetam/mcp-for-stata/issues/new)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/SepineTam/mcp-for-stata)

<!-- mcp-name: io.github.SepineTam/stata-mcp -->

---
## 💡 Quick Start

You do not need to edit any configuration. Just tell your agent:

```text
Install MCP-for-Stata for yourself globally following the instructions in the GitHub repository at SepineTam/mcp-for-stata.
```

## 🆕 News
- 📖 **Skills installed by default**: Stata-related skills are now installed together with the MCP, no separate setup needed. See the [installation guide](docs/install.md#3-choose-optional-components).
- 🚀 **DeepSeek Harness Day 0 Support**: Install MCP-for-Stata in DeepSeek Harness with `uvx stata-mcp install -c dsh`. See the [DeepSeek Harness guide](https://sepinetam.github.io/mcp-for-stata/agents/deepseek_harness/).
- 🧪 **Claude Science Support**: MCP-for-Stata now works in Claude Science with a sandbox allowlist. See the [Claude Science guide](https://sepinetam.github.io/mcp-for-stata/agents/claude_science).
- Find more in WeChat: [Why I made it?](https://mp.weixin.qq.com/s/VYkykdDgfPMa5KN0_1BeFQ), and [8 figures find out Stata-MCP](https://mp.weixin.qq.com/s/RKPKA4OWAM5SeZmGtbMRew)
- 🦞 **OpenClaw Support**: Standalone CLI tools for OpenClaw integration (`stata-mcp tool`), see [OpenClaw guide](https://sepinetam.github.io/mcp-for-stata/agents/openclaw.md)
- ✨ **Claude Code Plugin Support**: Official plugin package with MCP server and Stata LSP integration
- Use MCP-for-Stata in Claude Code, see [Claude Code advanced usage](#advanced-claude-code), or in Codex see [Codex advanced usage](#advanced-codex)

> Finding our **newest research**? [View latest research reports](https://aidea-labs.com/open/projects/mcp-for-stata/reports).

<details>
<summary>Looking for others?</summary>

> **MCP or AI about Stata**
> - A session based MCP server for Stata, [mcp-stata](https://github.com/tmonk/mcp-stata)
> - IDEs (VScode or Cursor) integrated [stata-mcp for VSCode](https://github.com/hanlulong/stata-mcp). Confused them? 💡 [Comparison](#comparison)
> 
> **Datasets and Information**  
> - [STOP Dataset](https://opendata.ai4cssci.com): StataMCP-Team Opendata Project 📊, we have open-sourced a comprehensive dataset collection for social science research, aiming to enable the future of AI-driven and data-powered research paradigms.
</details>

<details>
<summary>Why AGPL 3.0 License?</summary>

The AGPL 3.0 License is a type of open-source license. It does not affect your daily use, and allows you to use, modify, and distribute this software free of charge, provided that you comply with its terms, such as retaining the original copyright notices.

**Notes**: While we strive to make open source accessible to everyone, we regret that we can no longer maintain the Apache-2.0 License. Due to individuals directly copying this project and claiming to be its maintainers, we have decided to change the license to AGPL-3.0 to prevent misuse of the project in ways that go against our original vision.

**Notes**: 尽管我们希望尽可能让所有人都能从开源中获益，但我们很遗憾地宣布无法继续保持 Apache-2.0 License。由于有人直接抄袭本项目并标榜其为项目维护者，我们不得不将 License 更改为 AGPL-3.0，以防止有人滥用本项目进行违背项目初心的事情。

Reason following: 

**Background**: @jackdark425's [repository](https://github.com/jackdark425/aigroup-stata-mcp) directly copied this project and claimed to be the sole maintainer. We welcome open source collaboration based on forks, including but not limited to adding new features, fixing existing bugs, or providing valuable suggestions for the project, but we firmly oppose plagiarism and false attribution.

**Update**: The infringing project has been taken down via GitHub DMCA. [View DMCA takedown details](https://github.com/github/dmca/blob/master/2025/12/2025-12-30-stata-mcp.md).

**背景**: @jackdark425 的[仓库](https://github.com/jackdark425/aigroup-stata-mcp)直接抄袭了本项目并标榜为项目唯一维护者。我们欢迎基于fork的开源协作，包括但不限于添加新的feature、修改已有bug或对项目提出您宝贵的意见，但坚决反对抄袭和虚假署名行为。

**更新**: 侵权项目已通过GitHub DMCA被takedown，[查看DMCA下架详情](https://github.com/github/dmca/blob/master/2025/12/2025-12-30-stata-mcp.md)。

</details>

---

## Installation and Client Configuration

See the **[Installation Guide](docs/install.md)** for installation methods,
client setup, addon/extra options, and verification.

### 🚀 One-click installation for all clients!
No config, no manual JSON editing. Just one command installs MCP-for-Stata for **every supported agent** (Claude Code, Codex, OpenClaw, Cursor, Gemini CLI, and more):

```bash
uvx stata-mcp install --all
```

<details>
<summary>Supported Agents 🤖</summary>
Based on our own experience and testing, we recommend using Claude Code, Codex, and OpenClaw.
We have found that Claude and DeepSeek are the two best models across any framework.

| Agent                     | Tag      | Command                           |
|---------------------------|----------|-----------------------------------|
| Claude Desktop            | claude   | uvx stata-mcp install -c claude   |
| Claude Code               | cc       | uvx stata-mcp install -c cc       |
| Gemini CLI                | gemini   | uvx stata-mcp install -c gemini   |
| Cursor                    | cursor   | uvx stata-mcp install -c cursor   |
| Cline (VScode Extension)  | cline    | uvx stata-mcp install -c cline    |
| Codex CLI & Codex Desktop | codex    | uvx stata-mcp install -c codex    |
| OpenCode                  | opencode | uvx stata-mcp install -c opencode |
| OpenClaw                  | openclaw | uvx stata-mcp install -c openclaw |
| Claude Science            | —        | [Manual config](#advanced-claude-science) |

</details>

If you don't have `uv`, [see the uv installation guide](https://docs.astral.sh/uv/getting-started/installation) to install it. 
Or, use our beta install script (auto-installs `uv` if missing):

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/SepineTam/mcp-for-stata/master/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm h