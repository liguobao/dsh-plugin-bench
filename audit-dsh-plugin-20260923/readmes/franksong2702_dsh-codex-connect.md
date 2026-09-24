# Codex Connect

[![npm version](https://img.shields.io/npm/v/dsh-codex-connect/alpha?label=npm%20alpha&color=cb3837)](https://www.npmjs.com/package/dsh-codex-connect)

English | [中文](docs/README.zh.md)

Connect your ChatGPT subscription to DeepSeek Harness with OAuth, optional GPT Image generation, user-controlled defaults, Harness-native approvals, diagnostics, and reliable session recovery.

Community Alpha — not affiliated with or endorsed by OpenAI, ChatGPT, Codex, DeepSeek, or DeepSeek Harness.

Codex Connect adds the `openai-codex` model provider to the normal Harness agent loop. Harness continues to manage tools, permissions, approvals, attachments, session persistence, compaction, and recovery. Installing the plugin does not change your default model or search route, and it does not turn a ChatGPT subscription into an OpenAI Platform API key.

## Quick start

This guide describes the published pairing below. Check `dsh --version` first and use `doctor --json` for local diagnostics; the CLI version alone does not prove which model-runtime packages are installed, and missing metadata is reported as unknown. For other versions, use [Installation and upgrades](INSTALL.md). A moving npm tag such as `alpha` is not a compatibility guarantee.

| Requirement | Verified pairing |
|---|---|
| Codex Connect | `0.1.0-alpha.4.43` |
| DeepSeek Harness | `0.1.7-rc.1` |
| Node.js | `^22.19.0 \|\| >=24.0.0` |
| Account | ChatGPT OAuth with access to the requested Codex model; availability is decided by OpenAI |

As of 2026-09-24, npm `alpha` points to 4.43 while `latest` remains on 4.41. Use the exact version below for this DSH pairing; publishing an Alpha and changing the default installation channel are separate actions.

On stock DSH `0.1.7-rc.1`, ordinary Composer works, but Task controls remain paused: activation is rejected and fresh Sessions do not show them. Migration of earlier Task grants across a Harness upgrade is not verified. Older supported pairings and their task behavior are documented in [Installation and upgrades](INSTALL.md).

### 1. Install

```sh
dsh plugin --profile web add dsh-codex-connect@0.1.0-alpha.4.43
dsh web
```

Replace `web` with your existing profile name; use that same profile when starting Harness. From a DSH source checkout, prefix commands with `pnpm`. See [INSTALL.md](INSTALL.md) for other profiles and installation checks.

### 2. Authorize and select a model

Open **Settings → Models → Openai-Codex → Authorize**, then complete approval yourself in the browser. If an embedded window is blocked, select **Open ChatGPT sign-in page**. Choose an `openai-codex` model in the normal Harness model picker.

Never paste an authorization URL, code, token, or account identifier into an issue, log, chat, or configuration file. For a browser on another device, the optional manual callback form can complete the pending login without forwarding the localhost callback port; follow [Remote browser authorization](docs/reference.md#remote-browser-authorization).

### 3. Check the installation

```sh
dsh plugin --profile web exec dsh-codex-connect status --json
dsh plugin --profile web exec dsh-codex-connect doctor --json
```

`status --json` exits `0` when signed in and `1` when signed out, without starting OAuth. `doctor --json` reports local installation diagnostics without a network request or raw credentials. A passing diagnostic is not proof of model access; verify that with an actual request.

<p align="center">
  <img src="https://raw.githubusercontent.com/franksong2702/dsh-codex-connect/main/docs/assets/en/hero.jpg" alt="Codex Connect — ChatGPT OAuth for DeepSeek Harness" width="100%">
</p>

## Core capabilities

- **Accounts:** save up to 16 accounts on the DSH host and manually select the active account for subsequent requests. Account selection is not a per-session binding. Requests keep their captured account; the plugin does not rotate accounts or silently fail over.
- **Models and Astra support:** the currently verified DSH and plugin combination supports `gpt-6-astra`. The plugin supplies its missing model definition with Low, Medium, High, Xhigh, and Max reasoning levels; Default preserves the provider default. Saved Off/Minimal selections require an [explicit update](MIGRATION.md#astra-reasoning-selections). When the installed dependency catalog includes Astra, the plugin preserves its native metadata while retaining these five calibrated reasoning choices. A model appearing in the list does not mean the current account has permission to use it; overall compatibility with new dependency versions still requires separate verification.
- **Fast Mode:** request priority service for one conversation, off by default. Actual speed and quota consumption depend on the service; no fixed speed multiplier is guaranteed.
- **Quota:** show the server-returned `5h` and `7d` windows and reset times, normally refreshed every 60 seconds while signed in and the tab is visible; failures back off. Missing windows are not invented; Spark uses its separate quota bucket.
- **Plugin updates:** check for newer Codex Connect releases without installing anything or recommending changes to DSH. Host compatibility is available through explicit local diagnostics.

<p align="center">
  <img src="https://raw.githubusercontent.com/franksong2702/dsh-codex-connect/main/docs/assets/composer-capabilities.jpg" alt="Fast Mode and quota controls in the DeepSeek Harness Composer" width="820">
</p>

## Optional capabilities

**Earlier Alpha 4.40/4.41 pairings:** task-level model control is off by default. After explicit task authorization, GPT-5.6 Sol/Medium starts the task, and the active model may continue, change effort, or hand off the main task within the granted scope. The task shares one request ledger and budget; stopping, manual takeover, and restart recovery retain the grant boundary. Phase 2 read-only delegation requires separate consent and does not grant workers write access. Stock DSH `0.1.7-rc.1` with Alpha 4.43 keeps these Task controls paused; do not infer they are available from an older pairing. See [Phase 1](docs/experiments/adaptive-task-phase1.md) and [Phase 2 consent](docs/experiments/adaptive-task-phase2-consent.md).

Alpha 4.40 also supplies `gpt-6-sol` and `gpt-6-luna` when older provider catalogs omit them, retaining native metadata when present. Both expose Low through Max (including Xhigh); Default omits an explicit effort. Codex Sol's Ultra orchestration mode is not implemented. New task grants can explicitly include these models, but existing grants, GPT-5.6 Sol/Medium startup and Luna Reserve remain unchanged. A catalog entry is not proof of account access. See [compatibility scope and validation](docs/experiments/gpt6-sol-luna-compatibility.md).

All options below are off on a fresh installation. Edit them in **Settings → Plugins → Plugin configuration → Codex Connect** or **Settings → Models → Openai-Codex → More settings**, then select **Save changes**. A conflict or failed save preserves your draft.

| Capability | Enable with | Important behavior |
|---|---|---|
| Proxy | `enableProxy` | Credential-free HTTP(S), scoped to this plugin's traffic. A failed proxy request does not silently retry directly. |
| Codex Search | `enableSearch` | Selects Codex for the entire profile's search route; disabling restores the previously active route. |
| Luna Reserve | `enableReserveFallback` | Uses the hidden Reserve route only when the backend explicitly authorizes it for the captured account; never changes global defaults or retries a generic `429`. |
| Image viewing | `enableImageTool` | Adds `view_image` to vision-capable models for local files and validated public HTTP(S) images. |
| GPT Image generation | `enableImageGeneration` | Prompt-only generation; availability, dimensions, and quota remain account- and service-controlled. |
| Auto-review | `enableAutoReview` | Sends bounded approval context, tool arguments, working directory, and