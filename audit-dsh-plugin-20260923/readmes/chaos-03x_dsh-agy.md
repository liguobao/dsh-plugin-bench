# dsh-agy

[![CI](https://github.com/chaos-03x/dsh-agy/actions/workflows/ci.yml/badge.svg)](https://github.com/chaos-03x/dsh-agy/actions/workflows/ci.yml)
[![npm version](https://img.shields.io/npm/v/dsh-agy)](https://www.npmjs.com/package/dsh-agy)

Google Antigravity (agy) access for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness):
OAuth authentication, a multi-account pool with automatic 429 rotation, device
fingerprinting, and both CLI and web management.

> 中文文档：[docs/README_zh.md](docs/README_zh.md)

## Features

- **OAuth login**: one-click sign-in via browser OAuth callback, with headless
  paste-URL mode and a remote paste-credential blob channel.
- **Two management surfaces**: web and CLI, either one works, core features are
  the same.
- **Multi-account pool**: encrypted account store, usage-aware account
  selection (family-scoped quotas, OMP-aligned ranking), automatic rotation on
  rate limits, per-account cooldown to the real reset time, per-account device
  fingerprints.
- **Quota dashboard**: only active when DSH Web is running; append `/agy` to
  your dsh web address: login, account management, per-model quota bars, model
  testing, credential export/import, fingerprint management.
- **CLI**: `dsh-agy login|status|import|verify|logout` works standalone, with or
  without a harness.

## Screenshots

The `/agy` dashboard inside DSH Web — account cards, per-model quota bars, and
one-shot model tests:

![dsh-agy dashboard](https://raw.githubusercontent.com/chaos-03x/dsh-agy/main/assets/screenshot_en.png)

## Quickstart

### Path A: DSH Web GUI Users (Recommended — 100% Web UI, zero CLI commands)

For users using DeepSeek Harness browser workspace / Web GUI:

```sh
# 1. Install plugin into DSH web profile (via dsh CLI, or pnpx/npx if dsh is not in PATH)
dsh plugin --profile web add dsh-agy
# or: npx @deepseek-ai/dsh plugin --profile web add dsh-agy

# 2. Launch DSH Web
dsh web

# 3. Open dashboard at http://127.0.0.1:3080/agy
# Click "Login with Google", complete OAuth authorization, and start using the agy provider
```

Open **Settings → Plugins → Antigravity → Open Antigravity dashboard**; the button opens `/agy` in a new tab.

### Path B: Headless / Terminal Only (Standalone CLI)

For Linux VPS, SSH remote servers, or headless CI environments:

```sh
# Run directly without global install (npx / pnpx)
npx dsh-agy login
npx dsh-agy status

# Or install globally
npm install -g dsh-agy
dsh-agy login          # interactive OAuth (browser, --headless paste, or --blob)
dsh-agy status         # list accounts + quota summary
dsh-agy verify         # refresh + health check
dsh-agy health         # batch health check (optionally on an interval)
dsh-agy import <file>  # import agy auth.json or credential blob (--blob)
dsh-agy logout         # remove account
```

## CLI reference

| Command | Options | Description |
|---|---|---|
| `dsh-agy login` | `--headless` — print the auth URL and wait for a pasted redirect URL<br>`--blob` — print a paste-credential blob instead of storing the account<br>`--port <n>` — loopback callback port (default `51121`)<br>`--project <id>` — bind the login to a specific project<br>`--timeout <ms>` — callback timeout (default `300000`) | Interactive Google OAuth |
| `dsh-agy status` | — | List accounts + per-model quota summary |
| `dsh-agy import <files...>` | `--blob` — the pasted value is a credential blob<br>`--email <email>` — set the account email (skips userinfo verification)<br>`--overwrite` — replace an existing account with the same email | Import agy auth.json files or credential blobs (multiple files / multi-line paste = batch import) |
| `dsh-agy export` | `--index <n>` — export one account by index (default: all)<br>`--out <dir>` — write one `dsh-agy-<index>.blob` per account (default: print to stdout, one blob per line) | Export account credentials as paste blobs |
| `dsh-agy verify` | `--index <n>` — verify one account by index (default: all) | Refresh + health check |
| `dsh-agy health` | `--index <n...>` — check only these accounts (default: all enabled)<br>`--interval <ms>` — repeat on an interval instead of once | Batch health check (refresh + userinfo), re-enables accounts whose credentials are live again |
| `dsh-agy logout` | `--index <n>` — account index (default: active)<br>`--email <email>` — account email | Remove an account |

### Per-account proxy

Each account can have its own proxy; credentials are encrypted at rest and displayed masked as `protocol//host:port`.

```sh
dsh-agy login --proxy socks5://user:pass@host:1080
dsh-agy import --proxy <url> file.json
dsh-agy proxy set --index 0 --proxy <url>   # set / update
dsh-agy proxy clear --index 0               # clear (fall back to env)
dsh-agy proxy test --index 0                # TCP 2s fast-fail probe
dsh-agy proxy list                          # masked list
dsh-agy status                              # shows proxy column (masked host:port)
```

Fallback: with no per-account proxy, requests use `EnvHttpProxyAgent` (`HTTP_PROXY`/`HTTPS_PROXY` with `NO_PROXY` honored). Per-account proxies ignore `NO_PROXY`, are fail-closed (unreachable proxy skips the account without cooldown and clears affinity), and loopback targets (`localhost`/`127.0.0.1`/`::1`) are always forced direct.

Web dashboard (`/agy`): each account card shows an inline Proxy row `[input] [Save][Clear][Test]` with masked `host:port`; writes via `POST /agy/api/proxy`, probes via `POST /agy/api/proxy/test`.

### Path C: Local Development & Link

```sh
git clone https://github.com/chaos-03x/dsh-agy.git
cd dsh-agy && pnpm install && pnpm run build
dsh plugin --profile web link .
```

Requires Node >= 22.

## Uninstall

```sh
# 1. Remove the DSH plugin from a profile
dsh plugin --profile web remove dsh-agy

# 2. Uninstall the CLI
npm uninstall -g dsh-agy

# 3. Optional: delete local account data (accounts + master key + fingerprint override)
dsh-agy logout              # remove accounts first (or skip)
rm -f ~/.dsh/agy-accounts.json
# remove only the AGY_MASTER_KEY line from ~/.dsh/.credentials.yaml — keep other keys!
rm -f ~/.dsh/agy-fingerprint-data.json   # only if you created an override

# 4. Optional: revoke the Google-side authorization
#    Google account security → Third-party access → revoke "Antigravity"
```

Deleting local files does **not** revoke Google-side tokens; the refresh token stays
valid until it expires or you revoke it in your Google account security settings.

## Other things you may care about

### Rotation mechanics

Usage-aware selection: when several accounts are available, requests rank them
by the requested model's backend counter family (`gemini-*` → Google,
`claude-*` → Anthropic, `gpt-*` → OpenAI): accounts whose quota is about to
reset with headroom left are used first ("use it or lose it"), near-exhausted
families are avoided, and exhausted families block the account until the real
reset time.

429 (Too Many Requests) responses:

| Category | Behavior |
|---|---|
| `soft_rate_limit` (Retry-After < 3s) | immediate retry on the same account, no cooldown |
| `rate_limited` | cooldown until the server-reported reset time (capped 30min, 5min fallback) + switch to the next account (same account when single) |
| `quota_exhausted` ("quota reached", "individual quota", RESOURCE_EXHAUSTED…) | cooldown until the server-reported reset time (capped 24h) — no further calls to that account until then |
| `unknown` | exponential backoff |

401/403 → account revoked (marked for re-authentication). Success resets the failure
counter.

### Risk controls (environment switches)

| Env | Effect |
|---|---|
| `DSH_AGY_DISABLE=1` | Kill switch: the plugin registers nothing (provider + `/agy` routes) and the CLI refuses to run. |
| `DSH_AGY_FINGERPRINT_MODE=stable` | One fixed client identity per account — no per-request header randomization, no fingerprint regeneration (OMP-style fixed-client posture). Default `dynamic` keeps per-request randomizatio