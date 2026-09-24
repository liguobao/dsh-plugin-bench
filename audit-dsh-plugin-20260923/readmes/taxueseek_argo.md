<p align="center">
  <img src="assets/readme/hero.svg" width="100%" alt="Argo 阿尔戈：给 Agent 用的搜索，argo 的定位是不依赖任何订阅/账号体系的自主搜索基础设施，能够超越大部分 agent 的原生搜索能力">
</p>

<p align="center">
  <strong>中文</strong> ·
  <a href="README.en.md">English</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

<p align="center">
  <a href="#这是什么">介绍</a> ·
  <a href="#它和模型自带搜索-ai-搜索-聚合搜索比强在哪">对比</a> ·
  <a href="#问啥像啥">证明</a> ·
  <a href="#它怎么工作">机制</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#能做什么">能力</a> ·
  <a href="#安装与配置">配置</a> ·
  <a href="#最近更新">更新</a>
</p>

<p align="center">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="python" src="https://img.shields.io/badge/python-3.9+-green">
  <img alt="version" src="https://img.shields.io/badge/version-2.8.9-informational">
  <img alt="engines" src="https://img.shields.io/badge/engines-237-orange">
  <img alt="mcp" src="https://img.shields.io/badge/MCP-14%20tools-purple">
</p>

> **这是踏雪寻仙 DeepSeek Harness 插件系列的一员**，作者还有其他的优秀插件：[dsh-files](https://github.com/taxueseek/dsh-files)（传文件读文档） · [dsh-snippets](https://github.com/taxueseek/dsh-snippets)（片段收藏夹） · [dsh-healthcheck](https://github.com/taxueseek/dsh-healthcheck)（只读体检） · [dsh-plugin-guard](https://github.com/taxueseek/dsh-plugin-guard)（插件安全审计） · [taxue-dsh-artisan](https://github.com/taxueseek/taxue-dsh-artisan)（提示词反推与多供应商生图）—— 完整插件栏目见[个人主页](https://github.com/taxueseek#deepseek-harness-%E6%8F%92%E4%BB%B6)

## 它和「模型自带搜索 / AI 搜索 / 聚合搜索」比，强在哪

> 简单来说：前三种方案解决「**人**找信息」，Argo 解决「**Agent 及搜索核查于一身，具备一条龙的搜索服务**」。差别不在界面，在交付物，给人看的叫总结页或链接清单，给 Agent 的应是能排序、能复核、不撑爆上下文的优质内容，更可靠的搜索信息。

<p align="center">
  <img src="assets/readme/why-better.svg" width="100%" alt="左侧三种默认搜索给人看的结果，右侧 Argo 给 Agent 的可吸收证据 JSON">
</p>

| 维度 | 模型自带搜索 | AI 搜索（总结型） | 聚合搜索 / 搜索引擎 | **Argo** |
|------|------------|-------------------|---------------------|----------|
| 结果形态 | 拼好的长文本 | 给人看的总结页 | SERP 链接清单 | **精简 JSON：证据候选 + 可信度分解** |
| 垂直问题（行情 / 化学式） | 泛搜网页 | 泛搜再总结 | 泛搜网页 | **直连垂直源，直接给答案** |
| 证据可信度 | 无评分 | 无结构化评分 | 无评分 | **selection · absorption · freshness · 共识** |
| 重复查询 | 每次都打网 | 每次都打网 | 靠页面缓存 | **双层缓存（内存 + SQLite），热查询约 10ms** |
| 成本控制 | 不可控 | 单次贵 | 免费但费事 | **预算模式，免费优先，Key 全可选** |
| 多语言 | 随模型走 | 随模型走 | 随引擎走 | **语言检测 + 引擎语言参数 + 多国语言支持** |

> 机制上，Argo 把搜索当成一条**证据管线**：语言检测 → 领域路由 → 多引擎召回 → RRF 融合 → 证据快评，交付的是 Agent 可直接排序、可 `fetch` 复核、不撑爆上下文的材料。工具链不用换，需要换的是「搜索结果应该长什么样」——再往下一层，还有和「再包一层搜索 API 的差别」，那是实现细节的对比。

---

## 2026，检索正在发生什么变化

Agent 干活的量级变了，检索的玩法跟着变了四件事，每一件 Argo 都已经落在代码里：

1. **检索从「给链接」变成「给证据」。** Agent 不看网页排版，它要能排序、能复核、不撑爆上下文的结构化材料——所以 Argo 交付的是带可信度分解的 JSON，而不是 SERP 清单。
2. **上下文成为第一成本。** 一次网页抓取动辄上万 token，Agent 的窗口烧不起。Argo 的 Agent 档单次约 3.7KB，字段集合与字节预算都有检查卡着，升级不会悄悄变胖。
3. **网站开始为 AI 备料。** llms.txt 标准与 `.md` 直出在头部文档站快速铺开——Argo 抓取链第零级自动探测这些 AI 友好变体，命中即跳过整条反爬链；HTTP/TLS 都失败还有 r.jina.ai 阅读器级保底。
4. **免费开放生态够用了。** 政府、学术、标准、安全机构的开放 API + 免 key 引擎，已经能覆盖大多数领域（198 个免配置源）；稀缺免费额度（firecrawl 1000 credits/月、stackexchange 300 次/天）做了「日常补位、关键顶上」的分层，订阅墙不是唯一解。
5. **检索质量从「感觉」到「度量」。** 排序有金标（MRR/nDCG 地板）、融合有增益消融检查、路由有负向控制矩阵——「这版比上版好吗」从此是数字问题，不是玄学。

> v2.8.9 把以上全部落地：237 个源、92 个领域、198 个免配置开箱。逐项细节见 [docs/为什么选择argo.md](docs/为什么选择argo.md) 与 [发布说明](docs/RELEASE_NOTES_v2.8.9.md)。

---

## 这是什么

**Argo 是给 AI Agent 用的多语言搜索基础设施。**

真实检索从来不是「一种语言 + 一个搜索框」：有人问 A 股行情，有人问 World Cup，有人用日文找动画，有人要 IMDb 上的导演信息。Argo 的出发点很朴素——**按领域、按语言、按需求选路**，把问题送到合适的源，而不是一律扫网页标题。联网搜索与本机文件搜索一体可用。

> 产出不是「链接清单」，而是「证据候选 + 可信度分解」。路选对了，证据才站得住。

### 和「再包一层搜索 API」的差别

| 常见做法 | Argo |
|---------|------|
| 绑死一个引擎、一个 Key | 多引擎自动选路，免费优先、可配预算 |
| 啥问题都泛搜网页 | **垂直源优先**：行情、影视、体育、宏观、化学等先给答案型结果 |
| 默认只按中英优化 | **多语言识别 + 引擎语言参数 + 跨语言回退** |
| 搜完直接拼摘要 | 选择门槛 × 证据密度 × 时效 × 多源共识 |
| 引擎挂了整条链路挂 | 熔断、负缓存、分阶恢复（防垂直源串味） |
| 每次查询都重新打网 | 双层缓存（内存 + SQLite），热查询约 10ms 级 |
| 日常和研究一个慢 | **日常少开引擎、研究再放宽** |
| Agent 上下文被长 JSON 撑爆 | MCP 响应可紧凑裁剪，snippet 可控 |

---

## 问啥像啥

<p align="center">
  <img src="assets/readme/proof-routes.svg" width="100%" alt="四类真实路由：金融、影视、多语言、地理">
</p>

| 你这样问 | 大致会怎样 |
|----------|------------|
| python asyncio error handling | 编程问答域 → StackOverflow/StackExchange 官方 API，带得分与采纳标记 |
| AAPL / 美股盘前 | 美股域，与 A 股分流 |
| 肖申克的救赎 主演 / Inception director | 影视域 → IMDb 等 |
| 梅西 俱乐部 / 库里 球队 | 体育域 → TheSportsDB 等 |
| 埃菲尔铁塔在哪 / where is Eiffel Tower | 地理实体 → OpenStreetMap 等 |
| NASA founding year / 国务院职能 | 组织实体 → Wikidata 等 |
| 周杰伦 专辑 / Taylor Swift album | 媒体域 → iTunes 等 |
| アニメ おすすめ / 한국 영화 추천 | 识别日/韩语 → 语言友好源，少塞中文专用站 |
| 美国 CPI、日本 通胀率 | 宏观数据域；国别分流（本国权威源优先） |
| log4j 漏洞 CVSS / nodejs 22 end of life | 安全域 → NVD 官方；生命周期域 → endoflife.date |
| attention is all you need | 学术域 → arXiv/OpenAlex/CrossRef，元数据与 DOI 直连 |
| 阿司匹林 分子式 | 化学域 → PubChem 类答案 |
| 台积电估值分歧（深度研究） | 拆子问题 + 多源并行，垂直源被 boost |

---

## 它怎么工作

<p align="center">
  <img src="assets/readme/workflow.svg" width="100%" alt="查询 → 语言与域 → 多引擎召回 → RRF → 证据快评 → 统一 JSON">
</p>

```
查询
  ├─ 意图消歧（可选）
  ├─ 查询改写（可选；路由仍看原始意图）
  ├─ 语言检测 + 语言偏好
  ├─ 路由（域规则 + TF-IDF + 预算 + 语言补充源 + 热路径缓存）
  ├─ 多引擎召回（熔断 / 负缓存 / 并行）
  ├─ 空结果分阶恢复（放宽 → 换同族/通用 → 跨语言；防污染）
  ├─ RRF 融合 + 可选精排
  ├─ 证据快评（权威 · 证据密度 · 时效 · 共识）
  └─ 统一 JSON（含 engine_outcomes / recovery / route_reason）
```

### 证据评分（简版）

```
selection  ≈ 域名权威，SERP/跳转链压到很低
absorption ≈ 数字 / 定义 / 对比 / 披露等证据密度
freshness  ≈ 发布时间（会忽略「2015 年以来」这类历史对比年）
综合       ≈ 0.40·selection + 0.35·absorption + 0.15·freshness + 0.10·引擎分
```

结果字段含 `selection`、`absorption`、`credibility_fast`、`evidence_flags` 等，方便 Agent 直接排序。

### Agent 使用纪律（建议）

1. **高后果问题**（持仓、安全、是否属实）：search → 看快评分 → 对 top 结果 `fetch` → 再下结论  
2. **数字**：写清计算方式，冲突时并列，不要硬合并  
3. **搜索结果页 / 跳转链**：不要当正文信源  
4. **社交帖**：当舆情与叙事，不当事实真值  
5. **事实核查**：宁可多一两条分层查询（来源 / 对比 / 主体）

---

## 快速开始

任选一种即可。**以 GitHub 为唯一安装来源**（`npx github:taxueseek/argo` 或 `install.sh` / `install.ps1`），当前推荐 **v2.8.9**。**请勿用 `npm install argo-search`**——npm registry 上那份是**非官方陈旧版 v1.0.1**（非本仓库维护，功能残缺、不随本项目更新）。本包 `package.json` 已设 `private: true` 防止误发布到 npm registry。

**零配置就能跑**：不配 API Key 时走免费引擎 + 本地 `local_*` 引擎；配了 Key 的源质量通常更好，没配则自动跳过。

### 方式一：一键脚本（推荐本机长期用）

macOS / Linux：

```bash
curl -fsSL https://raw.githubusercontent.com/taxueseek/argo/main/scripts/install.sh | bash
```

Windows（PowerShell）：

```powershell
powershell -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/taxueseek/argo/main/scripts/install.ps1 | iex"
# 或下载后执行：
# powershell -ExecutionPolicy Bypass -File scripts/install.ps1
```

装到指定目录、并挂 Skill 入口：

```bash
curl -fsSL https://raw.githubusercontent.com/taxueseek/argo/main/scripts/install.sh \
  | bash -s -- --home "$HOME/.local/share/argo" --link "$HOME/.claude/skills/argo"
```

验证：

```bash
python3 ~/.local/share/argo/scripts/search.py "python asyncio error handling" --json
python3 ~/.local/share/argo/scripts/search.py --list-engines
```

### 方式二：MCP 不装包，直接用 GitHub（推荐 Agent 快速挂载）

需要 **Node.js 18+** 和 **Python 3.9+**，首次执行一次：

```bash
pip3 install pyyaml
```

```bash
npx -y github:taxueseek/argo
```

客户端配置示例（Claude Code / Cursor / Kimi 等）：

```json
{
  "mcpServers": {
    "argo": {
      "command": "npx",
      "args": ["-y", "github:taxueseek/argo"]
    }
  }
}
```

### DeepSeek Harness 一键插件（.dsh-plugin bundle）

在 DeepSeek Harness 里一行安装（两种装法）：

```bash
# 装法 A：14 个 mcp__argo__* 工具（主包自带 bundle，与 MCP 全量相同）
dsh plugin --profile web add "github:taxueseek/argo"

# 装法 B：搜索工具 + wide_research 并行研究调度（子包）
dsh plugin --profile web add "github:taxueseek/argo#main&path:packages/dsh-plugin"
```

重启 `dsh web` 后生效。包结构见 `packages/dsh-plugin/`；同 id `mcp-argo` / `wide-research` 可在用户层 `cordis.patch.yml` 覆盖。装法 B 的 `wide_research` 模块只存在于子包依赖树，主包 patch 不引用它，避免只装主包时 Cordis 解析失败。

### 依赖清单（通俗版）

| 依赖 | 必需？ | 干什么用 | 不装会怎样 |
|------|:------:|---------|-----------|
| **PyYAML** | ✅ 必需 | 读配置文件 | 完全跑不起来，安装脚本会自动装 |
| **curl_cffi** | ❌ 可选（v2.7.3 新增） | 模拟浏览器 TLS 指纹，过反爬站（Cloudflare 等） | 反爬站抓取成功率低一些，日常搜索无影响 |
| **ddgs CLI** | ❌ 可选 | 本地免 key 搜索的 10 个后端引擎 | 少一批零成本本地搜索源，其余不受影响 |
| **realtime-index CLI** | ❌ 可选 | 实时索引引擎（搜刚发布的内容） | 该引擎自动禁用，显式指定会回退通用引擎 |
| **Chrome** | ❌ 可选 | 页面截图、JS 渲染页、登录态抓取 | 截图工具不可用，其余正常 |
| *