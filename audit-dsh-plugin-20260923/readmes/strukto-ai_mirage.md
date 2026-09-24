<h1 align="center">
  <a href="https://www.strukto.ai/mirage">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/mirage-header-dark.svg">
      <img src="assets/mirage-header-light.svg" width="100%" alt="Mirage: A Virtual Terminal for AI Agents" />
    </picture>
  </a>
</h1>

<p align="center">
    <a href="https://docs.mirage.strukto.ai" alt="Documentation">
        <img src="https://img.shields.io/badge/mirage-docs-0C0C0C?labelColor=F0ECE2" /></a>
    <a href="https://github.com/strukto-ai/mirage/releases" alt="Status">
        <img src="https://img.shields.io/badge/status-preview-0C0C0C?labelColor=F0ECE2" alt="Status: preview" /></a>
    <a href="https://www.strukto.ai" alt="Website">
        <img src="https://img.shields.io/badge/made by-strukto.ai-0C0C0C?labelColor=F0ECE2" /></a>
    <a href="https://github.com/strukto-ai/mirage/blob/main/LICENSE" alt="License">
        <img src="https://img.shields.io/badge/license-Apache--2.0-0C0C0C?labelColor=F0ECE2" /></a>
    <a href="https://discord.gg/u8BPQ65KsS" alt="Discord">
        <img src="https://img.shields.io/badge/discord-join-0C0C0C?labelColor=F0ECE2&logo=discord&logoColor=0C0C0C" /></a>
    <br/>
    <a href="https://docs.mirage.strukto.ai/python/quickstart" alt="Python docs">
        <img src="https://img.shields.io/badge/python-docs-0C0C0C?labelColor=F0ECE2&logo=python&logoColor=0C0C0C" alt="Python docs"></a>
    <a href="https://pypi.org/project/mirage-ai/" alt="PyPI Version">
        <img src="https://img.shields.io/pypi/v/mirage-ai.svg?color=0C0C0C&labelColor=F0ECE2"/></a>
    <br/>
    <a href="https://docs.mirage.strukto.ai/typescript/quickstart" alt="TypeScript docs">
        <img src="https://img.shields.io/badge/typescript-docs-0C0C0C?labelColor=F0ECE2&logo=typescript&logoColor=0C0C0C" alt="TypeScript docs"></a>
    <a href="https://www.npmjs.com/package/@struktoai/mirage-node" alt="NPM Version">
        <img src="https://img.shields.io/npm/v/@struktoai/mirage-node.svg?color=0C0C0C&labelColor=F0ECE2"/></a>
</p>

<p align="center">
  <a href="./README.md"><img alt="README in English" src="https://img.shields.io/badge/English-F0ECE2"></a>
  <a href="./readme/README.zh-CN.md"><img alt="简体中文 README" src="https://img.shields.io/badge/简体中文-F0ECE2"></a>
  <a href="./readme/README.zh-TW.md"><img alt="繁體中文 README" src="https://img.shields.io/badge/繁體中文-F0ECE2"></a>
  <a href="./readme/README.fr.md"><img alt="README en Français" src="https://img.shields.io/badge/Français-F0ECE2"></a>
  <a href="./readme/README.de.md"><img alt="README auf Deutsch" src="https://img.shields.io/badge/Deutsch-F0ECE2"></a>
  <a href="./readme/README.vi.md"><img alt="README Tiếng Việt" src="https://img.shields.io/badge/Ti%E1%BA%BFng%20Vi%E1%BB%87t-F0ECE2"></a>
  <a href="./readme/README.ko.md"><img alt="README 한국어" src="https://img.shields.io/badge/%ED%95%9C%EA%B5%AD%EC%96%B4-F0ECE2"></a>
</p>

Mirage is **a Virtual Terminal for AI Agents**. The virtual filesystem delivers broad data context, virtualized CLIs give an agent more flexibility on tool use, dynamic runtimes save underlying infrastructure cost and are more token efficient, and fine-grained control over an agent's actions and even over what it can see gives the best security. Together these parts form one virtualized terminal, giving the best agent performance, cost efficiency and security.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/mirage-arch-dark.svg">
    <img src="assets/mirage-arch-light.svg" alt="Mirage architecture: agents and harness reach profiles and the Mirage shell, which resolve Unix-like commands, virtual CLIs and programming languages onto runtimes and the virtual filesystem, with authentication, the policy engine and notifications alongside" width="100%">
  </picture>
</p>

Here is an example of launching Mirage inside an application:

```python
ws = Workspace(
    {
        "/tmp":   (RAMVFS(), MountMode.EXEC),
        "/redis": (RedisVFS(url=redis_url), MountMode.WRITE),
        "/slack": (SlackVFS(SlackConfig(token=slack_bot_token)), MountMode.EXEC),
    },
    # monty captures python, so scripts run sandboxed inside the workspace
    runtimes=[MontyRuntime(captures=["python", "python3"]), "workspace"],
)

# one grep sweeps every source
await ws.shell("grep -rln session /redis /tmp")

# run a script that lives in Slack, file the report into Redis
await ws.shell("python3 /slack/channels/general_.../files/example__F....py > /redis/report.txt")

# install a typed CLI under a head word: dispatched by name, not by path,
# and discoverable through `man`, `type` and `which` like any other program
ws.register_cli("slack", SLACK, {"token": slack_bot_token})
await ws.shell('slack send-message --channel general --text "report is up"')
```

## About

- **Unified virtual terminal interface, not N SDKs and M MCPs.** Every backend speaks the same filesystem semantics, so pipelines compose across services.
- **A virtual filesystem over every source.** S3, Google Drive, Slack, Gmail, Redis and the rest mount side by side under one root, so an agent reaches all of them through a unified interface with the unix tools it already knows, like `ls`, `grep`, `find` and `jq`.
- **Virtual command line tools (CLIs).** `git`, `slack` and `ntn` are answered by Mirage itself, so an agent drives the service with nothing installed, across different runtimes and machines, and one tool can be virtualized into two or more, each under its own name with its own credentials.
- **Routed, dynamic runtimes.** Python, JavaScript and any other command can be sent to a configured runtime, in process, sandboxed or remote, which decouples computation from storage and lets either change without touching the other.
- **The virtualized Mirage shell.** It binds the filesystem, the CLIs and the runtimes into one command line, so pipes, redirection, variables, jobs and history work across all three.
- **Profiles designed for agents.** `allow`, `ask` and `deny` govern commands and CLIs, while `hide` and `show` govern files and folders, so a hidden path is not merely unreadable but absent from the filesystem the agent sees.
- **A scriptable policy engine.** A policy script can prohibit any dangerous action before it runs, and the same stack gates every VFS op and session write, so neither a file nor an environment variable leaks.
- **Notifications wired into the VFS and agents.** External changes become an event stream on the mount, so a new Slack reply surfaces as a change to the chat file in the virtual filesystem, and the agent reacts to it instead of rescanning the tree.

## Virtual Filesystem

Everything [Mirage](https://www.strukto.ai/mirage) "mounts" as one unified virtual filesystem for AI agents. Each
service sits side-by-side under a single root and answers the same POSIX semantics.

|                                  | VFS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      