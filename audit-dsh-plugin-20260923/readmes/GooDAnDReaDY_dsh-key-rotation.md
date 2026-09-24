# 📦 @goodandready/dsh-key-rotation

<div align="center">

<h3>Enterprise-Grade Transparent API Key Rotation, Rate-Limit Pre-emption & Failover Cascade for DeepSeek Harness</h3>

<p align="center">
  <a href="https://www.npmjs.com/package/@goodandready/dsh-key-rotation"><img src="https://img.shields.io/npm/v/@goodandready/dsh-key-rotation.svg?style=for-the-badge&color=6366f1&labelColor=1e1b4b" alt="npm version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/GooDAnDReaDY/dsh-key-rotation.svg?style=for-the-badge&color=10b981&labelColor=064e3b" alt="license"></a>
  <a href="https://github.com/topics/dsh-plugin"><img src="https://img.shields.io/badge/DSH-Plugin-8b5cf6.svg?style=for-the-badge&labelColor=2e1065" alt="DSH Plugin"></a>
  <a href="https://nodejs.org"><img src="https://img.shields.io/badge/Node-20%2B-f59e0b.svg?style=for-the-badge&labelColor=451a03" alt="Node version"></a>
</p>

<!-- Showcase Link -->
<p align="center">
  <a href="https://goodandready.app/"><img src="https://img.shields.io/badge/🌐_DSH_Hub-goodandready.app-ff4500.svg?style=for-the-badge&labelColor=1a1a2e" alt="GoodAndReady Showcase"></a>
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

## ⚡ Overview & The Problem

### 🚀 What's New in v0.8.11 (One-click Updater & Quality Gate)

- **Plugin updater in Settings**: see current/latest version and update from the card without leaving DSH (`#307`).
- **Safer best-effort side effects**: intentional non-critical failures log at debug instead of silent empty `catch` (`#315`).
- **Theme-only client colors** and production-path test cleanup (`#311`, `#314`).
- **Leaner publication set**: agent-only files no longer ship in git/npm (`#308`).

### 🚀 What's New in v0.8.10 (Stream Concurrency Hardening & Auto-Pruning)
- **Zero Concurrency Leaks**: Guaranteed release of stream concurrency slots via deterministic `try ... finally` block, preventing key starvation during clean finishes or client stream aborts.
- **Robust Probe Retry**: Added transient network socket error retry (`PROBE_RETRY_DELAY_MS`) in `SandboxRunner.probeModels` before marking keys as broken.
- **Memory & State Pruning**: Automated pruning of removed/stale keys from internal pool maps during periodic sweep cycles.

### 🚀 What's New in v0.8.9 (Routing Evolution & UI)
- **Proactive Rate-Limit Guard**: Automatic key pausing based on `x-ratelimit-remaining-*` and `Retry-After` headers before hitting 429 errors.
- **Self-Healing / Auto-Unbreak**: Periodic background probe via free `/models` endpoint to automatically revive broken keys without token burn.
- **Latency-Aware Routing**: Selectable strategies: `round-robin`, `least-loaded` (concurrency), and `lowest-latency` (p95 latency).
- **UI Evolution in `dsh-clinebot` Style**: Sequential batch "Test All Keys" runner with live progress, Live Event Stream drawer, and Quota Reset countdown badge.
- **Native Dual Language Support**: Native English (`en`) and Chinese (`zh`) UI dictionaries.

### 🛠️ What's New in v0.8.0 (Stability)
- **🔌 Circuit breaker**: after N consecutive provider failures the circuit opens and requests fail fast (`CIRCUIT_OPEN`) until a cool-down; half-open probes recover automatically.
- **🕒 Monotonic clock**: cooldown/breaker durations use process monotonic time so NTP steps cannot invert remaining times.
- **📮 Non-blocking webhooks**: alerts go through a bounded queue with backoff — stream rotation never waits on webhook HTTP.
- **🧱 Atomic I/O helpers**: crash-safe writes; corrupt JSON never overwrites previous in-memory state.
- **🧹 Clone-route GC**: orphaned auto-created clone routes are dropped from the runtime set.
- **🧭 Error taxonomy**: explicit switch/surface/soft classification for 408/425/429/5xx, sockets and gRPC codes.
- **📡 Status extras**: per-provider `circuit` plus `meta.expectedClones` / `meta.notifyQueue`.
- **🧪 Smoke harness**: scripted 429 → next-key → success path in `test/smoke-rotation-080.test.mjs`.

### 🛠️ What's New in v0.7.33 (Stability & Bugfix Release)
- **🔍 Resolved Key Probing BaseURL**: Fixed `resolveBaseUrl` to map key credential refs to owning provider pools, restoring live `probeModels` testing.
- **🛡️ Guarded Cascade Recursion**: Prevented call stack overflow in cross-provider failover when circular cascade chains occur.
- **🕒 Accurate Midnight PST Resets**: Corrected UTC-8 timezone calculation offset sign for calendar quota reset windows.
- **🧹 Lifecycle Timer Cleanup**: Wrapped `canaryTimer` and `selfHealTimer` in Cordis effect scopes, eliminating background orphaned intervals on hot reload.
- **⚡ Stale Lock Recovery in Load Balancer**: Added expired lock detection to `pickLeastLoaded` for uninterrupted least-connections routing.
- **📊 Load Distribution & Modals (Changed in v0.8.5)**: Interactive segmented load distribution charts per pool, modal action confirmation, and 429/5xx backoff jitter (#283, #284).
- **🎨 Native Design System (Changed in v0.8.3)**: Unified with `dsh-clinebot` baseline: modular section cards, live pool telemetry stat boxes, pill badges, and complete semantic theme token styling (#281).
- **🌐 Localization (Changed in v0.8.2)**: Source strings are English-only. Russian/Chinese UI comes from the DSH core locale service and translation plugins (`props.t`). Active locale: host snapshot → first `navigator.languages` entry → `en` (#277).

### 🚀 What's New in v0.7.31
- **⚡ O(1) TokenBucket Accumulator**: Upgraded rate limiting math to O(1) time and zero-allocation memory with adaptive header synchronization.
- **🛡️ Soft vs Hard Backoff**: Differentiates transient infrastructure drops (502/503/timeouts: 10s flat cooldown) from hard quota errors (progressive doubling).
- **⏳ Penalty Decay**: Stable keys that operate cleanly automatically decay their failure penalty multiplier every hour.
- **🎲 Cooldown Jitter**: Adds ±12.5% random dispersion to recovery timers, eliminating thundering herd stampedes.
- **🎯 Addressable Canary Probing**: Support for probing target pool models with lightweight single-token verification pings.
- **📊 TTFT Percentiles (p50 / p95 / p99)**: Sub-second high-resolution latency percentile tracking across all key pools.
- **🔔 Webhook Alert Digest**: Aggregates multiple rapid switch/cooldown events into consolidated incident digests for Telegram, Discord, and Slack.
- **🧹 30-Day Usage Compaction**: Automatic bounded memory management with 30-day rolling window data pruning.
- **✨ Optimistic UI & Filter Pills**: Instant zero-latency UI updates on reset, plus `All`, `Ready`, `In Cooldown`, and `With Errors` quick filter chips.

High-throughput autonomous agent workflows, parallel subagent swarms, and multi-turn tool loops inevitably hit upstream API rate limits (HTTP 429, RPM/TPM exhaustion, daily quotas, or sudden provider outages). In standard DeepSeek Harness deployments, a single exhausted API key breaks the entire agent execution chain, requiring manual intervention and destroying the session's replay state.

**`dsh-key-rotation`** provides a seamless, enterprise-ready **transparent API key pooling, pre-emptive rate-limiting, and cross-provider failover engine** built natively on the Cordis microkernel architecture.

Unlike naive routing proxies that alter provider identifiers, `dsh-key-rotation` hooks into `ctx.credentials.resolve` and intercepts `llm/stream` at runtime:
* **The provider identity never changes**: Agent replay