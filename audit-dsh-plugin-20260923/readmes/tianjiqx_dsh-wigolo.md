# dsh-wigolo

[中文文档](./README.zh.md)

**Self-hosted web search for [DSH](https://github.com/deepseek-ai/dsh) (DeepSeek Harness).** This plugin integrates a privately deployed [wigolo](https://github.com/KnockOutEZ/wigolo) meta-search daemon into DSH, replacing the built-in web search with your own self-hosted search infrastructure — full control over search engines, caching, and data privacy.

> **Core purpose:** Proxy and replace DSH's built-in `web_search` / `web_fetch` with a self-hosted wigolo daemon. One toggle switches all agent web searches to your private deployment — no cloud dependencies, no API keys, zero cost per query.

```
dsh web GUI ── sidebar panel ── /api/dsh-wigolo/* ──┐
                                                     │
agent tools (wigolo_search, …) ── MCP streamable-http ──► wigolo daemon
web seam (web_search / web_fetch) ───────────────────┘   18+ engines · RRF · local cache
```

## Features

- **Agent-first design** — seven tools (`wigolo_search`, `wigolo_crawl`, `wigolo_extract`, `wigolo_research`, `wigolo_find_similar`, `wigolo_cache`, `wigolo_watch`) expose trimmed, model-friendly parameter surfaces. Write operations stay agent-only; read-only cache/watch browsing also lives in an opt-in **"Wigolo Cache"** conversation tab (off by default).
- **Provider takeover, configurable** — route the official `web_search` / `web_fetch` through wigolo with one switch (on = wigolo drives both, off = official providers), toggled from the GUI with automatic cordis routing management.
- **Official settings integration** — `enabled`, `announceToAgent`, and `guidance` override live in the official DSH settings UI (dsh-ssh pattern). Hot-reload: change settings, no restart needed.
- **Sidebar panel** (React, i18n) — four tabs: Connection (live test + latency), Takeover & Tools, About, and Help (bundled usage guide rendered in-panel). Connection settings with live test + latency, takeover switch, tool exposure flags, and the cache-tab toggle, all loopback-fenced. Token can be written directly from the panel (no terminal required).
- **Hot-reconfigure** — connection and token edits take effect immediately (MCP client hot-reconfigured); only the takeover switch and tool exposure changes need a restart.
- **Fail-loud config validation** — unknown config keys trigger warnings with "did you mean?" hints instead of being silently dropped.
- **Secret-safe by construction** — the token lives in its own 0600 file, never in the config JSON, never returned to the browser.
- **Timezone-aware cache timestamps** — wigolo daemon stores timestamps in zone-less UTC; the plugin converts them to your configured timezone (`local`, numeric offset like `+8`, or IANA name like `Asia/Shanghai`) so `wigolo_cache` results display in your local time.

## Prerequisites

A running [wigolo daemon](https://knockoutez.github.io/wigolo/docs/) (v0.2+), reachable over HTTP with a bearer token. Local (`127.0.0.1:3333`) is the default and needs zero extra setup.

## Install

### From npm

```bash
dsh plugin --profile web add @tianjiqx/dsh-wigolo
```

### From GitHub

```bash
dsh plugin --profile web add github:tianjiqx/dsh-wigolo
```

Both methods install the plugin and automatically register it in the profile's bundle list (via the plugin's bundled `cordis.patch.yml`). No manual editing required.

### Local development (link mode)

```bash
git clone https://github.com/tianjiqx/dsh-wigolo.git
cd dsh-wigolo
pnpm install
pnpm build
dsh plugin --profile web add link:$PWD
```

This clones the repo, builds it, and registers the plugin in the profile's bundle list automatically via `link:` (no manual `cordis.patch.yml` editing needed).

### Post-install

Put your daemon token into `~/.dsh/wigolo-token` (first line, 0600):

```bash
echo "YOUR_TOKEN" > ~/.dsh/wigolo-token && chmod 600 ~/.dsh/wigolo-token
```

Restart dsh, open the **Wigolo** entry in the sidebar, and hit **Test connection**.

## Uninstall

```bash
dsh plugin --profile web remove @tianjiqx/dsh-wigolo
```

This removes the plugin and its bundle registration. The token file `~/.dsh/wigolo-token` and config `~/.dsh/wigolo.json` are preserved (delete manually if desired).

For detailed usage scenarios and examples, see the [Usage Guide (中文)](./GUIDE.zh.md).

## Configuration

### Via GUI (recommended)

All settings can be configured through the **Wigolo sidebar panel** (click the Wigolo icon in the sidebar):

- **Connection tab**: Host, port, token, hostHeader, test connection
- **Takeover & Tools tab**: Takeover switch, tool enable/disable, cache tab toggle
- **About tab**: Version info, documentation links

Changes take effect immediately (hot-reload), except for the takeover switch which requires a restart.

### Manual configuration file

For advanced settings not exposed in the UI (e.g., per-tool defaults, timeout overrides), edit `~/.dsh/wigolo.json` directly:

```jsonc
{
  "version": 2,
  "connection": {
    "host": "127.0.0.1",       // daemon address
    "port": 3333,
    "hostHeader": "auto",       // auto | none | "<literal>"
    "tokenFile": ""             // "" = ~/.dsh/wigolo-token
  },
  "takeover": false,            // true = wigolo drives web_search + web_fetch; false = official providers
  "tools": {
    "wigolo_search":  { "enabled": true,  "defaults": { "max_results": 10, "search_depth": "balanced" } },
    "wigolo_crawl":   { "enabled": true,  "defaults": { "max_pages": 50 }, "timeoutMs": 300000 },
    "wigolo_extract": { "enabled": true },
    "wigolo_research":{ "enabled": true,  "timeoutMs": 600000 },
    "wigolo_find_similar": { "enabled": false },
    "wigolo_cache":   { "enabled": true },
    "wigolo_watch":   { "enabled": true }
  },
  "cacheTab": { "enabled": false },   // "Wigolo Cache" read-only GUI tab (default off; hot-apply)
  "announceToAgent": true,
  "timezone": "local"               // cache timestamp timezone: "local" | "+8" | "-5" | "+5.5" | "Asia/Shanghai"
}
```

Per-tool `defaults` merge **under** the model's explicit arguments (the model always wins); `timeoutMs` overrides the built-in per-tool budget.

### Takeover switch

`takeover` is a simple boolean:

| Value | `web_search` | `web_fetch` | Notes |
|------|--------------|--------------|-------|
| `true` | wigolo | wigolo | full replacement |
| `false` | official | official | wigolo_* tools only (default) |

Why a switch at all: when several providers register into the web seam and none is explicitly routed, `web_search` fails with `WEB_PROVIDER_AMBIGUOUS`. Takeover on (`true`) therefore also writes a self-managed block into `~/.dsh/cordis.patch.yml` (`searchProvider: wigolo`, dsh-skin-style managed markers); takeover off (`false`) removes it and registers nothing, so it coexists safely with the official provider. Routing changes need a dsh **restart** — the panel tells you when.

### Timezone

The wigolo daemon persists cache timestamps as zone-less UTC (`"YYYY-MM-DD HH:MM:SS"`). The plugin converts them to the configured timezone before returning to the agent or rendering in the UI.

| Value | Example | Description |
|-------|---------|-------------|
| `"local"` | `"local"` | Use the DSH host's system timezone (default) |
| Numeric offset | `"+8"`, `"-5"`, `"+5.5"` | Fixed offset from UTC; supports half-hour zones |
| IANA name | `"Asia/Shanghai"`, `"America/New_York"` | Full timezone with DST rules |

Changes to `timezone` take effect after a dsh restart.

### The Host header, explained

wigolo guards against DNS-rebinding by allowlisting `Host` values: `localhost`, the loopback literals, and its own bind host. Two consequences:

- A daemon bound to `0.0.0.0` on a LAN machine accepts requests whose `Host` header is `0.0.0.0`.
- `fetch()` refuses to set `Host` (Fetch spec), so the plugin uses `node:http`, which allows it.

`hostHeader: "auto"` (default) sends **no** custom header for local daemons and the bind-host trick for remote ones. Set a literal only if your deployment needs it.

## Agent tools

| Tool | Wigolo capabil