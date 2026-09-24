# dsh-router-standard

> 任务感知思维模式路由预设：把 DeepSeek V4 在 persona 轴上"非连续、分相变"的实测特性，
> 量化到稳定区（spec / react / weak），在首轮注入匹配的 persona 与工具面。
> 属于 [`dsh-routing-suite`](../dsh-routing-suite) 套装，与 [`dsh-super-injector`](../injector)
> （免重启运行时注入）配合开发。
>
> 📄 研究史说明：[docs/statement.md](docs/statement.md)（勘误声明）｜ [docs/apology.md](docs/apology.md)（道歉函）

---

## 当前状态（v1.19.1，2026-08-24 · 研发线，尚未发布）

**Router Standard 处于「严格 workflow」研发线**（以 CHANGELOG 为准，版本线文件 `router-bootstrap-v34.mjs`）：

- **严格阶段 workflow**：完成信号驱动晋级（0→1 需澄清/计划、1→2 需计划锁定、2→3 需交付自检），
  阶段 0 强制对齐（歧义先 `ask_user_question`、复杂任务先 `todo_write`）；"工具名/文本即跳级"已删除。
- **任务回显**：`stageText` 新增 `Task: <首条真实用户消息>`——模型每轮都看得清在为什么事工作，不跑题。
- **渐进披露**：阶段化解锁 + 两档预放 + 直达语义 + 交付全量开放；`tools_catalog` 全量索引 / `tools_help` 完整 schema；
  已删除 `all:true`（无全量出口，未解锁工具不进入视野）。
- **标准模式基底**：native 直调（无 PTC/run_code 包装，SDK 全量段不存在，工具面注意力税大幅下降）。
- **页面验证内置**：`dev_page_check` = 截图 + DOM smoke + **console/pageerror/title/selector/scale**；
  `{js:…}` 模式 = 本地 JS 引擎（零外部 node 依赖）；external 证据一等公民。
- **描述 ⇄ 行为对齐**：`presentation=native` 自检、阶段文案只说真话、平台事实（win32 以 Git Bash 私有 shell seam 为准）。
- **主动性引导**：Proactivity 常驻段（自检信号，不是停手命令）；压力感应器已退役。

配套预设：**router-react（v17）/ router-spec（v10）**（基于标准模式的两大执行预设，均支持首轮读图）；
router-pro 线已退役删除。完整演进：见 [CHANGELOG.md](CHANGELOG.md) 与 [docs/STANDARD-PLAN.md](docs/STANDARD-PLAN.md)。

---

**【历史文档 · v0.3 时代】** Task-aware reasoning-mode router for DeepSeek Harness. One preset, two
**routing modes** (v0.2.0 naming), plus the measured three-band axis behind them:

| routing mode | first request | thinking shape |
|---|---|---|
| **standard（标准路由预设）** | 分类 persona（spec/react/weak）+ 完整 prompt sections + 分带首轮工具面 | 按分类带行动：react 直接产出、spec 先读后改、weak 内路由（每轮近距离引导） |
| **spec（spec 路由预设）** | 分类 persona（spec/react/weak）+ 完整 prompt sections | **雷霆大思考**：首轮超长思维链（101K 推理 0 行动是其特征，不是缺陷） |

> 选择：安装两个预设之一（Router Standard / Router Spec，见 Usage）。
> `dev_router_status` 显示当前路由模式。

> This is a research artifact. It encodes a measured property of DeepSeek V4
> Pro / V4 Flash: model behavior along the persona axis is **not a continuum**
> — it collapses into a few stable regions separated by phase transitions.
> The router therefore quantizes to the stable regions instead of pretending
> the axis is continuously tunable.

## v0.3.0 — real-assembly-chain fixes

v0.2.x shipped routing logic that was validated against bare-API probes but
was broken on the REAL DeepSeek Harness assembly chain. v0.3.0 fixes all of it,
verified against `@deepseek-ai/dsh-agent-loop` (0.1.0-rc.7) event ordering:

- **First-turn routing actually works** (issue #13): the loop claims the inbox
  BEFORE assembling the system prompt, and `inbox.claim()` emits the
  agent-scoped `agent/inbox/claimed` event synchronously — the router captures
  the first REAL user message there (`source.kind === 'user'` only), so the
  first request is classified instead of unconditionally falling into weak.
  (The captured text is CLASSIFIED, not fed to bandOf raw — the old capture
  path silently mapped every captured message to the spec band.)
- **Near-field guidance moved to `agent/pre-step`** (issues #34/#36/#55):
  `session/event` never fires inside agent-plane presets (dsh-scope filters
  it out of entry-local realms), so the old inbox re-append never delivered
  guidance — and wherever it did fire, the `next-step` append forced a SECOND
  model request per user message (the 2× API-call spike). The guide is now
  inserted into `decision.messages` at `agent/pre-step`: same request as the
  user message, near-field, cache-neutral, zero extra round-trips.
- **Fixes**: missing `extractText`/`bandOf` imports in both bootstrap files
  (#11) — the `session/event` handlers crashed with ReferenceError whenever
  they did fire; `sessionMode` ignoring plugin-origin messages when pinning
  the band; `router.test.mjs` import path; preset.yml YAML quoting (#53);
  subagent-session skip (#5); session-selected model from
  `assembled.variables` (#9); the RL-standard mode of the spec preset now
  returns the assembly untouched after the first tool/call (#44).
- **New**: `router.integration.test.mjs` replays the real claim → assemble →
  pre-step ordering against the actual bootstrap code.

## What it does

**router-standard**: reads the session's first REAL user message, classifies
the task (build → react / fix → spec / ambiguous → weak), and on the first
model request injects the matching persona while keeping the full prompt
sections; the first-turn core tool surface follows the band
(spec=read/edit/glob/grep, react=read/write/edit, weak=read/write/edit, each
plus the platform shell). Weak-band sessions also get a near-field routing
guide in the SAME request as every real user message.

**router-spec**: same routing core with the deep-think-first branding; keeps
the v0.2.0 dual-mode code path (`routerMode`), so a copy configured with
`routerMode: standard` still gets the RL-interface first turn (RL sentence +
shell/str_replace_editor) with full sections restored after the first durable
tool/call.

After the first durable tool call the full Standard catalog is exposed and the
router stops touching anything. The mode is derived from durable session
events, so resume/reload keeps it. The plan-mode prompt section is preserved,
so plan boundaries do not reset the model's focus.

## The three measured behavior bands

Fine-grained probing (21 mode points × n=2, official API, reasoning_effort=max)
on V4 Pro shows behavior along the persona axis collapses into **three bands**:

| band | mode | measured behavior |
|---|---|---|
| `spec` | 0 – 0.19 | stable plan-collective (`We` trajectories, let-me ≈ 0) |
| `mixed` | 0.2 – 0.49 | **transition trap**: unstable mixing of `We`/`The`/`Let` |
| `react` | 0.5 – 1.0 | stable doer (`The`/`Let` first-person, we ≈ 0) — 11 mode values behave alike |

V4 Flash is threshold-like (0–0.5 all spec side, jumps at 0.75+). The numeric
`dev_router_mode` interface is kept, but it quantizes to the three bands — the
transition band is never selected automatically.

## Why: dual-attractor RL policy

Evidence across projects (see `docs/paper.md` and `docs/experiments.md`):

- The **same model** reaches top-band scores under spec conditions on a
  maintenance benchmark (Project2: minimal 99/96, anchored 98/99) and under
  react/code conditions on a greenfield build task (Mario: 10/10), while the
  wrong mode scores 91 / 6 respectively — a ~10-point swing from prompt
  conditioning alone ("god/ghost duality").
- Persona is the dominant trigger (one-sentence swap flips the trajectory);
  tool-schema surface is a secondary condition; catalog text in a user message
  has no effect.
- Behavior is path-committed: once anchored, expanding the tool catalog
  perturbs at most one reasoning block and never flips the mode.
- Intermediate personas are **out-of-distribution** (training-distribution
  gap), which is the measured unstable band.

The model cannot self-route: P3 (same persona, task swap → trajectory
unchanged), P5 (router personas → doer attractor absorbs the instruction) and
P8 (domain-overlap scan) show the only internal-routing window is a WEAK
persona + few-shot routing instruction (lean, not flip; discrimination
+2.3..+3.3). There is no reward signal for switching modes mid session, and
the behavior phase transition means the model commits on the first request.
**Mode selection must come from outside** — a human (the "streamer"), a
heuristic classifier, or a learned router. This preset is the automated
version of that external routing.

## Usage

**Two presets** (v0.3.0; the router-pro line was retired): install one or more under `~/.dsh/.agent-presets/`:

```powershell
# 标准路由预设（RL 接口还原，默认推荐）
$target = Join-Path $env:USERPROFILE '.dsh\.agent-presets\router-standard'
Copy-Item -Recurse .\preset\router-standard $target

# spec 路由预设（深度思考优先）
$target = Join-Path $env:USERPROFILE '.dsh\.agent-presets\router-spec'
Copy-Item -Recurse .\preset\router-spec $target
```

**免重启安装（推荐）**：装好 [dsh-super-in