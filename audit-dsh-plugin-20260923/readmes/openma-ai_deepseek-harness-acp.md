<p align="center">
  <img src="assets/acp-x-deepseek.svg" width="520" alt="Agent Client Protocol × DeepSeek Harness" />
</p>

<h1 align="center">deepseek-harness-acp</h1>

<p align="center">
  Use <a href="https://github.com/deepseek-ai/deepseek-harness">DeepSeek Harness</a> from
  <a href="https://agentclientprotocol.com/">Agent Client Protocol</a> clients such as
  <a href="https://zed.dev">Zed</a> and
  <a href="https://github.com/openma-ai/backchat">Backchat</a>.
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@openma/deepseek-harness-acp"><img src="https://img.shields.io/npm/v/%40openma%2Fdeepseek-harness-acp?logo=npm&color=cb3837" alt="npm version" /></a>
  <a href="https://www.npmjs.com/package/@openma/deepseek-harness-acp"><img src="https://img.shields.io/npm/dm/%40openma%2Fdeepseek-harness-acp" alt="npm downloads" /></a>
  <a href="https://github.com/openma-ai/deepseek-harness-acp/actions/workflows/ci.yml"><img src="https://github.com/openma-ai/deepseek-harness-acp/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://agentclientprotocol.com/"><img src="https://img.shields.io/badge/ACP-protocol%20v1-6f42c1" alt="ACP protocol v1" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue" alt="Apache-2.0" /></a>
  <img src="https://img.shields.io/node/v/%40openma%2Fdeepseek-harness-acp" alt="node >= 22.15" />
</p>

---

The adapter composes the harness **in-process** and maps its session-event log
onto the full ACP vocabulary: streamed text and reasoning, tool calls with
diffs and display terminals, plans, permission requests, session modes,
config options, slash commands, skills, and MCP servers. Credentials never
touch your editor config — it reuses the key you saved in the dsh Web UI, or
`dsh-acp login` saves one to the same store.

## One package, standalone or plugin

| | **A · dsh profile plugin (recommended)** | **B · Standalone server** |
|---|---|---|
| Best for | Normal installation and upgrades | Connecting an ACP client without managing a dsh profile |
| Install | `dsh plugin --profile acp add @openma/deepseek-harness-acp@latest` | `npm i -g @openma/deepseek-harness-acp` |
| Zed runs | `dsh --profile acp` | `dsh-acp` |
| Harness | The dsh that owns the profile | Your installed dsh, then the package's locked private runtime |
| Composition | dsh-base + this bundle + your profile's own patches | dsh-base + this bundle (profile machinery booted in-process) |

Both shapes share `$DSH_HOME`: the same credential store, settings, presets,
and session logs as `dsh web` — conversations started in the Web UI can be
listed and loaded from the editor.

Other dsh surfaces can mount the transport-independent
`@openma/deepseek-harness-acp/plugin` on their Base Host tree and own the
transport adapter. The TUI profile uses this path: it starts a separate TUI
Client process and connects ACP over that process's standard stdin/stdout; it
does not start `dsh-acp` or use an in-process Client stream.

The package is therefore not only a CLI wrapper. It is also the ACP surface
plugin used by other dsh applications: one Host composition can expose the
same sessions, tools, presets, skills, and persistence through a transport
chosen by the surface.

### DSH compatibility

The bundled runtime is **DSH `0.1.5-rc.1`**, including the upstream
cross-process session write lock. Your installed DSH still takes precedence;
use an updated host or the bundled runtime to get the fix.

A competing load/resume returns a standard JSON-RPC error. Closing the
session or exiting the owner process allows another process to resume it.
Every process writing shared sessions must use a fixed backend; older hosts
do not participate in this lock.

Restoring historical sessions uses the host's V3 migration, which preserves
the original log. Upgraded sessions cannot be read by older hosts.
Multi-root workspaces remain unsupported.

### A · dsh profile plugin (recommended)

```bash
npm install -g @deepseek-ai/dsh
dsh web                                                    # save your API key once
dsh plugin --profile acp add @openma/deepseek-harness-acp@latest
```

```jsonc
// Zed settings.json
{
  "agent_servers": {
    "DeepSeek Harness": { "command": "dsh", "args": ["--profile", "acp"] }
  }
}
```

The plugin command creates `$DSH_HOME/profiles/acp`, installs or upgrades the
adapter, and registers its `dsh.bundle` patch. The bridge mounts over
`@deepseek-ai/dsh-base` — the same product baseline as `dsh web`, with the
module-reload watcher off. Extend the profile in
`$DSH_HOME/profiles/acp/cordis.patch.yml` like any other dsh profile. A global
`dsh-acp` installation is not required for this path.

### B · Standalone server

```bash
npm install -g @openma/deepseek-harness-acp
dsh-acp login        # interactive; or save the key in the dsh Web UI
```

```jsonc
// Zed settings.json
{
  "agent_servers": {
    "DeepSeek Harness": { "command": "dsh-acp" }
  }
}
```

The standalone binary finds DeepSeek Harness via `--dsh-path` / `DSH_PATH`,
`./node_modules`, `dsh` on PATH, or `npm root -g`, then falls back to the exact
runtime archived inside this package. DSH is only a wildcard optional peer for
Host integration, never an npm-installed dependency: plugin mode uses the
Host's tree, while standalone maps the same imports to the private runtime.
When a real `$DSH_HOME/profiles/acp` exists, that profile owns the composition.

## Plugin and extension model

There are two independent ways to extend an ACP-backed surface.

To use portable Agent Plugins, Codex plugins, Claude Code plugins, or Pi
packages through an ACP client, add the
[Agent Plugins Bridge](https://github.com/openma-ai/dsh-agents-plugins-bridge) to the
same profile:

```sh
dsh plugin --profile acp add @openma/dsh-agents-plugins-bridge@latest
```

The Bridge contributes ordinary Host rows. Imported commands, skills, tools,
hooks, MCP connections, agents, and Pi extensions therefore reach ACP through
this adapter's existing projections; there is no ACP-specific plugin import
runtime. The Bridge's Web management panel and MCP Apps HTML renderer remain
Web surfaces and are not sent over ACP.

For extensions that need a session-owned background lifecycle without an open
terminal UI, use
[Martty owner](https://github.com/openma-ai/deepseek-harness-tui/blob/main/README.en.md#martty-owner-long-lived-headless-acp--pi-rpc).
It is a generic ACP `rpc` client: this package remains the server/transport,
while Martty owns the long-lived Session and explicit startup/shutdown slash
commands.

### Extend the Host composition

The ACP adapter rides the Cordis tree that the profile already owns. Add dsh
plugins to that profile to change the agent composition instead of forking the
ACP server: providers and models join the live catalog, commands and skills
join the advertised session surface, tools and subagents appear through
standard `session/update`, and the same session persistence remains available
to every surface.

For applications embedding ACP, the public package entries are:

| Export | Role |
|---|---|
| `@openma/deepseek-harness-acp/plugin` | Complete Host-side surface plugin. It fills the ACP-required Host services that Base leaves to a surface and provides `ctx.acpServer`. It does not claim a transport. |
| `@openma/deepseek-harness-acp/server` | Lower-level transport-independent `acpServer` provider for a Host tree that already supplies the injected composition services. |
| `@openma/deepseek-harness-acp/stdio` | Standard profile adapter: connects `ctx.acpServer` to process stdin/stdout. |
| `@openma/deepseek-harness-acp/bridge` | Node stream adapter and compatibility entry for older profile patches. |

`ctx.acpServer.connect(stream)` creates a connection-owned bridge fiber over
the existing Host composition. The transport owner retains process, stream,
and TTY lifecycle; the ACP plugin retains session and agent semantics. This is
the shape used by
[`@openma/deepseek-