# SandBase Harness

[English](./README.md) | [中文](./README.zh-CN.md)

[![GitHub stars](https://img.shields.io/github/stars/sandbaseai/sandbase-harness?style=social)](https://github.com/sandbaseai/sandbase-harness/stargazers)
[![Listed on deepseek-plugin.org](https://img.shields.io/badge/listed_on-deepseek--plugin.org-007EC6)](https://deepseek-plugin.org/plugins/sandbaseai/sandbase-harness)
[![Release](https://img.shields.io/github/v/release/sandbaseai/sandbase-harness)](https://github.com/sandbaseai/sandbase-harness/releases/latest)
[![Official MCP Registry](https://img.shields.io/badge/Official_MCP_Registry-active-2ea44f)](https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.sandbaseai%2Fsandbase-harness)
[![Discussions](https://img.shields.io/github/discussions/sandbaseai/sandbase-harness)](https://github.com/sandbaseai/sandbase-harness/discussions)
[![CodeQL](https://github.com/sandbaseai/sandbase-harness/actions/workflows/codeql.yml/badge.svg)](https://github.com/sandbaseai/sandbase-harness/actions/workflows/codeql.yml)
[![License](https://img.shields.io/github/license/sandbaseai/sandbase-harness)](LICENSE)

AI-readable project metadata: [llms.txt](./llms.txt) · [installation guide](./llms-install.md)

A local-first runtime for AI agents. Sessions, sandboxed tools, memory,
credentials, audit trails, and a built-in Console — all running on your
machine or in your own infrastructure.

> Building with DeepSeek Harness? The independent [DeepSeek Harness Handbook](https://github.com/sandbaseai/deepseek-harness-handbook) provides source-backed runtime guides, multilingual troubleshooting, and a regularly updated [Agent-first resource map](https://sandbaseai.github.io/deepseek-harness-handbook/awesome-deepseek-harness-resources.html).

![SandBase Harness architecture](docs/assets/sandbase-harness-architecture.svg)

> Looking for a lightweight bridge instead of a full runtime? [SandBase CLI](https://github.com/sandbaseai/cli)
> connects 25 AI client targets to 2,000+ models and APIs through a local stdio MCP bridge.
> If it fits your workflow, [star SandBase CLI](https://github.com/sandbaseai/cli/stargazers)
> so other agent users can discover it.

> Need hosted model and media APIs instead? SandBase provides one interface for
> [LLM, image, and video generation APIs](https://blog.sandbase.ai/unified-ai-api-llm-image-video-2026/),
> with the [API quickstart](https://www.sandbase.ai/docs/getting-started/) covering keys and first calls.

```bash
git clone --branch v0.3.8 --depth 1 https://github.com/sandbaseai/sandbase-harness.git
cd sandbase-harness
npm ci
npm run build
mkdir ../my-agents && cd ../my-agents
node ../sandbase-harness/dist/index.js init
node ../sandbase-harness/dist/index.js start
# open http://127.0.0.1:3000/dashboard
```

Choose SandBase Harness when you need more than a model loop:

| Need | What Harness provides |
| --- | --- |
| Run generated code safely | Local, Docker, Kubernetes, and self-hosted worker sandboxes |
| Inspect long-running agents | Persistent sessions, resumable event streams, audit, and replay |
| Control tool access | MCP toolsets, credential vaults, permission policies, and approvals |
| Operate any model | OpenAI, Anthropic, MiniMax, and OpenAI-compatible providers, including DeepSeek V4 |
| Keep infrastructure yours | Local-first SQLite and file storage with no required hosted control plane |

If this runtime solves a real agent-infrastructure problem for you,
[star the repository](https://github.com/sandbaseai/sandbase-harness) so other builders can find it.

## Find SandBase Harness

The project is also discoverable through these independent ecosystem directories:

- [Official MCP Registry](https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.sandbaseai%2Fsandbase-harness)
- [deepseek-plugin.org](https://deepseek-plugin.org/plugins/sandbaseai/sandbase-harness)
- [DeepseekPlugin](https://deepseekplugin.org/en/plugins/sandbaseai-sandbase-harness)
- [DSH Plugin Directory](https://dshplugin.app/plugins/sandbase-harness)
- [DSH Plugin Hub](https://dshpluginhub.dev/en/plugins/sandbaseai/sandbase-harness)
- [DSH Directory](https://dsh.directory/plugins/sandbaseai/sandbase-harness)
- [DSH Harness](https://dsharness.io/en/plugins?search=sandbase-harness)
- [DSH Plugin](https://dshplugin.me/?q=sandbase-harness)
- [DSH Plugin](https://dsh-plugin.org/plugins/sandbaseai/sandbase-harness)
- [dsh.so Trust & Discovery Registry](https://www.dsh.so/artifact/sandbase-harness/)
- [DeepSeek Harness Hub](https://deepseek-harness-hub.com/plugins/sandbase-harness/) — community discovery page; its metadata is currently stale at v0.3.4, so use the current official installation guide
- [Duink DSH Universe](https://duink.com/plugins/1297278222/)
- [DSH Plugin Leaderboard](https://dshpluginleaderboard.com/)
- [Awesome repository index](https://awesome.lvtd.dev/repos/?topic=dsh-plugin)
- [Awesome DSH Plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin)
- [Awesome DeepSeek Harness](https://github.com/0xsline/awesome-deepseek-harness)
- [Awesome DeepSeek Harness — ecosystem list](https://github.com/fendouai/awesome-deepseek-harness)
- [DSHarness 101 Plugin Radar](https://dsharness101.com/plugins/)
- [DeepSeekDocs Ecosystem](https://deepseekdocs.com/en/ecosystem)
- [Awesome Agents](https://github.com/kyrolabs/awesome-agents)
- [Sifted Awesome AI Agents — Agent Runtime Top 100](https://github.com/sifted-network/sifted-awesome-ai-agents/blob/main/top100/Agent%20Runtime.md)
- [Arnon-hs Open Source — MCP projects](https://github.com/Arnon-hs/open-source/blob/main/mcp/README.md)
- [SandBase Awesome Agent Runtime](https://github.com/sandbaseai/awesome-agent-runtime)
- [abordage/awesome-mcp](https://github.com/abordage/awesome-mcp)
- [cccakeee/awesome-dsh-plugins](https://github.com/cccakeee/awesome-dsh-plugins)
- [anbeime/skill — Skills index](https://github.com/anbeime/skill)
- [Awesome DeepSeek Harness Plugins](https://github.com/Zhiyuan-Fan/Awesome-DeepSeek-Harness-Plugins)
- [Hermes Ecosystem — SandBase stack](https://github.com/ksimback/hermes-ecosystem/blob/main/projects/sandbaseai/cli.html)
- [AgentStack](https://www.agentstack.live/mcp/io.github.sandbaseai/sandbase-harness)
- [HVTracker](https://hvtracker.net/agents/sandbase-harness/): independent automated Agent Frameworks profile and ranking snapshot; not a maintainer review or security certification.
- [MCP Servers Live](https://linny006.github.io/mcp-servers-live/r/sandbaseai/sandbase-harness/)
- [DSH X-Ray](https://unstone.github.io/dsh-xray/p/sandbaseai__sandbase-harness.html)
- [DSH Plugins](https://github.com/HackSing/dsh-plugins)
- [Awesome DSH Hub](https://github.com/ukinch605/awesome-dsh-hub)
- [Awesome DSH Plugins 2026](https://github.com/Herdeny/awesome-dsh-plugins-2026)
- [MCP Repository](https://mcprepository.com/sandbaseai/sandbase-harness)
- [MCP Server Hub](https://mcpserver.dev/s/sandbase-harness_4o5awxb): public MCP Server Hub listing for SandBase Harness.
- [MCPFly submission](https://mcpserver.so/submit): repository submission accepted and pending approval; no public listing is claimed yet
- [MCP Central API](https://mcpcentral.io/api/servers?search=sandbase): public downstream registry mirror returning the active `io.github.sandbaseai/sandbase-harness` entry; its version snapshot may lag the current release.
- [MCPVault](https://mcpvault.io/servers/sandbase-harness)
- [F8W 中文项目档案](https://www.f8w.com/github/sandbaseai__sandbase-harness/)
- [RepoRank Русский профиль](https://reporank.net/ru/repo/sandbaseai-sandbase-harness.html)
- [Agent Plugins Hub — legacy snapshot](https://agentplugin.net/dsh/plugins/managed-agents)
- [MCP Market](https://mcpmarket.com/server/sandbase-harness)
- [OpenAgentSkill — code-review](https://www.openagentskill.com/skills/sandbaseai-sandbase-harness-code-review)
- [PluginBench](https://pluginbench.com/mcp/io.github.sandbaseai/sandbase-harness)
- [DSH Plugin Store](https://www.dshplugin.store/pl