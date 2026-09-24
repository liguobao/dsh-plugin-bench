<p align="center">
  <img src="./docs/images/dsh-harbor-logo.png" alt="DSH Harbor" width="120" />
</p>

<h1 align="center">DSH Harbor</h1>

<p align="center">
  <strong>Evidence-first governance for the DeepSeek Harness plugins already installed on your machine.</strong><br />
  <sub>Capability Inventory &bull; Declared vs Detected &bull; Runtime Attribution &bull; Conflict Detection &bull; Version Drift &bull; Change Timeline &bull; Upgrade Preflight</sub>
</p>

<p align="center">
  <sub>npm: <code>@zseven-w/dsh-harbor</code> &middot; Current plugin release: <code>0.1.0-rc.3</code> &middot; Tested with DSH <code>0.1.5-rc.2</code></sub>
</p>

<p align="center">
  <a href="./README.md"><b>English</b></a> &middot; <a href="./README.zh.md">简体中文</a> &middot; <a href="./README.zh-TW.md">繁體中文</a> &middot; <a href="./README.ja.md">日本語</a> &middot; <a href="./README.ko.md">한국어</a> &middot; <a href="./README.fr.md">Français</a> &middot; <a href="./README.es.md">Español</a> &middot; <a href="./README.de.md">Deutsch</a> &middot; <a href="./README.pt.md">Português</a> &middot; <a href="./README.ru.md">Русский</a> &middot; <a href="./README.hi.md">हिन्दी</a> &middot; <a href="./README.tr.md">Türkçe</a> &middot; <a href="./README.th.md">ไทย</a> &middot; <a href="./README.vi.md">Tiếng Việt</a> &middot; <a href="./README.id.md">Bahasa Indonesia</a>
</p>

<p align="center">
  <a href="https://github.com/ZSeven-W/dsh-harbor/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/ZSeven-W/dsh-harbor/ci.yml?label=CI" alt="CI" /></a>
  <a href="https://github.com/ZSeven-W/dsh-harbor/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ZSeven-W/dsh-harbor?color=64748b" alt="License" /></a>
</p>

<br />

<p align="center">
  <img src="./docs/images/dsh-harbor-overview.png" alt="DSH Harbor light-theme overview — runtime evidence, route attribution, versions, and scan changes" width="100%" />
</p>
<p align="center"><sub>The Harbor settings page in DSH light mode — live runtime registries, profile-scoped attribution, local version truth, and the change baseline.</sub></p>

## Why DSH Harbor

DSH plugins run in the host's Node realm with the same local permissions as DSH itself. Harbor does not pretend this can be solved with a score or a badge: it keeps a read-only, evidence-backed ledger of what is installed, what each plugin declares, what its code and live host actually expose, where plugins collide, and what changed since the previous scan.

<table>
<tr>
<td width="50%">

### 🔎 Capability Inventory

Harbor scans every installed third-party bundle across DSH profiles and reports a fixed 13-capability vocabulary. Source findings carry `file:line` evidence; manifest, filesystem, and runtime facts state their origin explicitly.

</td>
<td width="50%">

### 🤝 Declared vs Detected

Plugins may declare `dsh.capabilities` in `package.json`. Harbor reconciles the declaration against detection, exposes missing and unknown ids, and fails closed on malformed declarations instead of letting one bad package break the whole report.

</td>
</tr>
<tr>
<td width="50%">

### 🟢 Runtime Attribution

Inside a live DSH host, Harbor enumerates tools, providers, and routes, then attributes them only to plugins installed in the active profile. Missing host registries remain visible as coverage gaps rather than empty proof.

</td>
<td width="50%">

### ⚠️ Conflict Detection

The ledger finds same-profile tool names, route prefixes, provider ids, client-module ids, and order-sensitive message hooks. A quoted route used by a client does not make that client the route owner.

</td>
</tr>
<tr>
<td width="50%">

### 🧭 Two Version Axes

Cross-profile drift is local and always offline. The optional upstream check is separate, explicit, registry-aware, credential-redacted, and cached for six hours. `link:` and `file:` installs never masquerade as current registry versions.

</td>
<td width="50%">

### 🕰️ Change Timeline

Snapshots track additions, removals, version transitions, profile moves, capability changes, and claim changes. Even two artifacts exchanging profiles are reported as concrete per-profile transitions.

</td>
</tr>
<tr>
<td width="50%">

### 🛫 Upgrade Preflight

Before you move DSH to a new version, Harbor installs that exact version into its own cache, then import-probes every installed plugin against it in a child process, checks `dsh.client.inject` ids against the target's client module graph, and checks host peer ranges. The answer is per profile: boots after the upgrade, or blocked — by which plugin, with the real link-time error.

</td>
<td width="50%">

### 🧷 One Settings Check

The only user-settings check with a known upgrade casualty: when a built-in agent preset is renamed (`code` → `ptc` in DSH 0.1.2) the stored `agent-presets.default` is not migrated and every new session fails. Preflight reports the stale value against the target's preset list.

</td>
</tr>
</table>

## How it works

```text
~/.dsh/profiles/*
  ├─ installed package + provenance
  │    registry artifact | link: working tree | file: snapshot
  ├─ declared
  │    package.json + cordis.patch.yml
  ├─ static
  │    bounded source scan + file:line evidence
  ├─ runtime (when loaded inside DSH)
  │    tools + providers + routes + profile-scoped attribution
  ├─ versions
  │    local cross-profile drift + opt-in registry check
  └─ snapshot
       additions + removals + version/profile/capability/claim changes
```

The CLI and the settings page consume the same scan core. The default path is offline. Only `harbor scan --check-updates`, `harbor preflight`, or the panel's **Check for updates** / **Upgrade preflight** actions contact a registry.

### Upgrade preflight

```sh
harbor preflight --list                 # dist-tags, recent versions, locally cached host trees
harbor preflight --dsh next             # or a concrete version: --dsh 0.1.5-rc.2
harbor preflight --dsh 0.1.5-rc.2 --json
```

What runs, in order:

1. The target is resolved (a dist-tag needs one registry request) and `@deepseek-ai/dsh@<version>` is installed into `<state dir>/hosts/<version>` with `npm install -g --prefix`. A completed install is reused; the global npm prefix and your profiles are never written.
2. Every installed third-party plugin's server entry is imported in a fresh `node` child. A `module.register` resolve hook rewrites `@deepseek-ai/*` imports to the target tree, so the plugin links against the version under evaluation while its own dependencies keep resolving from its real install. Missing packages and removed exports fail at link time and are reported verbatim — the DSH loader is fail-loud, so one such plugin blocks the whole profile.
3. `dsh.client.inject` / `external` ids are checked against the packages in the target that declare a web client module (DSH ≥ 0.1.5 skips unknown ids silently, so this never errors on its own). Host peer ranges are matched with npm's prerelease rule.
4. `agent-presets.default` from `settings.yaml` is checked against the target's built-in presets.

Verdicts are per plugin (**blocks boot** / **loads** / **unresolvable** / **not probed**) and per profile; peer-range and dead-inject findings are advisories and never change a verdict. *Unresolvable* means the plugin's own dependency could not be found — a packaging problem, not a host problem. Exit code 3 means at least one profile would not boot. Node ≥ 20.6 is required for the resolve hook.

Outside a profile — in CI, or for a package you have not installed — name the subjects explicitly:

```sh
harbor preflight --dsh next --plugin .                        # this repository (build it first)
harbor preflight --dsh next --pack @scope/some-plugin@1.2.3   # fetched from the registry, deps installed with scripts disabled
```

### Contract diff between two DSH versions

```sh
harbor host-diff --from 0.1.1-rc.2 --to 0.1.5-rc.1
```

Installs both versions into the cache and reports what a plugin could have de