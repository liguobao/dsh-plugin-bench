<h1 align="center">OpenDesign: The open-source Claude Design alternative</h1>

> ⚡ **[OpenDesign Cloud — the official model service.](https://open-design.ai/zh/pricing/)** One recharge to use both agent and image models inside OpenDesign: GPT, Claude, and DeepSeek for agents; GPT Image 2.0, Seedream 5.0 Pro, and Nano Banana 2.0 for images.
>
> 🚀 **[DeepSeek V4 Flash and V4 Pro are now available.](https://open-design.ai/zh/pricing/)** Put top-tier intelligence to work across prototypes, decks, design systems, and everyday agent tasks. OpenDesign members can use both models without limits for two weeks, directly inside the app.
>
> 🧩 **[DeepSeek Harness is now supported.](https://open-design.ai/zh/agents/deepseek-harness-design/)** Connect DeepSeek's official `dsh` agent harness to OpenDesign as a native runtime, with structured thinking, tool calls, model discovery, cancellation, and session resume. Generated files stay in the OpenDesign workflow for live preview and delivery.

<p align="center">
  <img src="https://repo-assets.open-design.ai/resources/images/hero.png" alt="OpenDesign hero banner — the headline &quot;The open-source Claude Design alternative&quot; over a classical scene of columns and robed figures on a digital-code backdrop, with stat cards for design systems, plugins, coding agents, and media providers" width="100%" />
</p>

<p align="center">
  <a href="https://open-design.ai/?utm_source=github&utm_medium=referral&utm_content=readme_website">Website</a> ·
  <a href="https://open-design.ai/?utm_source=github&utm_medium=referral&utm_content=readme_download">Download</a> ·
  <a href="https://open-design.ai/cloud/?utm_source=github&utm_medium=referral&utm_content=readme_cloud">OpenDesign Cloud</a> ·
  <a href="https://discord.gg/mHAjSMV6gz">Discord</a> ·
  <a href="https://x.com/OpenDesignHQ">Follow @OpenDesignHQ</a>
</p>

<p align="center">
  <a href="https://github.com/nexu-io/open-design/releases"><img alt="release" src="https://img.shields.io/github/v/release/nexu-io/open-design?style=flat&color=blueviolet&label=release&include_prereleases&display_name=tag" /></a>
  <a href="LICENSE"><img alt="license" src="https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat" /></a>
  <a href="https://discord.gg/mHAjSMV6gz"><img alt="discord" src="https://img.shields.io/discord/1479002485040480266?style=flat&logo=discord&logoColor=white&label=discord&color=5865F2&cacheSeconds=3600" /></a>
  <a href="QUICKSTART.md"><img alt="quickstart" src="https://img.shields.io/badge/quickstart-3%20commands-green?style=flat" /></a>
</p>

<p align="center"><b>English</b> · <a href="docs/i18n/README.es.md">Español</a> · <a href="docs/i18n/README.pt-BR.md">Português</a> · <a href="docs/i18n/README.de.md">Deutsch</a> · <a href="docs/i18n/README.fr.md">Français</a> · <a href="docs/i18n/README.zh-CN.md">简体中文</a> · <a href="docs/i18n/README.zh-TW.md">繁體中文</a> · <a href="docs/i18n/README.ko.md">한국어</a> · <a href="docs/i18n/README.ja-JP.md">日本語</a> · <a href="docs/i18n/README.ar.md">العربية</a> · <a href="docs/i18n/README.ru.md">Русский</a> · <a href="docs/i18n/README.uk.md">Українська</a> · <a href="docs/i18n/README.tr.md">Türkçe</a> · <a href="docs/i18n/README.th.md">ภาษาไทย</a></p>

---

## What is OpenDesign

🎨 **The open-source Claude Design alternative.** &nbsp;🖥️ **Local-first native desktop app for macOS and Windows.** &nbsp;⚡ **Composable skills, brand-grade `DESIGN.md` design systems, and ready-to-use plugins.** &nbsp;🖼️ Generates **web · desktop · mobile prototypes**, **live dashboards / artifacts**, **decks**, **images**, **video**, plus **HyperFrames** motion graphics. 🔒 Sandboxed iframe preview · HTML / PDF / PPTX / MP4 export. &nbsp;🤖 **Runs on DeepSeek Harness (`dsh`) · Claude Code · OpenClaw · Codex · Cursor · OpenCode · Qwen · Copilot · Amp · Hermes · Kimi · Antigravity and 26 distinct local CLI executables**, or any OpenAI-compatible endpoint via BYOK.

OpenDesign is what you get when the **agent-native** loop Anthropic shipped with Claude Design — discover the brief, lock the direction, stream the artifact, critique, deliver — stops being closed and becomes a **filesystem of functional skills, rendering design templates, design systems, and plugins** that the coding agents already on your laptop can read, write, and remix. Your CLI becomes the design engine, your laptop becomes the studio, and your team's `DESIGN.md` becomes the brand contract.

It's also the **Figma alternative for the agent era** — instead of pushing pixels on a canvas, it delivers single-page artifacts in real CSS, real fonts, real components, exported straight to HTML / PDF / PPTX / MP4 — already shaped by your design system, already runnable inside the agent you use every day.


---

## Product tour

A quick look at the core OpenDesign workflow. Start from **Home** with a brief, explore reusable skills in **Plugins**, and turn brand references into a **Design System**. Then enter a project's **Studio** to create and refine prototypes, decks, mobile apps, images, documents, and HyperFrames in one place.

### Core pages

<table>
<tr>
<td valign="top">
<img src="docs/screenshots/product-tour/home.png" alt="OpenDesign Home page with artifact types, brief composer, model picker, and examples" /><br/>
<sub><b>Home</b> — choose an artifact type, enter a brief, and set the design system, working directory, and model before you start.</sub>
</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/plugins.png" alt="OpenDesign Plugins page showing the official skills catalog" /><br/>
<sub><b>Plugins</b> — browse official skills by category, search the catalog, and launch a workflow with <code>Try it</code>.</sub>
</td>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/design-system.png" alt="Shopify design system preview inside OpenDesign Studio" /><br/>
<sub><b>Design System</b> — extract and refine a brand's visual language, preview the result, and create with it in the same workspace.</sub>
</td>
</tr>
</table>

### Studio — many artifact types in one project

Inside a project's Studio, the conversation, generated files, and live preview stay together across six artifact types:

<table>
<tr>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/studio-prototype.png" alt="Web prototype preview in OpenDesign Studio" /><br/>
<sub><b>Prototype</b> — generate or reconstruct web experiences, inspect the rendered page, and iterate with the agent in place.</sub>
</td>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/studio-deck.png" alt="Multi-slide deck preview in OpenDesign Studio" /><br/>
<sub><b>Deck</b> — create multi-slide presentations, review thumbnails and speaker notes, and export when ready.</sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/studio-mobile-app.png" alt="Mobile app artifact preview in OpenDesign Studio" /><br/>
<sub><b>Mobile app</b> — generate and polish mobile interfaces in a device preview, with the conversation, output files, and next-step actions beside it.</sub>
</td>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/studio-image.png" alt="Generated image preview in OpenDesign Studio" /><br/>
<sub><b>Image</b> — generate visual assets from the project conversation, preview the result at full size, then download or open it.</sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/studio-document.png" alt="Multi-page document preview in OpenDesign Studio" /><br/>
<sub><b>Document</b> — create polished, multi-page guides and editorial documents, inspect the rendered layout, and export or share when ready.</sub>
</td>
<td width="50%" valign="top">
<img src="docs/screenshots/product-tour/studio-hyperframe.png" alt="HyperFrame motion graphic preview in OpenDesign Studio" /><br/>
<sub><b>HyperFrame</b> — build code-driven motion graphics, preview the an