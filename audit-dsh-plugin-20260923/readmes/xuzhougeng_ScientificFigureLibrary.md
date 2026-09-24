<p align="center">
  <img src=".github/assets/sfl-banner.svg" alt="Scientific Figure Library — local-first MCP App for your scientific figures on Claude Science and Wisp Science." width="100%" />
</p>

# Scientific Figure Library

[Website](https://xuzhougeng.github.io/ScientificFigureLibrary/) ·
[简体中文](README.zh-CN.md) ·
[Quickstart](docs/QUICKSTART.md) ·
[User Guide (online)](https://github.com/xuzhougeng/ScientificFigureLibrary/blob/main/docs/USER_GUIDE.md) ·
[Protocol](docs/PROTOCOL.md) ·
[Releases](https://github.com/xuzhougeng/ScientificFigureLibrary/releases) ·
[Wisp Science](https://github.com/xuzhougeng/wisp-science)

Scientific Figure Library (SFL) is a **local-first MCP server and MCP App** for
**your scientific figures**. You import a figure and its code, review them,
publish an immutable Release to **one global Library on your machine**, then
reuse that exact template across projects in **Claude Science**, **Wisp Science**,
**Codex**, **Cursor**, **Pi**, **dsh**, and other stdio MCP hosts.

The Library stays on disk you choose. Nothing is copied into every project
until you confirm a materialization. The server does **not** execute plotting
code and does not contain a second model: the host agent inspects files; SFL
hashes, versions, gates, and publishes them.

The default retrieval order is **Local Published → FigureYa → Open Figure
Modules → enabled dynamic personal Providers**. The bundled Community snapshot
is retained for explicit compatibility, but is frozen and excluded from default
search (`includeInDefaultSearch: false`). The source of truth for your own
figures is always **Local Published**.

A bundled extra catalog may currently contain zero releases after an authorized
redaction; that is a healthy empty source, not a failure, and default search
continues across other providers.

<p align="center">
  <img src="docs/assets/sfl-gallery.png" alt="Scientific Figure Library MCP App: browse locally published scientific figure templates, then confirm one exact Release before materializing it." width="100%" />
</p>

<p align="center"><em>Search your local published library in the MCP App, confirm one exact template, then materialize it into a project.</em></p>

## Local client preview

Separate native macOS Apple Silicon and Intel DMGs, plus Windows and Linux ZIPs with bundled Node, are available through the local-client release workflow. Both bundled-Node and `no-node` editions (requiring installed Node.js 22+) omit gallery images and download previews on demand. See [installation and preview limitations](docs/INSTALL_LOCAL.md). The macOS preview is ad-hoc signed and is not notarized.

## Install with a coding agent

Node.js 22+ is required. Do not execute user plotting code. After install, bind
one global Library directory on disk; if `setup_required`, also bind a Local
workspace before searching.

### Pi

Install the published npm package. Do not `pi install` a GitHub URL or git
clone: the repository does not contain `dist/`, so MCP cannot start.

```bash
pi install npm:pi-mcp-adapter
pi install npm:scientific-figure-library
```

Restart Pi. The package loads the `figure-library` Skill and registers the
stdio MCP server through pi-mcp-adapter. If you already copied a local SFL app
MCP config into `~/.config/mcp/mcp.json` or `.mcp.json`, skip
`pi install npm:scientific-figure-library` — that duplicates tools.

Paste this request:

```text
Install Scientific Figure Library for Pi.
Run: pi install npm:pi-mcp-adapter
Then: pi install npm:scientific-figure-library
Restart Pi. Do not clone the GitHub repo and do not add a second
figure-library MCP entry. First test: figure_library_get_skill, then
figure_library_source_status. If setup_required, bind the global Library
and Local workspace. Tell me when I need to restart Pi.
```

### DeepSeek Harness (dsh)

`--profile` is required. Use `web` unless you run another profile.

```bash
dsh plugin --profile web add scientific-figure-library
```

Restart the profile (`dsh --profile web` or `dsh web`). The bundle registers
the Skill and mounts `@deepseek-ai/dsh-mcp-client` against this package. If you
already added a dsh MCP client row for a local SFL app, do not also run
`dsh plugin add scientific-figure-library`.

Paste this request:

```text
Install Scientific Figure Library for DeepSeek Harness.
Run: dsh plugin --profile web add scientific-figure-library
Restart the web profile. Do not clone the GitHub repo and do not add a
second figure-library MCP row. First test: figure_library_get_skill, then
figure_library_source_status. If setup_required, bind the global Library
and Local workspace. Tell me when I need to restart dsh.
```

### Claude, Codex, Cursor, Wisp, or another stdio host

Give the agent this repository and the following request:

```text
Install Scientific Figure Library from
https://github.com/xuzhougeng/ScientificFigureLibrary.

Follow docs/QUICKSTART.md. Prefer a GitHub Release ZIP when one is published.
Node.js 22+ is required. Register the stdio MCP server as figure-library
pointing at dist/index.js. For Wisp Science, use npm run package:wisp and
install the generated plugin. For Cursor, use npm run package:cursor and unzip
into ~/.cursor/plugins/local/figure-library/. Bind one global Library directory on disk.
Do not execute user plotting code. First test: open or source_status; if
setup_required, bind the global Library and Local workspace before searching.
Tell me when I need to grant folder access or start a new host session.
```

Manual steps: [docs/QUICKSTART.md](docs/QUICKSTART.md).

## What is included

- **Local Published library** — one user-selected directory, shared across
  projects and hosts
- Direct **image + code intake**, review gates, immutable Revisions and Releases
- MCP App gallery: browse, exact preview, user confirmation
- Search, describe, preview, then **materialize** an exact confirmed template
- Portable backup / restore / fork of the Library
- Optional extra search providers; they do not replace local review
- **Open Figure Modules** — the same `io.github.jarxunlai.personal-figures`
  Provider. A bundled snapshot is only the offline bootstrap. After install,
  SFL asynchronously checks a signed GitHub feed and atomically switches the
  local Catalog overlay. Ordinary template updates no longer require
  repackaging the plugin. Complete module ZIPs are still fetched only for one
  exact selected materialization.

## Bundled figure workflow

The host plugin ZIPs and the npm package used by Pi and dsh include one core figure-library Skill with on-demand
description, script-organization and style references. Ordinary MCP hosts can
read the same guidance with `figure_library_get_skill`, browse thumbnails with
`figure_library_get_candidate_images` or resource URIs, and paginate with
`figure_library_search_page`. The MCP App is optional. Approved R/Python runtimes and host execution/image tools
are still required when the user asks to draw.

Template details render safe Markdown for the requirement, biological use
cases and data profile, with actual input/code/package lists visible.
Technical identities and validation state are available in a collapsed area.
Historical Local Published/OFM entries remain readable; this update does not
rewrite their content or the bundled FigureYa catalog.

## First success

```text
Call figure_library_source_status. If writes are disabled, help me bind one
absolute global Library directory (plan then apply after I confirm the path).
Open the workbench and search my Local Published templates. Wait for me to
confirm one card. Then plan materialization into an empty folder I specify.
Do not execute R or Python. Do not redraw the figure.
```

If the local library is empty, import a figure/code pair, review it, and
publish a Release before searching. Full contract: [docs/PROTOCOL.md](docs/PROTOCOL.md).

## Develop from source

Requires Node.js 22+:

Pull requests run tests, type checking, build and MCP smoke across Linux, Win