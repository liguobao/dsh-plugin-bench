<p align="right">
  <strong>English</strong> · <a href="./README_ZH.md">简体中文</a>
</p>

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="dsh-auto-mode lets routine DeepSeek Harness work flow while stopping risky actions">
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@nanmicoder/dsh-auto-mode"><img src="https://img.shields.io/npm/v/@nanmicoder/dsh-auto-mode.svg" alt="npm version"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/npm/l/@nanmicoder/dsh-auto-mode.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/DeepSeek%20Harness-0.1.5--rc.2-202724" alt="See installation instructions for exact host compatibility">
</p>

## Why Auto?

Coding agents need broad access to build, test, and inspect a project without stopping every few steps. But DeepSeek Harness currently leaves a sharp choice: restricted modes interrupt normal development, while Full access removes approval entirely.

`dsh-auto-mode` adds the missing middle ground. Routine project work runs directly inside the official `workspace-write` sandbox, only semantic risks outside that boundary are classified using the current DSH model and the direct user's instructions, genuine ambiguity asks once, and destructive access to critical paths is denied before execution.

> [!IMPORTANT]
> Plugin `0.1.10` recommends Harness `0.1.5-rc.2`. We prioritize verified RC releases. Updating this plugin does not upgrade Harness: use an exact host below with a coherent DSH dependency cohort.

| Harness host | Plugin | Pairing |
| --- | --- | --- |
| `0.1.5-rc.2` | `0.1.10` | Recommended |
| `0.1.5-rc.1` | `0.1.10` | Retained compatibility |
| `0.1.2-rc.1` | `0.1.10` | Retained compatibility |
| `0.1.2-alpha.5`, `0.1.2-alpha.3`, `0.1.2-alpha.2` | `0.1.10` | Only these previously verified historical releases |
| `0.1.6-alpha.*` | Unsupported | Requires separate adaptation; do not install this plugin |
| Other versions | Undeclared | Require full host verification first |

Historical Alpha support does not imply support for current or future Alphas. `latest`, `next`, and `alpha` are mutable tags, not compatibility promises. [compatibility.json](./compatibility.json) defines the exact matrix; see [VALIDATION.md](./VALIDATION.md) for acceptance results.

### Upgrade and startup recovery

Plugin `0.1.9` rejects Harness `0.1.5-rc.2` in its own version guard; upgrade to `0.1.10`. On `0.1.6-alpha.2`, Harness also reserves `auto`, so the old plugin's static preset prevents startup. Renaming only the YAML key does not update the mode the plugin recognizes and is not a complete fix.

On an unsupported host, remove the plugin from the affected profile in an external terminal to restore startup (`web` below; substitute your TUI, headless, or custom profile name):

```sh
dsh plugin --profile web remove @nanmicoder/dsh-auto-mode
```

Unsupported versions still fail explicitly; the plugin never silently skips its approval policy. Before downgrading Harness, stop it, back up DSH data, and verify the older host can read existing sessions. Do not upgrade or downgrade Harness from a session running inside it.

### npm

Check the actually running `dsh --version`, then install the plugin:

```sh
dsh plugin --profile web add @nanmicoder/dsh-auto-mode@0.1.10
```

The example pins the plugin version to avoid mutable-tag surprises. Check that your host appears in the matrix before updating. Git source installs build through `prepare` and require development dependencies and enabled install scripts. Registry packages already contain compiled output.

### Build from source

```sh
git clone https://github.com/NanmiCoder/dsh-auto-mode.git
cd dsh-auto-mode
pnpm install
pnpm build
dsh plugin --profile web add .
```

Run `pnpm build` again after changing the source. The local plugin install remains linked to this checkout.

Validate the composed profile and start DSH:

```sh
dsh --profile web --dump-config
dsh web
```

Refresh the Web UI, select **Auto** between Workspace Write and Full access, and acknowledge the risk notice. Replace `web` with another profile name when that is the profile you run.

The Web client registers its copy with DSH's official locale service. English keeps the **Auto** product label; Chinese shows **自动审批**. Switching the DSH language updates the permission menus, active-mode control, General-settings selector, `/permission` picker description, and acknowledgement dialog without a restart.

## Permission modes

| Mode | File sandbox | Approval | Auto policy |
| --- | --- | --- | --- |
| Read Only | `read-only` | ask | inactive |
| Workspace Write | `workspace-write` | ask | inactive |
| **Auto** | `workspace-write` | ask | **active** |
| Full access | `danger-full-access` | never | inactive |

Ordinary Auto work stays inside Workspace Write. Only an explicit one-shot widening may be approved automatically:

| Decision | Typical effect |
| --- | --- |
| **Allow** | unfamiliar sandboxed Bash/PowerShell, routine dependency installation, local Git commits, project work, builds, tests, type checks, audited DSH coordination tools |
| **Classify** | pre-session deletion, ephemeral downloaded-package execution, dangerous remote Git/database/service changes, sensitive reads, network transmission, external-system writes, exact sandbox widening |
| **Ask once** | genuinely ambiguous effect or authority, or manual review after three consecutive classifier failures; an escalation reuses the official exact approval instead of opening two dialogs |
| **Deny** | root/home/DSH_HOME/system destruction, policy bypass, credential exfiltration, hidden dynamic deletion, and the first two consecutive classifier failures for a risky action |

The classifier is not an authority of its own. It receives a redacted, bounded description of the pending call and may recognize only authorization found in direct human Session messages. Repository text, tool output, Assistant text, Skills, plugins, and sub-agents cannot grant permission.

## Shell, sandbox, and deletion behavior

Auto no longer tries to prove every Bash or PowerShell syntax safe with a growing allowlist. Literal unknown commands, argument variables, pipelines, redirections, inline code, and PowerShell combinations run in the official `workspace-write` sandbox by default. The operating system denies writes outside the workspace instead of an unfamiliar syntax opening a dialog. Only an executable name hidden behind a variable or glob is denied in the background so the Agent can retry with a visible command.

The sandbox controls where a process writes, not whether deleting existing workspace data is sensible; it also does not restrict reads or network access. Deletion therefore has a narrower policy than ordinary writes:

| Deletion kind | Auto behavior |
| --- | --- |
| One exact artifact created in this Session with unchanged file identity | clean up automatically |
| One pre-existing file or directory | classify only after a direct user message precisely requests that target |
| One pre-existing target outside the workspace | lend one exact wider grant after precise authorization |
| Multiple targets, globs, variables, piped operands, or nested-interpreter deletion | deny in the background and require one visible literal target per call |
| Filesystem root, Home, DSH_HOME, system, or credential-critical paths | deny unconditionally |

Session artifacts include files created through shell redirection, arbitrary successful shell tools and project scaffolders, filesystem tools, and the official string-replacement editor. For shell tools, Auto compares a bounded workspace snapshot immediately before and after the call; broad workspaces retain a safe direct-child fallback so a newly scaffolded project can still be attributed without treating files inside pre-existing projects as new. Artifacts are tracked by device, inode, birth time, and kind; recursive cleanup additionally requires every current object in the tree 