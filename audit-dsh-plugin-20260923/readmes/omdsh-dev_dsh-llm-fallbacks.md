# dsh-llm-fallbacks

[English](README.md) | [中文](README.zh-CN.md)

[![npm](https://img.shields.io/npm/dt/dsh-llm-fallbacks)](https://www.npmjs.com/package/dsh-llm-fallbacks)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![node](https://img.shields.io/badge/node-%3E%3D22-339933.svg)
![pnpm](https://img.shields.io/badge/pnpm-%3E%3D10-f69220.svg)
![dsh tui](https://img.shields.io/badge/dsh%20tui-compatible-4B32C3.svg)
![dsh](https://img.shields.io/badge/DSH-0.1.7--rc.1-4B32C3.svg)
[![dshfind](https://dshfind.com/api/badge/omdsh-dev/dsh-llm-fallbacks?lang=en)](https://dshfind.com/zh/plugins/omdsh-dev/dsh-llm-fallbacks?ref=badge)

Automatic provider/model fallback chains for dsh (DeepSeek Harness): when an agent's LLM requests keep failing — retries exhausted, auth errors, quota exceeded, rate limiting (429) — the plugin switches provider/model along the fallback chain for the current role, and the current step/turn continues on the target model: tasks are not interrupted by model problems.

Works in both dsh front ends: the **web** profile (Settings → Plugins → Fallbacks card) and the **dsh-tui** terminal profile (`/fallbacks` session diagnostics, `/fallbacks config` readback, and the `/settings` fallbacks section for editing).

## Time slots

Time slots rotate the **effective root chain** by wall-clock windows: each slot row carries its own fallback chain, and the first row whose window contains the current moment replaces the all-day chain for the next root request — the all-day chain stays as the last resort when no slot matches. Peak and valley windows can therefore use different chains while the failure walk (fallback switch) remains untouched.

![Time slots](docs/assets/screenshot-1-en.png)

Four frozen UTC+8 presets (windows are code constants; preset rows lock `tz` to Asia/Shanghai):

| Preset | Window |
|---|---|
| `liang-peak` | Monday–Friday 09:00–12:00 and 14:00–18:00 |
| `liang-valley` | every other UTC+8 time (complement of Liang Peak) |
| `glm-peak` | Monday–Friday 14:00–18:00 |
| `glm-valley` | every other time (complement of GLM Peak) |

GLM Peak and GLM Valley are offered in the card picker only when `zai-coding-cn` is configured.

The first extra row whose window contains the current moment (in `fallbacks.tz`, default Asia/Shanghai) wins; no match → the all-day `rootChain`, whose tail (Default model) must be exactly one official model — `deepseek-official/deepseek-flash` or `deepseek-official/deepseek-pro` (XOR). Slot rotation is a routing seed, not a failure decision: it applies on the next root request, consumes no cooldown, and is logged as a time-slot switch — failure walks keep fallback switch. Full semantics → [Time-slot presets](#time-slot-presets) and [docs/configuration.md](docs/configuration.md).

## Quick start

### Install

```sh
dsh plugin --profile web add dsh-llm-fallbacks      # web profile (Settings → Fallbacks card)
dsh plugin --profile dsh-tui add dsh-llm-fallbacks  # dsh-tui terminal profile
```

Same plugin, either front end — the only difference is the `--profile` flag. Pin a version with `@<version>`. A registry install fetches the **built package** (`dist/`), nothing builds on the target machine. Registry / git / local-directory variants, uninstall, and `--dump-config` verification → [docs/install.md](docs/install.md).

### Configuration surfaces

The plugin's settings live in a shared `fallbacks:` namespace, editable from three surfaces:

| Surface | What it is | Notes |
|---|---|---|
| **Web settings card** | Settings → Plugins → Fallbacks | Full GUI editor for the `fallbacks:` namespace; writes the shared settings document |
| **`$DSH_HOME/settings.yaml`** | `fallbacks:` section in the dsh settings document | The shared source of truth — the same file the web card writes; readable and editable everywhere, including scripted setups |
| **TUI `/settings`** | fallbacks section in the dsh-tui settings screen | dsh-tui ≥ v0.8.5; native fields for simple keys, JSON text fields for complex structures (see [dsh-tui profile (terminal)](#dsh-tui-profile-terminal)) |

Pick the surface that matches your front end: web users get the card, terminal users get `/settings`, and the YAML file works everywhere. (`/fallbacks` and `/fallbacks config` are diagnostics — read-only views, not edit surfaces.)

### Minimal configuration

Add a `fallbacks:` section to the shared settings document (`$DSH_HOME/settings.yaml` — see [Configuration surfaces](#configuration-surfaces)):

```yaml
fallbacks:
  enabled: true            # feature switch — defaults to off (plugin is a no-op otherwise)
  rootChain:               # all-day chain: leading entries = fallback walk, last = Default model (official)
    - anthropic/claude-3-5-sonnet          # walked first
    - deepseek-official/deepseek-flash  # last resort (Flash or Pro)
  timeSlots:               # optional: rotate the effective root chain by wall-clock windows
    - kind: preset         # frozen UTC+8 window; only the chain is editable
      preset: liang-peak   # Monday–Friday 09:00–12:00 and 14:00–18:00
      chain:
        - anthropic/claude-3-5-sonnet
    - kind: custom         # custom window (may wrap midnight)
      name: evening        # optional display name
      start: '22:00'
      end: '02:00'
      days: [1, 5]         # optional; omitted/empty = every day (0=Sunday…6=Saturday)
      chain:
        - openai/gpt-4o
  roles:                   # optional: declare role entities, then reference them from rules
    list:
      - id: reviewer       # unique id; "inherit" is reserved
        persona: Code-review subagents
        chain:
          - openai/gpt-4o-mini
        fallback: inherit-root   # role chain first, then the inherited rootChain
    rules:                 # subagent-only: rules never match root requests
      - role: reviewer     # all subagents → the reviewer role
```

Build the section up in four steps:

**1. Enable the plugin.** `enabled: true` turns the fallback engine on. It defaults to **off** — with no chains configured the plugin is a complete no-op.

**2. Set the all-day `rootChain`.** Leading entries are the fallback chain, walked first when a request fails; the **last** entry is the Default model.

> **Conformance**: the last entry must be exactly one official model — `deepseek-official/deepseek-flash` or `deepseek-official/deepseek-pro` (XOR). The settings card and gateway reject any other tail on save; a legacy non-official tail warns at startup and keeps working as a fallback-only walk, but cannot be saved as-is. The retired `deepseek-v4-flash` / `deepseek-v4-pro` ids are no longer legal tails — a saved V4 tail now warns, goes inert (slot rows + virtual picker), and blocks save until a legal tail is picked. `deepseek-pro` is a legal selector whose model is not yet served by the catalog: the card shows it disabled ("not yet available"), and requests to it fail at the provider until the gateway enables the id. The plugin does not probe catalog availability — a chain containing `deepseek-pro` dispatches to it like any other exact entry, and on the virtual route the `stream()` delegate serves the first dispatchable exact head of the effective chain, so a chain with a working entry before Pro still routes to that earlier entry.

**3. Add `timeSlots` (optional).** Rows rotate the effective root chain by wall-clock windows. Preset rows use frozen UTC+8 windows (only their chain is editable; while a preset row exists, `tz` locks to `Asia/Shanghai`); custom rows take `start`/`end` (may wrap midnight) and an optional `days` list. The first row whose window contains the current moment wins; no match → the all-day `rootChain`. Rotation is a routing seed — it applies on the next root request and consumes no cooldown (see [Time slots](#time-slots)).

**4. Add `roles` (optional).** Declare role entities in `roles.list` (id, persona, chain, optional `fallback` policy), then map subagents to them with `roles.rules`. Rules never match 