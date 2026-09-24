# dsh-plugin-freecodego

**FreeCodeGo for DeepSeek Harness** — a Cordis bundle that adds the FreeCodeGo engine inventory, a managed free-model gateway, per-provider accounts, media generation, and the engineering (code-graph + memory) toolchain to [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (`dsh`).

English | [中文](README.zh.md)

FreeCodeGo is **not** a DeepSeek product, and this is not an official DeepSeek distribution: it is a plugin that mounts into a Harness you install yourself. See [TRADEMARK.md](plugin/TRADEMARK.md) for the naming policy that applies to forks of this repository.

## Screenshots

The five views below are the plugin as it looks mounted: the plugin market card shows the same set, and the first one is what that card previews.

**Model picker** — the managed catalog and the free providers it reads, grouped by provider, each row carrying its own free and latency label; the composer's engine selector sits beside it.

![Model picker: provider groups with free rows and the engine selector in the composer](plugin/packages/freecodego/bundle-latest/screenshots/01-model-picker.png)

**Accounts and providers** — Settings → FreeCodeGo → Accounts & providers: each provider's key stays in the Harness host, and that provider's free-model roster is listed under it.

![Settings showing a per-provider API key field and the provider's free-model roster](plugin/packages/freecodego/bundle-latest/screenshots/02-providers-and-accounts.png)

**Engineering enhancement** — the master switch and what sits behind it: engineering skills, project-long-term memory, the code graph, post-implementation verification, and multi-role review.

![Engineering enhancement settings: the master switch and its per-capability toggles](plugin/packages/freecodego/bundle-latest/screenshots/03-engineering-enhancement.png)

**Plugin safety and updates** — conflict protection at load time, the release update check, and the unified MCP / Skill capability layer.

![Plugin conflict protection, the update check, and the MCP/Skill capability layer](plugin/packages/freecodego/bundle-latest/screenshots/04-plugin-safety-and-updates.png)

**Community picks** — the DSH market ranking and the MCP.SO directory, installed into the local Harness with one click.

![Community picks: the DSH market ranking and the MCP.SO directory, each with one-click install](plugin/packages/freecodego/bundle-latest/screenshots/05-community-mcp-marketplace.png)

## What it adds

- **Managed model catalogs** — one picker over the FreeCodeGo gateway and the free providers it manages (OpenCode, Logfare, SenseNova, NVIDIA, VyceAI, Kilo, Agnes, Cline, WorkBuddy International, Qoder, TRAE, Groq Whisper), each row carrying its own health, rate, and training-data label.
- **Native engines** — a session runs on DeepSeek, Codex, or Claude, each behind its own verified runtime, with this plugin's router as the only Harness `AgentFactory`.
- **Advisor review loop** — an independent, read-only reviewer that steers the active Agent with bounded findings.
- **Code review** — an OCR-style reviewer over the change itself (the workspace, a ref range from its merge base, or one commit), with four layer-resolved rule sets, per-file coverage accounting, three report formats, adversarial re-checking of high-severity findings, and an opt-in stop-time gate.
- **Engineering enhancement** (behind one master switch) — multi-engine engineering review, a multi-member team, CodeGraph / Graphify code graphs, durable per-project engineering memory, checkpoints and a hunk journal, a repository map, and deterministic scan inspection.
- **Context and cost discipline** — Headroom output compression (including code skeletonization), deferred tool schemas with `tool_search`, cache-cold clearing with spill recall, a model-visible context budget, and cache-miss attribution.
- **Guardrails** — a declarative command policy, Plan Mode, folder trust, a credential-path shield that also covers native engines, and credential screening on memory writes.
- **Model menu control** — the provider and model rows the chat picker shows, non-interactive price/health labels on the stock menu, a picker label that echoes the durable selection, and a reconnect retry that does not empty an open menu.
- **Capabilities** — MCP servers, Skill roots (including skills.sh installs), LSP auto-mount, calendar scheduling rules, declarative hook chains, media generation and audio transcription, voice input, agent presets, and personas.
- **Release updates** — the plugin reads this repository's releases and installs the bundle built for the Harness you are running.

Every feature below states the setting that gates it, and where something is off by default it says so. The decision behind each one is written up in [`plugin/packages/freecodego/harness-plugin/README.md`](plugin/packages/freecodego/harness-plugin/README.md), the top-level feature document.

## Free models

<!-- generated:free-models:begin by scripts/generate-free-model-tables.ts -->
Every free row below comes from the provider's own directory, read when you open the picker, so this is what those directories returned on 2026-09-24 (sorted, where the picker keeps directory order) — and the picker is the count that is true when you look.

| Provider | Free models | Directory |
|---|---|---|
| **OpenCode** | `big-pickle`, `deepseek-v4-flash-free`, `jev-1.13-free`, `ling-3.0-flash-fin-free`, `mimo-v2.5-free`, `mimo-v2.6-flash-free`, `muse-spark-1.2`, `muse-spark-1.2-contributor-free`, `muse-spark-1.3`, `muse-spark-1.3-contributor-free`, `nemotron-3-ultra-free`, `nemotron-3.5-lightning-free`, `space-bunny-free` | 13 of 80 rows; public, no sign-in |
| **Kilo** | `cohere/north-mini-code:free`, `dots-studio/dots-3-note-preview:free`, `inclusionai/ling-3.0-flash-fin:free`, `inclusionai/ling-3.0-flash-sante:free`, `kilo-auto/free`, `liquid/lfm-2.5-2.6b:free`, `nex-agi/nex-n2.5-mini:free`, `nex-agi/nex-n2.5-pro:free`, `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`, `nvidia/nemotron-3-super-120b-a12b:free`, `nvidia/nemotron-3-ultra-550b-a55b:free`, `nvidia/nemotron-3.5-content-safety:free`, `nvidia/nemotron-3.5-lightning:free`, `openrouter/free`, `poolside/laguna-s-2.1:free`, `poolside/laguna-xs-2.1:free`, `qwen/qwen3.8-27b:free`, `stealth/space-bunny-alpha`, `stepfun/step-3.7-flash:free`, `thinkingmachines/inkling-small:free`, `z-ai/glm-5.2:free` | 21 of 393 rows; public, 200 requests/hour per egress IP |
| **Logfare** | chat `claude-opus-4.6`, `deepseek-v3.2`, `deepseek-v4-pro-0813`, `gemma-4-26b`, `glm-5`, `glm-5.3`, `glm-5.3-flash`, `grok-4.6`, `kimi-k2.5`, `kimi-k2.6`, `kimi-k2.7-code`, `kimi-k3`, `logfare/auto`, `moondream3.1`, `qwen-3.8-27b`, `step-3.7-flash`; images `flux-1-schnell`, `flux-2-dev`, `flux-2-klein-4b`, `flux-2-klein-9b`, `sdxl-lightning`; audio `melotts`, `whisper-large-v3-turbo`; other routes `aura-2-en`, `lucid-origin`, `nova-3`, `phoenix-1.0` | 27 rows; 20 need a training-data opt-in, the other 7 do not |
| **Qoder** | `Qwen 3.8 Flash` (route `qmodel_38flash`) | the free flash route, plus daily check-in campaigns |
| **NVIDIA** | `google/gemma-4-31b-it`, `moonshotai/kimi-k3`, `z-ai/glm-5.3`, `z-ai/glm-5.3-flash` — the roster also names `deepseek-ai/deepseek-v4-flash-0731` and `deepseek-ai/deepseek-v4-pro-0813`, which are gone from NVIDIA's live catalogue of 82 rows | an API key is required to call them; cross-checked 2026-09-24 |
| **SenseNova** | `deepseek-v4-flash`, `deepseek-v4-pro`, `glm-5.2`, `kimi-k3`, `sensenova-6.8-flash-lite` — 1M context and 128K output each | roster ships in the bundle; an API key is required |
| **TRAE** | the rows its directory lists | free credits reset daily, per account |
| **Cline** | the rows the directory marks `×0 · 官方免费模型` | an account pool |
| **WorkBuddy International** | the rows a credit package marks `x0` | device login, several accounts |
| **Agnes** | chat and image/video rows | a control-plane account |
| **VyceAI** | no free rost