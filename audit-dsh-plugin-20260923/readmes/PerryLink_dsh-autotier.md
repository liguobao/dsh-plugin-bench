# dsh-autotier

[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-autotier)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-autotier/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-autotier)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-autotier.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19.0%20%7C%7C%20%3E%3D24.0.0-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-autotier/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-autotier/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-autotier?label=version)](https://github.com/PerryLink/dsh-autotier/releases)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-autotier?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-autotier?ref=badge)

**English** | [简体中文](README-zh.md) | [Español](README-es.md) | [Português](README-pt.md) | [हिन्दी](README-hi.md)

Automatic model-tier routing for DeepSeek Harness: one user instruction enters,
one tier decision comes out — no manual model switching.

Complex intent (architecture, planning, debugging, multi-step engineering) is
planned on the **strong** tier and then implemented on the **cheap** tier.
Simple intent (questions, retrieval, batch chores, daily work) is designed and
implemented on the **cheap** tier directly. While the cheap tier executes,
high-risk tool calls are denied by a deterministic guard, and repeated failures
escalate to the strong tier with a TTL fallback.

- **Official repository**: <https://github.com/PerryLink/dsh-autotier>
- **npm**: `dsh-autotier` (bare, unscoped)

## Compatibility

| Harness | Status |
|---|---|
| `@deepseek-ai/dsh` `0.1.2-rc.1` | no longer supported; that line predates the `SettingsForms` contract this plugin now targets |
| `@deepseek-ai/dsh` `0.1.5-rc.2` | no longer supported; the `settings.register` / `settings/updated` contract it exposes was removed upstream |
| `@deepseek-ai/dsh` `0.1.6-alpha.2` | no longer supported; same removal, first line to ship `SettingsForms` |
| `@deepseek-ai/dsh` `0.1.7-alpha.2` | **required**; verified against the matching checkout (`typecheck`) and the published packages (`typecheck:ci`, 214 tests) |
| `@deepseek-ai/cordis` `^4.0.3`, `@deepseek-ai/cosmokit` `^1.8.4`, `@deepseek-ai/schemastery` `^3.18.3` | peer baseline |

Peer ranges name all published lines explicitly (`>=0.1.2-rc.1 <0.2.0 || >=0.1.5-alpha.1 <0.2.0 || >=0.1.6-0 <0.2.0 || >=0.1.7-0 <0.2.0`), because a semver range whose only prerelease
comparator sits on an earlier version tuple does not admit a later alpha.
They are refreshed per published wave. The declared range is deliberately wider
than the verified one: it documents what the manifest accepts, not what has been
tested.

**This release is a breaking adaptation.** The `0.1.6`-generation harness
removed the settings *provider* seam this plugin was built on: the
`@deepseek-ai/dsh-settings-file` package is gone, `ctx.settings` is now
`SettingsForms` (a schema→form projector, with no `register`), and
`settings/updated` no longer exists. There is no shared surface that lets one
plugin observe another plugin's settings document, so no version of this plugin
can support both contracts at once. Configuration now flows through the host's
volatile-config mechanism, and the per-session routing mode — the setting that
actually changes behaviour at runtime — is unchanged.

The plugin is host-plane only. It needs no agent preset of its own: the host
row applies to every session. A one-line prompt section in *your* preset is
optional and only makes the router's decisions visible to the model (see
[Install & uninstall](#install--uninstall)).

## What you get

- **Intent gate** — every turn is classified from deterministic signals
  (message text, tool names, image presence, conversation length). The
  zero-token rule layer decides when it is confident; only a low-confidence turn
  calls the cheap judge model, and never on a cooldown.
- **Tier landing on the official seam** — the decision is applied on the
  `agent/request` waterfall by returning a replacement provider/model/effort
  triple. Sampling scalars the session already chose (`temperature`, `maxTokens`,
  `stop`) are preserved.
- **Plan-mode handoff** — a complex instruction enters plan mode on the strong
  tier; leaving plan mode drops back to the cheap tier for implementation.
- **High-risk guard** — while the cheap tier executes, destructive commands
  (`rm -rf`, `sudo`, `mkfs`, `git push --force`, credential-file writes, …) are
  denied with a corrective message telling the model to escalate instead.
- **Failure escalation** — repeated failures (optionally same-signature) raise
  the tier for a TTL; a model/route failure walks the configured fallback chain.
- **Manual escape hatches** — `/tier auto|strong|cheap|off` and the
  `tier_status` / `tier_route` tools. Setting `routingMode: delegated` (or
  `/tier off`) stops routing for a session that must keep its own model.
- **`ctx.autotier` service** — a small read surface (`status`) plus the
  `autotier/route` veto waterfall and `autotier/tier-changed` event, so other
  plugins can observe or override a decision.

## Quick start

```bash
dsh plugin --profile web add dsh-autotier
npm i -g dsh1024
dsh1024 plugin --profile web add dsh-autotier
```

Then start (or restart) the harness. The row is appended to your profile's
`cordis.patch.yml`; routing starts on the next turn with no further setup.

## Install & uninstall

**npm channel**

```bash
dsh plugin --profile web add dsh-autotier
npm i -g dsh1024
dsh1024 plugin --profile web add dsh-autotier
```

**git channel**

```bash
dsh plugin --profile web add "github:PerryLink/dsh-autotier#main"
git clone https://github.com/PerryLink/dsh-autotier.git
cd dsh-autotier && pnpm install && pnpm run build
dsh plugin --profile web add .
```

**Optional preset prompt section.** The router works without it. To let the
model know which tier it is running on, add one row to *your* agent preset
(`docs/preset-row.md` has the exact block):

```yaml
- insert:
    - id: autotier-prompt
      name: '@deepseek-ai/dsh-system-prompt'
      # sections: [...]  — see docs/preset-row.md
```

**Uninstall**

```bash
dsh plugin --profile web remove dsh-autotier
```

The row, its command, its tools and its listeners are all removed with the
plugin. Configuration a user saved through the Plugins page lives in the active
profile patch and belongs to that profile, not to this plugin; removing the row
leaves it there untouched.

## Configuration

Every key is validated at load time; an invalid value fails loudly instead of
silently disabling routing. `cordis.patch.yml` in this repository documents the
same keys inline.

| Key | Default | Meaning |
|---|---|---|
| `tiers.strong.provider` | `deepseek-official` | Provider for the planning/review tier. |
| `tiers.strong.model` | `deepseek-v4-pro` | Catalog id of the strong model. |
| `tiers.strong.effort` | `high` | Adapter vocabulary `off` \| `low` \| `high` \| `max`. |
| `tiers.strong.followSession` | `false` | `false` = this tier's effort overrides the session's. |
| `tiers.strong.fallback` | `[]` | Ordered provider/model landings when the tier is unavailable. |
| `tiers.cheap.provider` | `deepseek-official` | Provider for the implementation tier. |
| `tiers.cheap.model` | `deepseek-flash` | Catalog id of the cheap model. |
| `tiers.cheap.effort` | `low`