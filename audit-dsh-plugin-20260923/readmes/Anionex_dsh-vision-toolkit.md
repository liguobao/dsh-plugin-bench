<p align="center">
  <img src="assets/hero-v2.png" alt="DSH Vision Toolkit helps text-only DeepSeek Harness agents understand images and complete visual tasks" />
</p>

<div align="center">

# DSH Vision Toolkit

<a href="https://trendshift.io/repositories/149708?utm_source=trendshift-badge&amp;utm_medium=badge&amp;utm_campaign=badge-trendshift-149708" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/149708/daily?language=TypeScript" alt="Anionex%2Fdsh-vision-toolkit | Trendshift" width="250" height="55"/></a>

[![Recommended by dshfind](https://img.shields.io/badge/recommended%20by-dshfind-FFD700?style=flat-square)](https://dshfind.com/en/plugins/Anionex/dsh-vision-toolkit)
[![dshfind score: 94 — highest-rated plugin](https://img.shields.io/badge/dshfind%20score-94%20%7C%20highest--rated%20plugin-5B4CF0?style=flat-square)](https://dshfind.com/en/plugins/Anionex/dsh-vision-toolkit)
[![agentic leaderboard](https://www.theagenticleaderboard.com/badges/new/dsh-vision-toolkit.svg)](https://www.theagenticleaderboard.com)

[![npm](https://img.shields.io/npm/v/@anionex/dsh-vision-toolkit?style=flat-square&color=5B4CF0)](https://www.npmjs.com/package/@anionex/dsh-vision-toolkit)
[![MIT](https://img.shields.io/badge/license-MIT-0B7285?style=flat-square)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-Web%20%2B%20Headless-5B4CF0?style=flat-square)](cordis.patch.yml)

**A more powerful vision toolkit—give text-only models in DeepSeek Harness eyes: image Q&A, long-screenshot OCR, UI restoration, and GUI visual tasks in one toolkit and Skill.**

🚀 Paste an image and ask directly | Install with one command | Broad use cases

[Highlights](#highlights) | [Quick start](#quick-start-three-steps) | [Toolbox](#toolbox) | [Configuration and limits](#configuration-and-limits) | [Troubleshooting](#troubleshooting) | [Community](#development-and-community)

🌐 **English** | [中文](README.zh.md)

</div>

🏆 This project is the first comprehensive vision-tool plugin in the DeepSeek Harness ecosystem: it was initiated before internal beta and built during the beta with reference to [`agent-vision-toolkit`](https://github.com/Anionex/agent-vision-toolkit).

> **Original work:** The system and division of responsibilities behind these visual tools, together with the `vision-skills` Skill, were personally created and continuously refined by the author through long-term real-world use and repeated iteration.

> If this project helps you or gives you some inspiration, feel free to star 🌟 & fork.

## Highlights

- **Paste an image and ask directly.** In DSH Web, pasting an image switches the text-only model to its `(Vision Toolkit)` variant automatically — no manual path copying or model changes. Native thumbnails, session history, and workspace paths stay intact; Web can preview artifacts.
- **One command to install.** After installation, configure a vision provider in **Settings → Vision Toolkit** and start using the tools.
- **Not just a caption — the content that matters.** The model does not produce a generic description; it extracts evidence around the current task, such as “Where is the error?” or “Where is the button?”.
- **A battle-tested visual-task methodology.** The bundled Skill tells the agent what to look at for different visual tasks, which tool to choose, how to proceed, and how to verify the result.

[`agent-vision-toolkit`](https://github.com/Anionex/agent-vision-toolkit) gives an agent more than image captions: it can read, locate, crop, trace, rebuild, and verify visual work. DSH Vision Toolkit is its native DeepSeek Harness integration, bringing that workflow into Web and Headless Profiles.

This project has two layers:

1. **Visual tools and a Skill:** the agent learns when to inspect, ground, OCR, crop, trace, or compare pixels.
2. **Native DSH integration:** those capabilities live inside Profiles, sessions, Settings, Artifacts, and the Web UI.

```sh
dsh plugin --profile web add @anionex/dsh-vision-toolkit
```

**Upstream toolkit:** [Anionex/agent-vision-toolkit](https://github.com/Anionex/agent-vision-toolkit) · **Project website:** [agent-vision.anionex.me](https://agent-vision.anionex.me)

## ❤️ Sponsor

> Want to sponsor this project? See [FUNDING.md](FUNDING.md) or email davidyang042@gmail.com.

<details open>
<summary>Click to collapse</summary>

<table>
<tr>
<td width="220" align="center" valign="middle"><a href="https://aihubmix.com/?aff=sinZ"><img src="assets/logo_aihubmix.png" alt="AIHubMix" height="48"></a></td>
<td valign="middle">Thanks to <a href="https://aihubmix.com/?aff=sinZ">AIHubMix</a> for sponsoring this project! AIHubMix is a stable, high-concurrency AI model API gateway that connects Claude, GPT, Gemini, DeepSeek, and other mainstream models through a single API key, compatible with multiple protocols, with <b>free model options</b> available. To sign up, use the <a href="https://aihubmix.com/?aff=sinZ">AIHubMix entry</a> outside mainland China or the <a href="https://inferera.com/?aff=sinZ">Inferera entry</a> within mainland China.</td>
</tr>
<tr>
<td width="220" align="center" valign="middle"><a href="https://api.ewo.so/register?aff=U6PT7J"><img src="assets/logo_eapi_dark.png" alt="E-API" height="48"></a></td>
<td valign="middle">Thanks to <a href="https://api.ewo.so/register?aff=U6PT7J">E-API</a> for sponsoring this project! E-API aggregates mainstream AI models behind OpenAI-, Anthropic-, and Codex-compatible APIs, with selected Claude models up to <b>98% below official prices</b> and DeepSeek V4 models about <b>25% below official prices</b>.</td>
</tr>
</table>

</details>

**Contents**

- [Highlights](#highlights)
- [Recent updates](#recent-updates)
- [Who it is for](#who-it-is-for)
- [See it in action](#see-it-in-action)
- [Quick start: three steps](#quick-start-three-steps)
- [Toolbox](#toolbox)
- [Configuration and limits](#configuration-and-limits)
- [Troubleshooting](#troubleshooting)
- [Donation](#donation)
- [Development and community](#development-and-community)

## Recent updates

- **2026-08-20 · AIHubMix setup guide:** Added a screenshot-based guide for getting an API key through the Inferera entry and configuring the Gemini 3.7 Flash vision model; Settings now links directly to this guide.
- **2026-08-19 · Transparent routing by default:** The model selector keeps one entry per model with the original name, and image input (paste, history, `read_image`) works without manually switching to a `(Vision Toolkit)` variant. Disable “Transparent variant routing” in advanced settings → image input to restore the explicit entries.
- **2026-08-16 · Windows Python:** Added Microsoft Store Python support, fixing first-time isolated-runtime setup failures for affected Windows users.
- **2026-08-17 · Vision upgrade:** Switched the default model to Gemini 3.7 Flash and fixed Qwen/Gemini bounding-box coordinate order.
- **2026-08-16 · Image paste:** Text-only routes now switch to a `(Vision Toolkit)` variant and keep a workspace path, fixing blocked pastes and images that could not be reused later.
- **2026-08-16 · Service stability:** Expanded service capacity to reduce peak-time `429` responses.
- **2026-08-16 · Real model test:** Added a full image-request test in Settings, fixing the false confidence caused by a successful `/models` request to a model that still cannot process images.

## Who it is for

1. Want an interaction experience similar to a multimodal model: paste an image directly and ask a question or make a request.
2. Want more than image Q&A — complete more complex, high-value visual tasks such as turning a sketch into a front-end page, converting an image into HTML, or extracting chat messages from long screenshots; more scenarios are added over time.

The bundled `vision-skills` Skill carries the complete upstream playbooks, explaining when to use each workflow, in what order to call the tools, and how to verify the result:

| Playbook | What the agent l