# dsh-codex-pin

**Codex-style session pinning for the DeepSeek Harness Web sidebar — a pin is a flag, not a position.**

Pinning a session lifts it into a single **Pinned** section above the whole
workspace list. Toggling a pin never calls `workspace.insertSessionBefore`,
never writes the workspace view store's order, and never switches the sidebar's
sort mode: the durable session order in `~/.dsh/storages/workspace.json` is not
touched. That promise is guarded by a static check in this repo (`npm test`),
not just by documentation.

![The Pinned section above the workspace groups](assets/pinned-sidebar.png)

> Independent community plugin. Not an official DeepSeek product, and not
> affiliated with OpenAI — “Codex-style” describes the interaction model it
> copies, not any official connection.

## What you get

- **A pinned flag.** Hover a session row and click the pin (📌). The session
  moves into **已置顶 / Pinned** at the top of the sidebar, newest pin first.
- **The pinned row leaves its group**, so nothing is duplicated: click the row in
  the section to open the session, click the pin control there to unpin, and the
  row is back where the list order says it belongs.
- **Host-durable state.** The ordered list lives in the host settings namespace
  `codex-pin` (`~/.dsh/settings.yaml`), so it survives restarts and is shared by
  every browser whose settings transport reaches the host.
- **Honest degradation.** A browser that cannot reach the namespace keeps its own
  `localStorage` list and the section header says `仅本浏览器` /
  `This browser only`. That fallback is a fail-safe, not a one-way lock: a failed
  host write is retried once, and even after the page has fallen back every later
  pin keeps probing the host, so the note clears itself at the first write that
  lands.
- **No model-visible effects.** No session events, no tokens, no telemetry and
  no external network calls — the browser half reaches only same-origin host
  surfaces: the settings namespace, the row menu's `workspaces.openSession` /
  `forkSession` / `archiveSession`, and the session's own `rename`.

## How it differs from the other pinning plugins

| | **dsh-codex-pin** | [dsh-pin](https://github.com/Yu-tao-Li/dsh-pin) | [dsh-session-pin](https://github.com/PerryLink/dsh-session-pin) |
|---|---|---|---|
| Pin levels | one: a Pinned section above all workspaces | two: in-workspace + global tray | two: workspace + session |
| Durable session order | **never written** — no ordering API is called at all | in-workspace pins go through `workspace.insertSessionBefore` and switch the sort mode to manual; the global tray is display-level | pinned sessions move to the front of their account |
| Pin state | host settings namespace `codex-pin.pinned`, `localStorage` fallback | host order anchors + local records | host settings, per-browser durable |
| Extras | deliberately none | anchor-exact restore, sort-mode restore | 8 colours, boards, tags, saved views, `/goto` |
| Footprint | one bundle entry; no HTTP routes | client-only | host + browser |

Pick this one if you want pinning to be a purely visual, always-reversible
annotation. Pick the others if you want pins to also drive ordering, colours or
boards.

## Requirements

- DeepSeek Harness with the **web** profile (the plugin is `platform: web`).
- Verified against `dsh web` **0.1.5-rc.1**, and re-verified against
  **0.1.6-alpha.2** (that host rewrote the sidebar, so the browser half now
  probes host capability shapes instead of one build's API); the declared peer
  range is `>=0.1.2-rc.1 <0.2.0` and other builds in it are untested (see
  Compatibility).
- Node `>=22.19.0` (only for building from source).
- `dsh plugin add` prints a peer-dependency warning on every known DSH build —
  the ecosystem's peer declarations are optional overlays, so the warning is
  expected and harmless.

## Install

```bash
# straight from GitHub — the path that works today
dsh plugin --profile web add github:jackovibe/dsh-codex-pin

# pin a release instead of tracking main (any tag works)
dsh plugin --profile web add github:jackovibe/dsh-codex-pin#v0.2.7

# from the tarball attached to a release (Releases → Assets)
dsh plugin --profile web add ./dsh-codex-pin-0.2.7.tgz

# from a checkout
npm run build && npm pack && dsh plugin --profile web add ./dsh-codex-pin-0.2.7.tgz

# from npm (once published)
dsh plugin --profile web add dsh-codex-pin
```

The `github:` spec is what this plugin's own development profile uses, so it is
exercised on every local run; the npm name is reserved for a later publish and
does not resolve yet.

Then restart `dsh web` (the loader composes bundle layers at boot) and hard-refresh
the browser (`Ctrl+Shift+R`). Open the sidebar: session rows now carry the pin
control on hover.

### How it mounts

The package ships a bundle patch (`cordis.patch.yml`) that inserts exactly one
loader entry:

```yaml
- insert:
    - id: codex-pin
      name: dsh-codex-pin
```

`dsh plugin add` reconciles `dsh.profile.bundles` by itself, so **do not** also add
this insert to your profile's own `cordis.patch.yml`: two layers inserting the
same loader id fail the boot. Check the composition before restarting:

```bash
dsh --profile web --dump-config | grep -c 'id: codex-pin'   # must print 1
```

### Upgrade / uninstall

```bash
# upgrade: re-run the same spec (adds the newest commit on main, then restart)
dsh plugin --profile web add github:jackovibe/dsh-codex-pin
# or move to a specific release
dsh plugin --profile web add github:jackovibe/dsh-codex-pin#v0.2.7

dsh plugin --profile web remove dsh-codex-pin       # uninstall, then restart
```

Session ids stay in `settings.yaml` under `codex-pin` after uninstalling; delete
that block to clean up.

## Usage

| Action | How |
|---|---|
| Pin / unpin a session | hover the row, click the pin control (📌 toggles) |
| Open a pinned session | click its row in the **已置顶 / Pinned** section |
| Unpin from the section | click the filled pin on the section row |
| Rename / fork / archive / delete / copy title or id | right-click any session row for the row menu |
| Pin / rename / archive the **current** session | `Ctrl+Alt+P` / `Alt+Ctrl+R` / `Ctrl+Shift+A` |

Pinned and unpinned rows carry the **same pair** of controls — the pin (outlined
when unpinned, filled when pinned) and archive — and the rows inside the Pinned
section carry them too, so archiving stays available while a session is pinned.
The menu's red **Delete session** entry calls the archive manager's
`workspaceRegistry.deleteSession` behind a confirmation dialog; without that
plugin the entry reports why instead of failing silently.

Menu copy and tooltips follow the **GUI language**: the plugin registers zh/en
dictionaries through `ctx.inject(['locale'])`, so a Chinese GUI shows
重命名 / 置顶聊天 / 归档会话 / 删除会话 and an English GUI shows
`Rename / Pin chat / Archive session / Delete session` — switching the language
re-labels a running page with no reload.

`Ctrl+Shift+A` asks for confirmation before archiving the current session (a
single global keystroke should not archive silently); the row menu's archive
entry is a deliberate click and archives directly. Right-clicking a session row opens
**this plugin's** menu — a Codex-style overlay. It only intercepts rows it can act
on; a row without a session identity keeps whatever context menu it had. The app's
own surfaces (multi-select, search, the settings pages) are untouched.

## Configuration

| Key | Default | Meaning |
|---|---|---|
| `maxPins` | `0` | Cap on pinned sessions; `0` = unlimited. Set it on the loader entry: |

```yaml
# profile cordis.patch.yml
- id: codex-pin
  config:
    maxPins: 5
```

When the cap is reached, the oldest pin is dropped as a new one is added, and a
lowered cap prunes the view on the next read. Changing the cap re-composes the
host plugin: an already-open page picks the new value up when the host pushes
it (observed to take tens of seconds, and writes in that window can race 