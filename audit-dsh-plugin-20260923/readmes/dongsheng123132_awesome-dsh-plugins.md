![Awesome DSH Plugins — evidence-backed plugin radar](docs/assets/awesome-dsh-plugins-hero.png)

# Awesome DSH Plugins

> Discover installable DeepSeek Harness plugins, inspect the evidence behind each listing, and explore the 2Origin plugin lab.

[![Repository checks](https://github.com/dongsheng123132/awesome-dsh-plugins/actions/workflows/check.yml/badge.svg)](https://github.com/dongsheng123132/awesome-dsh-plugins/actions/workflows/check.yml)
[![MIT license](https://img.shields.io/github/license/dongsheng123132/awesome-dsh-plugins)](LICENSE)
[![DSH plugin topic](https://img.shields.io/badge/GitHub_topic-dsh--plugin-0969da)](https://github.com/topics/dsh-plugin)
[![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)

[中文](README.zh-CN.md) · [Official DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) · [Browse verified bundles](#radar) · [Search from the terminal](#search-from-the-terminal) · [2Origin plugin lab](#2origin-plugin-lab)

## Start here

| I want to… | Go to |
|---|---|
| Find an installable DSH profile bundle | [Radar](#radar) |
| Estimate the work needed to port an Agent Skill | [Capability Port Score](#capability-port-score) |
| Search plugins offline from a terminal | [CLI search](#search-from-the-terminal) |
| Inspect plugins with reproducible runtime evidence | [Runtime compatibility layer](#runtime-compatibility-layer) |
| Explore evidence-first plugins built in this lab | [2Origin plugin lab](#2origin-plugin-lab) |

Normal CLI searches use the committed snapshot and need no GitHub token:

```bash
npx github:dongsheng123132/awesome-dsh-plugins search memory
```

This repository deliberately distinguishes a repository that mentions DSH from an installable DSH profile bundle. A plugin receives the **Verified Bundle** mark only when the scanner finds both:

1. a `package.json` declaration at `dsh.bundle.patch`; and
2. the declared patch file in the same Git tree.

This is structural verification, not a security audit or a promise that the plugin works with today's DSH main branch.
Categories are heuristic navigation aids; manifest and patch evidence, not the category label, determines verification.

## Radar

<!-- RADAR:START -->
**1098** verified bundles / **1003** topic repositories examined / **11490** reported by GitHub

Other: 329 · UI / TUI: 225 · Token & Cost: 68 · Browser: 67 · MCP Bridge: 63 · Security: 61 · Memory: 55 · Model & Routing: 54 · Coding: 34 · Office: 32 · Developer Tools: 28 · Finance: 28 · Long-running: 22 · Writing / Novel: 19 · Research: 12 · Provenance & Lineage: 1

| Plugin | Category | Stars | License | Evidence | Install |
|---|---:|---:|---|---|---|
| [@open-design/dsh-runtime](https://github.com/nexu-io/open-design)<br><sub>nexu-io/open-design</sub> | Office | 91246 | Apache-2.0 | `packages/dsh-runtime/package.json` → `packages/dsh-runtime/cordis.patch.yml` | See package docs |
| [dsh-plugin-reactive-resume](https://github.com/amruthpillai/reactive-resume)<br><sub>amruthpillai/reactive-resume</sub> | MCP Bridge | 41696 | MIT | `packages/dsh-plugin/package.json` → `packages/dsh-plugin/cordis.patch.yml` | See package docs |
| [@openviking/dsh-memory-plugin](https://github.com/volcengine/OpenViking)<br><sub>volcengine/OpenViking</sub> | Memory | 33116 | AGPL-3.0 | `examples/dsh-memory-plugin/package.json` → `examples/dsh-memory-plugin/cordis.patch.yml` | See package docs |
| [@wxg-prc-cpg/dsh-weknora](https://github.com/Tencent/WeKnora)<br><sub>Tencent/WeKnora</sub> | Office | 20577 | NOASSERTION | `packages/dsh-weknora/package.json` → `packages/dsh-weknora/cordis.patch.yml` | See package docs |
| [dsh-plugin-desktop](https://github.com/anywhere-labs/dsh-desktop)<br><sub>anywhere-labs/dsh-desktop</sub> | Other | 19998 | MIT | `dsh-plugin-desktop/package.json` → `dsh-plugin-desktop/cordis.patch.yml` | See package docs |
| [@tt-a1i/archify-dsh](https://github.com/tt-a1i/archify)<br><sub>tt-a1i/archify</sub> | Long-running | 15658 | MIT | `integrations/deepseek-harness/package.json` → `integrations/deepseek-harness/cordis.patch.yml` | See package docs |
| [@memtensor/memos-local-plugin](https://github.com/MemTensor/MemOS)<br><sub>MemTensor/MemOS</sub> | Token & Cost | 10966 | Apache-2.0 | `apps/memos-local-plugin/package.json` → `apps/memos-local-plugin/adapters/deepseek-harness/cordis.patch.yml` | See package docs |
| [@dsh-external/dsh-super-injector](https://github.com/yjh051108/dsh-routing-suite)<br><sub>yjh051108/dsh-routing-suite</sub> | Model & Routing | 6777 | MIT | `injector/package.json` → `injector/cordis.patch.yml` | See package docs |
| [@dsh-web/files](https://github.com/zhu1090093659/dsh-web)<br><sub>zhu1090093659/dsh-web</sub> | Browser | 6005 | Apache-2.0 | `market/shell/packages/dsh-web-files/package.json` → `market/shell/packages/dsh-web-files/cordis.patch.yml` | See package docs |
| [dsh-ouroboros](https://github.com/Q00/ouroboros)<br><sub>Q00/ouroboros</sub> | Long-running | 5657 | MIT | `integrations/dsh-plugin/package.json` → `integrations/dsh-plugin/cordis.patch.yml` | See package docs |
| [deepseek-idesign](https://github.com/Devin-AXIS/iPolloWork)<br><sub>Devin-AXIS/iPolloWork</sub> | Other | 4774 | NOASSERTION | `external-plugins/deepseek-harness/design-studio/package.json` → `external-plugins/deepseek-harness/design-studio/cordis.patch.yml` | See package docs |
| [@petdex/dsh-plugin](https://github.com/crafter-station/petdex)<br><sub>crafter-station/petdex</sub> | Other | 3974 | MIT | `packages/petdex-desktop-native/integrations/dsh/package.json` → `packages/petdex-desktop-native/integrations/dsh/cordis.patch.yml` | See package docs |
| [@liustack/modlens](https://github.com/liustack/modlens)<br><sub>liustack/modlens</sub> | MCP Bridge | 3644 | MIT | `package.json` → `cordis.patch.yml` | `dsh plugin --profile web add github:liustack/modlens` |
| [@struktoai/mirage-dsh](https://github.com/strukto-ai/mirage)<br><sub>strukto-ai/mirage</sub> | Other | 3563 | Apache-2.0 | `typescript/packages/dsh/package.json` → `typescript/packages/dsh/cordis.patch.yml` | See package docs |
| [@agentscope-ai/reme](https://github.com/agentscope-ai/ReMe)<br><sub>agentscope-ai/ReMe</sub> | Memory | 3344 | Apache-2.0 | `packages/typescript/package.json` → `packages/typescript/dsh/cordis.patch.yml` | See package docs |
| [dsh-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar)<br><sub>omdsh-dev/DSH-better-sidebar</sub> | UI / TUI | 2861 | MIT | `package.json` → `cordis.patch.yml` | `dsh plugin --profile web add github:omdsh-dev/DSH-better-sidebar` |
| [dsh-codex-taskboard](https://github.com/chuspeeism/dashi-taskboard)<br><sub>chuspeeism/dashi-taskboard</sub> | Other | 2541 | Apache-2.0 | `integrations/deepseek-harness/package.json` → `integrations/deepseek-harness/cordis.patch.yml` | See package docs |
| [@deepseek-harness-tui/dsh-tui](https://github.com/ccch1mneyyy/dsh-TUI)<br><sub>ccch1mneyyy/dsh-TUI</sub> | UI / TUI | 2511 | MIT | `package.json` → `cordis.patch.yml` | `dsh plugin --profile web add github:ccch1mneyyy/dsh-TUI` |
| [@zilliz/memsearch-dsh](https://github.com/zilliztech/memsearch)<br><sub>zilliztech/memsearch</sub> | Memory | 2503 | MIT | `plugins/dsh/package.json` → `plugins/dsh/cordis.patch.yml` | See package docs |
| [dshmarket](https://github.com/dsh-market/dsh-market)<br><sub>dsh-market/dsh-market</sub> | Finance | 2299 | MIT | `package.json` → `cordis.patch.yml` | `dsh plugin --profile web add github:dsh-market/dsh-market` |
| [@dsh-external/dsh-client-ui-skin-maid-atelier](https://github.com/Small-tailqwq/dsh-deep-whale)<br><sub>Small-tailqwq/dsh-deep-whale</sub> | UI / TUI | 1696 | — | `maid-atelier/package.json` → `maid-atelier/cordis.patch.yml` | See package docs |
| [@wxg-prc-cpg/browser-skill-dsh-plugin](https://github.com/Tencent/BrowserSkill)<br><sub>Tencent/BrowserSkill</sub> | Browser | 1310 | MIT | `packages/dsh-plugin-browserskill/package.json` → `packages/dsh-plugin-browserskill/cordis.patch.yml` | See package docs |
| [@mem9/ds