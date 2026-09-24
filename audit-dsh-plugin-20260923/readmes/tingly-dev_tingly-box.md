![Tingly Box Web UI Demo](./docs/hero.png)

<h1 align="center">Tingly Box</h1>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#key-features">Features</a> •
  <a href="#integration-guide">Integration</a> •
  <a href="#documentation">Documentation</a> •
  <a href="https://github.com/tingly-dev/tingly-box/issues">Issues</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Go-1.26+-00ADD8?style=flat&logo=go" alt="Go Version" />
  <img src="https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg" alt="License" />
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform" />
</p>

Tingly Box **serves agents, coordinates AI models, optimizes context, and routes requests** for maximum efficiency — with built-in **remote control and secure, customizable integrations**.

## Key Features

* **Agent-First Model Gateway**
  * Unified endpoint for AI — seamlessly bridge any providers
  * One-click config for Agents - Claude Code, OpenCode, Codex, Xcode, and more 
  * Profiles for Claude Code — switch between profiles with different models under different scenarios
  * Both API keys and OAuth - use your existing quotas anywhere
* **Harness-Driven Infra**
  * VModel (Virtual Model) - for testing, validation, benchmarking, and harness-driven evaluation
  * Harness-driven - for robustness across protocols, routing, load balancing, clients, and more
* **UX-First**
  * Visual management of providers, routes, aliases, models, and remote bots
  * Intuitive workflows that make complex operations easy to understand and control
* **Production-Ready**
  * Smart Routing — Intelligently route requests across models and tokens based on cost, speed, or custom policies
  * Remote Control — Control AI agents remotely through Telegram, DingTalk, Feishu, Lark, Weixin, WeCom, Slack, and Discord
  * Team Management — Isolate data per user with dedicated API tokens, usage tracking, provider access, and configuration
  * Usage Analytics — Track token consumption, latency, cost estimates, and model selection per request
  * Blazing Fast Performance — Typically adds **< 1ms** of overhead

## Preview

![Tingly Box Web UI Demo](./docs/images/output.gif)

## Quick Start

[English](https://github.com/tingly-dev/tingly-box/issues/678#issuecomment-4273812882) | [中文](https://github.com/tingly-dev/tingly-box/issues/678#issue-4244345496) | [Fault Record](https://github.com/tingly-dev/tingly-box/discussions/626)

### Install

**Run with npx (quickest)**

```bash
# One command: fetch, restart the server in the background, migrate and open the web UI
# (a golang binary release; npx wraps the cli for convenience)
npx tingly-box@latest

# or -y for convenience
npx -y tingly-box@latest

# the binary for your platform comes from npm too (no GitHub download),
# so an npm mirror is all you need for CN (one of below)
npx --registry=https://registry.npmmirror.com -y tingly-box@latest
npx --registry=https://mirrors.huaweicloud.com/repository/npm/ -y tingly-box@latest
npx --registry=http://mirrors.tencent.com/npm/ -y tingly-box@latest
```

**Install globally with npm**

```bash
npm install -g tingly-box@latest   # --registry=<mirror> works here too

tb start   # tb = tingly-box; runs in the background (--no-daemon for foreground)
tb open    # open the web UI

# update: reinstall, then restart to apply
npm install -g tingly-box@latest
tb restart
```

> if any trouble, please check tingly-box output, or call for an issue to help.

**Install Node & NPX**

```
# MacOS & Linux
## Install Node.js LTS via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash

## Restart terminal or load nvm
source ~/.nvm/nvm.sh

## Install Node.js LTS
nvm install --lts

## Verify installation
node -v
npx -v
```

```
# Windows
## Powershell with Winget
winget install OpenJS.NodeJS.LTS

## Restart terminal, then verify installation
node -v
npx -v

## Or download and install Node.js LTS manually:
https://nodejs.org/en/download
```

**From Docker (GitHub Host)**

```bash
mkdir tingly-data
docker run -d \
  --name tingly-box \
  -p 12580:12580 \
  -v `pwd`/tingly-data:/home/tingly/.tingly-box \
  ghcr.io/tingly-dev/tingly-box
```

**From Docker Compose (recommended for isolated env), building your own image, or troubleshooting** — see the [Docker Guide](./docs/docker.md).

### Integration Guide

<details>
<summary><strong>Agent Integration - Claude Code / Claude Desktop / OpenCode / Codex / Xcode / VSCode / OpenClaw</strong></summary>

- Claude Code (support 1-click config)
- OpenCode (support 1-click config)
- Xcode (require manual config)
- ……

Any application is ready to use.

> We've provided detailed config guide in application

![Agent Integration Demo](./docs/images/5-claude-code.png)

</details>

<details>
<summary><strong>DeepSeek Best Compatibility</strong></summary>

DeepSeek is optimized for mainstream agent workflows, offering broad compatibility across protocol adapters, agent clients, extended context, vision, web search, and cache optimization.

| Module                           |      Status | What It Solves                                                        |
| -------------------------------- | ----------: | --------------------------------------------------------------------- |
| Model List                       | ✅ Supported | Keeps the official model list up to date in real time                 |
| Protocol Adaptation              | ✅ Supported | Supports official Anthropic/OpenAI APIs with bidirectional conversion |
| Reasoning Capability             | ✅ Supported | Provides compatibility with Thinking workflows                        |
| Cache Hit Optimization           | ✅ Supported | Improves cache hit rates for DeepSeek requests                        |
| Vision Proxy                     | ✅ Supported | Enables DeepSeek to understand and process images                     |
| Web Search                       | ✅ Supported | Calls official Web tools through the Anthropic endpoint               |
| 1M Context Window                | ✅ Supported | Enables one-click setup for 1M context                                |
| Codex Adaptation                 | ✅ Supported | Ensures compatibility with mainstream agent workflows                 |
| Claude Code / Desktop Adaptation | ✅ Supported | Ensures compatibility with mainstream agent workflows                 |

Supports one-click configuration where available. For applications that require manual setup, detailed in-app configuration guides are provided.

Any compatible application is ready to use.

> Detailed configuration guides are available inside each application.

</details>

<details>
<summary><strong>Remote Control Agent via IM Bots - TG / DingTalk / Feishu / Lark / Weixin / WecCom</strong></summary>

Tingly Box now supports remote control through popular IM platforms. Interact with your AI agents remotely without direct server access.

**Supported Platforms**

- ✅ Telegram
- ✅ DingTalk
- ✅ Feishu
- ✅ Lark
- ✅ Weixin
- ✅ WeCom

**Quick Setup**

1. Open Web UI like `http://localhost:12580`
2. Navigate to **Remote** section
3. Configure your preferred IM platform bot
4. Start interacting with your agents remotely

**Use Cases**

- Execute tasks and queries from your phone or any device
- Team collaboration with shared agent access
- Monitor and control agents while away from your workstation

![Remote Control Demo](./docs/images/7-remote.png)

</details>

<details>
<summary><strong>OpenAI SDK</strong></summary>

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-tingly-model-token",
    base_url="http://localhost:12580/tingly/openai/v1"
)

response = client.chat.completions.create(
    model="tingly-gpt",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response)
```

</details>

<details>
<summary><strong>Anthropic SDK</strong></summary>

```python
from anthropic import Anthropic

client = A