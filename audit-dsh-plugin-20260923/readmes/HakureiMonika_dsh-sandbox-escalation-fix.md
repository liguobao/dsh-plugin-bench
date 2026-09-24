# dsh-sandbox-escalation-fix (DSH 0.1.6-alpha.2 supported, Win & Linux & macOS)

English | [简体中文](README.zh.md)

> [!IMPORTANT]
> This is an independent community plugin. It is not published, maintained, or endorsed by DeepSeek, and it does not modify DeepSeek Harness core packages.

> [!CAUTION]
> DSH `0.1.6-alpha.2` has significantly mitigated the issue addressed by this plugin. In testing, a model may still fail its first tool call because of unsuitable sandbox-escalation arguments, but it will usually adjust those arguments after receiving the error and eventually complete the call successfully. Escalation schemas remain registry-global and are still not narrowed according to each Session's current permissions, so the underlying cause has not been fully removed. However, users who can tolerate a small number of retries and some additional token usage may now find the official behavior acceptable. **Users should try the official behavior first and install this plugin only when the remaining retries, overhead, or instability are unacceptable.**
>
> **Given the current effectiveness of the official improvements, this plugin may stop being maintained after the next official release. If you still need this plugin to be maintained at that time, please proactively open an issue, and the developer will respond as soon as possible.**

> Currently supported:<br>
> Latest supported DSH version: `0.1.6-alpha.2` (full list in [Compatibility](#compatibility))<br>
> Desktop version: `2.0.3`<br>
> OS: `Windows` & `Linux`  & `macOS` (theoretically supported, not yet tested)
>  
>  If there is any platform that has not yet been adapted and needs compatibility, please submit an issue.<br>
> *If it's useful, please stars let more people can see it~ Thanks♪(･ω･)ﾉ*

**dsh-sandbox-escalation-fix** is a zero-configuration compatibility plugin that directly resolves the issue of third-party models like GPT failing to call tools such as `bash`, `pwsh`, `write`, and `edit` under DSH All Access, resulting in repeated retries due to incorrect sandbox escalation parameter prompts.

If you've encountered the following errors, this plugin is designed for them:

```text
Error: invalid justification: expected a non-empty sentence
Error: sandbox escalation to "danger-full-access" is not strictly wider than this call's current "danger-full-access" mode
Error: sandbox escalation to "workspace-write" is not strictly wider than this call's current "danger-full-access" mode
```

<details>
  <summary>Some minor explanations</summary>

  > DSH `0.1.1-rc.2` focuses on image handling: the DeepSeek adapter prefers Files API uploads, reuses uploaded files, and automatically resizes or converts images for model requirements. The sandbox escalation, Bash, Pwsh, ToolRuntime, and approval implementations used by this plugin are unchanged from `0.1.1-rc.1`, so rc.2 neither fixes the issue described here nor requires a plugin logic change.<br> <br>DSH `0.1.2-alpha.1` improves composition-level advertising: Bash, Pwsh, Write, and Edit omit escalation fields when no confining sandbox backend is mounted. DSH `0.1.2-alpha.2` through `0.1.3-alpha.1` do not add session-aware schema projection. The published sandbox package still describes schemas as registry-global and the effective mode as per-call truth, keeps `workspace-write` and `danger-full-access` in the global target vocabulary, and checks strict widening during execution. `ctx.tools.schemas(scope)` and `sdkSchemas(scope)` still have no Session input, while `approval=never` adds a model instruction without removing escalation fields. Native tool calling and PTC Mode consume the same registered definition, so the issue addressed by this plugin remains possible. Alpha.4 replaces `Session.events` with `seq`, `eventAt()`, and `snapshotEvents()`; alpha.5 fixes application upgrade migration and session-title restoration. The `0.1.3-alpha.1` Tool Registry, Sandbox escalation, Sandbox Policy, Approval, and Bash sources are byte-for-byte identical to `0.1.2-rc.1`; FS changes only standardize `FS_NOT_OBSERVED` diagnostics, and the Session persistence/Agent creation breaking changes do not affect this plugin's runtime hooks.<br> <br>The complete public `0.1.5-rc.1` npm package set is the current integration baseline. All 40 tests and the TypeScript build pass against the real Agent, ToolRuntime, Session Projection, Sandbox Policy, Approval, LLM, Scope, Session, and System Prompt contracts; Session V3, removal of `ctx.agent`, and the Inbox API changes do not affect this plugin. `0.1.5-alpha.2` adds the `deliverables/presented` and `subagent/catalog` session event names and makes the `read`/`write`/`edit` system prompts scope-aware, and `0.1.5-rc.1` is byte-for-byte identical to `0.1.5-alpha.2` across all 15 plugin-relevant published packages, so the escalation schema contract is unchanged.<br> <br>Plugin `0.1.1-desktop.2` includes compatibility with DSH Desktop `2.0.3`. Desktop 2.0.3 deliberately limits its CommonJS package-manifest overlay to direct Profile anchors, so a third-party plugin cannot read host `@deepseek-ai/dsh-*/package.json` files from its own module. When all checked manifests are hidden uniformly, this plugin uses its existing strict runtime tool-contract validation instead. Partially readable manifests, mixed versions, malformed manifests, and incompatible tool definitions still fail closed.<br> <br>Linked and external plugin layouts are also supported. If `link:`, a workspace symlink, or an external plugin directory places the plugin outside the host dependency tree, the compatibility gate may read the complete DSH manifest set from the host working directory. One candidate root must provide the entire checked package set: partial roots, cross-root package mixing, malformed manifests, and non-resolution loader errors still fail closed. `DSH_HOME` is not treated as a dependency root because it stores Harness configuration and Profile data rather than a stable Node.js package tree.
</details>

## Contents

- [What It Does](#what-it-does)
- [The Problem It Solves](#the-problem-it-solves)
- [Before and After](#before-and-after)
- [Compatibility](#compatibility)
- Quick Start & Installation
  - [Release ZIP installation](#release-zip-installation)
    - [Install into the default Web Profile](#install-into-the-default-web-profile)
    - [Install into another Profile](#install-into-another-profile)
    - [Build the Release ZIP](#build-the-release-zip)
  - [Command-line installation](#command-line-installation)
  - [Manual Windows Installation](#manual-windows-installation)
- Upgrade & Maintenance
  - [Upgrade an existing installation](#upgrade-an-existing-installation)
    - [GitHub commit installation](#github-commit-installation)
    - [Manual Web Profile installation](#manual-web-profile-installation)
- [Uninstall](#uninstall)
- [Why This Plugin](#why-this-plugin)
- [Verification, Behavior, and Plugin Cooperation](#verification-behavior-and-plugin-cooperation)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [Development](#development)
- [License](#license)

## What It Does

This plugin makes DeepSeek Harness show the model **only the sandbox escalation options that the current session can actually use**.

In an All Access session (`danger-full-access` + `never`), the stock DSH tools still advertise `sandbox_permissions` and `justification` on `bash`, `pwsh`, `write`, and `edit`. But in that state:

- the session is already at the highest sandbox mode, so no wider mode exists;
- the approval policy is `never`, so every escalation request is rejected.

When a model fills in those parameters, the call fails before it runs. The model may then retry with different values and get stuck in a loop.

This plugin projects the model-visible tool schema per session, based on the live Sandbox Mode and Approval Policy. It also adds a minimal execution-time fallback: it handles redundant same-mode requests and, under `workspace-wr