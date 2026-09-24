
## 🚀 Updates v0.10.8: Lossless JSON Unification, Dual-Output & Strict Validation (#199)
- **Lossless JSON & Dual-Output Unification**: `upscale_image`, `remove_background`, `blend_images`, and `vectorize_image` now consistently return `toLosslessJson` and formatted markdown `summary` for text-only LLMs.
- **Strict Input Image Validation**: `extract_design_tokens`, `image_to_css_gradient`, and `check_image_contrast` explicitly validate source image readability instead of silent fallback.
- **Unit Testing Suite**: Added `test/tool-consistency.test.mjs` covering tokenization, gradient generator, and PWA suite.

# 📦 @goodandready/dsh-image-gen

<div align="center">

<h3>Comprehensive Visual Generation & Image Processing Suite for DeepSeek Harness</h3>

<p align="center">
  <a href="https://www.npmjs.com/package/@goodandready/dsh-image-gen"><img src="https://img.shields.io/npm/v/@goodandready/dsh-image-gen.svg?style=for-the-badge&color=6366f1&labelColor=1e1b4b" alt="npm version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/GooDAnDReaDY/dsh-image-gen.svg?style=for-the-badge&color=10b981&labelColor=064e3b" alt="license"></a>
  <a href="https://github.com/topics/dsh-plugin"><img src="https://img.shields.io/badge/DSH-Plugin-8b5cf6.svg?style=for-the-badge&labelColor=2e1065" alt="DSH Plugin"></a>
  <a href="https://nodejs.org"><img src="https://img.shields.io/badge/Node-20%2B-f59e0b.svg?style=for-the-badge&labelColor=451a03" alt="Node version"></a>
</p>

<p align="center">
  <a href="https://goodandready.app/"><img src="https://img.shields.io/badge/All_Author_Projects-goodandready.app-ff4500.svg?style=for-the-badge&logo=rocket&logoColor=white&labelColor=1a1a2e" alt="All Projects"></a>
</p>

<p align="center">
  <a href="README.md"><b>🇬🇧 English</b></a> •
  <a href="README.ru.md"><b>🇷🇺 Русский</b></a> •
  <a href="README.zh.md"><b>🇨🇳 中文说明</b></a>
</p>

<table align="center">
  <tr>
    <td align="center">
      ⭐ <strong>If you like this plugin, please star it on GitHub</strong> — it shows me that the plugin is useful to you and motivates me to keep developing it.
      <br><br>
      🐛 <strong>If you find a bug or would like to request a feature</strong>, open a GitHub issue in any language — I will review your proposal and implement useful suggestions in a future plugin version.
    </td>
  </tr>
</table>

</div>

---

## 🚀 Updates v0.10.26: Architecture Decomposition & Repository Sanitization (#235, #238, #239)
* **Architecture & Modular Decomposition (#239)**: All server modules in `lib/` now strictly meet the <= 600 line threshold: extracted `lib/tools/generation-pack.js` (74 lines, reduces `lib/tools/generation.js` to 547 lines), `lib/history.js` (93 lines), and `lib/attachment-helper.js` (82 lines, reduces `lib/index.js` to 557 lines). Client codebase modularized across 15 sub-modules in `src/client/*` (all <= 337 lines).
* **Repository Sanitization (#235)**: Internal agent workflow files (`AGENTS.md`, `index.md`) fully untracked from Git and excluded via `.gitignore` and `.gitattributes`.
* **Theme Parity Completed (#238)**: Full verification and closure of zero-standalone-color rule across all Web UI surfaces with native `--dsw-alias-*` variables and `color-mix(...)` state tints.
* **Package Integrity**: Added canonical `README.ru.md` and `README.zh.md` to npm package `files` allowlist.

## 🚀 Updates v0.10.25: Theme Color Parity, Responsive Mockups, Patterns & Spritesheets (#173, #177, #178, #238)
* **100% Theme Color Parity (#238)**: Completely replaced all hardcoded `rgba(...)` and hex color literals in the Web UI (`src/client/10-css.js`, `src/client/80-gallery.js`) with native DSH theme variables (`--dsw-alias-*`) and dynamic `color-mix(...)`. Badges, alerts, and modal overlays automatically adapt to light and dark themes with zero hardcoded values.
* **Responsive Multi-Device Mockup Generator (`generate_responsive_mockups`, #173)**: Single product prompt generates coherent Mobile (9:16), Tablet (3:4), and Desktop (16:9) viewports in parallel via `asyncPool` concurrency limit (3). Interactive toolview with tabbed preview navigation.
* **Seamless Pattern Generator (`generate_seamless_pattern`, #178)**: Automated tileable background texture generation with periodic boundary condition checks and CSS tiling preview.
* **2D Spritesheet Generator (`generate_spritesheet`, #177)**: Produces horizontal animation strips with CSS keyframe generator and multi-frame SVG previews for 2D game dev and web UI animations.
* **Client Modular Source Build (#244)**: Decomposed monolithic `lib/client.js` into 15 structured fragments under `src/client/*` with automated build runner `scripts/build-client.mjs`. Preflight check `FAIL=0`, 179/179 automated tests passing.

## 🚀 Updates v0.10.24: Quality Block — Publication Boundary, Settings Status, Theme Colors & Module Split (#235–#242)
* **Publication Boundary**: Added `.gitattributes` with `export-ignore` for `AGENTS.md`, `index.md`, `docs/`, and `.gitea/` so GitHub source archives and `git archive` no longer ship internal workflow files.
* **Settings Status Fallback**: Corrected provider/config status handling in the Settings Card so partial/unknown states no longer show a false “unavailable”.
* **Design-System Alignment**: Renamed residual `fal-` CSS class prefixes to the `ig-` system and bound colors to DSH theme variables via `var(--dsw-alias-*, <fallback>)`.
* **Sensitive File Hardening**: History, cache meta/data, and spend-meter writes now enforce `0600` permissions after write.
* **Dead Code Removal & Module Split**: Removed unused `listCuratedStyles`; split oversized server modules — `providers.js` utils extracted to `provider-utils.js`, `processing.js` into `processing-basic.js` + `processing-advanced.js`. Client file split is tracked separately (#244).

## 🚀 Updates v0.10.23: In-App Auto-Updater, Settings Synchronization, Active Probes & Language Purity (#232)
* **One-Click In-App Auto-Updater**: Direct 1-click update support inside the plugin Settings Card (`UpdaterSection`) backed by `/api/dsh-image-gen/update`. Fetches the npm registry for release manifests, verifies semver differences, and securely triggers `dsh plugin add @goodandready/dsh-image-gen@latest` restricted to loopback and private LAN connections.
* **1:1 Settings Synchronization**: Fully synchronized host `Config` schema in `lib/index.js` with client UI fields (`lib/client.js`), exposing `autoEnhancePrompt` and `defaultStylePreset` under the `✨ Enhancer` tab.
* **Active Diagnostic Probes**: Added real HTTP network probes in `testProviderConnection` for Replicate (`/v1/models`), Google Gemini (`/v1beta/models`), and ByteDance Seedream with timeout protection and live roundtrip latency tracking.
* **Strict Multi-Language Compliance**: Pure standard `en` and `zh` localization bundles embedded in core package; modularized Russian language support via `goodandready/dsh-russian-lang` per DSH plugin guidelines. Exactly 0 Cyrillic characters in product code (`lib/`).
* **WAI-ARIA Accessibility Hardening**: Enhanced tab navigation and input form validation with `role="tablist"`, `role="tab"`, `aria-selected`, `aria-controls`, `role="tabpanel"`, `aria-describedby`, and `role="alert"`.

## 🚀 Updates v0.10.22: Referential Stability & React Error #185 Infinite Loop Fix (#230)
* **Settings Card Referential Stability**: Resolved React Error #185 (`Maximum update depth exceeded`) in `FalSettingsCardController` and `CardForm.prototype.bind`. Store snapshots are referentially cached during render cycles (`Object.is(prev, next) === true`), completely preventing infinite re-render loops in React 18 / `useSyncExternalStore`.
* **Deep DSH Store Integration**: Added seamless runtime integration with `@deepseek-ai/dsh-client-store` (`runtime.createSnapshotStore`) paired with a robust standalone snapshot caching fallback.
* **Automated Regression Test Suite**: Added dedicated referential identity test in `test/client-syntax.test.mjs` verify