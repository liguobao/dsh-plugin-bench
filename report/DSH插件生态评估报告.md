# DeepSeek Harness（DSH/dsh）插件生态评估报告

> **单一权威版本**：整合 v1 全景审计、v1.1 适配型剔除、v2 原生视角、v3 活跃清单（1,150 逐仓）与 star≥10 宇宙计算。原独立分册（原生插件整理、活跃插件全量清单分析）已并入本文，不再单独保留。

- **评估日期**：2026-08-22
- **数据来源**：GitHub API 实测抓取（非目录站转述）
- **枚举范围**：`dsh-plugin` topic 官方计数 10,529 个，实际去重枚举 **9,393 个**（覆盖率 89%，缺口为评估当日新建仓库）
- **深读范围**：star ≥ 10 全部 **701 个** README 逐个阅读；「活跃 × 有星」交集 **1,150 个** README 逐个阅读（1,149 可读，1 个无 README）
- **活跃度口径**：以官方 **v0.1.1-rc.1**（2026-08-21 07:12 UTC 发布，含破坏性变更）发布时间为锚，`pushed ≥ 该时间` 记为"已适配/真活跃"
- **数据文件**：`data/repos.jsonl`（9,393 元数据）、`data/active_inventory.md`（1,150 逐仓 27 品类清单）、`data/native_plugins.jsonl`（538 原生清单）
- **复现**：`skills/github-topic-audit/`（审计 Skill）、`scripts/classify_native.py`（三桶判定）、`scripts/make_charts.py`（图表）

---

## ⚠️ 特别声明：关于"擦边"插件的处理

本报告不把两类仓库与真正的 DSH 原生插件混排：

1. **适配型独立产品（62 个，占 top 701 星数的 61%）**：先有产品/品牌、后顺手接入或贴上 `dsh-plugin` 标签——OpenViking（火山引擎通用上下文库）、MemOS / EverOS / mem9 / mnemon（通用记忆产品）、ruflo（Claude Code/Codex 元 harness）、open-design、WeKnora、PicGo（2017）、NocoBase（2020）、hol-guard、EchoBird 等。它们的兴衰不由 DSH 生态决定。
2. **蹭 tag / 无关 / 空壳（约 100 个）**：reactive-resume（41.5k★）、Aria（C++ 框架）等与 DSH 毫无关系的知名项目靠打标签引流。

**处理**：判定规则固化为 `scripts/classify_native.py`（native 538 / adapted 62 / unrelated ~100，含 40 项 PRODUCT_FIRST 人工覆盖名单与 2026-02 时间线规则）；正文榜单与选型建议默认只面向原生插件；生态级统计（总量、rc.1 活跃率）仍基于全量 9,393 仓库。**剔除 ≠ 否定价值**：OpenViking/MemOS 作为外接记忆底座依然可用，但那是"选数据库"，不是"选 DSH 插件"。

---

## 一、核心结论（TL;DR）

1. **总量与内核**：topic 仓库 10,529 个，rc.1 后仍活跃仅 **20.6%**（1,932）；「活跃 × 有星」交集 **1,150**；star ≥ 10 宇宙 701 个中活跃 305 个。**真正值得持续追踪的观察名单 ≈ 305，其中原生且活跃 ≈ 236。** 86% 的仓库 star 不足 5，48.3% 只在创建当天推送过一次。
2. **活跃度必须用"破坏性变更锚点"衡量**："近三天有 push"口径（38.7%）是发射噪声；rc.1 锚点下另有 31.2% 在 rc.1 前已停滞。100★+ 头部也只有 59.4% 跟进——**star 与维护度不挂钩**。
3. **star 榜被适配型主导**：剔除 DSH 本体后 star 前 11 名全部不是原生插件（open-design 90k、ruflo 68.8k、reactive-resume 41.5k、DeepSeek-Reasonix 35k、OpenViking 31.8k、PicGo 27k、colleague-skill 23.8k、NocoBase 23.8k、WeKnora 20.3k、voyager 19.8k），第一个原生要数到第 12 名（anywhere-labs 桌面端，18k★）。
4. **原生基本盘**：视觉桥、桌面/TUI 交互层、策展市场、远程访问——需求由 DSH 特性直接派生（纯文本模型、Web 优先、万物皆插件）；记忆底座之争已让位给外部平台，原生层在争**治理与整理**（审批门、审计、自进化，品类 rc1 率 70% 全场最高）。
5. **最大缺口是安全**：原生安全插件无一同时满足 200★+ 与 rc.1 适配，供应链风险敞口与防护装机量严重失衡。
6. **娱乐层全部存活**：40 个桌宠/皮肤/小游戏在 rc.1 后都有 push——玩物是留存粘合剂，不是弃物。

---

## 二、方法论

| 步骤 | 做法 | 局限声明 |
|---|---|---|
| 全量枚举 | Search API 按 star 分桶 + 创建日期递归二分，绕过单查询 1000 条上限（离线单测覆盖） | 当日新建 ~1,100 个未覆盖 |
| README 深读 | star ≥ 10 的 701 个 + 活跃×有星 1,150 个（前 8KB）逐个阅读 | star<10 的非活跃长尾仅元数据统计（48% 一次性，逐读边际价值极低） |
| 活跃判定 | rc.1 发布时间戳（2026-08-21T07:12:39Z）前后是否有 push | 皮肤类可能不受 API 破坏影响；锚点后 36h 内"未跟进"是风险指标而非死亡判决 |
| 原生/适配/蹭tag | 时间线（2026-02 后创建）+ DSH-first 定位 + 40 项人工覆盖名单 | 边界争议项存在（如 engramory 因"your host's rules file"定位归入剔除） |
| 品类分类 | 关键词预分类 + 全量逐行人工校正（27 品类 + 显式覆盖表） | 1,150 中 16 个无法判断归"其他" |

---

## 三、规模与增长

- **增长曲线**：生态从 2026-07 底萌芽。创建数：08-13 639 → **08-14 峰值 1,508** → 08-15 1,385 → 08-16 1,289 → 08-17 953 → 08-18 671 → 08-19 872 → 08-20 917 → 08-21 513 → 08-22（半天）113。
- **星标金字塔**：100★+ 180（1.9%）｜20–99★ 249｜5–19★ 869｜1–4★ 3,592｜0★ 4,503——86% 不足 5 星。
- **语言**：JS 5,440 + TS 2,975 ≈ 90%（Cordis 插件体系决定）；Python 378、Rust 78、PowerShell 64。
- **生命周期**：48.3% 只在创建当天 push 过；仅 25 个归档——没人退出，只是不再回来；10.4% 无描述。

## 四、活跃度：rc.1 试金石

| 星级段 | 已跟进 rc.1 | 真活跃率 |
|---|---|---|
| 100★+ | 107/180 | **59.4%** |
| 20–99★ | 108/249 | 43.4% |
| 5–19★ | 226/869 | 26.0% |
| 1–4★ | 709/3,592 | 19.7% |
| 0★ | 782/4,503 | 17.4% |
| **全量** | **1,932/9,393** | **20.6%** |

「活跃 × 有星」交集：≥1★ **1,150**/4,890（24%）｜≥5★ 441/1,298（34%）｜≥10★ 305/701（44%）｜≥20★ 215/429（50%）｜≥100★ 107/180（59%）。

全生态真正跟得上版本节奏的估算为 700–900 个；其中 DSH 原生插件的 rc.1 跟进率为 44%（236/538），显著健康于全量。

## 五、star ≥ 10 分析宇宙（701 个）

| 层 | 数量 | 占比 |
|---|---|---|
| 全部 | 701 | 100% |
| ├─ rc.1 后仍活跃 | 305 | 43.5% |
| └─ rc.1 后无动静 | 396 | 56.5% |
|    ├─ 曾维护、后停滞 | 348 | 真掉队 |
|    └─ 一次性（仅创建日 push） | 48 | 交作业 |

与原生口径交叉：原生 538 中活跃 236（44%）；非原生 163 中活跃 69（42%）——**是否原生与维护意愿无关**，被适配进来的成熟项目同样在跟进 rc.1。

**高星掉队名单**——确定性：▲EverOS（12.3k★，8/17 起）、dsh-anchored-standard（3.7k）、Vibe-Skills（3k）、zhuzhiliao（2.9k）、last30days-skill-cn（1.5k，7/20 起）、▲openpets（1.1k）；临界（差几小时未过锚点）：colleague-skill（23.8k）、▲yao（7.8k）、agent-vision-toolkit（1.1k）。带 ▲ 者为适配型，仅作数据点。

## 六、原生 vs 适配 vs 蹭 tag

| 桶 | 仓库数 | 星数 | 星数占比 |
|---|---|---|---|
| native（为 DSH 而建） | 538（77%） | 266,115 | 33% |
| adapted（先有产品后接入） | 62（9%） | 496,636 | 61% |
| unrelated（蹭 tag/无关/空壳） | ~100（14%） | 39,696 | 4% |

典型剔除分组：**记忆厂商组**（OpenViking 31.8k、MemOS 10.9k、EverOS 12.3k、mem9、mnemon、MindMemOS、graph-memory、memtrace——v1 初版的明星记忆阵容全部产品优先）；**独立产品贴牌组**（PicGo、NocoBase、Yao、DeepSeek-Reasonix 竞品 harness、open-design、ruflo、WeKnora、voyager、archify、colleague-skill、petdex、ouroboros、openpencil、iPolloWork）；**泛 host 协议组**（hol-guard、engramory、MisakaNet、Co-Engram、cc-notify-hooks）。

## 七、品类全景

### 7.1 全量计数（1,150 活跃插件，27 品类校正版）

| 品类 | 数量 | 头部代表 | 判断 |
|---|---|---|---|
| 会话/Web UI 微增强 | 169 | DSH-better-sidebar（2.6k）、dsh-genui | **第一大类但极碎片**：导航条×8、折叠×5、输入历史×4、撤回×4——官方 UI 只交付了 MVP，细节全靠社区补 |
| 搜索/网页/浏览器 | 89 | BrowserSkill（1.3k）、dsh-free-search、modsearch（2 月元老） | 刚需，装了就回不去 |
| 桌面客户端/启动器 | 88 | anywhere-labs（18k，原生星数第一）、hairyf（907，Tauri 5MB） | 同质化最严重，第 5 名后不必看 |
| 插件市场/目录 | 83 | awesome-dsh-plugin（11.3k）、AdamPlatin123（1.3k，唯一容器实测） | 五种形态内卷；可信度：实测＞人工核实＞自动同步＞静态 |
| 订阅/Provider/路由 | 80 | dsh-plugin-subscriptions、codex-oauth 系 | 原生数量最大质量最稀（品类 rc1 率 32%），踩 ToS 红线 |
| 编排/多Agent/工作流 | 73 | dsh-agent-teams（784）、taskboard 系、dsh-cron | 第二增长曲线：单会话→团队看板/后台代理/定时任务 |
| 用量/计费 | 58 | TokenLedger（130）、dsh-cost-meter（153） | 同质化重灾区；峰谷计费自成迷你亚品类（≥7 个错峰省钱插件） |
| 记忆/知识库 | 55 | 官方 dsh-mnemon、dsh-memory-evolve（218）、dsh-noema（121） | 原生层争治理与整理，品类 rc1 率 70% 全场最高；原生记忆竞争 rc.1 前一周才爆发（全部创建于 08-05 后） |
| 工程化/Git/CI | 51 | dsh-auto-review（73）、checkpoint-rewind、harness-action | Claude Code 能力补齐 |
| 垂直领域 | 49 | A股研究、数学建模、EDA（easyeda）、J-Link 调试、ROS2 | "一切皆插件"兑现最充分 |
| 技能包/预设 | 47 | superpowers 移植系、anchored-standard（3.7k，未适配） | 玄学重灾区但有真实用户 |
| 安全/权限/治理 | 41 | dshscan、auto-approve 系、dsh-defend、time-travel | 完整防御谱系（权限档→注入防御→静态扫描→运行时防护→时间旅行审计），但无 200★+ 且适配 rc.1 者 |
| 视觉/多模态 | 40 | modlens（3.5k，2026-02 元老）、dsh-vision-router（936）、dsh-vision-toolkit（805） | 纯原生赛道，由 V4 纯文本派生 |
| 娱乐/桌宠/皮肤 | 40 | dsh-pet（311）、petdex 画廊、鲸鱼娘系 | 活跃的玩具层，留存粘合剂 |
| IM/通知 | 30 | dsh-im（470，9 渠道）、飞书家族 | 中文生态特色，飞书系最密 |
| 远程/移动 | 29 | dsh-remote-web-gateway（116）、dsh-mobile-apk（112）、liguobao/deepseek-harness-remote（48） | 三条存活路线：Web 网关 / APK / 中继+多客户端 |
| TUI/终端 | 23 | dsh-TUI（2.3k）、tianshu-tui（自研 ANSI 核心） | Claude Code 风终端壳稳定需求 |
| IDE 集成 / 文件工作区 / MCP / 上下文 / 语音 | 66 | for-vscode、paste-input、mcp-panel、context-doctor、billion-context | 基础体验补齐层 |
| 被适配独立产品 / 教程 / 蹭tag / 其他 | 38 | open-design、learn-harness-engineering（13.6k）、PicGo | 元生态与噪声 |

star ≥ 10 活跃子集（305 个）的结构差异：市场/目录（29）与桌面客户端（28）占比大幅上升——基础设施先吃到 star；1–9★ 长尾主力"Web UI 微增强"在此仅排第四——微增强类做的人多、拿到的认可少。

### 7.2 原生产品线细节（v1.1 口径）

**① 记忆/知识（原生约 14 个，rc1 70% 全场最高）**：dsh-memory-evolve（218★，五轨记忆 + git 分支感知 + 后台自进化）、官方 dsh-mnemon（169★，三层控制平面 + 9 provider）、dsh-noema（121★，durable & inspectable）、dsh-memento（59★，审批门 + 审计轨迹）、dsh-meow-memory（33★，七层 SQL）、dsh-mneme（32★，autoDream）、dsh-memoir（18★，PROJECT_MEMORY.md 沉淀）、dsh-knowledge（10★，RAG）。

**② 视觉桥（12 个，纯原生赛道，rc1 58%）**：modlens（3.5k，2026-02 元老）、dsh-vision-router（936，内置免费视觉 API）、dsh-vision-toolkit（805）、dsh-browser（383，Chrome 侧边栏）、picturereader（32）。

**③ 桌面客户端/启动器（30 个，rc1 53%）**：anywhere-labs（18k，原生星数第一）、hairyf（907，Tauri 5MB）、lencx/Minke（391）、dsh-at-file（453）、fufankeji studio（450）、whitelonng/dshcode（191）、Ruler4396/dsh-launcher（170）。

**④ 策展/市场（原生约 35 个，rc1 62% 全场最高，最内卷）**——五种形态：
- a. **静态 awesome 列表（11 个）**：awesome-dsh-plugin（11.3k，头牌，org + 网站、事实目录标准）、0xsline（809）、Zhiyuan-Fan（254）、libukai（184）等；
- b. **自动发现+验证管道（8 个）**：AdamPlatin123（1.3k，唯一 k8s 容器实测、四档判定）、bruc3van（261，日抓+人工核实+明示反蹭 tag）、imsai-sh（156）、dshfind（203）、Oh-My-DSH（68，每 4h 同步）、dsh-suite（44，每小时）等；
- c. **装进 DSH 的一键市场（13 个）**：dsh-market（1.7k 旗舰）、DSH-Plugins-Marketplace（135）、dsh-webui-market-plugin（99）、dsh-find-plugin（75，"找插件的插件"）、2BingLing（51，五维评分）等；
- d. **垂类市场（2 个）**：dsh-skin-market（71，人工审核）、dsh-meme-hub（31）；
- e. **官方配套**：dsh-plugin-check（27，检查 hub 收录状态——官方承认收录体系）。
- ⚠️ 品类内寄生者：**Anil-matcha/awesome-dsh-plugin（973★）创建于 2023-05，老仓库改名蹭热度**且未适配 rc.1；Awesome-AI-Pedia（227）、SkillCorpus（92）、ru-marketplace-mcp（68）亦为蹭 tag。
- 收录数量普遍虚报（自称 1,500–4,310 vs 真实内核 500–900），选型看验证手段而非收录量。

**⑤ Provider/订阅（90 个，rc1 32% 全场最低）**：dsh-anchored-standard（3.7k，**未适配**）、dsh-plugin-subscriptions（232）、dsh-codex-connect（39）、dockyard-dsh（74，账号池）——灰色属性不因原生化洗白。

**⑥ 安全（原生约 13 个，rc1 42%）**：dsh-pentest（189）、dsh-auto-mode（116）、dsh-undo-savepoint（112，崩溃救援）、dsh-auto-review（73）、dsh-plugin-guard（29）、dsh-permission-rules（27）、官方 dsh-security-audit（13）、dsh-plugin-anti-ads（11，反制 dsh-ads 恶搞）。无一是 200★+ 且适配 rc.1。

**⑦ 远程/移动（18 个，rc1 61%）**：见第八节专项。

**⑧ 用量计费（25 个，rc1 44%）**：dsh-cost-meter（153）、TokenLedger（130）、dsh-usage-stats（105）、dsh-damage-pulse（83，扣血动画）、dsh-green-meter（52，能耗/碳排)。

**⑨ 垂直技能（长尾）**：dsh-ios（192，iOS 模拟器）、招聘 copilot（41）、法律诉讼可视化、外贸 SDR（24）、3GPP 协议库（14）、dsh-hdc-bridge（12，鸿蒙）。

**⑩ 官方周边（omdsh-dev，17 个）**：DSH-better-sidebar（2.6k）、dsh-genui（293）、dsh-mnemon（169）、dsh-toolkit、dsh-notification、plugin-template、dsh-plugin-check 等——全部适配 rc.1，原生生态唯一"全绿"产品线。

## 八、Remote 品类专项

| 项目 | Star | rc.1 | 技术路线 |
|---|---|---|---|
| dsh-pocket | 393 | ✗ | 手机扫码同屏 |
| dsh-remote-web-gateway | 116 | ✓ | Web 网关 |
| dsh-mobile-apk | 112 | ✓ | APK 打包 |
| dsh-mobile (saya-ch) | 101 | ✗ | 原生 App（Alpha） |
| **liguobao/deepseek-harness-remote** | **48** | **✓** | **中继 + 端到端加密，多客户端（浏览器/VS Code/Android）** |
| xgone/dsh-remote | 42 | ✓ | LAN 认证层 |
| DeepSeekHarnessRemoteGateway | 19 | ✗ | sidecar 网关 |
| 其余（dsh-tether、dsh-phone、dsh-lan-gate 等） | ≤18 | 部分 | P2P / FRP / Tailscale 教程流 |

按 rc.1 标准，仍在牌桌的前 3–4 名：dsh-remote-web-gateway、dsh-mobile-apk、liguobao/deepseek-harness-remote、xgone/dsh-remote。其中 liguobao 版本是**唯一实现端到端加密 + 中继不可见明文 + 只读文件预览 + 设备级撤销**的方案，安全模型最完整；短板为中继不可自托管（信任模型最大扣分项）与 Host/客户端版本耦合较紧。作者本人项目，利益相关特此披露。

## 九、生产力 vs 玩具 vs 蹭 tag（top 701 人工判定）

| 判定 | 占比 | 说明 |
|---|---|---|
| 真生产力 | ~45–50% | 记忆、视觉桥、远程、计费、安全、IM、垂直技能、深度研究 |
| 有用但同质化 | ~25% | 桌面壳、会话管理、侧边栏、余额挂件——同类第 5 名之后无存在必要 |
| 纯玩物 | ~10%（60–70 个） | 桌宠家族、动漫皮肤（鲸鱼娘/流萤/终末地/赛博朋克/QQ2006）、meme、五子棋、竹知了（2.8k）、SillyTavern 家族。文化现象大于工具价值 |
| 适配型独立产品 | 62 个 / 61% 星 | 已移出正文推荐（见特别声明） |
| 蹭 tag / 无关 / 空壳 | ~15%（约 100 个） | reactive-resume、PicGo、NocoBase、Aria 等引流 + 模板/AI stub |

**star 榜单不可直接作为选型依据。**

## 十、最出色的原生插件 Top 10（原生 + rc.1 适配 + 不可替代；DSH 本体不计入）

1. **modlens**（3.5k★）——生态最早仍在维护的原生插件（2026-02），视觉桥定义者
2. **anywhere-labs/deepseek-harness-desktop**（18k★）——原生星数第一，桌面端事实标准
3. **awesome-dsh-plugin**（11.3k★）——策展头牌，事实目录标准
4. **dsh-web-ui**（5.5k★）——Web 端皮肤/插件集合
5. **omdsh-dev/DSH-better-sidebar**（2.6k★，官方）——侧边栏底座，三方拓展注册
6. **dsh-TUI**（2.3k★）——官方公众号收录的终端补位
7. **dsh-market**（1.7k★）——DSH 内置插件市场
8. **AdamPlatin123/awesome-dsh-plugins**（1.3k★）——唯一容器实测目录，选型可信度最高
9. **dsh-agent-teams**（784★）——多 agent 编排
10. **dsh-context**（778★）——上下文洞察与管理

荣誉提及：modsearch（221，2 月元老）、hairyf 桌面版（907，Tauri 5MB）、官方 dsh-mnemon（169）、liguobao/deepseek-harness-remote（48，唯一端到端加密远程方案）。omdsh-dev 官方全家桶（17 个全适配）可视为第 0 名。
出局警示：dsh-anchored-standard（3.7k）、dsh-pocket（393）——高星未适配 rc.1。

## 十一、逐行理完 1,150 后的新发现

1. **PerryLink 是最高产的"单人插件工坊"**：活跃集 24 个仓库（auto-review、permission-rules、memento、checkpoint-rewind、lsp-actions、defend、local-ai……），全部适配 rc.1——一个人的 JetBrains。
2. **omdsh-dev 官方线 30+ 个活跃仓库全适配 rc.1**——维护纪律明显好于社区平均。
3. **安全类从"洼地"变"暗流"**：41 个活跃仓库自组织形成完整防御谱系，但缺少规模化头部。
4. **远程赛道存活格局清晰**：网关 / APK / 中继三路线；扫码同屏与 FRP 教程流大量死在 rc.1 上。
5. **原生记忆竞争在 rc.1 前一周才爆发**（全部创建于 08-05 之后）——底座之争让位外部平台后，原生层转向治理与整理。
6. **峰谷计费是分时定价催生的电费焦虑赛博复刻**（≥7 个错峰插件：offpeak-saver、tidewatch、peak-pricing 等）。

## 十二、风险与建议

**生态级风险**：① 供应链风险敞口 vs 安全装机量失衡（原生安全无 200★+ 且适配 rc.1 者）；② 48% 一次性仓库 + 下次破坏性变更预计再淘汰一批（rc.1 已示范）；③ 灰色 Provider 插件随时可能因官方收紧批量失效；④ 策展目录普遍虚报收录量，选型看验证手段而非收录量。

**给使用者**：起步用 omdsh-dev 官方线 + awesome-dsh-plugin 精选；核心生产力选已适配 rc.1 的原生头部（记忆官方 dsh-mnemon / dsh-memory-evolve、视觉 modlens、上下文 dsh-context、用量 TokenLedger、安全 dsh-undo-savepoint + 官方 dsh-security-audit）；若外接 OpenViking/MemOS 底座，注意另行评估其 DSH 桥接层维护状态。避开：同质化区（第 5 个以后的桌面壳/余额挂件）、未适配 rc.1 的停滞项目、纯 star 导向榜单、一切"顺手打 tag"的适配型仓库。**选型三指标：适配最新 rc / 持续 push / 被实测型目录收录。**

**给插件作者**：竞争最不充分的三条线——规模化安全防护、企业治理（权限/合规/审计日志）、自托管中继（远程品类共同短板）。跟进 rc 节奏本身就是竞争力信号，适配日志写进 README 能直接转化为信任。

---

## 附录：数据快照与产物

- 抓取时间：2026-08-22（UTC+8）；rc.1 分界时间戳 2026-08-21T07:12:39Z
- 工具：GitHub Search/Repos API（gh CLI）+ 分类脚本（离线单测覆盖枚举逻辑）
- `data/repos.jsonl`（9,393 元数据）｜`data/digest.txt`（700 摘要）｜`data/analysis.json`（预分类）｜`data/active_inventory.md|.json`（1,150 × 27 品类）｜`data/native_plugins.jsonl`（538 原生）
- 复现：`python3 scripts/classify_native.py`（三桶）；`python3 scripts/make_charts.py`（图表）；审计全流程见 `skills/github-topic-audit/`
- 本仓库报告与脚本：MIT；`data/repos.jsonl` 为 GitHub API 公开元数据快照，版权归各仓库所有者
