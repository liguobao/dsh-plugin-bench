<div align="center">

**English** · [**中文**](README.zh-CN.md)

<img src=".github/assets/banner.svg" alt="Agent-Body — plugins as organs: 26 curated organs across 8 systems, one heartbeat, 84.7% of tool-schema tokens gated away, 0 chronic wounds" width="92%">

# Agent‑Body

**An organ‑based plugin layer for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness): organs, nerve impulses, a heartbeat, reflex arcs, long‑term memory, and closed‑loop self‑healing.**

**26 organ identities · 84.7% of tool-schema tokens gated · 200+ offline assertions · MIT**

</div>

**Agent-Body turns a plugin list into an organism.** Every plugin declares itself an *organ*; a nerve bus routes your
command to the organs that should handle it, a heartbeat circulates state between them, reflex arcs fire without a
single model call, and every failure is attributed by cause before anything retries.

**Try it in 30 seconds — no install, no host, no API key.** The core imports nothing outside Node built-ins, so a fresh
clone runs the real end-to-end chain offline:

```bash
git clone https://github.com/1420079678-ctrl/agent-body && cd agent-body
npm run demo     # command → impulse → dispatch → execute → attribute → reflex fires
npm run check    # the gate CI runs: constant tables, catalog, tests, benchmark — all offline
```

**Already running DeepSeek Harness?** One command installs the body kernel, the memory organ and the context engine:

```powershell
$rel = "https://cdn.jsdelivr.net/gh/1420079678-ctrl/agent-body@v0.1.2/dist"
dsh plugin --profile web add "$rel/dsh-external-dsh-organism-0.1.1.tgz" "$rel/dsh-external-dsh-cortex-0.1.1.tgz" "$rel/dsh-external-dsh-zero-residence-0.1.0.tgz"
```

Restart the harness and `body_status` lists the organs. **The claim you can check for yourself:** the tool-schema block
of the prompt drops **84.7%** across 48 representative commands, and `npm run bench:check` fails the build if that
number drifts. The scope of the number is stated wherever it appears — tool-schema tokens only, not the whole prompt.

⭐ **[Star the repository](https://github.com/1420079678-ctrl/agent-body/stargazers)** if you want it to keep tracking
the host closely — it is a one-person project and the stars are how the next DSH user finds it.

---

<div align="center">

[![Organs](https://img.shields.io/badge/catalog-26%20organs-ff69b4)](#organ-catalog)
[![Plugins](https://img.shields.io/badge/plugins-24%20in%20this%20repo-blue)](#organ-catalog)
[![Schema gating](https://img.shields.io/badge/schema%20gating-84.7%25%20tool--schema%20tokens%20gated-2ecc71)](#token-economy)
[![Benchmark](https://img.shields.io/badge/benchmark-reproducible%20in--repo-blueviolet)](benchmarks/results/REPORT.md)
[![Regressions](https://img.shields.io/badge/offline%20regressions-200%2B%20assertions-informational)](#verify-it-yourself)
[![Node](https://img.shields.io/badge/node-22.19%20%7C%2024-339933)](#quick-start)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/1420079678-ctrl/agent-body?style=flat&logo=github&label=%E2%AD%90%20stars)](https://github.com/1420079678-ctrl/agent-body/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/1420079678-ctrl/agent-body)](https://github.com/1420079678-ctrl/agent-body/issues)
[![dshfind](https://dshfind.com/api/badge/1420079678-ctrl/agent-body)](https://dshfind.com/en/plugins/1420079678-ctrl/agent-body)

[Architecture](ARCHITECTURE.md) · [Organ Catalog](catalog/organs.json) · [Benchmark](benchmarks/results/REPORT.md) · [Roadmap](ROADMAP.md) · [**中文文档**](README.zh-CN.md)

[Official DSH discussion — **Show Your Plugins!**](https://github.com/deepseek-ai/deepseek-harness/discussions/7555) · the channel the harness `CONTRIBUTING` points plugin authors to

**v0.1.1** · MIT · Windows-first (Node 22.19 / 24) · **26 organ identities in the catalog, realised by 24 plugin packages in this repository** · [release notes](https://github.com/1420079678-ctrl/agent-body/releases/tag/v0.1.1)

[![Live vitals replay — recorded from a real install](docs/preview.png)](https://1420079678-ctrl.github.io/agent-body/)

▶ **[Open the live demo](https://1420079678-ctrl.github.io/agent-body/)** — a recorded replay of a real install: the heartbeat, the organs, the pulse stream, the healing ledger and the token gate, with nothing installed. It is generated from the runtime files (`vitals.json`, `bloodstream.json`, `pulse.jsonl`), not retyped from screenshots.

**Contents** · [Where it's listed](#where-its-listed) · [Install in one line](#install-in-one-line) · [Why this exists](#why-this-exists) · [What makes it different](#what-makes-it-different) · [The five biological layers](#the-five-biological-layers) · [Architecture at a glance](#architecture-at-a-glance) · [Organ catalog](#organ-catalog) · [Quick start](#quick-start) · [Write your own organ](#write-your-own-organ) · [Verify it yourself](#verify-it-yourself) · [When not to use this](#when-not-to-use-this) · [FAQ](#faq) · [Repository layout](#repository-layout) · [Contributing](#contributing) · [Roadmap](#roadmap)

</div>

---

## Where it's listed

Checked, not claimed — every entry below resolves today:

| Listing | What it is |
| --- | --- |
| [`awesome-dsh-plugin`](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) · 16.7k ★ | the main DSH plugin directory; both `dsh-organism` and `dsh-cortex` are indexed as separate entries |
| [dshfind](https://dshfind.com/en/plugins/1420079678-ctrl/agent-body) | DSH plugin search engine, with a per-repository page |
| [`imsai-sh/awesome-deepseek-harness-plugins`](https://github.com/imsai-sh/awesome-deepseek-harness-plugins) | plugin hub with machine-readable catalogue entries |
| [`bruc3van/awesome-dsh-plugin`](https://github.com/bruc3van/awesome-dsh-plugin) | daily-crawled DSH plugin list, human-reviewed |
| [`billLiao/awesome-dsh-plugin`](https://github.com/billLiao/awesome-dsh-plugin) | curated list, memory category |
| [`unStone/dsh-xray`](https://github.com/unStone/dsh-xray) | declared-capabilities scanner; carries a page for this repository |
| [`linny006/agent-framework-radar`](https://github.com/linny006/agent-framework-radar) · [`llmops-radar`](https://github.com/linny006/llmops-radar) | live indexes of newly shipping agent frameworks and LLMOps tooling |

It is also the subject of the harness's official showcase thread —
[**Show Your Plugins!** discussion #7555](https://github.com/deepseek-ai/deepseek-harness/discussions/7555).

---

## Install in one line

Two supported paths — start with the first, switch to the second if your network blocks `github.com`.

### Path 1 — GitHub release assets

Versioned assets built by CI. `releases/latest/download/` always resolves to the newest release, so this command does
not need editing when a version is bumped.

```powershell
$rel = "https://github.com/1420079678-ctrl/agent-body/releases/latest/download"
dsh plugin --profile web add `
  "$rel/dsh-external-dsh-organism-0.1.1.tgz" `
  "$rel/dsh-external-dsh-cortex-0.1.1.tgz" `
  "$rel/dsh-external-dsh-zero-residence-0.1.0.tgz"
```

```bash
rel=https://github.com/1420079678-ctrl/agent-body/releases/latest/download
dsh plugin --profile web add \
  "$rel/dsh-external-dsh-organism-0.1.1.tgz" \
  "$rel/dsh-external-dsh-cortex-0.1.1.tgz" \
  "$rel/dsh-external-dsh-zero-residence-0.1.0.tgz"
```

### Path 2 — served from this repository over jsDelivr

The same tarballs, committed under [`dist/`](dist/) and served by a CDN with mainland nodes. Reach for this when Path 1
hangs: those URLs 302-redirect to `objects.githubusercontent.com`, a hop that is blocked on some networks. The symptom
is `fetch failed` with `downloaded 0` **while dependency resolution succeeds** — the download hop is the problem, not
the packages.

```powershell
$rel = "https://cdn.jsdelivr.net/gh/1420079678-ctrl/agent-body@v0.1.2/dist"
dsh plugin --profile web add `
  "$rel/dsh-external-dsh-organism-0.1.1.tgz" `
  "$rel/dsh