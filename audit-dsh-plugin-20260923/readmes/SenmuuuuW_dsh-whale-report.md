<p align="center">
  <img src="assets/whale/whale-happy.svg" alt="" width="56">
</p>

<h1 align="center">深迹 · DeepTrace</h1>

<p align="center"><b>Your Agent, in numbers.</b></p>

<p align="center">Agent 可观测 → 诊断 → 改进 → 受控修改 → 回验：<br/>把 DSH 的 session、token、cost、tool call 与异常，转成可追踪的事实、确定性诊断、可执行建议，以及真正能被验证的改进。</p>

<p align="center">
  <a href="https://www.npmjs.com/package/dsh-whale-report"><img src="https://img.shields.io/npm/v/dsh-whale-report?label=npm&color=4d6bfe" alt="npm version"></a>
  <a href="https://github.com/SenmuuuuW/dsh-whale-report/releases"><img src="https://img.shields.io/github/v/release/SenmuuuuW/dsh-whale-report?label=version&color=4d6bfe" alt="version"></a>
  <a href="https://github.com/SenmuuuuW/dsh-whale-report/actions/workflows/ci.yml"><img src="https://github.com/SenmuuuuW/dsh-whale-report/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/Anil-matcha/awesome-dsh-plugin"><img src="https://img.shields.io/badge/awesome--dsh--plugin-listed-4d6bfe" alt="awesome dsh plugin"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-4d6bfe.svg" alt="license"></a>
</p>

<table align="center">
  <tr>
    <td align="center" style="background:#0b1733;border-radius:12px;padding:10px 30px">
      <span style="color:#4d6bfe;font-weight:700;font-family:ui-monospace,Menlo,monospace">6 PERIODS</span>
      <span style="color:#33445f"> · </span>
      <span style="color:#cbd5e1;font-family:ui-monospace,Menlo,monospace">DETERMINISTIC</span>
      <span style="color:#33445f"> · </span>
      <span style="color:#cbd5e1;font-family:ui-monospace,Menlo,monospace">4 IMPROVE RULES</span>
      <span style="color:#33445f"> · </span>
      <span style="color:#cbd5e1;font-family:ui-monospace,Menlo,monospace">APPLY + VERIFY</span>
      <span style="color:#33445f"> · </span>
      <span style="color:#cbd5e1;font-family:ui-monospace,Menlo,monospace">HISTORICAL PRICING</span>
      <span style="color:#33445f"> · </span>
      <span style="color:#cbd5e1;font-family:ui-monospace,Menlo,monospace">INCREMENTAL INDEX</span>
      <span style="color:#33445f"> · </span>
      <span style="color:#cbd5e1;font-family:ui-monospace,Menlo,monospace">FAULT ISOLATION</span>
      <span style="color:#33445f"> · </span>
      <span style="color:#cbd5e1;font-family:ui-monospace,Menlo,monospace">READ-ONLY BY DEFAULT</span>
    </td>
  </tr>
</table>

<br/>

<img src="docs/images/deeptrace-overview.png" alt="DeepTrace inside DSH" width="100%" style="border:1px solid #d9e3e8;border-radius:14px">

---

## Why DeepTrace

Agent 跑完之后，真正难回答的问题不是"它做了什么"，而是：

- 哪些 session 最贵？
- 为什么突然开始 retry？
- 哪些操作值得注意？
- 夜里到底跑了多少？
- 是哪次任务把成本拉高的？
- **这周有什么值得改的？**

DeepTrace 不是 log viewer，也不是普通 dashboard——它把会话事件日志聚合成报告，让这些问题有答案。

## The loop

<table align="center">
  <tr>
    <td align="center" width="15%" style="background:#f5f8f9;border:1px solid #d9e3e8;border-radius:12px;padding:16px 8px">
      <b style="color:#4d6bfe">TRACE</b><br/>
      <span style="color:#33445f;font-size:12px">Sessions / tokens / cost / tools become queryable evidence.</span>
    </td>
    <td align="center" width="3%" style="color:#94a2b3">→</td>
    <td align="center" width="15%" style="background:#f5f8f9;border:1px solid #d9e3e8;border-radius:12px;padding:16px 8px">
      <b style="color:#4d6bfe">DIAGNOSE</b><br/>
      <span style="color:#33445f;font-size:12px">Deterministic findings locate failures, waste and cost anomalies.</span>
    </td>
    <td align="center" width="3%" style="color:#94a2b3">→</td>
    <td align="center" width="15%" style="background:#f5f8f9;border:1px solid #d9e3e8;border-radius:12px;padding:16px 8px">
      <b style="color:#4d6bfe">IMPROVE</b><br/>
      <span style="color:#33445f;font-size:12px">Recommendations include evidence and a verification plan.</span>
    </td>
    <td align="center" width="3%" style="color:#94a2b3">→</td>
    <td align="center" width="15%" style="background:#f5f8f9;border:1px solid #d9e3e8;border-radius:12px;padding:16px 8px">
      <b style="color:#4d6bfe">APPLY</b><br/>
      <span style="color:#33445f;font-size:12px">Only predefined safe changes can be applied after explicit approval.</span>
    </td>
    <td align="center" width="3%" style="color:#94a2b3">→</td>
    <td align="center" width="15%" style="background:#f5f8f9;border:1px solid #d9e3e8;border-radius:12px;padding:16px 8px">
      <b style="color:#4d6bfe">VERIFY</b><br/>
      <span style="color:#33445f;font-size:12px">Post-change evidence determines VERIFIED / NOT IMPROVED / INCONCLUSIVE.</span>
    </td>
  </tr>
</table>

一次报告，走完整个闭环。Apply 只接受**用户批准的、allowlisted 的、受控的**修改；Apply 不是 autonomous optimization，self-healing 不在范围内。

## v0.6.1 — Accounting Correctness

**Correct history. Complete sessions.**

这一版修的是"数字是否可信"。[v0.6.1 release](https://github.com/SenmuuuuW/dsh-whale-report/releases/tag/v0.6.1)

### Historical pricing

DeepSeek pricing 按真实生效日期回溯（Asia/Shanghai）：

- before **2026-08-17**：legacy flat pricing
- **2026-08-17** onward：peak / off-peak pricing
- **2026-08-23** onward：weekends fully off-peak

### Complete session ingestion

- plugin 启动后新建的 sessions 会被 periodic reconcile 自动发现，**不需要 restart**
- repeated reconciliation 不重复计数

### Resume history

- normal resume 保留完整历史；only true fork inherited seed is excluded
- 升级 v0.6.1 后，旧 v17 index 自动失效并重建（见 Semantic migration）

### Semantic migration

v0.6.1 bumps the persisted accounting semantics: **INDEX_VERSION 18 · REPORT_SEM 7**. Old incompatible index / report state is not silently reused.

## Accounting model

DeepTrace cost = **complete event history** × **historically correct pricing**。

v0.6.1 同时修正了价格口径、session discovery 与 resume history——因此 **affected historical reports may change materially after upgrade**（历史报告的数字会按正确口径重算）。

## Product

<img src="docs/images/overview.png" alt="DeepTrace overview" width="100%" style="border:1px solid #d9e3e8;border-radius:14px">

<sub>DeepTrace overview — hero, provider balance, cost, findings and the whale note.</sub>

<img src="docs/images/report.png" alt="Full report" width="100%" style="border:1px solid #d9e3e8;border-radius:14px">

<sub>The full DeepTrace report — findings, collaboration review, activity, resources, risks and session trace.</sub>

## Query Engine

DeepTrace 架构是一句话：**INGEST ONCE → QUERY MANY**。会话事件只在进入时被读取、聚合、落库一次，此后 Overview / Report / History 全部只查询建好的 canonical index——不再重放 Session、不再解压、不再重新聚合。

### Ingest（进入一次）

- **session/event firehose = primary incremental path**（baseline + seq 去重）；已索引会话保持增量、去重，绝不重复计数
- **periodic reconcile = discovery / recovery path**：发现插件启动后新建的 session header 并纳入索引，不需要 restart；损坏会话只读 salvage（worker_threads 解压，不阻塞查询）
- resume 的会话保留恢复前的完整历史（仅真实 fork 继承的 seed 事件除外）
- v0.6.1 uses INDEX_VERSION 18：previously persisted indexes built under the old resume/session interpretation are automatically rebuilt
- 持久化：canonical index 用 coalesced checkpoints 落盘，避免反复整库重写

### Query（查询多次）

- 所有页面把 PeriodSpec 解析成窗口后直接查询 canonical index（10 分钟分桶 + 精确边界行），零 readSession / 零解压
- rolling 24h 是精确窗口 `[now-24h, now)`；PeriodSpec 是唯一时间窗口真相源，周期之间绝不串数据

### Exact accounting（精确对账）

- 窗口边界逐事件精确过滤（无比例近似）；对于完整可读的 event history，integer token accounting 与 raw-event oracle **exactly** 一致，cost 由同一 canonical 贡献按历史价格边界计算
- 统计与周期口径统一 Asia/Shanghai（不依赖机器时区）
- Source-log gaps 或 truncated session logs 会限制历史完整性——DeepTrace 不虚构缺失事件

当前 version：**v0.6.1**（npm `latest`；官方兼容基线 DSH 0.1.1-rc.2）· [v0.6.1 release](https://github.com/SenmuuuuW/dsh-whale-report/releases/tag/v0.6.1)

## Performance

Benchmarked on the real production dataset used during v0.5.3 acceptance; results vary with environment.

| 场景 | 之前 | v0.5.3 |
| --- | --- | --- |
| Refresh / Overview | ~31s（重放 + 重新聚合 session） | ~7ms median（纯索引查询） |
| Live session | ~6.5s（每 30s 整读） | <1ms steady state（增量维护） |
| Refresh ×100 压测 | — | p95 8.3ms / max 11.3ms |

## Apply & Verify

DeepTrace 不再只告诉你哪里有问题。对于**少量、明确、可回滚的安全修改**，它可以在用户批准后执行改变，然后用之后的新会话数据验证是否真的改善。

```
IMPROVE → REVIEW CHANGE → APPLY → OBSERVE → VERIFY → OPTIONAL