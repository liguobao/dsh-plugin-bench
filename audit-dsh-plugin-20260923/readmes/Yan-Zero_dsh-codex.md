# dsh Codex

English | [中文](README.zh.md)

**[Migration guide: repair Sessions created by dsh-codex versions before 0.3.0](docs/session-repair.md)**

Use a ChatGPT subscription in [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) through OpenAI's Codex sign-in flow—no OpenAI Platform API key required and no dsh source patch required.

`dsh-codex` is an independent dsh bundle. It adds:

- ChatGPT OAuth from the dsh Settings panel or a standalone CLI, with automatic token refresh
- the Codex GPT catalog, including vision-capable models when the account offers them
- a live client-side context-window capacity override for dsh's token meter and compaction policy
- streaming, tool calls, reasoning replay, prompt caching, and dsh compaction through the normal LLM service
- Codex standalone web search through dsh's existing `web_search` tool
- optional HTTP(S) URL input added to Harness's existing `read_image` tool
- an `imagegen` tool backed by `gpt-image-2`, with workspace or conversation reference images and automatic workspace output
- browser image input through dsh's existing paste and drop controls
- a per-conversation Fast Mode switch and compact weekly quota indicator in the Web composer
- optional backend-authorized model recovery, including hidden Luna Reserve routing
- a three-scope HTTP(S) proxy control for Codex-only or process-wide routing

ChatGPT subscription authentication and usage-based OpenAI API access are different products. This plugin uses the ChatGPT Codex backend only; it does not turn a subscription into a general-purpose OpenAI API credential.

## Install

Install the prebuilt bundle from npm into the selected dsh profile:

```sh
dsh plugin --profile web add dsh-codex
dsh web
```

From a DeepSeek Harness source checkout, use `pnpm dsh plugin --profile web add dsh-codex`. A local plugin checkout can still be installed with `link:/absolute/path/to/dsh-codex` for development.

Open **Settings → OpenAI Codex → Sign in with ChatGPT**. The plugin opens OpenAI's authorization page and completes the localhost callback. The account page shows live Codex quota bars and exact remaining percentages; exact credit balances or workspace limits appear only when the account API supplies them.

Loopback Web pages are trusted automatically. If dsh runs on another machine, the account page shows the exact origin command that must be approved on the dsh host, for example `dsh plugin --profile web exec dsh-codex trust-origin http://host:port`. The allowlist is exact-origin, stored separately from OAuth credentials, and can be inspected or revoked with `trusted-origins` and `untrust-origin`.

The CLI remains available for terminal and headless installations:

```sh
dsh plugin --profile web exec dsh-codex login
dsh plugin --profile web exec dsh-codex login --device-code
dsh plugin --profile web exec dsh-codex status
dsh plugin --profile web exec dsh-codex doctor --json
dsh plugin --profile web exec dsh-codex logout
```

For `dsh-tui`, install the bundle into the same profile:

```sh
dsh plugin --profile dsh-tui add dsh-codex
```

After restarting the TUI, `/model` lists the `openai-codex` catalog. With no explicit route or saved selection, the TUI adopts the bundle's `gpt-5.6-sol` default. Use `/codex status|login|logout|usage|config` for the account and live settings; `/codex set backend-fallback on|off` controls automatic model recovery, while the remaining switches are listed by `/codex set`. Browser login shares the same dsh credential file used by the Web profile.

Codex, Claude Code, and other automation agents should follow [INSTALL.md](INSTALL.md). It is a complete, idempotent runbook and does not require reading this repository's source or design notes.

The bundle selects `openai-codex` / `gpt-5.6-sol` for new agents and selects the Codex search provider. A model already saved in dsh settings still takes precedence; the model picker can select any other Codex model visible to the signed-in account.

Automatic model fallback is off by default. When enabled under **Settings → OpenAI Codex**, the plugin follows only a recovery instruction returned by OpenAI for the current account. Ordinary recovery uses the backend's ordered replacement list; a `luna_reserve` instruction resolves the official hidden `gpt-reserve` route with Luna's context, reasoning, and image capabilities. The decision happens before dsh prepares the retry, so the actual model, context budget, image admission, and Session request header agree. A vision route never falls back to a text-only replacement, keeping attachments, `read_image`, and `imagegen` available. If no compatible fallback exists—or the usage refresh fails—the original quota failure continues through Harness's normal retry path. `imagegen` remains independent and follows Codex's current fixed `gpt-image-2` model.

## Model catalog

The plugin reads the Codex CLI/Desktop `models_cache.json` to discover models not yet bundled by pi-ai and update their names, input modalities, reasoning levels, and default `context_window`. It checks the file specified by `DSH_CODEX_MODELS_CACHE`, then `CODEX_HOME/models_cache.json`, then `~/.codex/models_cache.json`. Only valid entries with `visibility: list` are imported; the maximum expandable window does not replace the default capacity.

Codex CLI/Desktop refreshes this cache. Catalog discovery reads model metadata only and does not launch a Codex subprocess. OAuth login remains separate unless `credentialFile` is explicitly configured (see below). After updating and opening Codex, reopen the plugin's model settings or refresh the model list to discover changes. Missing, corrupt, or partially written caches retain the last usable catalog; a fresh start without a cache uses bundled models, including GPT-6 Astra. Catalog metadata does not guarantee model access for the account signed into dsh.

Saved model selections are preserved. Enable newly discovered models in the settings below; a temporarily unavailable cache does not delete saved model IDs. Newly discovered models without bundled pricing use a zero cost estimate, which does not mean the model is free.

By default, the model picker advertises the complete `openai-codex` catalog. Open **Settings → OpenAI Codex** and use the model checkboxes to choose which entries remain visible. The selection is live and durable; dsh refreshes the Web and TUI model directories after it changes.

The same initial subset can be seeded through `models` on the `llm-openai-codex` entry while preserving provider order:

```yaml
- id: llm-openai-codex
  config:
    models:
      - gpt-5.6-luna
      - gpt-5.6-sol
      - gpt-5.6-terra
```

The checkboxes and `models` setting control discovery only. A hidden model already stored in an existing session or supplied explicitly remains resolvable, so narrowing the picker does not invalidate older records. Omit `models` to start with the full catalog; an empty list advertises no models.

## Context window

Open **Settings → OpenAI Codex → Context window** to override the client-side capacity in K tokens. For example, enter `512` for 512,000 tokens. Leave the field empty to restore each model's pi-ai catalog default. The saved value applies to every Codex model on its next request and is shown by `/codex config`; an open conversation's meter refreshes after that request.

The initial value can also be seeded in exact tokens:

```yaml
- id: llm-openai-codex
  config:
    contextWindow: 512000
```

This mirrors Codex CLI's `model_context_window` concept on the Harness side; no context-window field is sent to the Responses endpoint. The resolved capacity drives dsh's context meter, overflow classification, output-token clamping, and automatic-compaction threshold. A smaller value compacts earlier. A larger value does not increase the backend model's real capacity, so unsupported values can still end in a provider overflow error.

## Network proxy

Open **Settings → OpenAI Codex → Netwo