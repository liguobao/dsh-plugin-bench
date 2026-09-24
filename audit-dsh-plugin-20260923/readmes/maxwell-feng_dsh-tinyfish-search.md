# dsh-tinyfish-search

English | [Chinese](README.zh.md)

> [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) plugin that backs the built-in `web_search` tool with the [TinyFish Search API](https://docs.tinyfish.ai/search-api). One GET per query, no model call — fast and free (TinyFish Search is free at any wallet balance).

## What it does

DeepSeek Harness's built-in `web_search` tool normally runs through the DeepSeek Anthropic-compatible endpoint (`web-search-deepseek`). This plugin registers an alternative **web search provider** on the `ctx.web` capability seam:

- Stable provider id: `tinyfish`
- Every `web_search` call becomes `GET https://api.search.tinyfish.ai?query=...` with the `X-API-Key` header
- `results[]` (title / snippet / url / date) are normalized into the seam's portable source shape
- No LLM turn consumed per search — unlike the Anthropic server-tool approach

Installing the bundle **takes over the built-in `web_search` automatically**: the
bundle patch overrides the `web` seam row (`searchProvider: tinyfish`,
`fetchProvider: http` restated), because `dsh-base` pins the seam to
`deepseek-official` and would otherwise keep the tool on the DeepSeek backend.
It also **re-enables the host-level `tool-web` row** (`disabled: false` plus
`search: true`, `fetch: true` and the base timeouts restated): the
`dsh-web-app` bundle ships that row disabled (the Web app normally composes
web tools per agent preset), so without it the model would see no `web_search`
tool at all on a clean web profile install. **Scope note:** re-enabling the
host row makes the tools visible to *every* agent preset on the profile —
including presets that would not otherwise carry web tools (e.g. `minimal`);
a preset that mounts its own `tool-web` row still shadows this global
registration for its agents. To scope the tools to one preset instead,
override or remove the `tool-web` row in your profile's `cordis.patch.yml`
and add `tool-web` to that preset's agent composition. Later layers (profile
/ home `cordis.patch.yml` / `--patch`) can still override both rows.

Configuration is declared as a **volatile schema** (DeepSeek Harness 0.1.7+): the
Host reads the `Config` schema this plugin exports and renders it as the form for
the `dsh-tinyfish-search` row on the Plugins page. There is no plugin-side
settings registration and no plugin-supplied browser half. A saved edit reaches
the next search without a restart.

## Requirements

- DeepSeek Harness `dsh` CLI (any profile with the web seam, e.g. `web`) — verified on `0.1.7-rc.1` (latest release); the plugin declares `^0.1.7-alpha.2` peers, the release line that introduced volatile config
- Node.js `^22.19.0 || >=24.0.0` (matches the harness engine range)
- A [TinyFish API key](https://agent.tinyfish.ai/api-keys) (free to create; Search is free)
- The harness credential seam and launch environment (`@deepseek-ai/dsh-credentials`, `@deepseek-ai/dsh-launch-environment`) are required peers — every `dsh` profile carries them already

### Harness compatibility gate

DeepSeek Harness 0.1.7-rc.1 verifies a plugin's `@deepseek-ai/dsh*`
`peerDependencies` against the running runtime **before** it admits the row, and
refuses an incompatible plugin instead of loading it. This release declares
peers it actually satisfies, so no exemption is needed. If you run a `dsh`
outside the declared range, DSH refuses the row with a diagnostic naming the
exact pair; to accept that risk explicitly, grant the exemption it prints:

```sh
dsh plugin allow-version dsh-tinyfish-search@0.11.1 <your-dsh-version>
```

## Documentation

- [Install Guide](INSTALL.md) ([Chinese](INSTALL.zh.md))
- [Usage Guide](USAGE.md) ([Chinese](USAGE.zh.md))
- [Configuration Guide](CONFIG.md) ([Chinese](CONFIG.zh.md))
- [Update Guide](UPDATE.md) ([Chinese](UPDATE.zh.md))
- [Uninstall Guide](UNINSTALL.md) ([Chinese](UNINSTALL.zh.md))
- [Changelog](CHANGELOG.md) ([Chinese](CHANGELOG.zh.md))

## Install

```sh
dsh plugin --profile web add dsh-tinyfish-search
```

or from the repository / a tarball:

```sh
dsh plugin --profile web add ./dsh-tinyfish-search        # source checkout
dsh plugin --profile web add ./dsh-tinyfish-search-0.11.1.tgz
dsh plugin --profile web add github:maxwell-feng/dsh-tinyfish-search
```

> Git installs fetch sources, not built artifacts: pnpm runs the package's `prepare` script, which builds `lib/` from source. pnpm ≥ 10 requires you to allow the build once (it prints the exact `pnpm-workspace.yaml` snippet).

See the [Install Guide](INSTALL.md) for requirements, all install methods, and verification.

## Configure

Set your API key (recommended — no secret in config files):

**Linux / macOS:**

```sh
export TINYFISH_API_KEY="your_api_key_here"                      # current shell
echo 'export TINYFISH_API_KEY="your_api_key_here"' >> ~/.bashrc  # permanent (bash)
echo 'export TINYFISH_API_KEY="your_api_key_here"' >> ~/.zshrc   # permanent (zsh)
source ~/.bashrc                                                 # or reopen the terminal
```

**Windows (PowerShell):**

```powershell
setx TINYFISH_API_KEY "your_api_key_here"    # permanent — takes effect in new terminals
$env:TINYFISH_API_KEY = "your_api_key_here"  # current session only
```

Or set fields in your profile's `cordis.yml` / patch layer:

```yaml
- insert:
    - id: dsh-tinyfish-search
      name: dsh-tinyfish-search
      config:
        # apiKey: "literal-key"          # alternative to the env var; avoid committing it
        # apiKeyEnv: TINYFISH_API_KEY     # default
        # baseURL: https://api.search.tinyfish.ai   # default
        # location: US                    # optional geo targeting forwarded to TinyFish
        # language: en                    # optional search language forwarded to TinyFish
```

| Field | Default | Meaning |
|---|---|---|
| `apiKey` | — | Literal TinyFish API key (secret role; wins over the env var) |
| `apiKeyEnv` | `TINYFISH_API_KEY` | Environment variable carrying the API key |
| `baseURL` | `https://api.search.tinyfish.ai` | TinyFish Search API endpoint base |
| `location` | — | Optional geo location forwarded as TinyFish's `location` (e.g. `US`); blank/unset sends nothing |
| `language` | — | Optional search language forwarded as TinyFish's `language` (e.g. `en`); blank/unset sends nothing |

See the [Configuration Guide](CONFIG.md) for the full schema, credential resolution order, and runtime settings UI.

## Verify

```sh
dsh --profile web --dump-config | grep tinyfish   # layer present
```

Inside a session, call `web_search` and check that results carry TinyFish URLs/snippets. The web search settings card in the GUI shows the provider state.

## Usage

After installation, no code changes required. In any session with the `web` profile:

1. The model calls `web_search` as usual (e.g. “search for TinyFish docs”).
2. The harness routes it through `ctx.web → tinyfish → https://api.search.tinyfish.ai`.
3. Results appear as `WebSearchSource[]` (`url` / `title` / `snippet` / `publishedAt`) in the tool result.
4. Check GUI: **Settings → Web Search** shows provider `tinyfish` and `available: true` when the API key is configured.

Abort and error semantics follow the `dsh-web` seam: `WEB_PROVIDER_CREDENTIAL_MISSING` when no key, `WEB_ABORTED` on cancellation, `WEB_PROVIDER_ERROR` otherwise.

See the [Usage Guide](USAGE.md) for providers, credential configuration, worked examples, and the error table.

## Uninstall

```sh
dsh plugin --profile web remove dsh-tinyfish-search
```

Removes the bundle layer and the `tinyfish` provider registration, and restores
the composed `web` / `tool-web` rows to exactly what the underlying bundles
ship (an inserted row's override returns to the row's own defaults when the
inserting layer is removed). Restart `dsh --profile web` to confirm
`web_search` falls back to the base `deepseek-official` provider (or none if
no other provider is installed).

## Updating

```sh
dsh plugin --profile web add dsh-tin