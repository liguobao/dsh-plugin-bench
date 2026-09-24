# Wegent

> An open-source AI work system spanning your local desktop, cloud agents, and remote machines.

English | [简体中文](README_zh.md)

[![CI](https://github.com/wecode-ai/Wegent/actions/workflows/test.yml/badge.svg)](https://github.com/wecode-ai/Wegent/actions/workflows/test.yml)
[![License](https://img.shields.io/github/license/wecode-ai/Wegent)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/wecode-ai/Wegent)](https://github.com/wecode-ai/Wegent/issues)
    <a href="https://linux.do" alt="LINUX DO">
        <img
            src="https://img.shields.io/badge/LINUX-DO-FFB003.svg?logo=data:image/svg%2bxml;base64,DQo8c3ZnIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjEwMCIgaGVpZ2h0PSIxMDAiPjxwYXRoIGQ9Ik00Ni44Mi0uMDU1aDYuMjVxMjMuOTY5IDIuMDYyIDM4IDIxLjQyNmM1LjI1OCA3LjY3NiA4LjIxNSAxNi4xNTYgOC44NzUgMjUuNDV2Ni4yNXEtMi4wNjQgMjMuOTY4LTIxLjQzIDM4LTExLjUxMiA3Ljg4NS0yNS40NDUgOC44NzRoLTYuMjVxLTIzLjk3LTIuMDY0LTM4LjAwNC0yMS40M1EuOTcxIDY3LjA1Ni0uMDU0IDUzLjE4di02LjQ3M0MxLjM2MiAzMC43ODEgOC41MDMgMTguMTQ4IDIxLjM3IDguODE3IDI5LjA0NyAzLjU2MiAzNy41MjcuNjA0IDQ2LjgyMS0uMDU2IiBzdHlsZT0ic3Ryb2tlOm5vbmU7ZmlsbC1ydWxlOmV2ZW5vZGQ7ZmlsbDojZWNlY2VjO2ZpbGwtb3BhY2l0eToxIi8+PHBhdGggZD0iTTQ3LjI2NiAyLjk1N3EyMi41My0uNjUgMzcuNzc3IDE1LjczOGE0OS43IDQ5LjcgMCAwIDEgNi44NjcgMTAuMTU3cS00MS45NjQuMjIyLTgzLjkzIDAgOS43NS0xOC42MTYgMzAuMDI0LTI0LjM4N2E2MSA2MSAwIDAgMSA5LjI2Mi0xLjUwOCIgc3R5bGU9InN0cm9rZTpub25lO2ZpbGwtcnVsZTpldmVub2RkO2ZpbGw6IzE5MTkxOTtmaWxsLW9wYWNpdHk6MSIvPjxwYXRoIGQ9Ik03Ljk4IDcwLjkyNmMyNy45NzctLjAzNSA1NS45NTQgMCA4My45My4xMTNRODMuNDI2IDg3LjQ3MyA2Ni4xMyA5NC4wODZxLTE4LjgxIDYuNTQ0LTM2LjgzMi0xLjg5OC0xNC4yMDMtNy4wOS0yMS4zMTctMjEuMjYyIiBzdHlsZT0ic3Ryb2tlOm5vbmU7ZmlsbC1ydWxlOmV2ZW5vZGQ7ZmlsbDojZjlhZjAwO2ZpbGwtb3BhY2l0eToxIi8+PC9zdmc+" /></a>

Wegent includes a desktop workbench and a self-hostable web platform. Wegent Desktop works with local projects, files, commands, tests, and code changes. Wegent Web provides browser-based agents, knowledge, automation, and administration. Wegent Backend connects these applications to shared project spaces, models, and execution devices.

[Download the latest Wegent Desktop](https://github.com/wecode-ai/Wegent/releases/latest) · [Documentation](https://wecode-ai.github.io/wegent-docs/) · [Contributing](CONTRIBUTING.md)

## Wegent Desktop

Wegent Desktop organizes local coding work by project and task. The task view keeps the conversation, tool activity, tests, changed files, and diffs together; the project-space view provides the board, shared files, automation, and execution status.

<img src="https://github.com/wecode-ai/Wegent/releases/download/readme-assets/wegent-desktop-workbench.png" width="100%" alt="A real Wegent Desktop coding task showing the verified result, changed files, and an expanded source-code diff in one workbench" />

<p align="center"><sub>Running and reviewing a local coding task in Wegent Desktop.</sub></p>

<img src="https://github.com/wecode-ai/Wegent/releases/download/readme-assets/wegent-project-workspace.png" width="100%" alt="A real Wegent Desktop project workspace with its kanban board, project navigation, and a remote-machine test task in progress" />

<p align="center"><sub>A project space in Wegent Desktop with its task board, shared files, automation, and execution status.</sub></p>

## Features

- **Desktop workbench** — Organize local projects, tasks, sessions, files, tool activity, tests, and diffs.
- **Reusable agents** — Combine models, prompts, Skills, knowledge, tools, and collaboration settings.
- **Project spaces** — Share task boards, files, discussions, automation, execution history, and deliveries.
- **Multiple execution targets** — Run tasks locally, on remote work machines, or with server-managed executors.
- **Self-hosting** — Deploy Wegent Web and Backend for team access, APIs, permissions, scheduling, and knowledge services.

## Why Wegent

**The local coding experience built on Codex is the foundation of Wegent Desktop.** It works directly with the code, files, commands, and development environment in your projects. Connect it to Wegent Backend when coding work needs to move beyond one computer or one person. Once connected, the desktop workbench and Web use the same projects, tasks, and execution devices.

- **Run tasks on the right device** — Keep using the code, files, commands, and development environment already on a local machine, or run a task for the same project on a remote work machine or server-managed executor.
- **Move a project forward as a team** — Project spaces connect task boards, shared files, discussions, execution status, and deliveries instead of leaving conversations and code changes on separate computers.
- **Automate repeated project work** — Project spaces can configure automation and execution queues to keep routine work moving.
- **Keep services and data under team control** — Self-host Web and Backend for shared access, permissions, model configuration, scheduling, knowledge services, and remote-device management.

If work always stays on one computer, Wegent Desktop provides a familiar Codex coding experience. Connect it to Wegent to extend that experience when tasks must move across people, devices, or a self-hosted environment.

## Wegent Web

Wegent Web provides the browser interface for remote agents. Agents can use configured models, knowledge, Skills, and tools while Wegent Backend manages their tasks and execution.

<img src="https://github.com/wecode-ai/Wegent/releases/download/readme-assets/wegent-remote-agent.png" width="100%" alt="A Wegent remote agent using tools to generate and display a Gantt chart" />

<p align="center"><sub>A Wegent remote agent uses tools to generate a Gantt chart.</sub></p>

## How it works

Wework is the Wegent desktop workbench. Electron owns desktop windows, system capabilities, and process management. DeepSeek Harness (DSH) is the embedded application and plugin runtime, and the Wework product UI is composed from a set of DSH plugins. Executor manages tasks and sessions, then drives Codex to perform the actual work in local projects.

```mermaid
flowchart LR
    Electron["Electron<br/>Desktop host"]

    subgraph DSH["DSH Runtime"]
        direction TB
        Core["DSH Core<br/>Plugin discovery, dependency injection, and lifecycle"]
        App["dsh-app-wework<br/>Wework product shell and UI extension points"]
        UI["dsh-ui-*<br/>Tasks, project spaces, settings, apps, and automation"]
        ElectronPlugin["dsh-electron-host<br/>Electron capability bridge"]
        ExecutorPlugin["dsh-executor-runtime<br/>Task execution and event adapter"]
        TerminalPlugin["dsh-terminal-runtime<br/>Local interactive terminals"]

        Core --> App
        Core --> UI
        Core --> ElectronPlugin
        Core --> ExecutorPlugin
        Core --> TerminalPlugin
        App --> UI
    end

    Executor["Executor<br/>Task and session execution"]
    Codex["Codex<br/>Coding agent"]
    Workspace["Local project<br/>Files and commands"]

    Electron -->|"Starts and hosts"| Core
    Electron -->|"Starts and supervises"| Executor
    ElectronPlugin <-->|"Restricted desktop capabilities"| Electron
    UI <-->|"User actions and UI updates"| ExecutorPlugin
    ExecutorPlugin -->|"Create, follow up, approve, cancel"| Executor
    Executor -->|"Status, messages, tool events, results"| ExecutorPlugin
    Executor <-->|"Launch, control, and events"| Codex
    Codex <-->|"Read, modify, and execute"| Workspace
    TerminalPlugin <-->|"PTY"| Workspace
```

DSH does not execute coding tasks itself. `dsh-app-wework` defines the product shell and extension points, `dsh-ui-*` provides the product modules, `dsh-electron-host` bridges restricted Electron capabilities, `dsh-executor-runtime` communicates bidirectionally with Executor throughout execution, and `dsh-terminal-runtime` manages local interactive terminals. Executor is the task execution layer, while Codex is the concrete coding agent it drives.

Wework can also connect