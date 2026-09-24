<p align="center">
  <a href="./README_EN.md">English</a> · <strong>简体中文</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.5.4-0891b2?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-22c55e?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/DSH-Plugin-7C3AED?style=flat-square" alt="DSH Plugin">
  <img src="https://img.shields.io/badge/DSH-0.1.5--rc.2-7C3AED?style=flat-square" alt="DSH">
  <img src="https://img.shields.io/badge/node-%E2%89%A518-339933?style=flat-square" alt="Node">
  <img src="https://img.shields.io/badge/tools-31-0ea5e9?style=flat-square" alt="31 tools">
</p>

<h1 align="center">Normify · 归一化框架图构建器</h1>

<p align="center"><b>把整个项目描述成一棵"人机共读"的分形模块树：AI 负责分析与创作，确定性引擎负责校验、编译与渲染 —— 点开任意模块，就是一张更精细的子图。</b></p>

---

## 0. 一句话

Normify 是 **DeepSeek Harness（DSH）插件**，也是**一套写给 AI 用的开发流程**：

- **给 AI 的**：`normify-gen` 技能 + **31 个 `normify_*` 工具** —— 让模型把仓库分析成模块树结构数据，
  并在后续开发中**先建图后编程、伴随编程改图**（计划态建树 → 逐个实现 → 关单收尾）。
- **给引擎的**：零容忍校验（L1 写时 / L2 全项目 / L3 冻结）+ 确定性编译（`tree.json` 等四件产物，SHA-256 冻结）
  + 渲染数据（`renders/`，决定"每一层怎么画"）。
- **给人的**：**单文件交互式架构图**（`normify.html`）—— 逐层下钻、悬停看介绍、一键中英切换、深链接、
  多树、**API 直连箭头**、跨层聚合、缩放与搜索。零依赖，双击即开。

> 它不是"生成一张图就结束"的工具：结构数据与代码**互为契约**，每次改动都能被 `normify_sync` 检出漂移，
> 并以 `normify_change_close`（**0 error 强制**）收尾，让"代码 → 架构图"永远同步。

<p align="center">
  <img src="https://raw.githubusercontent.com/yan-mc/dsh-normify/main/docs/screenshots/engine.png" alt="引擎层：API 直连箭头" width="100%">
  <br><sub><b>引擎层</b>：14 个模块、API 直连箭头（箭头锚定到具体 API 行）、带标签的子系统依赖、跨层聚合虚线</sub>
</p>

## 1. 它解决什么问题

| 痛点 | Normify 的做法 |
| --- | --- |
| 架构图一画完就过期 | 结构数据是**可校验的源数据**：`normify_sync` 按 `fingerprint` 检出漂移，`normify_change_close` 强制 0 error 收尾 |
| 图太粗，看不出接口契约 | 粒度到**单一功能单元**，API 写在叶子上，箭头可锚定到具体 API（`from_api`/`to_api`） |
| AI 改代码时"看不见全局" | `normify_brief` 给出目标模块契约、影响面（谁依赖我）、规则约束与验收清单 |
| 设计先写代码后补文档，必然漂移 | **计划态先建树**（`state: planned`）→ 实现后 `normify_module_refresh(activate)` 自动转 active |
| 结构规范靠人自觉 | `policy.yml` 架构规则（依赖方向 / 禁依赖 / 无环 / 深度 / 跨树 / 命名）由 `validate` 强制执行 |
| 大仓库一次生成太重 | 增量再生成：只重建受影响子树，`layouts_to_review` 点名要复核的层 |

## 2. 核心特性

### 2.1 数据模型：分形 + 零冗余

- **唯一元素**：整个数据库由无数个结构完全相同的**基本模块**构成（每个模块 = 一个 Markdown 文件）。
- **只存 `parent`**：单方向引用，`children` 由索引导出 —— 不会出现"父子各说各话"。
- **API 只在叶子存一次**：聚合、统计、索引全部是编译期派生数据（`tree.json` / `api-index.json`）。
- **两类边**：containment（树边，导航骨架）+ dependency（箭头，可跨子树、跨树，按 `kind` 着色）。
- **路径式 id + 不变 uid**：AI 沿 id 逐层定位（类二分查找）；`uid` 在改名/移动时保持不变，git diff 稳定。
- **深度不设上限**（0.5.0 起）：想有多细就拆多细，深度不再成为"合并模块"的理由。

### 2.2 三层校验，fail-closed

| 层 | 时机 | 内容 |
| --- | --- | --- |
| **L1** | 每次写入 | 必填字段、id 文法、uid、parent 一致性、双语长度、source/apis/deps 形状、state/replacement |
| **L2** | `normify_validate` | 全项目：唯一性、文件↔id 映射、叶子/非叶子规则、API 键唯一、依赖目标、环、渲染数据交叉校验、架构规则、变更日志、（可选）仓库证据（source 存在性 + 指纹一致） |
| **L3** | `normify_build` | 任何 error 都不产出产物；产出即 SHA-256 冻结进 `receipt.json` |

每条诊断都带 `severity / code / message / subject / evidence / supportedFixes` —— **AI 可自行修复**。

### 2.3 渲染器：单文件、可下钻、API 直连

- 单文件 HTML（内联 CSS/JS，**零外部依赖**、零遥测），双击即开，可直接归档/发人。
- 逐层下钻 + 面包屑 + 搜索（模块名/API）+ 大纲视图 + API 浏览器。
- **API 直连**：叶子框内展示 API 明细行，箭头锚定到具体 API 行的端口；同一 API 行上的多条边自动扇形分离。
- 跨层依赖聚合为虚线 `×N`（默认隐藏，工具栏或 `?agg=1` 开启，悬停看明细）。
- 深链接：`#module=<id>`、`#api=<rpc:key>`、`#view=outline`、`?lang=zh|en`、`?agg=1`；缩放 / 悬停高亮 / 明暗主题。
- **几何自检**：仓库自带 `check-geometry.mjs`，逐层断言"线不出界 / 不贴框 / 不穿框 / 不压线"。

### 2.4 伴随开发：先建图后编程

```
change_open → brief → check → module_batch(state=planned) → 【写代码】
   → module_refresh(activate) → change_close(0 error 强制) → verified + revision.after
```

- **计划态**：源码还不存在也能先建树（`fingerprint: pending`），`validate` 放行；
- **禁止假激活**：源码没落地就 `activate` 直接被拒；
- **收尾即闭环**：`change_close` 会刷新指纹 → 校验（0 error 强制）→ 编译（可选渲染）→ 标记 `verified`，
  任何一步失败都不关闭，变更保持原状态；
- **改图随代码**：`normify_sync` 用 `git diff` + 未跟踪文件定位受影响模块与指纹漂移，`module_patch` 跟随更新。

### 2.5 架构规则先行（policy.yml）

| 规则 | 作用 |
| --- | --- |
| `dependency-direction` | 层顺序即允许的依赖方向（如 plugin → tools → engine），可控制同层是否允许 |
| `forbid-dependency` | 禁止某些 from → to 的依赖（可按 kind / state 过滤） |
| `acyclic` | 依赖图禁止成环（可含跨树） |
| `max-depth` | id 段数上限（**可选**：不写就是不限，0.5.0 起默认不限） |
| `cross-tree` | 跨树依赖策略：`forbid` / `allow` / `require-to-api` |
| `naming` | 作用域内 id 段的命名正则 |

安装后 `normify_validate` / `normify_build` / `normify_check` 全部强制执行；**违规先改设计，不能绕过**。

## 3. 最新变化

### v0.5.4 · 把"第二轮 A/B 实测"暴露的 4 个工具缺陷修掉（当前版本）

第二轮 A/B 换了题目（**表格公式引擎 + CLI**，同一份规范、隐藏黑盒 88 项、外加**差分模糊测试**）。
两组最终 B 88/88、A 87/88（差异只有一条 §5.2 语义）；这一版修的是**工具侧**新暴露的 4 个坑：

- **`mode:"patch"` 的静默 no-op 被拦下**：原来 `items:[{patch:{id, tags:[...]}}]`（少一层包装）会返回
  `ok:true, count:1` 却**一个字段都没改**——最危险的"假成功"。现在直接报 `args/invalid-patch`，
  evidence 里给出收到的键与正确形状 `{patch:{id, patch:{...}}}`；单模块 `normify_module_patch` 传空补丁
  同样报 `args/empty-patch`（只给 `expect_updated_at` 也不再静默通过）。
- **`normify_module_refresh` 不再强依赖 git**：`repoRoot` 不是 git 仓库时，以前直接
  `refresh/git-failed` 失败（实测中 AI 只能 `git init` 才能激活模块）。现在改成**降级**：指纹照常重算、
  `state` 照常激活，`revision` 保持模块原值，并给出 `refresh/git-unavailable` 警告与修法。
- **`change_open` 的 `acceptance` 报错具体化**：以前把 `{zh,en}` 写进 acceptance 只有一句笼统报错；
  现在明确写出"**第 N 条不是非空字符串（收到 …）：验收标准只接受纯字符串**"，并提示双语描述写进 `title`/`intent`。
- **`normify_help` 支持 `topic:"tool:<工具名>"`**：`tools` 主题现在每个工具都带**必填/可选**摘要，
  新主题可按需打印**完整参数树**（类型 / 描述 / 必填，由注册表实时生成、与运行时校验同源）。
  实测里 AI 为确认 `mode=patch` 的嵌套形状去读了插件源码——这条主题正是为了消灭这种绕路。

### v0.5.3 · 把「伴随编程实测」暴露的 4 个摩擦点修掉

这四个问题来自一次真实的 A/B 对照实验：两个 AI 用同一份规范写同一个后端，一个带插件走伴随流程、一个纯手写
（最终代码在隐藏黑盒验收上都是 **42/42**）。插件组多交付了 41 模块 / 110 API / 10 层的结构数据，但也踩到了下面 4 个坑：

- **`normify_help` 支持 `topic`**：此前它完全忽略入参，只返回同一份字段速查 —— 实测里 AI 为了拿准
  `change_open` / `layout_upsert` / `change_close` 的参数名，只能去读插件源码（多花约 4 分钟）。
  现在按主题返回：`fields`（默认）/ `deps`（箭头与 API 直连）/ `renders` / `flow`（伴随流程）/ `tools`（工具清单）/
  `policy` / `errors`（常见诊断码与修法）/ `all`；**传错主题会直接报错并列出可用主题**，不再静默忽略。
- **项目初始化通道**：新增第 31 个工具 `normify_project_init` —— 建 `normify-<slug>/` + 默认架构规则，
  可选 `root` 一步创建"计划态根模块"（幂等）；同时 `normify_change_open` 现在也会**自动建项目目录**
  （此前报 `project/no-modules`，AI 只能用 `module_batch {items:[],dry_run:true}` 绕过去）；
  `normify_brief` 遇到不存在的模块会给出"先 init / 先建树 / 改用 task"的可执行提示。
- **批量诊断的因果链**：一条 `label-too-long` 曾连带出 3 条 `dep/target-missing`（因为 L1 失败的模块会被移出批次工作集），
  AI 只能去读源码才能确认根因。现在连带错误改报 `dep/target-dropped` / `structure/parent-dropped`，
  在 message 与 evidence 里点明**根因诊断码**，并在失败响应的 `root_causes` 里直接列出被丢弃的模块（附 `hint`）。
- **「API 直连」引导**：两端都声明了 API 却没写 `from_api` / `to_api` 的箭头，`normify_validate` 会给出**聚合**
  warning `dep/unanchored`（条数 + 前 3 条示例）。这正是实验里被浪费的能力：110 条 API 声明，54 条箭头 0 条锚定 ——
  不锚定，箭头就只能落在框边，钉不到 API 行上。**引导≠放宽**：锚错键仍然是 error。

### v0.5.2 · 修掉三处会写坏数据的真实缺陷

- **`normify_module_upsert` 的必填表不再丢失**：`parameters.required` 恢复为 `["frontmatter"]`，
  `frontmatter` 的 9 个必填字段（uid / id / parent / name / description / source / revision / updated_at / fingerprint）
  也重新出现在 schema 里。此前嵌套 schema 被二次编译，必填表被整段丢掉 —— 模型看到的约束与运行时实际校验不一致。
- **`normify_module_move` 迁移渲染数据时重写内容**：`id` / `order` / `groups.children` / `edge_hints` 全部改写到新 id，
  并同步维护**旧父级**（删掉已迁出子模块的引用）与**新父级**（把新 id 补进 `order`）。
  修复前：move 完之后项目立刻被 L2 判为 `layout/id-mismatch` + `layout/order-child` 等（实测 8–9 个 error，0.5.2 后为 0）。
- **晋升为容器时不再把 API 留在容器上**：叶子被晋升（显式 `normify_module_promote`、写子模块自动晋升、move 到叶子底下）
  时，容器上残留的 `apis` 会被摘除，并回报 `structure/api-dropped-on-promote` 警告（附丢失的 API 键清单）——
  修复前项目会直接卡在 `api/non-leaf`。
- **API 默认全展开**：渲染数据字段 `max_api_rows` 缺省 **0 = 全部展开**，叶子上的 API 一行不折叠；需要收窄时显式写 1..48。
- 三处缺陷各自配了回归断言：`tests/regression-0.5.2.mjs`（34 项，全绿）。

### v0.5.1 · 渲染器防重叠（线压线 12 → 0）

- **修复连线共线重叠**：28 层合计 **12 处 → 0 处**。四处根因：
  ① 首选路由只判"不穿别人的框"，从不检查是否压到已画的线 → 改为只接受 `violations === 0` 的候选；
  ② API 锚定端口没有端口分离（同一 API 行被多条边共用） → 行内 ±5.5px 扇形分离；
  ③ API 端口落在上下边时被放进框内部 → 上下边退回按边均匀分离；
  ④ `segClear` 整块跳过源/目标框 → 新增"进入自身框内部"检查（内缩 2px）。
- 节点/分组间距 170 → 220，给密集层更多自由通道。

### v0.5.0 · 取消模块数量上限

- **删除 `MAX_DEPTH = 12`** 硬限制：树可以一直下钻到"单一功能单元"；需要限层时用 `policy.yml` 的
  `max-depth` 规则显式声明（`maxDepth` 放宽到 1..64）。
- SKILL：目标深度改为"不设上限"，单批上限 40 → 200，新增"每叶 API 尽量 3–5 条"的粒度指引。
<details>
<summary>更早的版本