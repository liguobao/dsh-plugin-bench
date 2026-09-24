**English** | [中文](README.zh-CN.md)

# godot-bridge

[![Awesome DSH Plugin](https://awesome-dsh-plugin.com/badge.svg)](https://awesome-dsh-plugin.com)
[![Listed on DSH Directory](https://dsh.directory/badges/listed.svg)](https://dsh.directory/plugins/smalldy/godot-bridge)

Native **DeepSeek Harness (DSH)** plugin that launches and drives a running **Godot 4.x** game through its in-game TCP interaction server — replacing the [`godot-mcp`](https://github.com/tugcantopaloglu/godot-mcp) MCP server with first-class agent tools.

No MCP protocol, no Python server, no editor addon. The game side is untouched: `McpInteractionServer` (the `mcp_interaction_server.gd` autoload) already listens on `127.0.0.1:9090` and speaks newline-delimited JSON — godot-bridge speaks the same protocol natively from inside the DSH host.

## Tools

| Tool | Replaces (godot-mcp) | Purpose |
| --- | --- | --- |
| `godot_run_project` | `run_project` | Launch the project in debug mode (`godot -d --path …`), wait for port 9090 |
| `godot_stop_project` | `stop_project` | Terminate the game process (tree-scoped kill) |
| `godot_get_debug_output` | `get_debug_output` | Incremental stdout/stderr of the launched process |
| `godot_command` | all `game_*` (~130) | Send any interaction-server command: `get_scene_tree`, `get_ui_elements`, `eval`, `get/set_property`, `call_method`, `click`, `key_press`, `screenshot`, `raycast`, `serialize_state`, `ui_*`, … |
| `godot_screenshot` | `game_screenshot` | Viewport capture as base64 PNG |
| `godot_ping` | — | Probe whether the game answers on 9090 (also reports installed/latest plugin version) |
| `godot_set_engine_path` | — | Persist the Godot engine executable path into settings (the model asks the user for it, then saves it here; hot-reloaded) |
| `godot_headless_op` | `read_scene`, `modify_scene_node`, `remove_scene_node`, `attach_script`, `create_resource`, `save_scene`, `create_scene`, `add_node`, `get_uid`, `manage_scene_signals`, … | Headless static operations (`godot --headless --script godot_operations.gd`): 16 ops, no running game needed |
| `godot_validate_script` | `validate_script` | Headless GDScript compile-check via `validate_script.gd` → `{valid, errors}` |
| `godot_set_project_setting` | `modify_project_settings`, `set_main_scene`, `manage_layers`, `manage_plugins`, `manage_translations` | Set a typed key in any project.godot section (`PackedStringArray(...)` / `Vector2i(...)` / bool / …) |
| `godot_manage_autoloads` | `manage_autoloads` | List / add / remove autoload singletons (`Name="*res://…"`) |
| `godot_manage_input_map` | `manage_input_map` | List / add / remove input actions — **correct Godot 4 keycodes** (fixes godot-mcp's Godot 3 baseline bug) |
| `godot_manage_export_presets` | `manage_export_presets` | List / add / remove export presets (`export_presets.cfg`) |
| `godot_create_script` | `create_script` | GDScript template (extends / class_name / method stubs / source) |
| `godot_create_project` | `create_project` / `create_csharp_script` | Project scaffold, optional Godot .NET `.csproj` |
| `godot_export_project` | `export_project` | Headless export (`--export-release` / `--export-debug <preset> <output>`) |

The remaining godot-mcp tools were implemented in the MCP server's own Node process: pure file/editor operations are covered by DSH's native file tools, while a handful carry **Godot-specific write logic** (`manage_input_map`, `manage_export_presets`, `modify_project_settings`, project/script templates) that a generic edit replaces only with format knowledge — see [COVERAGE.md](COVERAGE.md) for the full breakdown.

## How it works

```
DSH session
  └─ godot-bridge (Host plugin)
       ├─ godot_run_project ──────► subprocess.spawn(Godot -d --path <project>)
       ├─ godot_get_debug_output ─► collect-mode output (incremental offsets)
       └─ godot_command / godot_screenshot / godot_ping
            └─ subprocess.spawn(node -e <bridge> <command> <paramsJson>)
                 └─ TCP 127.0.0.1:9090 ◄── in-game McpInteractionServer autoload
```

- The in-game protocol (`{command, params, id}` + newline) is **identical** to godot-mcp, so the game side and any existing workflows keep working.
- Each command spawns a one-shot `node -e` bridge that connects, sends one line, prints the first response line, and exits. The game server is single-connection/single-command (`_busy`), so short-lived connections are a perfect fit.
- Spawning uses the harness's raw `subprocess` service (not the sandboxed shell executor), so Godot can write its `user://` files without the DSH file sandbox killing it (see Pitfalls).

## Requirements

- DeepSeek Harness (a session with a host runtime)
- A Godot 4.x project with the `McpInteractionServer` autoload registered. If your project does not have it yet, copy `plugin/mcp_interaction_server.gd` to the project root and register it as an autoload named `McpInteractionServer` (godot-mcp projects already have this). **`godot_run_project` also auto-installs it when missing** (copies the vendored file into `autoload/` and registers it in `project.godot`), so no manual setup is needed — and non-Godot projects are completely unaffected.
- `node` on PATH
- Godot executable — resolved in this order: the `godot_path` tool argument → the **`godotPath` setting** (the Web plugin-config page, or the `godot-bridge:` section of `settings.yaml`) → the `godot` command on PATH. Nothing to configure when `godot` is on PATH; otherwise set your engine path in **settings** (the plugin author does not preset it — Godot is a portable exe that can live anywhere). Use the **real exe full path**, never a version-manager shim (see Pitfalls).

## Install

**Recommended — one command** (requires the `dsh` CLI):

```sh
dsh plugin --profile web add github:Smalldy/godot-bridge
```

`dsh plugin` is a pnpm forwarder: it installs the package into the profile's `node_modules` and — because the package declares `dsh.bundle` (its `cordis.patch.yml` inserts the `tool-godot-bridge` row) — appends it to the profile's `dsh.profile.bundles` layer list. The `web` profile is the standard one the Web app already boots from, so this simply adds the tools to standard mode — **no new profile is created**. After a restart, the sixteen `godot_*` tools are available in every session on that profile. Listed in the [awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) community registry (topic: `dsh-plugin`).

The same command installs a local checkout or tarball (`dsh plugin --profile web add ./path/to/godot-bridge`).

> The plugin is a standard DSH bundle module: it imports `defineTool` from `@deepseek-ai/dsh-tools` and registers via `ctx.tools.register`. It must be installed through the bundle mechanism above — the harness heals the shared `@deepseek-ai/*` dependency layer inside the profile's `node_modules`, which is what makes the import resolve. Do not copy the file into a user agent preset (`~/.dsh/.agent-presets/...`); Node cannot resolve `@deepseek-ai/dsh-tools` from that location.

### Uninstall

```sh
dsh plugin --profile web remove godot-bridge
```

Removes the package and its `godot-bridge` bundle layer from the profile — after a restart the sixteen `godot_*` tools are gone from sessions on that profile. The standard `web` profile itself is untouched (this never creates or removes a profile). Stop any running game first with `godot_stop_project`; the plugin's unload cleanup also terminates a Godot child it started. Reinstall any time with the `add` command above.

## Update notices

On load the plugin does a **best-effort** version check: it fetches the repo's `main`-branch `package.json` (`raw.githubusercontent.com`, 5s timeout, silent on failure/offline) and compares it with the installed version. When a newer version exists it registers a system-prompt section, so the model surfaces **"godot-bridge update available: installed X, latest Y"** in every session until the plugin is updated (`dsh plugin --pro