# pi2dsh

**English** | [中文](README.zh.md)

**Move a Pi setup to DeepSeek Harness without rebuilding it.** The
extensions, MCP manager, subagents, memory and background tasks you use on Pi
install on DSH as the same npm packages and run unmodified — web, terminal
and headless.

```sh
dsh plugin add pi2dsh            # once
dsh plugin add pi-mcp-adapter    # then the Pi packages you already use, straight from npm
```

MCP is the deepest-verified path: the full protocol surface — OAuth,
resources, prompts, MCP Apps, elicitation, sampling, cancellation — runs
through DSH's own approval and rendering
([evidence matrix](docs/mcp-compatibility.md)). What has been verified end to
end is listed in [What actually works today](#what-actually-works-today);
nothing outside that table is claimed.

pi2dsh `0.25.2` targets Pi `0.84.1` and uses one engine for DSH `0.1.1-rc.2`
and `0.1.5-rc.1` / `0.1.5-rc.2`. Exact tested workflows and exclusions are in
the [version acceptance record](community/dsh-015-compat/README.md) and
[rc.2 checks](community/dsh-015-rc2-20260914/README.md). Cross-version saved-data
migration is outside this release.

## Why this exists

[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) is built
on ideas worth betting on — a durable, reconstructable session log, a clean
service composition, an agent loop you can actually reason about. Its plugin
ecosystem is young. [Pi](https://pi.dev/) has a mature one: hundreds of
published packages, many with real users.

pi2dsh is one compatibility layer that implements Pi's public extension ABI on
top of DSH's native services, so a Pi package runs on DSH **as published** —
no fork, no patch, no per-package adapter. For a Pi user or team that means
switching hosts without rebuilding the toolchain; for a Pi plugin author it
means a second host with no port to maintain. To the user everything looks
like DSH; to the plugin everything looks like Pi.

At the same time, pi2dsh is an ongoing, full-surface, real-world test of DSH's
architecture. Instead of patching individual plugins, it asks whether the
models, tools, sessions, interaction, resources and client capabilities that Pi
plugins rely on can preserve their logic and lifecycle using only DSH's public
services and extension seams. If they can, that is strong evidence that DSH's
architectural goals for building agents and an agent-plugin ecosystem have been
achieved, at least along this dimension. Wherever the bridge must bypass,
degrade or cannot express a capability, it pinpoints an architectural gap that
remains.

## Install

One engine, then whatever plugins you want:

```sh
dsh plugin --profile web add pi2dsh
dsh plugin --profile web add pi-mcp-adapter
```

Then **restart `dsh`** — plugins mount at startup.

> **A profile needs a surface bundle.** DSH's built-in templates are `web` and
> `headless`. A custom profile is valid when its product installs a surface —
> for example `@deepseek-harness-tui/dsh-tui` in the `dsh-tui` profile. A bare
> arbitrary profile has no surface and can start with nothing to drive it, so
> add the intended surface to `dsh.profile.bundles` first.

That is the whole model. There is no conversion step, no generated bundle, no
build. The engine discovers the Pi packages in your profile (every one is
something you explicitly added) and mounts them through a single bridge
instance: one model directory, one login, one credential store, one upgrade
unit.

Day-to-day:

| Task | Command |
|---|---|
| Add a plugin | `dsh plugin add <pkg>` (then restart dsh) |
| Remove a plugin | `dsh plugin remove <pkg>` — remove plugins before removing the engine |
| Upgrade a plugin | `dsh plugin add <pkg>@latest` — the engine is untouched |
| Upgrade the engine | `dsh plugin add pi2dsh@latest` — your plugins are untouched |
| Check a plugin before upgrading | `npx pi2dsh inspect <pkg>@<version>` |

Two installer messages worth knowing:

- **`ERR_PNPM_IGNORED_BUILDS`** — pnpm blocks dependency build scripts by
  default. Run `pnpm approve-builds` inside
  `$DSH_HOME/profiles/web`, or set the listed packages to `true`
  under `allowBuilds` in that profile's `pnpm-workspace.yaml`. Then re-run the
  add. (This is your call to make, so the bridge does not work around it.)
- **An add silently installs an older version** right after a release —
  pnpm's `minimumReleaseAge` skips versions published very recently. Pin it:
  `dsh plugin add pi2dsh@<version>`.

Requires Node.js 22.19+ and DeepSeek Harness.

### Engine configuration

The engine reads one `config` block from its plugin row. Today it takes a
single opt-in:

```yaml
# $DSH_HOME/profiles/<profile>/cordis.patch.yml
- id: pi2dsh
  config:
    serveNativeSubagents: true
```

`serveNativeSubagents` (default: **off**) serves DSH-native subagents with
the profile's Pi packages. With it on, a child agent DSH spawns through its
own subagent delegation (one whose session carries the subagent origin)
receives every discovered Pi package mounted on its own agent scope — the
package's tools, commands and prompt sections appear for that child only,
and every contribution unwinds when the child ends. With it off, such
children run as plain DSH agents, exactly as before.

The mount is guaranteed for the child's **first** turn: prompt assembly and
tool execution wait for it, so even a child that runs a single turn sees the
full tool set. Each child is served exactly once, whichever path DSH created
it through — children the agent registry reports as runtime roots are served
by the engine's root mount path, and the subagent path serves the rest; the
two never overlap. Pi subagent-bridge children are unaffected either way:
they already receive the creator package's own per-spawn loader mount, and
the bridge recognizes them by the `pi2dsh-sub-` session-id prefix (stable
across a persisted resume), so no child is ever mounted twice.

## Walkthrough: advanced MCP in your terminal

The clearest example of what the bridge buys you. dsh-TUI ships a native
`/mcp` command for DSH's official MCP client — it works, and it stays
untouched. The Pi ecosystem has a much richer MCP power tool: a full-screen
server manager, lazy tool discovery, one proxy tool instead of flooding the
model context with dozens of tools, JavaScript orchestration of multiple MCP
calls, OAuth logins, resources and prompts. With the bridge, that package runs
unmodified.

### 1. Install

```sh
dsh plugin --profile dsh-tui add @deepseek-harness-tui/dsh-tui   # skip if the profile exists
dsh plugin --profile dsh-tui add pi2dsh
dsh plugin --profile dsh-tui add pi-mcp-adapter
```

Or use the same unmodified Pi packages in dsh-pi-tui:

```sh
dsh plugin --profile pi-tui add @xmoon76/dsh-pi-tui
dsh plugin --profile pi-tui add pi2dsh pi-mcp-adapter @tintinweb/pi-subagents
dsh --profile pi-tui
```

That composition keeps dsh-pi-tui's native `/login` and projects Pi OAuth
flows into it, mounts the original MCP manager through the public
`piTuiExtensions` surface, and exposes the original Pi subagent flow at
`/agents`. See [`examples/pi-tui-ecosystem`](examples/pi-tui-ecosystem/).

Then restart `dsh` — plugins mount at startup.

### 2. Configure your MCP servers

Inside dsh-TUI, run:

```text
/pi-mcp setup
```

The setup flow can adopt MCP server definitions from host configs you already
have into the adapter's own standard `mcp.json`. No bridge-specific
configuration exists — everything you touch is the package's own surface.

### 3. Use it

```text
/pi-mcp
```

opens the full-screen interactive server manager — its footer documents the
keys for enable/disable, reconnect and OAuth login. The model receives the
adapter's `mcp` and `mcpScript` tools through DSH's normal tool registry, and
each agent (`/new` included) gets its own fully connected instance.

dsh-TUI's native command remains separate, and both stay available:

```text
/mcp       # native DSH MCP-client status
/pi-mcp    # the installed Pi adapter's manager
```

What is verified behin