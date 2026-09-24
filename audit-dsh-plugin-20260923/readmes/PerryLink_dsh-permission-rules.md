<div align="center">

# 🛡️ dsh-permission-rules
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-permission-rules` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-permission-rules)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-permission-rules?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-permission-rules?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-permission-rules/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-permission-rules)

**Claude Code-style declarative permission rules for DeepSeek Harness.**

*Rules decide what is known. A reviewer model decides what is not.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-permission-rules.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-top-rated.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-permission-rules/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-permission-rules/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-permission-rules?label=version)](https://github.com/PerryLink/dsh-permission-rules/releases)
[![npm version](https://img.shields.io/npm/v/dsh-permission-rules)](https://www.npmjs.com/package/dsh-permission-rules)
[![npm downloads](https://img.shields.io/npm/dm/dsh-permission-rules)](https://www.npmjs.com/package/dsh-permission-rules)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (adapted 2026-09-22, full gate chain): its plugin config is the live settings contract — every field is declared `.volatile()`, the Loader hands `apply` a live reference per field, and a saved edit is committed into the running references WITHOUT remounting the plugin, with out-of-range values refused by the schema before anything is written. A host whose Schemastery predates `volatile()` (before 3.18.3) still mounts and runs this plugin — the fields simply stay ordinary values and the live config form is unavailable — because the marker is applied through a capability probe rather than assumed. `Session.append` on this line still cannot stamp the `ignorable` marker (its third argument is the surface-intent bag, and the envelope field survives for stored-log reads only), so the whole `0.1.7-alpha` line is pre-checked as unmarked and session-log audit stays disabled by default; the earlier `0.1.5-rc.2` (adapted 2026-09-09) and `0.1.3-alpha` lines keep the same surface-only append signature. Those lines' log migrations refuse unclassified plugin events even when marked, so `strip` v1 audit rows before a `0.1.3-alpha` host opens the log and v2 audit rows before a `0.1.5-alpha` host migrates it (native v3 logs only need `repair`). |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (host + web settings client) |
| Model | Any (deny/ask reasons surface through tool results) |

## What you get

`dsh-permission-rules` puts an ordered **`allow` / `deny` / `ask`** rule list in front of every tool call on the `tools/pre-execute` waterfall — deterministic, instant, auditable, and written by you in plain YAML:

- **`deny`** blocks the call; the rule's `reason` becomes the model-visible error.
- **`ask`** rides the official approval seam (mount `dsh-auto-review` for a second-model answerer, or a human answers; with neither, the harness fails closed).
- **`allow`** (and no-match) strictly delegates via `next()` — downstream listeners are never short-circuited.

Every hit **and** every passthrough is audit-logged as a `permissionRules/decision` session event (log-only — nothing extra is injected into the model context).

- **Rich matching** — tool-name globs (including `mcp__*`), agent-identity selectors (`main` / `subagent` / `preset:*`), argument key/value globs **or** regexes (with `!pattern` negation and an `absent` key dimension), workspace-relative path globs at **any nesting depth**, `when` host conditions (env vars, platform), and **shell command decomposition** (`argv`: command word, argument tokens, pipeline signature) for token-precise command matching.
- **Built-in high-risk baseline** — a shipped deny/ask ruleset (destructive commands, privilege escalation, download-and-execute, sensitive paths) enabled by default and appended after user rules so a nearer user rule can override it; toggle with `builtin.enabled`.
- **Hierarchical rule files** — optional `searchUp` merges every `.dsh/rules.yaml` from the session cwd to the filesystem root, nearest first.
- **Dry-run rollout** — `enforce: false` audits what the policy *would* do while passing every call through.
- **Hot reload** — Chokidar watch with debounce; a broken edit keeps the previous rules, never crashes. On a WSL host, or for a rule file under `/mnt/<drive>`, the watch switches to polling because native change events are unreliable there.
- **Fail loud** — invalid YAML, unknown actions/fields, bad globs/regexes, backtracking-prone patterns, or more than `maxRules` rules fail the load.

## Rule syntax

```yaml
# <project>/.dsh/rules.yaml
rules:
  - match: { tools: [bash, pwsh], params: { command: "git push*" }, paths: ["**/secrets/**"] }
    action: deny
    reason: "No pushes from protected paths"

  - match: { tools: [edit, write] }
    action: ask
    reason: "File writes need confirmation"
```

- **Match dimensions** — `tools` (globs, incl. `mcp__*`), `agents` (`main` / `subagent` / `preset:<name>`; unknown identity never matches — fail closed), `params` (key/value globs or regexes, `!pattern` negation, `absent` key dimension), `paths` (workspace-relative globs extracted at any nesting depth), `when` (`env` var globs/regexes + a closed `platform` list), and `network` (`domains` / `ips` / `ports` / `schemes` — globs, wildcards, CIDRs, port ranges).
- **Actions** — `allow` / `deny` / `ask`, evaluated in file order, first match wins.
- **Rule metadata** — `enabled: false` (visible but inert), `description`, `tags`; unknown fields fail the load.
- **Schema** — a JSON Schema ships at [docs/rules-format.schema.json](docs/rules-format.schema.json) (editor completion via `# yaml-language-server: $schema=...`); the full vocabulary and a 5-rule security baseline live in [docs/rules-format.en.md](docs/rules-format.en.md).

## Network policy

A Codex-style **process-level network policy**: shell subprocess traffic flows through a built-in local **HTTP/CONNECT proxy**, and every connection is decided by ordered network rules or by three modes mapped onto the official sandbox presets:

- **`deny-all`** — the read-only sandbox preset: block all outbound.
- **`whitelist`** — the workspace-write preset: allow listed targets, `unlisted: ask` (or `deny`) for the rest.
- **`allow-all`** — the danger-full-access preset: allow everything.
- **`auto`** (default) — follows the sandbox preset; on hosts without the sandbox-policy service it resolves to `autoFallback` (`allow-all`).

- **Matching** — `match.network` with `domains` / `ips` / `ports` / `schemes` (globs, wildcards, CIDRs, port ranges; numeric YAML ports are accepted). URL-candidate extraction on the `tools/pre-execute` hot path fires on web-tool arguments and URLs embedded in bash/pwsh command text; loopbac