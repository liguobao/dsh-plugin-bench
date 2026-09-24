<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=200&section=header&text=K8E%20🚀&fontSize=80&fontColor=ffffff&fontAlignY=38&desc=Open%20Source%20Agentic%20AI%20Sandbox%20Matrix&descAlignY=60&descSize=22&animation=fadeIn" width="100%"/>
<br/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=00D4FF&center=true&vCenter=true&width=700&lines=Open+Source+Agentic+AI+Sandbox+Matrix+%F0%9F%A4%96;Secure+Isolated+Agent+Execution+at+Scale+%F0%9F%94%92;Up+and+Running+in+60+Seconds+%E2%9A%A1;Single+Binary+%3C+100MB+%F0%9F%93%A6;E2B+SDK+Compatible+%F0%9F%A4%9D" alt="Typing SVG" />
</a>

<br/><br/>

[![Go Version](https://img.shields.io/badge/Go-1.25+-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://golang.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge&logo=apache&logoColor=white)](https://github.com/xiaods/k8e/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/xiaods/k8e?style=for-the-badge&logo=github&color=FFD700)](https://github.com/xiaods/k8e/stargazers)
[![Release](https://img.shields.io/github/v/release/xiaods/k8e?style=for-the-badge&logo=github&color=green)](https://github.com/xiaods/k8e/releases)
[![Arch](https://img.shields.io/badge/Arch-x86__64%20%7C%20ARM64%20%7C%20RISC--V-blueviolet?style=for-the-badge)](https://github.com/xiaods/k8e/releases)

<br/>

> **k8e.sh** — Open Source Agentic AI Sandbox Matrix. A **single binary under 100MB** that turns any Linux host into a secure, isolated execution platform for AI agents — gVisor, Kata, or Firecracker isolation, warm-pool fast starts, and an E2B-compatible API. Up and running in **60 seconds**.

<br/>

```bash
curl -sfL https://k8e.sh/install.sh | sh -
```
*That's it. Your agentic sandbox matrix is ready. 🤖*

</div>

---

## 📖 Table of Contents

| # | Section |
|---|---------|
| 1 | [🤖 What is K8E?](#-what-is-k8e) |
| 2 | [🏗️ Architecture](#️-architecture) |
| 3 | [⚙️ Components](#️-components) |
| 4 | [🚀 Quick Start](#-quick-start) |
| 5 | [🔒 Sandbox Runtime Setup](#-sandbox-runtime-setup) |
| 6 | [🤖 Sandbox CLI](#-sandbox-cli) |
| 7 | [🖥️ Advanced Installation](#️-advanced-installation) |
| 8 | [🆚 K8E vs Other Sandbox Platforms](#️-k8e-vs-other-sandbox-platforms) |
| 9 | [🤝 Contributing](#-contributing) |
| 10 | [🙏 Acknowledgments](#-acknowledgments) |

---

## 🤖 What is K8E?

**K8E** is the **Open Source Agentic AI Sandbox Matrix** — a self-hosted sandbox platform for running secure, isolated AI agent workloads at scale, packaged as a single binary under 100MB.

As autonomous AI agents increasingly generate and execute untrusted code, robust sandboxing infrastructure is no longer optional. K8E ships everything needed to spin up a production-grade cluster in under 60 seconds, with first-class primitives for agent isolation, resource governance, and ephemeral execution environments — purpose-built for the AI era.

> 🔒 **One cluster. Many agents. Zero trust between them.**

### Sandbox Capabilities

| Capability | Description |
|---|---|
| 🔒 **Hardware Isolation** | Pluggable runtimes: gVisor (default), Kata Containers, Firecracker microVM |
| 🌐 **Network Policies** | Cilium eBPF `toFQDNs` egress control — per-session, no proxy process needed; `allowed_hosts` enforced via `--cilium-dns-proxy` (KIP-16 M10) |
| ⚖️ **Resource Quotas** | CPU/memory caps per agent session to prevent runaway costs |
| 🗑️ **Ephemeral Workspaces** | Auto-cleanup after agent session ends; per-session workspace isolation for sub-agents (KIP-16 M1) |
| 🧠 **Warm Pool** | Pre-booted sandbox pods for sub-500ms session claim latency; application-layer readiness handshake, adaptive sizing, per-session background-run caps |
| 📸 **Content-Addressed Snapshots** | SHA-256 CAS layerstore with zstd compression, chunked multi-layer manifests, incremental `--base` restore, server-side registry, autosquash (KIP-16 M2) |
| 📜 **Exec Transcripts** | File-backed, windowed, offset-resumable command transcripts — `k8e-sandbox-cli log` (KIP-16 M4) |
| 📊 **Observability** | Prometheus metrics, disk-only NDJSON event stream, process topology — `events` / `ps` CLI (KIP-16 M5) |
| 🔄 **Sub-agent Reuse** | Sub-agents share the parent pod + workspace; isolated reset (KIP-16 M1) |
| 🧾 **CLI Catalog** | Machine-readable command/flag surface for SDK generation — `catalog` (KIP-16 M9) |
| 🤝 **agent-sandbox compatible** | Works with [`kubernetes-sigs/agent-sandbox`](https://github.com/kubernetes-sigs/agent-sandbox) |
| 🔄 **SKILL + CLI** | AI agents (claude code, codex, pi) connect via `k8e-sandbox-cli` CLI commands |

---

## 🏗️ Architecture

<div align="center">

```
 AI Agents (Claude Code / Codex / Pi / dsh)
        │  k8e-sandbox-cli / plugin tools    (gRPC over mTLS)
        ▼
┌──────────────────────────────────────────────┐
│              SANDBOX GATEWAY                 │
│  sessions · exec · files · PTY terminals     │
│  expose · allow-hosts · snapshots            │
│  warm pool · metrics · event stream          │
└──────────────┬───────────────────────────────┘
               │ claims ready pods from the warm pool
   ┌───────────▼───────────┐   ┌────────────────┐
   │   SANDBOX POD         │   │   SANDBOX POD  │
   │   gVisor / Kata / FC  │ … │   (isolated)   │
   │   agent's code + fs   │   │                │
   └───────────────────────┘   └────────────────┘
        eBPF per-session network policy between all of them
```

</div>

One gateway fronts every operation — session lifecycle, streaming exec,
filesystem, PTY terminals, service exposure (`expose`), live egress policy
(`allow-hosts`) and content-addressed snapshots — so agents get one audited
door instead of raw infrastructure access.

---

## ⚙️ Components

<div align="center">

| Component | Purpose |
|---|---|
| 🚪 **Sandbox Gateway** | Single gRPC (mTLS) + E2B-compatible HTTP door: sessions, exec, files, PTY terminals, exposure, snapshots |
| 🛡️ **gVisor / Kata / Firecracker** | Pluggable sandbox isolation runtimes (user-space kernel / lightweight VMs / microVMs) |
| 🔷 **Cilium (eBPF)** | Per-session network policy & egress control — no proxy process |
| 🧠 **Warm Pool Controller** | Pre-booted sandbox pods, adaptive sizing, sub-500ms claims |
| 🤖 **k8e-sandbox-cli** | Standalone agent CLI — connect, run, expose, snapshots (`catalog` for SDK generation) |
| 🔌 **dsh plugin family** | `@k8e-sandbox/*` npm packages — DeepSeek Harness integration with model-surface tools |

</div>

---

## 🚀 Quick Start

### Step 1 — Install a Sandbox Runtime (recommended: before K8E)

Install the runtime shim **before** K8E so it is auto-detected on first startup. **gVisor is recommended** — no KVM required.

```bash
# Download runsc + containerd-shim-runsc-v1 directly from the gVisor release bucket (requires wget)
ARCH=$(uname -m)   # x86_64 on most servers, aarch64 on ARM
URL=https://storage.googleapis.com/gvisor/releases/release/latest/${ARCH}

wget ${URL}/runsc ${URL}/runsc.sha512 \
     ${URL}/containerd-shim-runsc-v1 ${URL}/containerd-shim-runsc-v1.sha512

sha512sum -c runsc.sha512 -c containerd-shim-runsc-v1.sha512   # both must print OK
chmod +x runsc containerd-shim-runsc-v1
sudo mv runsc containerd-shim-runsc-v1 /usr/local/bin/
ls -l /usr/local/bin/runsc /usr/local/bin/containerd-shim-runsc-v1   # verify both installed
```

> K8E detects `runsc` at startup and automatically injects the gVisor stanza into its containerd config (`/var/lib/k8e/agent/etc/containerd/config.toml`). Do **not** run `runsc install` — K8E manages its own containerd configuration.

> Need stronger isolation? See [Sandbox Runtime Setup](#-sandbox-runtime-setup) for Kata Containers and Firecracker.

### Step 2 — Install K8E

```bash
curl -sfL https://k8e.sh/install.sh | sh -
```

### Step 3 — Verify the Sandbox

```bash
k8e-sandbox-cli status        # -> {"available": true, ...}
k8e-sandbox-cli run 'echo hello from