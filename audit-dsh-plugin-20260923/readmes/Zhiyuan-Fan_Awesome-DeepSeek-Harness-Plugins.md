# Awesome DeepSeek Harness Plugins

[English](README.md) | [简体中文](README.zh-CN.md)

A concise, daily-curated directory of public plugins and extensions for [DeepSeek Harness](https://www.deepseek.com/harness/en/) (DSH), the open-source DeepSeek agent harness. Explore tools, skills, model providers, memory, automation, runtimes, desktop clients, browser integrations, and developer utilities.

Every entry links to its canonical GitHub repository, current star count, and independently verified references.

> Inclusion: public, useful, maintained, and clearly built for DSH. Review a plugin's code and permissions before installing it.

## Core

| Project | Description | Stars | Referenced by |
| --- | --- | --- | --- |
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) | A developer-preview agent harness where every capability is a swappable, composable plugin. | [![GitHub stars](https://img.shields.io/github/stars/deepseek-ai/deepseek-harness?style=flat&label=stars)](https://github.com/deepseek-ai/deepseek-harness/stargazers) | <details><summary>1 page</summary><ul><li><a href="https://www.deepseek.com/harness/en/">DeepSeek Harness official overview</a> · <sub>Docs</sub></li></ul></details> |
| [DeepSeek Harness Handbook](https://github.com/sandbaseai/deepseek-harness-handbook) | Provides source-backed operator guides for DeepSeek Harness architecture, plugins, MCP, sessions, sandboxing, evaluation, and troubleshooting. | [![GitHub stars](https://img.shields.io/github/stars/sandbaseai/deepseek-harness-handbook?style=flat&label=stars)](https://github.com/sandbaseai/deepseek-harness-handbook/stargazers) | <details><summary>1 page</summary><ul><li><a href="https://sandbaseai.github.io/deepseek-harness-handbook/">DeepSeek Harness Handbook</a> · <sub>Docs</sub></li></ul></details> |

**Taxonomy:** Models & Providers · Tools & Skills · Sessions & Storage · Loops & Scheduling · Runtime & Sandboxes · UI & Clients · Integrations · Developer & Operations

**Browse:** [Models & Providers](#models--providers) · [Tools & Skills](#tools--skills) · [Sessions & Storage](#sessions--storage) · [Loops & Scheduling](#loops--scheduling) · [Runtime & Sandboxes](#runtime--sandboxes) · [UI & Clients](#ui--clients) · [Integrations](#integrations) · [Developer & Operations](#developer--operations)

The taxonomy follows the capability seams defined by the [official Harness overview](https://www.deepseek.com/harness/en/).

Projects in each section are ranked by GitHub stars, then by verified reference count.

## Models & Providers

| Project | Description | Stars | Referenced by |
| --- | --- | --- | --- |
| [dsh-routing-suite](https://github.com/yjh051108/dsh-routing-suite) | Bundles a runtime injector with an experimental preset that routes DSH sessions among task-aware reasoning modes. | [![GitHub stars](https://img.shields.io/github/stars/yjh051108/dsh-routing-suite?style=flat&label=stars)](https://github.com/yjh051108/dsh-routing-suite/stargazers) | <details><summary>0 pages</summary><sub>No verified references yet.</sub></details> |
| [dsh-plugin-subscriptions](https://github.com/V1ki/dsh-plugin-subscriptions) | Adds DSH model providers for eligible ChatGPT, Claude, Grok, and GitHub Copilot subscriptions through OAuth, device login, or existing local credentials. | [![GitHub stars](https://img.shields.io/github/stars/V1ki/dsh-plugin-subscriptions?style=flat&label=stars)](https://github.com/V1ki/dsh-plugin-subscriptions/stargazers) | <details><summary>0 pages</summary><sub>No verified references yet.</sub></details> |
| [dsh-commandcode-provider](https://github.com/Mars-Sea/dsh-commandcode-provider) | Adds an unofficial Command Code provider with browser sign-in, live model discovery, plan filtering, account rotation, image input, and Web search. | [![GitHub stars](https://img.shields.io/github/stars/Mars-Sea/dsh-commandcode-provider?style=flat&label=stars)](https://github.com/Mars-Sea/dsh-commandcode-provider/stargazers) | <details><summary>0 pages</summary><sub>No verified references yet.</sub></details> |
| [dsh-reasoning-effort](https://github.com/HanaAyane/dsh-reasoning-effort) | Adds model and reasoning-effort controls to DSH Web, including configurable effort levels for custom providers. | [![GitHub stars](https://img.shields.io/github/stars/HanaAyane/dsh-reasoning-effort?style=flat&label=stars)](https://github.com/HanaAyane/dsh-reasoning-effort/stargazers) | <details><summary>0 pages</summary><sub>No verified references yet.</sub></details> |
| [dsh-codex-connect](https://github.com/franksong2702/dsh-codex-connect) | Adds ChatGPT OAuth model access and optional GPT Image generation to DSH, with diagnostics and session recovery through native Harness services. | [![GitHub stars](https://img.shields.io/github/stars/franksong2702/dsh-codex-connect?style=flat&label=stars)](https://github.com/franksong2702/dsh-codex-connect/stargazers) | <details><summary>0 pages</summary><sub>No verified references yet.</sub></details> |
| [dsh-workbuddy-connect](https://github.com/corrinehu/dsh-workbuddy-connect) | Connects models from a locally installed and signed-in WorkBuddy desktop app to DSH Web, Desktop, or TUI with account status and remaining-credit views. | [![GitHub stars](https://img.shields.io/github/stars/corrinehu/dsh-workbuddy-connect?style=flat&label=stars)](https://github.com/corrinehu/dsh-workbuddy-connect/stargazers) | <details><summary>0 pages</summary><sub>No verified references yet.</sub></details> |
| [dockyard-dsh](https://github.com/AITabby/dockyard-dsh) | Connects macOS DSH profiles to official provider CLI and OAuth sessions for account pooling, model discovery, quota views, and provider-native requests. | [![GitHub stars](https://img.shields.io/github/stars/AITabby/dockyard-dsh?style=flat&label=stars)](https://github.com/AITabby/dockyard-dsh/stargazers) | <details><summary>0 pages</summary><sub>No verified references yet.</sub></details> |
| [rapid-mlx-dsh-provider](https://github.com/raullenchai/rapid-mlx-dsh-provider) | Adds a configurable OpenAI-compatible Rapid-MLX provider with model discovery, advertised context limits, and local-server routing. | [![GitHub stars](https://img.shields.io/github/stars/raullenchai/rapid-mlx-dsh-provider?style=flat&label=stars)](https://github.com/raullenchai/rapid-mlx-dsh-provider/stargazers) | <details><summary>0 pages</summary><sub>No verified references yet.</sub></details> |
| [dsh-codex-subscription](https://github.com/WSL043/dsh-codex-subscription) | Adds ChatGPT or Codex subscription OAuth, models, quotas, search, speed controls, usage resets, and image generation or editing to DSH. | [![GitHub stars](https://img.shields.io/github/stars/WSL043/dsh-codex-subscription?style=flat&label=stars)](https://github.com/WSL043/dsh-codex-subscription/stargazers) | <details><summary>0 pages</summary><sub>No verified references yet.</sub></details> |
| [dsh-agy-link](https://github.com/amlyczz/dsh-agy-link) | Connects Google Antigravity CLI models to DSH with streaming responses, tool activity, usage reporting, and Web OAuth sign-in. | [![GitHub stars](https://img.shields.io/github/stars/amlyczz/dsh-agy-link?style=flat&label=stars)](https://github.com/amlyczz/dsh-agy-link/stargazers) | <details><summary>0 pages</summary><sub>No verified references yet.</sub></details> |
| [opencode2dsh](https://github.com/FishBottle7/opencode2dsh) | Adds OpenCode Zen models to DSH through a native provider with live catalog discovery, offline fallback, and classified upstream errors. | [![GitHub stars](https://img.shields.io/github/stars/FishBottle7/opencode2dsh?style=flat&label=stars)](https://github.com/FishBottle7/opencode2dsh/stargazers) | <details><summary>0 pages</summary><sub>No verified references yet.</sub></details> |
| [deepseek-harness-model-config](https://github.com/MarvekG/deepseek-harness-model-config) | Adds a Web editor for custom model endpoints, protocols, headers, credentials, capability metadata, retries,