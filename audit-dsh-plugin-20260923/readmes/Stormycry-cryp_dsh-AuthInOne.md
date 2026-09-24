# dsh-AuthInOne

English | [简体中文](README.zh-CN.md)

![dsh-AuthInOne cover](docs/assets/cover.png)

dsh-AuthInOne is a DeepSeek Harness plugin for Provider login, API and custom OpenAI-compatible Provider setup, model switching, optional vision fallback for text-only models, token usage analytics, and cost tracking inside DSH's native **Models** and **Usage** settings.

OpenAI Codex uses browser OAuth with state, S256 PKCE, and a loopback callback. Kimi Code opens the Provider's complete authorization link backed by an RFC 8628 device flow; the link carries the short code, so the user normally only signs in and confirms. xAI Grok, Anthropic, GitHub Copilot, Command Code, Cursor, Google Antigravity, and Kiro are explicitly marked **Experimental compatibility**. Installed-Host validation reached each Provider's authorization boundary and stopped before user consent; mock/fixture tests cover exchange or polling, refresh rotation, denial, timeout, cancellation, logout, route activation, and secret redaction.

> **Alpha `v0.2.0-alpha.4`** · exact compatibility target: official DSH `47f9438` · the self-contained bootstrap uses the official DSH plugin CLI and returns Web on its original port · [release notes](docs/releases/v0.2.0-alpha.4.md) · MIT · community-maintained and not a DeepSeek or OpenAI product.

```sh
pnpm dlx github:Stormycry-cryp/dsh-AuthInOne#v0.2.0-alpha.4 install --profile web
```

The command is owned by this package. It validates the running standard DSH Host, calls the official `dsh plugin` add path, then replaces that Host on the same URL. It does not require a patched DSH core, a manual profile edit, a second Web instance, or a temporary port. See [Install, upgrade, and remove](#30-second-install-upgrade-and-remove) for source-checkout and non-default-port forms.

If AuthInOne is useful to you, a [Star on GitHub](https://github.com/Stormycry-cryp/dsh-AuthInOne) is a welcome way to support the project.

Open DSH, then go to **Settings → Models** or **Settings → Usage**. The browser receives aggregated usage, redacted status, an authorization URL, and where required a user code. OAuth verifier, authorization code, device code, access token, and refresh token stay on the Host; the plugin never imports `~/.codex/auth.json`, OpenCodex state, cookies, browser storage, OTPs, or another product's credentials.

Agent instruction: **Run the documented `pnpm dlx … install --profile web` command as one operation. Do not split it into a manual `dsh plugin add` plus an improvised restart. The AuthInOne bootstrap must verify the listener, install through the official DSH plugin CLI, return the original URL, and report `ready` before UI acceptance. Never start a second Web instance, choose a temporary port, patch DSH, edit profile YAML, or read credentials. If the bootstrap rejects an unknown launcher or DSH owner fingerprint, stop and show that error instead of guessing.**

## Use this plugin when

- you want OpenAI Codex or Kimi Code login inside DSH, or knowingly opt into a labeled compatibility flow;
- you manage API-key or custom OpenAI-compatible Providers in DSH's native Models page;
- you switch the future-session default model without replacing DSH's per-session selector;
- you want a separately configured vision model to describe images only when the selected main model explicitly declares text-only input;
- you need reconstructable Provider/model/tool token usage and auditable calculated cost.

![DeepSeek Harness Models settings with Provider state and OpenAI Codex account authorization](docs/assets/models-dark-desktop.png)

![DeepSeek Harness Usage settings with token activity, model usage, and cost analytics](docs/assets/usage-light-desktop.png)

Additional real DSH captures: [Auth login dialog](docs/assets/auth-login-dark.png), [Models action area](docs/assets/models-auth-actions-dark.png), [dark Usage](docs/assets/usage-dark-desktop.png), [light narrow Usage](docs/assets/usage-light-narrow.png), [dark narrow Usage](docs/assets/usage-dark-narrow.png), and [second-precision time range](docs/assets/usage-time-range-light.png).

## Verified capabilities

| Capability | Status | Verification | Minimum DSH |
| --- | --- | --- | --- |
| OpenAI Codex browser account authorization | **Verified to user-confirmation boundary** | Real navigation reached `auth.openai.com`; mock issuer covers callback, state/PKCE, exchange, refresh, denial, expiry, cancellation, logout, revocation, and redaction | Official DSH `47f9438` with the bundled compat owner |
| Kimi Code authorization connection | **Experimental; verified to user-confirmation boundary** | Installed Host returned the complete Kimi authorization link without returning the Host-only device code; the UI does not ask users to re-enter a short code already embedded in that link | Official DSH `47f9438` with bundled compat owner |
| Seven compatibility account flows | **Experimental; verified to user-confirmation boundary** | xAI, Anthropic, GitHub Copilot, Command Code, Cursor, Antigravity, and Kiro each reached their expected authorization boundary; mocked completion registers and later disposes the corresponding model route | Official DSH `47f9438` with bundled compat owner |
| Provider subscription quota | **Best effort where upstream data exists** | Codex, Kimi, xAI, Anthropic, Cursor, and Antigravity have token-free Remote projections; the Models page omits the quota block when the upstream response is missing, incomplete, unsupported, or cannot yield a reliable percentage | Official DSH `47f9438` with bundled compat owner |
| Plan/API presets | **Available with vendor limits shown** | OpenAI, xAI, Gemini, Anthropic, Kimi Code, GLM Coding Plan, and ModelStudio/Qwen presets write credentials through DSH; GLM and Qwen usage restrictions remain visible | Official DSH `47f9438` with bundled compat owner |
| DeepSeek API-key Provider and live model call | **API-key only** | Native Provider remained connected; a real DeepSeek call populated Usage without exposing the key | DSH `0.1.0-rc.6` |
| Custom OpenAI-compatible Base URL, headers, model mapping | **Native DSH capability** | AuthInOne preserves the native Models cards and reads their public Provider projection | DSH `0.1.0-rc.6` |
| Future-session default model and connection test | **Verified** | Models contribution and Host/Remote route exercised in the installed Web profile | Official DSH `47f9438` with bundled compat owner |
| Vision fallback for text-only main models | **Verified** | PNG/JPEG/WebP/GIF use DSH `ImageBlock` references; multi-image, native multimodal pass-through, disabled fallback, failure, resume, and fork paths have keyless coverage | Official DSH `47f9438` with bundled compat owner |
| Cross-session Usage and cost analytics | **Verified** | Real DSH session logs rebuilt 26,383 Token into KPI, heatmap, model, Provider, bucket, and cost projections | DSH `0.1.0-rc.6` |
| Usage navigation icon | **Verified** | The bundled generic owner projects a keyed icon seat; AuthInOne contributes a 16 px three-bar `currentColor` icon and unknown sections retain the native fallback | Official DSH `47f9438` with the bundled compat owner |

### Account-login support matrix

| Provider | Flow | Stability | Authorization boundary verified | Refresh/logout/model route | Quota |
| --- | --- | --- | --- | --- | --- |
| OpenAI Codex | Browser OAuth, state + S256 PKCE + loopback | Stable | `auth.openai.com` | Yes / Yes / Yes | Primary and secondary windows, best effort |
| Kimi Code | Complete authorization link backed by RFC 8628 | Experimental | `www.kimi.com` | Yes / local logout / Yes | Best effort |
| xAI Grok | Device login | Experimental | `accounts.x.ai` | Yes / Yes / Yes | Weekly or monthly, best effort |
| Anthropic | Browser/manual compatibility login | Experimental compatibility | `claude.ai` | Yes / local logout / Yes | Best effort |
| GitHub Copilot | Device login | Experimental compatibility | `github.com` | Yes / local logout /