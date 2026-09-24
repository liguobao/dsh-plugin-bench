<div align="center">

<img src="docs/media/mimir-cover.png" alt="Mimir — open-source AI research workspace" width="720">

<h1>Mimir</h1>

<p><strong>The research-lifecycle copilot inside <a href="https://github.com/deepseek-ai/deepseek-harness">DeepSeek Harness</a>:</strong><br>
literature · experiments &amp; remote GPUs · figures · LaTeX writing → compile → preview · group-meeting decks — one workbench, driven by your agent.</p>

<p>
<a href="https://github.com/1692775560/dsh-Mimir-Academic-research/actions/workflows/ci.yml"><img src="https://github.com/1692775560/dsh-Mimir-Academic-research/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
<a href="https://www.npmjs.com/package/dsh-mimir"><img src="https://img.shields.io/npm/v/dsh-mimir?label=dsh-mimir" alt="npm: dsh-mimir"></a>
<a href="https://mimir.smartlarkai.com"><img src="https://img.shields.io/badge/website-mimir.smartlarkai.com-47608c" alt="Website"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
</p>

<p><strong>English</strong> · <a href="README.zh.md">中文</a> · <a href="https://mimir.smartlarkai.com">Website</a></p>

</div>

## What it is

Mimir is a single npm package (`dsh-mimir`) that plugs into dsh and gives you:

- **Nine-view web workbench** (sidebar toggle → overlay, dark/light, 中/EN):
  **Overview** pipeline & stats · **Paper** Overleaf-style LaTeX studio (edit → compile → PDF preview, one-click AI fix) · **Library** arXiv + web search, AI relevance scoring, fullscreen PDF reader · **Experiments** metric charts, one-click paper figures · **Figures** upload/organize/insert into the paper · **Meetings** one-click group-meeting PPT (real paper figures + optional AI illustrations) · **Servers** GPU fleet probes + remote jobs · **Ledger** humanized research journal — idea evolution auto-captured into a worktree, six-perspective digest capsules, one-click progress report · **Venues** CCF conference-deadline countdown (ccfddl catalog, per-project watchlist) + CCF-A journal directory — every view live-refreshes over SSE as the agent writes, no manual reload
- **Agent tools & slash commands**: `/research-idea` `/research-plan` `/research-review` `/paper-write` `/paper-compile`, plus `arxiv_search`, `web_search`, `wiki_note`, `figure_save`, `latex_compile`, `meeting_deck`, `venue_search`, and the remote-compute quartet `server_list` / `server_check` / `server_submit_job` / `server_list_jobs` (same remembered servers and jobs as the Servers tab)
- **Eleven bundled research skills** (literature review, novelty check, experiment planning, citation audit, bilingual de-AI polish, rebuttal…) that teach the agent the workflow — no setup needed

| Overview | Paper | Library | Experiments |
| --- | --- | --- | --- |
| ![Overview](docs/screenshots/tab-overview.png) | ![Paper](docs/screenshots/tab-paper.png) | ![Library](docs/screenshots/tab-papers.png) | ![Experiments](docs/screenshots/tab-experiments.png) |

| Figures | Meetings | Servers | Ledger |
| --- | --- | --- | --- |
| ![Figures](docs/screenshots/tab-figures.png) | ![Meetings](docs/screenshots/tab-meetings.png) | ![Servers](docs/screenshots/tab-servers.png) | ![Ledger](docs/screenshots/tab-ledger.png) |

▶ [Full MP4 demo](https://raw.githubusercontent.com/1692775560/dsh-Mimir-Academic-research/main/docs/media/mimir-demo.mp4) (22 MB)

## Quickstart

Prerequisites: Node.js ≥ 22, the dsh CLI (`npm install -g @deepseek-ai/dsh`), and a `DEEPSEEK_API_KEY` for agent sessions.

```sh
dsh plugin --profile web add dsh-mimir@latest   # installs and self-activates
dsh web                                          # then open http://127.0.0.1:3080
```

Got an old version (e.g. 0.11.x/0.12.x)? dsh's plugin store uses pnpm, which holds back freshly published releases by default. Pin the exact version instead: `dsh plugin --profile web remove dsh-mimir && dsh plugin --profile web add dsh-mimir@0.21.0`

Version compatibility: **0.18.x requires dsh ≥ 0.1.2-alpha.4** (upstream breaking changes). On an older dsh, pin the previous release: `dsh plugin --profile web add dsh-mimir@0.16.0`.

Click **Mimir** in the sidebar footer. The wiki persists at `~/.dsh/storages/research_wiki.json`; artifacts land under `./.research`.

Optional capabilities:

- **Paper compilation** — install a LaTeX engine (`brew install tectonic` is easiest), or set `latex.engine` to a binary path
- **Web search** — the sxng CLI ships with the package; give it a SearXNG server with one command (Docker-free, local venv):
  ```sh
  bash scripts/setup-web-search.sh
  ```
- **Zotero** — set `zotero.apiKey` / `zotero.userId` in the plugin config (keys at zotero.org/settings/keys)

## Related projects

- **[Mimir-Desktop](https://github.com/hxhy00/Mimir-Desktop)** — a standalone Electron desktop edition of the workbench: no dsh install, no backend to run, same feature set. Community-maintained by [@hxhy00](https://github.com/hxhy00), MIT.

## Configuration

All keys are optional; set them in the profile's `cordis.patch.yml` (full commented example: [examples/mimir-agent/cordis.yml](examples/mimir-agent/cordis.yml)).

| Key | Default | Meaning |
| --- | --- | --- |
| `workspaceDir` | `.research` | Research workspace root (artifacts, backups) |
| `latex.engine` | `auto` | `latexmk` / `tectonic` probe, or absolute binary path |
| `search.command` | `auto` | Web search: `auto` uses `sxng` from PATH or the bundled copy |
| `reviewer.maxRounds` | `3` | Per-project review-round budget |
| `backup.enabled` / `intervalMinutes` / `keep` | `true` / `60` / `24` | Scheduled wiki snapshots |
| `skills.enabled` | `true` | Register the eleven bundled research skills |

## Troubleshooting

- **Plugin not found** — dsh resolves plugin names from the profile directory; install with `dsh plugin --profile web add dsh-mimir@latest`, not from your cwd.
- **LaTeX engine not found** — `brew install tectonic`, or point `latex.engine` at an absolute path. First tectonic compile downloads packages; raise `latex.timeoutMs` if it times out.
- **arXiv fails** — export `HTTPS_PROXY` before starting dsh when behind a proxy.
- **Web search unavailable** — run `bash scripts/setup-web-search.sh` (local SearXNG), or `sxng init` against your own instance, then restart dsh.

## Changelog

- **0.21.0** — manage projects inside the panel: create, rename, and delete with a cascaded cleanup (experiments, figures, venue watches, ideas, paper links, meeting decks; the paper directory goes only for imported projects) plus the dsh session switcher for the "… with AI" target ([#160](https://github.com/1692775560/dsh-Mimir-Academic-research/issues/160)); delete runs as a disk-first orchestrator under per-project/paper mutation locks, and deselecting a project flushes the draft and clears every per-project slice · venue_search timeline schema fix, arXiv search fallback, and a configurable `arxiv.timeoutMs` ([#264](https://github.com/1692775560/dsh-Mimir-Academic-research/issues/264)) · meeting-deck paper picking reworked: preselected top-5 candidates, search, and per-paper score reasons
- **0.20.0** — quality batch 4: compile status survives restarts (backfilled from the on-disk PDF as "compiled in a previous session") ([#221](https://github.com/1692775560/dsh-Mimir-Academic-research/issues/221)) · scheduled tasks get bounded exponential backoff plus a per-task health view on the overview ([#223](https://github.com/1692775560/dsh-Mimir-Academic-research/issues/223)) · unified remote-job lifecycle contract — duration-cap kills settle as `unknown` (outcome unobserved), capture-cap floods as an explicit `failed` ([#225](https://github.com/1692775560/dsh-Mimir-Academic-research/issues/225)) · experiment metrics gain min/max directions and zero-baseline charts (negative bars extend left, best run shaded) ([#220](https://github.com/1692775560/dsh-Mimir-Academic-research/issues/220)) · one cancellation contract for long tasks — compiles and deck generations abort on panel cancel AND host dispo