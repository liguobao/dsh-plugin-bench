# dsh-win32

## Fix DSH on Windows. No WSL.

**Official PowerShell. Workspace Write. One command.**

```powershell
npx dsh-win32 setup
```

Current DeepSeek Harness already includes persistent PowerShell and a Windows ACL sandbox. dsh-win32 checks that official stack, finds known Windows failures, applies the repairs it can prove safe, and creates a desktop shortcut.

It does not install Git, PowerShell, busybox, WSL, or another DSH bundle on the current path.

Use the standalone CLI above on current DSH. Do **not** run `dsh plugin --profile web add dsh-win32` for this workflow: that installs the legacy bundle, not the current Windows setup path.

[中文](./docs/README.zh.md) · [Windows evidence and legacy details](./docs/windows-details.md)

Using a coding agent? [Copy the setup and verification request](https://github.com/sjh9714/dsh-win32/blob/master/docs/agent-setup.md). For a guided walkthrough, see [Windows troubleshooting in Chinese](https://github.com/sjh9714/dsh-win32/blob/master/docs/windows-first-run.zh.md).

Start with the [Windows first-run walkthrough](./docs/windows-first-run.md) if DSH will not launch or a check fails. It follows one problem from diagnosis through the next verification step. [Share your first-run result](https://github.com/sjh9714/dsh-win32/issues/new?template=first-run.md), including attempts that are still blocked.

<p>
<a href="https://www.npmjs.com/package/dsh-win32"><img src="https://img.shields.io/npm/v/dsh-win32?style=flat-square&label=npm&color=cb3837" alt="npm"></a>
<a href="https://github.com/sjh9714/dsh-win32/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/sjh9714/dsh-win32/ci.yml?style=flat-square&label=CI" alt="CI"></a>
<a href="https://github.com/sjh9714/dsh-win32/stargazers"><img src="https://img.shields.io/github/stars/sjh9714/dsh-win32?style=flat-square" alt="stars"></a>
<img src="https://img.shields.io/badge/platform-win32-0078D4?style=flat-square" alt="win32">
<img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT">
</p>

## See the current setup

**Reproduced setup flow. This is not a screen recording.**

![Reproduced dsh-win32 setup on current DSH](./assets/demo.gif)

The command checks the official persistent PowerShell and Workspace Write packages, creates the shortcut, and leaves the profile on the stock Minimal preset.

## What setup does

- Checks the latest published DSH Windows package contract
- Checks PowerShell 7 and known broken koffi runtimes
- Creates a `DeepSeek Harness` desktop shortcut for the Web profile
- Leaves the official profile and preset unchanged
- Shows the exact next steps for a first session

After setup, open DSH, add a workspace, choose the stock **Minimal** preset, and keep **Workspace Write** enabled.

Use another profile without creating a shortcut.

```powershell
npx dsh-win32 setup --profile desktop --no-shortcut
```

`--sandboxed` remains accepted for old notes and scripts. Current DSH already provides the sandbox, so the flag makes no extra change.

## Live verification of an installed stack

From **0.17.12**, opt in to setup followed by one installed-stack check:

```powershell
npx dsh-win32 setup --verify
```

Use `--profile NAME --no-shortcut` when appropriate. Ordinary `setup` is unchanged; `--legacy --verify` is rejected. Setup and component acceptance are reported separately, and a failed or unsupported verification makes the command exit nonzero. This does not install DSH or prove a complete Desktop/Minimal session. For a check without setup or JSON output, use the standalone command:

```powershell
npx dsh-win32 verify
npx dsh-win32 verify --json
```

`verify` is a model- and API-key-free acceptance run against an **already installed** `@deepseek-ai/dsh` dependency tree. It does not use registry metadata as proof. In an isolated temporary home and workspace it invokes the installed model-facing persistent `pwsh` tool through the official terminal, subprocess, Workspace Write policy, and Windows ACL sandbox components.

A pass requires all of these live observations:

- 64-bit PowerShell 7 launches and reports a real executable
- two `pwsh` calls retain the same PTY, current directory, and environment state
- exact content is written and read inside the temporary workspace
- a normal-process control can write the isolated outside target, while confined PowerShell is denied and creates no file
- the shell recovers after denial; cancellation tears down its PTY; a replacement call works; and a second cancellation tears down cleanly
- every runtime resource, temporary home, and temporary workspace is removed

No user DSH profile, config, workspace, or PowerShell profile is loaded or changed. Secret-bearing environment variables are not passed to the worker, and reports contain no tested paths or terminal output. Native Windows and a DSH-supported Node release are required; Node 23 is explicitly unsupported.

If a timeout or output limit leaves worker or descendant containment unconfirmed, verification fails and preserves the isolated snapshot instead of deleting files under a potentially live process.

`verify` creates its own Workspace Write policy and Windows ACL-confined PowerShell child. If you run it from an agent that is already inside another Workspace Write or Windows ACL sandbox, approve one unsandboxed/full-access execution for **this verify command only**; otherwise the nested restricted-token/ConPTY layers can stall before PowerShell launches. This does not bypass the acceptance boundary: the inner child under test remains confined, and the outside-write denial is still required to pass. Worker timeouts report only a fixed, path-free progress checkpoint so nested-launch stalls can be distinguished without exposing terminal output or environment values.

The boundary is deliberate: this composes the installed official components and invokes the real persistent tool, but it does not start the complete stock Minimal host/preset, run the plugin installer, execute hook bridges, or make a model request. A pass must therefore be read as component-chain acceptance, not as an end-to-end stock-session or hook-enforcement claim.

Tools run under a non-driving synthetic agent with a real temporary DSH session. The verifier does not instantiate DSH's private agent-loop inbox; any attempt to use that inbox fails the check instead of returning fabricated state.

The repository CI installs `@deepseek-ai/dsh@latest` from scratch and runs this acceptance on real Windows. Pushes, pull requests, and manual runs cover npm and strict pnpm layouts on Node 22.19 and 24. A weekly upstream watch retains both installers on Node 22.19, so a new DSH publication is checked even when dsh-win32 itself has not changed.

The pnpm lane preserves a strict 24-hour publication cooldown and an explicit build-script allowlist. It can select an older eligible release than npm. Read the installed DSH version in each result; a pass is not evidence for a release that the package manager has not installed.

## Doctor and safe repair

```powershell
npx dsh-win32 doctor
npx dsh-win32 doctor --json
npx dsh-win32 fix
```

`doctor` verifies the published DSH Windows package contract and checks local Windows failures. Its JSON output follows the `dsh-doctor/v1` envelope. Use `verify` when you need live evidence from the installed stack rather than registry metadata.

`fix` only repairs installed koffi versions that are known broken or fail a real runtime load. It verifies the load again after repair.

## Upstream plugin and hook boundaries

Two current DSH control paths sit outside repairs that dsh-win32 can safely apply:

- On Windows, `dsh plugin add` can split a local package path containing spaces, and relative package paths can resolve from an unexpected working directory ([upstream #2485](https://github.com/deepseek-ai/deepseek-harness/discussions/2485)). Prefer a published package specifier. If a local package is unavoid