# dsh-thinking-effort

A [DSH (DeepSeek Harness)](https://github.com/deepseek-ai/deepseek-harness) plugin that adds configurable reasoning effort levels to hand-declared `llm-pi-ai` models and sets a default reasoning effort for subagents.

[![npm version](https://img.shields.io/npm/v/@hytime/dsh-thinking-effort)](https://www.npmjs.com/package/@hytime/dsh-thinking-effort)
[![npm downloads](https://img.shields.io/npm/dm/@hytime/dsh-thinking-effort)](https://www.npmjs.com/package/@hytime/dsh-thinking-effort)
[![GitHub license](https://img.shields.io/github/license/hytime/dsh-thinking-effort)](https://github.com/hytime/dsh-thinking-effort/blob/main/LICENSE)

- [中文 README](./README.zh.md)
- [日本語 README](./README.ja.md)
- [한국어 README](./README.ko.md)
- [Installation guide](./docs/INSTALL.md)
- [中文安装指南](./docs/INSTALL.zh.md)
- [日本語インストールガイド](./docs/INSTALL.ja.md)
- [한국어 설치 안내](./docs/INSTALL.ko.md)
- [Changelog](./docs/CHANGELOG.md)
- [日本語 changelog](./docs/CHANGELOG.ja.md)
- [한국어 changelog](./docs/CHANGELOG.ko.md)

> **Compatibility boundaries:** DSH Runtime compatibility covers the Settings transport only: modern DSH exposes `remote.settings`, while legacy DSH exposes `connection.api.settings`. The plugin detects the available runtime capability and keeps the legacy fallback optional, so the settings page does not require a Remote provider on older DSH builds.
>
> Gateway Protocol compatibility is a separate layer. When the DSH schema exposes them, the plugin supports 15 common scalar `llm-pi-ai.compat` fields, grouped into role/reasoning, format/output, streaming/tools, and storage/cache. Boolean fields offer `Auto`, supported, and unsupported; enum fields offer `Auto` and their concrete values. DSH `0.1.0-rc.7` does not provide gateway compat settings. DSH `0.1.0-rc.8` through `<0.1.2-alpha.1` provide the other fields, but not `supportsFinishReason` or `supportsThinkingTokenBudget`; DSH `0.1.2-alpha.1` and later expose all 15 when supported by the schema. The optional `dsh-llm-openai-completions` transport can take over eligible custom OpenAI-compatible thinking providers when it is installed and enabled. `Auto` unsets the current-layer override and restores the next value in the inheritance chain.
>
> DSH `0.1.2-alpha.1` and later accept language-pack locale IDs through `LocaleRuntime`. This plugin registers `ja` and `ko` dynamically, so no DSH core fork is required. Older DSH builds that only expose built-in locale IDs support `zh` and `en` only.
>
> The published runtime entries are `lib/index.js` (Host) and `lib/client.js` (Client). After changing TypeScript or locale sources, run `npm run build` before running DSH or packing the plugin. Current DSH does not expose a public semver metadata contract, so runtime capability detection is authoritative. An optional version is used only when explicit metadata or test input supplies it; unknown valid versions still use the detected capabilities. The plugin supports both modern `remote.settings` and legacy `connection.api.settings`.
>
> The Host registers its `dsh-thinking-effort` Settings namespace through the host-provided Settings `installSection` when available, and falls back to the legacy `register` path otherwise. Under the `0.1.7`+ entry-config model neither path exists, and the section comes from the exported `Config` instead. It does not depend on `@deepseek-ai/dsh-settings` at runtime, so the package installs cleanly into DSH profiles configured with `autoInstallPeers: false` without introducing a second Cordis runtime.

## DSH compatibility

| DSH range | Gateway compatibility settings |
| --- | --- |
| `0.1.0-rc.7` | Not available |
| `0.1.0-rc.8` to `<0.1.2-alpha.1` | Available when exposed by the DSH schema, but without `supportsFinishReason` and `supportsThinkingTokenBudget` |
| `0.1.2-alpha.1` to `<0.1.7-0` | All 15 fields when exposed by the DSH schema. Releases at or beyond the newest bound are unmapped: the plugin keeps working and follows the capabilities the running host reports instead |

From DSH `0.1.0-rc.8` onward, field availability follows the runtime schema. The table shows the maximum field set for each DSH version; the route protocol can further reduce it.

A gateway compat field can be configured only when the DSH version, runtime schema, and route's `api` protocol all support it. Unsupported fields stay hidden and are not written to Settings. Among these 15 fields, `openai-completions` supports all 15, while `openai-responses`, `azure-openai-responses`, and `openai-codex-responses` support only `supportsDeveloperRole`, `supportsStrictMode`, and `supportsLongCacheRetention`. If `api` is missing or unrecognized, the runtime schema and DSH validation remain the final authority.

DSH `0.1.7` and later derive each settings form from the Loader entry's own `Config` schema (the entry-config model); a plugin that exports none gets no form at all. This plugin exports that schema, so on `0.1.7`+ its section is the Loader entry id `thinking-effort`, while `0.1.0-rc.7` through `0.1.6` keep the registered namespace `dsh-thinking-effort`; the Client resolves whichever id the running Host publishes. `subagentEffort` now lives in this plugin's own section, and on `0.1.7`+ the old `llm-pi-ai` location is no longer a fallback: that section's schema declares only `providers`, so the Host refuses a write to any other path and drops undeclared keys from the user layer it reports. An existing subagent default therefore reads as unset there and has to be chosen again in the plugin's settings card. A snapshot this plugin exported before `0.1.7` still carries the value inside `llm-pi-ai`; importing it migrates the value into the plugin's own section, which is also what lets its providers import, because the Host refuses the whole batch when any op path is not volatile. On `0.1.7`+ settings are stored in the active profile's `cordis.patch.yml` instead of `~/.dsh/settings.yaml`, which `0.1.7` no longer uses.

## Why use it?

The `llm-pi-ai` adapter supports hand-declared third-party models, but those entries often do not declare `reasoningEfforts`. As a result, Composer does not show a reasoning effort selector, and gateway-specific values such as `ultra` cannot be mapped to DSH's standard levels.

This plugin provides the configuration layer needed to:

- Add default `off`, `high`, and `max` options to models your own profile declares without a declaration; a model that only a composition base or a schema default supplies is left unfilled and counted in the Host log;
- Configure reasoning levels per model from the DSH settings page;
- Map a DSH level such as `high` to a gateway value such as `ultra`;
- Set a default reasoning effort for subagents while preserving explicit request values;
- Keep existing user-defined model declarations unchanged.

The plugin is usually unnecessary when you only use built-in DSH models and their reasoning controls already work.

## Identifiers

These identifiers have different responsibilities:

| Identifier | Purpose |
| --- | --- |
| `@hytime/dsh-thinking-effort` | npm package, browser bundle path, loader ID, and host/client runtime ID |
| `thinking-effort` | Cordis composition entry ID and settings Slot ID |

## Features

| Feature | Description |
| --- | --- |
| Default levels | Adds `off`, `high`, and `max` without overwriting custom values, for the models your user layer declares; a model only a composition base or a schema default supplies is left unfilled and counted in the Host log |
| Per-model editor | Select levels and configure gateway values for both catalog/modelOverrides and `models[]` entries in Settings |
| Gateway compatibility | Configure 15 common scalar fields globally per provider or separately per model, grouped by role/reasoning, format/output, streaming/tools, and storage/cache; groups are collapsed by default |
| OpenCode session Header | Enable a dynamic `x-opencode-session` per exact model. By default a deterministic `ses_…` generator bo