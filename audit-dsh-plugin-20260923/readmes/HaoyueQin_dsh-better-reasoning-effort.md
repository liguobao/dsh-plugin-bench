# DSH Better Reasoning Effort

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/banner-dark.svg">
    <img src="docs/banner.svg" alt="DSH Better Reasoning Effort" width="720">
  </picture>
</p>

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![npm version](https://img.shields.io/npm/v/dsh-better-reasoning-effort)](https://www.npmjs.com/package/dsh-better-reasoning-effort)
[![npm downloads](https://img.shields.io/npm/dw/dsh-better-reasoning-effort)](https://www.npmjs.com/package/dsh-better-reasoning-effort)
![DeepSeek Harness](https://img.shields.io/badge/DeepSeek%20Harness-plugin-4d6bfe)
![dsh-plugin](https://img.shields.io/badge/dsh--plugin-ecosystem-4d6bfe)
![Version](https://img.shields.io/badge/version-0.4.1-4d6bfe)
![Docs](https://img.shields.io/badge/docs-EN%20%7C%20ZH-4d6bfe)
[![Awesome DSH Plugin](https://awesome-dsh-plugin.com/badge.svg)](https://awesome-dsh-plugin.com)
[![Commit activity](https://img.shields.io/github/commit-activity/t/HaoyueQin/dsh-better-reasoning-effort)](https://github.com/HaoyueQin/dsh-better-reasoning-effort/graphs/commit-activity)
[![Last commit](https://img.shields.io/github/last-commit/HaoyueQin/dsh-better-reasoning-effort)](https://github.com/HaoyueQin/dsh-better-reasoning-effort/commits)

**English** | [中文](README.zh.md)

Reasoning-effort **and input-modality** editing for **third-party models** in DeepSeek Harness — thinking levels and image-input support declared per model, auto-adapted from a model knowledge base + wire-protocol inference, edited right inside the official Models page card. Plus a **quick reasoning-effort slider inside the official model menu** (white round thumb, integrated from HanaAyane's dsh-reasoning-effort — see [Acknowledgements](#acknowledgements)) — the composer's official bottom-right *model · effort* display is left untouched.

<p align="center">
  <img src="docs/demo.svg" alt="demo" width="640">
</p>

<p align="center">
  <img src="assets/models-page-effort-editor.png" alt="The thinking-effort editor injected into a model row on the official Models page" width="720">
</p>

## Why

The `llm-pi-ai` adapter of DeepSeek Harness natively supports per-model `reasoningEfforts` declarations (which thinking levels a model accepts, and the exact string to send on the wire for each). But the official Models page editor **deliberately keeps this field out of reach** — the official notes say it is a per-model capability and a provider-level knob would break some models. As a result:

- Third-party models get **no thinking-level picker** in the composer (`getSupportedThinkingLevels` short-circuits to `["off"]`);
- Only the official DeepSeek API (the built-in catalog) can set reasoning effort;
- Setting levels for a third-party model meant hand-writing the `reasoningEfforts` / `compat` blocks in `settings.yaml`.
- Hand-declared third-party models are treated as **text-only** (`input` defaults to `["text"]`): image attachments are refused before they are sent, the read-image tool refuses, and every gateway path in between gates on the same flag. The core already accepts a per-model `input: ["text", "image"]` declaration — the official page just does not expose it either.

This plugin brings both configuration surfaces back into the UI: **edit right inside the official model editor card**, plus **one-click auto-adapt**.

## Features

- **In-page injection**: an editor block appears in the official Models page under each model row's disclosure, next to context window / max tokens — not a separate settings page, but part of the official editing flow (same `settings.mutate` contract, same save style). The block spans the full row; its level rows split into the same two columns as the official capacity pair. It now carries two sections — **Reasoning effort** and **Input modalities** — whose changes commit with the official card's own **Save**, with the editor's **Reset** underneath them.
- **Pending until you save the card (zero writes while editing)**: the editor also appears on rows that are not saved yet, through one pipeline for two shapes — a provider's create card (auto-adapt reads the typed protocol/endpoint straight off the card), and a **new model row added under an already-saved provider** (auto-adapt then works from the stored route facts plus the display name typed on the row). **A change is pending the moment you make it**, and it lands together with your **Save** in that card — the official card freezes its own settings revision while it is open, so this plugin commits on the same Save instead of racing it (the "configured it, saved it, and it is gone" report). **Cancel** (or a reload) discards it together with the card's own fields. A declaration already in the document is never overwritten. Note staging cannot express a deliberate "unset": applying an all-clear draft simply withdraws the staging and lets host auto-fill fill its suggestion back in — to declare nothing durably, save the row first, then clear every level and Save.
- **Input-modality declaration**: one checkbox ("Image input") turns a hand-declared model vision-capable end to end — composer attachments, the read-image tool, and proxy gating all key off the same flag. Unchecking narrows the declaration to text-only; clearing it writes a durable `inputUnset` marker that host auto-fill respects, exactly like its reasoning-efforts sibling. On kernels whose official Models page already ships its own **Input-types** editor (`0.1.6-alpha.2`+), this section self-disables so there is exactly one modality surface — the capability is sniffed from the row DOM, never from a version number; older kernels keep it.
- **Endpoint-compatibility controls**: the editor carries a third section, rendered only on the protocol whose compat gate takes it. On `openai-completions` routes: the **thinking budget field** (which parameter carries the thinking-token budget — some vLLM / self-hosted endpoints read `thinking_token_budget`, others `thinking_budget` or `thinking_budget_tokens`; unset sends none) and the **vLLM priority** (scheduler priority for endpoints started with `--priority`). On `openai-responses` routes: **max_output_tokens in requests** — some Responses gateways reject the parameter, so "Omit it" keeps an output cap out of the request entirely. Controls use the official field shape (caption above, the official enum width, a hint line below) and each one says what it does. These switches are per-endpoint passthroughs, not model facts: the knowledge base deliberately never predicts them (no model is *known* to reject `max_output_tokens`), so Auto-adapt will not fill them — set them once for a gateway that needs them. Picking "Unset" and saving the card really removes the key again rather than keeping the last choice; the editor only ever deletes the fields it showed, so a compat field you wrote into `settings.yaml` by hand stays put.
- **Zoned suggestion display**: Auto-adapt reports what it applied (source · confidence) on its own line, says where modality advice came from (endpoint listing / knowledge base / name heuristic — the last one explicitly flagged low-confidence), and renders reference capacities (context window, max output) in a separate read-only block marked "hints only, never auto-filled". Values are thousands-grouped so you can copy them straight into the official capacity inputs by hand.
- **Auto-adapt**: a built-in model knowledge base (DeepSeek V3/V4/R1 with its vision experiment — re-checked 2026-09, when the current official ids became **deepseek-flash** = V4.1-Flash and **deepseek-v4-pro** = V4-Pro-0813, the older v4 spellings being compatibility aliases; the official enumeration is Off / low / high / max with high as default; plus dedicated entries for GPT-6 Astra — which rejects `none` with a 400 — and GPT-5.6-cyber; OpenAI GPT-4o/GPT-4.1/GPT-5.1–5.6 by generation including the codex variants, the o-series, the gpt-oss open weights and the n