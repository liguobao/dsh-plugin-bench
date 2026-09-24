

<!-- banner -->
<div align="center">

# 🔐 dsh-coding-subscription-oauth

**v0.8.5** · formerly `dsh-grok-build`

**Coding-subscription OAuth for [DeepSeek Harness](https://github.com/deepseek-ai/dsh).** Use SuperGrok / X Premium (Grok Build), ChatGPT Plus/Pro (Codex), Kimi Code, Claude Pro/Max and Google Antigravity inside DSH — without a second API-key bill and **without pasting any token into chat.**

[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

*[English](README.md) · [中文版](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português (BR)](README.pt-BR.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)*

</div>

---

> **Upgrade / 升级：** Follow the versioned steps in [`INSTALL.md`](INSTALL.md). `0.8.0` adds opt-in OpenCode Go compatibility (sticky `x-opencode-session` on the local gateway). Current main pins the shared dispatcher runtime on `dsh-coding-oauth-core@0.1.2` and `undici@7.29.0`, and restricts gateway key reveal/rotate to loopback access; no configuration, credential, data, or route migration is required. Grok Imagine retains its explicit pinned dispatcher. Releases from `0.6.2` onward include the strict Cordis injection startup fix and DSH `0.1.1-rc.2` support; keep profile/config/credential files and restart one existing DSH Web process only after updating.

---

## Name change

Published first as **`dsh-grok-build`** when it only covered Grok Build. The current name matches the full coding-subscription OAuth surface.

| | Use this | Still works |
|---|---|---|
| npm (recommended) | Current release is `0.8.5`: `dsh plugin --profile web add dsh-coding-subscription-oauth@0.8.5` | No legacy npm package was published |
| GitHub / development | [`dsh-coding-subscription-oauth`](https://github.com/lninghaha/dsh-coding-subscription-oauth) | Previous GitHub repo `dsh-grok-build` was removed |
| CLI | `dsh-coding-oauth` | `dsh-grok-build` |
| Cordis plugin id | `llm-grok-build-oauth` | unchanged |
| Settings HTTP API | `/plugins/dsh-grok-build/*` | unchanged |
| Credential files | `$DSH_HOME/.grok-build-auth.json` and the other `*-oauth-auth.json` files | unchanged |

## ✨ Features

- 🧽 **Bring your own subscription** — SuperGrok, ChatGPT Plus/Pro, Kimi Code, Claude Pro/Max; no extra pay-as-you-go key.
- 🔑 **Local OAuth, no key-pasting** — authorize in Settings or CLI; access/refresh tokens never enter chat, logs or HTTP status.
- 🧩 **One plugin, five providers** — Grok Build (`cli-chat-proxy.grok.com`), Codex, Kimi Code, Claude Code and Google Antigravity.
- 🛡️ **Secure by design** — credential files are owner-only `0600`, atomically written, cross-process locked.
- ⚙️ **Dynamic catalog** — the selector lists only signed-in routes, labelled `(OAuth)`, including grok-4.6 `xhigh`.
- 🌐 **Proxy-aware** — proxies only reviewed subscription domains; Kimi China stays direct by default.
- 📥 **Manual CLI Pull** — Settings discovers allowlisted official Grok/Codex/Kimi/Claude CLI OAuth files read-only; you pull a one-way copy after preview and overwrite confirmation.
- 🗂️ **Tabbed Settings** — Accounts, Gateway, Capabilities, and About; remote hosts prefer device-code sign-in with quieter CLI-missing tips; signed-in cards stay collapsed until expanded.
- 🎛️ **Optional capabilities, default off** — Codex search, usage/quota, image generate/edit, Fast, and Grok Imagine apply live when you turn them on. An additional default-off switch lets non-Codex model routes call Codex image tools while preserving Codex sign-in, session, and attachment-ownership checks.
- 🔌 **Opt-in local API gateway** — default-off loopback OpenAI/Anthropic-compatible server for your own tools, with copyable base URLs and Bearer key; never a public relay.
- **OpenCode Go** — Connect OpenCode Go in **Accounts & Models** under the isolated provider `coding-opencode-go` (separate from DSH-native `opencode-go`) and use it in DSH without enabling Gateway. External tools use explicitly configured `coding-opencode-go/<model-id>` routes (legacy `opencode-go/<model-id>` still accepted) and the matching protocol, with a stable conversation header. The local gateway key and upstream credential are separate; missing session IDs are rejected. If an older plugin config still lives under `opencode-go`, migrate it from the Accounts card. Review the migration preview before replacing the old global gateway mode.

## Problems this plugin solves

These are the searches and DSH errors that usually lead here. If one of them is your tab title, you are in the right repo.

| You searched / saw | What was actually broken | What this plugin does |
|---|---|---|
| SuperGrok / X Premium in DSH, “Grok Build vs `api.x.ai`” | The built-in `xai` route is the **pay-as-you-go API**. Coding-plan inference is `cli-chat-proxy.grok.com` | Dedicated `grok-build` route + official CLI fingerprint headers (`X-XAI-Token-Auth`, `x-grok-client-identifier`, `x-grok-client-version`) so you do not get a silent 403 |
| `本轮运行失败` **API key is invalid** / `AUTH` mid-turn | The GUI maps **every** `AUTH` code to that banner. Often the OAuth access token just expired (Kimi ~15 min) | Refresh **5 minutes** before expiry; on a 401, invalidate the stored token and **retry the step** after refresh |
| `INVALID_REPLAY_STATE` on the second Codex / Kimi turn | Replay state still carried the native pi-ai provider id after the Harness route alias | Keep the Harness route id in replay state and heal older poisoned messages |
| grok-4.6 **xhigh** / Extra High Effort missing | Live `GET /v1/models-v2` already returns `reasoning_efforts` including `xhigh`; cloning the grok-4.5 template hides it (pi-ai treats absent `xhigh` as unsupported) | Parse live `reasoning_efforts` into `thinkingLevelMap`. grok-4.6 gets `xhigh`; grok-4.5 stays low/medium/high |
| Kimi Code 401, or requests going out as Anthropic `x-api-key` | The OAuth token was attached as an Anthropic key | Wire **only** `Authorization: Bearer` on `api.kimi.com/coding` |
| Unsigned-in Grok / Codex / Claude still in the model picker | Every registered route was listed | Unauthenticated routes expose **no models**; signed-in names show `(OAuth)` |
| Device login on a **remote / headless** DSH | Browser PKCE cannot reach `localhost` | Device-code for Grok, Codex and Kimi; Claude accepts a pasted localhost redirect URL |
| Proxy works for Grok/Codex but breaks Kimi in China | One global `HTTPS_PROXY` | Allowlisted proxy; Kimi stays **direct** unless `proxyKimi: true`. `auth.kimi.com` ≠ `api.moonshot.cn` |
| ChatGPT Plus / Claude Pro in DSH without another API bill | Separate OpenAI / Anthropic API keys | Local OAuth on `codex-oauth` / `claude-code-oauth`, coexist with existing `openai` / `kimi-coding` API-key routes |
| OpenCode Go: `MissingSessionID` | Missing stable conversation ID | DSH: use Accounts & Models; external tools: provide `x-opencode-session`. See [migration](docs/repair-candidate.md). |

Grok Build device login, live `/v1/models-v2` and Responses streaming are verified on real deployments. Codex / Kimi / Claude reuse `@earendil-works/pi-ai` native OAuth instead of re-implementing vendor flows.

## Supported providers

| Provider | Route | Auth | Coexists with |
|---|---|---|---|
| **xAI Grok Build** | `grok-build` | SuperGrok / X Premium OAuth | `xai` |
| **OpenAI Codex** | `codex-oauth` · optional `codex-oauth-fast` | ChatGPT Plus/Pro OAuth | `openai` |
| **Kimi Code** | `kimi-code-oauth` | Kimi Code OAuth | `kimi-coding` |
| **Claude Code** | `claude-code-oauth` | Claude Pro/Max OAuth | — |
| **Google Antigravity** | `agy` | `dsh-agy` Google OAuth | — |

> Grok Build's device login, dynamic `/v1/models-v2` catalog and Responses streaming are verified on real deployments. Codex/Kimi/Claude reuse the provider-native OAuth/refresh from `@earendil-works/pi-ai` instead of re-impleme