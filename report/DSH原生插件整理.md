# DSH 原生插件整理（v2 · 剔除「适配型独立产品」）

> 姊妹篇：[DSH插件生态评估报告.md](DSH插件生态评估报告.md)（v1 全景审计）。
> v1 把「独立产品顺手接入 DSH」和「为 DSH 而建」混在一张榜上，star 榜被前者主导。
> 本篇只回答一个问题：**剔除适配型之后，真正的 DSH 原生插件生态长什么样。**

- 数据基础：与 v1 相同的 2026-08-22 快照（top 700 README 深读层）
- 分类产出：`data/native_plugins.jsonl`（538 个原生插件清单）
- 复现脚本：`python3 scripts/classify_native.py`

---

## 一、判定规则

一个仓库算「DSH 原生」需同时满足：

1. **时间线**：创建于 2026-02-01 之后。DSH 生态的可信起点是 2026 年 2 月（modlens 2026-02-22 自称 "first vision plugin for DeepSeek Harness"；官方周边 omdsh-dev 仓库 2026-08 起集中出现）。创建早于这个日期的仓库不可能是为 DSH 而建。
2. **定位 DSH-first**：仓库名含 `dsh` / `deepseek-harness`，或描述/README 以 DSH 为主战场。反过来，"works with DeepSeek Harness, Claude Code, OpenClaw, and any agent runtime" 这类把 DSH 列为 N 个运行时之一的，计为产品优先。
3. **头部人工复核**：高星样本逐个过目，产品优先覆盖名单固化在 `scripts/classify_native.py` 的 `PRODUCT_FIRST`（40 项）。

三个桶：

| 桶 | 含义 |
|---|---|
| **native** | 为 DSH 而建（或以 DSH 为主分发渠道） |
| **adapted** | 先有产品/品牌，DSH 只是接入目标之一；含竞品 harness、多平台工具 |
| **unrelated** | 蹭 tag / 无关 / 空壳（与 v1 的判定一致） |

诚实边界：判定覆盖 top 700 深读层；star < 10 的 8,693 个长尾仓库仅有元数据，不逐一判定。`PRODUCT_FIRST` 是人工判断，存在边界争议项（如 engramory：协议本身泛 host，但 npm 包名叫 `dsh-engramory`——按"主分发渠道"本可保留，最终因定位写明 "your host's rules file" 归入剔除）。

---

## 二、总量重构：砍掉 24% 的仓库，砍掉 66% 的星

| 桶 | 仓库数 | 占比 | 星数 | 星数占比 |
|---|---|---|---|---|
| native | 538 | 77% | 266,115 | 33% |
| adapted | 62 | 9% | 496,636 | 61% |
| unrelated | 100 | 14% | 39,696 | 4% |

两个直接后果：

**1. star 榜前 11 名（除 DSH 本体）全军覆没。** 剔除 `deepseek-ai/deepseek-harness` 平台本体后，star 第 2～11 名全部是 adapted/unrelated：open-design（90k）、ruflo（68.8k）、reactive-resume（41.5k）、DeepSeek-Reasonix（35k，竞品 harness）、OpenViking（31.8k）、PicGo（27k）、colleague-skill（23.8k）、NocoBase（23.8k）、WeKnora（20.3k）、voyager（19.8k）。**第一个原生插件要数到第 12 名**（anywhere-labs/deepseek-harness-desktop，18k★）。

**2. v1 的「最出色插件」榜一半作废。** OpenViking、ruflo、hol-guard 三项按原生标准出局。v1 报告「记忆选 OpenViking/MemOS」的建议，在纯原生视角下不再成立——见第六节修订。

原生插件自身的 rc.1 跟进率为 **44%**（236/538），与全生态 20.6% 相比健康得多，但仍有半数以上没跟上破坏性变更。

---

## 三、剔除名单（adapted，62 个的代表）

**记忆赛道「厂商下场」组**——v1 报告的明星阵容，全部是先有产品后接 DSH：

| 仓库 | 星 | 创建 | 剔除理由 |
|---|---|---|---|
| volcengine/OpenViking | 31.8k | 2026-01 | 通用上下文数据库，DSH 靠社区桥接插件接入 |
| MemTensor/MemOS | 10.9k | 2025-07 | 独立记忆 OS，早于 DSH 存在 |
| EverMind-AI/EverOS | 12.3k | 2025-10 | 便携记忆层，"every AI agent"；且未适配 rc.1 |
| mem9-ai/mem9 | 1.2k | 2026-03 | 托管记忆服务，主打 OpenClaw |
| mnemon-dev/mnemon | 504 | 2026-02 | 单二进制，"any agent runtime" |
| mindscale-noah/MindMemOS | 947 | 2026-06 | 自有平台 + arXiv 论文，DSH 只是 npm 插件之一 |
| adoresever/graph-memory | 565 | 2026-03 | DSH + OpenClaw 双平台；未适配 rc.1 |
| syncable-dev/memtrace | 459 | 2026-04 | "for AI coding agents" 泛定位 |

**独立产品贴牌组**（部分）：open-design、ruflo（Claude Code/Codex 元 harness）、DeepSeek-Reasonix（竞品 coding agent）、WeKnora（腾讯知识平台）、PicGo（2017 年图床）、NocoBase（2020 年低代码）、voyager、archify、colleague-skill、mirage、EchoBird、petdex、ouroboros、openpencil、iPolloWork、Yao（2021）、OpenBiliClaw、CloudBase-AI-Toolkit、awesome-gpt-image-2、J-Space 认知套件。

**泛 host 协议/多平台工具组**：engramory、Co-Engram、MisakaNet、hol-guard（通用 agent 防病毒）、cc-notify-hooks（Claude Code/Codex/DSH/Reasonix 四端通知）、MuseAI、AI-Novel-Writer、Abu-Cowork、flowix、claude-paper、working-activity。

> 注意：**剔除 ≠ 无价值**。OpenViking/MemOS 作为记忆底座仍然可用，MisakaNet 的失败记忆、engramory 的零基建协议仍有启发。剔除的含义是：它们的兴衰不由 DSH 生态决定，不该出现在「DSH 插件」的榜单和选型建议里。

---

## 四、原生插件目录（538 个）

按 digest 分类聚合，_rc1 为该品类跟进率_。头部项目后的括号为 star 数：

**① 交互层：TUI / 侧边栏 / 主题（39，rc1 46%）——原生最强产品线之一**
dsh-web-ui（5.5k，皮肤+插件集合）、官方 DSH-better-sidebar（2.6k，侧边栏底座：文件/终端/Git/子代理页）、dsh-TUI（2.3k，Claude Code 风终端，鲸鱼顶栏/双击 Esc 回滚）、dsh-deep-whale（1.6k）、DSH-Transparent-UI（361，玻璃质感）、oh-dsh（256，Desktop/Web/TUI 三形态 runtime）、dsh-tianshu-tui（229，自研 ANSI 渲染核心）。

**② 桌面客户端/启动器（30，rc1 53%）**
anywhere-labs/deepseek-harness-desktop（18k，**原生星数第一**）、hairyf 桌面版（907，Tauri 仅 5MB）、lencx/Minke（391）、dsh-at-file（453，Codex 式 @file 引用）、fufankeji studio（450，零代码）、pilot-harness（250）、whitelonng/dshcode（191）、Ruler4396/dsh-launcher（170）。第 5 名之后同质化，与 v1 判断一致。

**③ 市场/策展/收录（原生约 35 个，rc1 率全场最高 62%）——最内卷的品类**
五种形态：**静态 awesome 列表**（awesome-dsh-plugin 11.3k，头牌，已发展成 org + 网站、事实目录标准；0xsline 809、Zhiyuan-Fan 254、libukai 184 等 11 个）；**自动发现+验证管道**（AdamPlatin123 1.3k，唯一容器实测、四档判定；bruc3van 261，脚本日抓+人工核实+明示反蹭 tag；imsai-sh 156、dshfind 203、Oh-My-DSH 68 每 4 小时同步、dsh-suite 44 每小时刷新等 8 个）；**装进 DSH 的一键市场**（dsh-market 1.7k 旗舰、DSH-Plugins-Marketplace 135、dsh-webui-market-plugin 99、zat-dsh-engine 77、dsh-find-plugin 75「找插件的插件」agent 内实时搜 topic、2BingLing/dsh-market 51 五维评分等 13 个）；**垂类市场**（dsh-skin-market 71 皮肤市场+人工审核、dsh-meme-hub 31 meme 策展）；**官方配套**（dsh-plugin-check 27，检查 hub 收录状态——官方承认收录体系）。
收录赛道内部同样有寄生者：**Anil-matcha/awesome-dsh-plugin（973★）创建于 2023-05，早于 DSH 诞生两年，老仓库改名蹭热度**且未跟进 rc.1，已按蹭 tag 剔除。可信度排序：容器实测 ＞ 自动抓取+人工核实 ＞ 纯自动同步 ＞ 纯静态列表；各家自称收录 1,500–4,310 个，普遍虚高于真实可用内核（500–900），选型看验证手段而非收录量。

**④ Provider/预设/订阅（90，rc1 32%）**
dsh-anchored-standard（3.7k，**未适配 rc.1**）、dsh-plugin-subscriptions（232）、dsh-codex-oauth（14）等。灰色地带性质不变；原生视角下这一类**数量庞大但质量稀疏**，rc1 率最低。

**⑤ 视觉桥（12，rc1 58%）——纯原生赛道**
modlens（3.5k，2026-02 元老）、dsh-vision-router（936，内置免费视觉 API）、dsh-vision-toolkit（805）、dsh-browser（383，Chrome 侧边栏）、picturereader（32）。"给纯文本大脑配眼睛"从第一天就是 DSH 独有需求。

**⑥ 记忆/知识（约 14，rc1 70%——全场最高）**
csyangwen/dsh-memory-evolve（218，五轨记忆 + git 分支感知 + 后台自进化）、官方 dsh-mnemon（169，三层控制平面 + 9 provider）、dsh-noema（121，durable & inspectable）、dsh-memento（59，审批门 + 审计轨迹）、seriousz158/dsh-memory（57）、dsh-meow-memory（33，七层 SQL）、dsh-mneme（32，autoDream 自整理）、FuRongJun-1999/dsh-memory（29）、dsh-auto-memory（26）、dsh-memoir（18，写 PROJECT_MEMORY.md）、dsh-knowledge（10，RAG）。**全部创建于 2026-08-05 之后**——原生记忆竞争在 rc.1 发布前一周才爆发。

**⑦ 远程/移动（18，rc1 61%）**
dsh-pocket（393，**未适配 rc.1**）、dsh-remote-web-gateway（116）、dsh-mobile-apk（112）、saya-ch/dsh-mobile（101，未适配）、liguobao/deepseek-harness-remote（48，端到端加密+中继，作者本人项目）、xgone/dsh-remote（42）、dsh-full-remote（21，token 门禁）、dsh-tether（16）、dsh-lan-gate（12）。洗牌结论与 v1 一致。

**⑧ 用量计费（25，rc1 44%）**
Balance-Whale-Widget（442，鲸鱼娘余额）、dsh-cost-meter（153）、TokenLedger（130，中继站归因）、dsh-usage-stats（105）。同质化重灾区，前四名之后不必看。

**⑨ 安全（约 13，rc1 42%）——剔除 hol-guard 后洼地更深**
dsh-pentest（189）、dsh-auto-mode（116，安全自动授权）、dsh-undo-savepoint（112，崩溃救援/回滚）、dsh-auto-review（73，第二模型复核审批）、dsh-plugin-guard（29，安装前快照）、dsh-permission-rules（27，Claude Code 式声明式权限）、dsh-computer-use（26，作用域权限）、dsh-context-doctor（18，上下文注入审计）、官方 dsh-security-audit（13）、dsh-secure-audit（12）、dsh-plugin-anti-ads（11，反制 dsh-ads）。**没有一个是 200★+ 且已适配 rc.1 的**——供应链风险敞口与防护装机量的缺口，在原生视角下更刺眼。

**⑩ IM/通知（9，rc1 44%）**：dsh-im（470，9 渠道）、dsh-lark-bot（28）、dsh-notifier（56）。

**⑪ 编排/子代理（6，rc1 33%）**：dsh-agent-teams（784）、dsh-crew（97）、DSH-pipeline-kernel（33）。

**⑫ 办公/文档（16，rc1 31%）**：deepseek-design（282）、Invoice-Downloader（132）、dsh-univer-office（68）。

**⑬ 垂直技能（长尾）**：dsh-ios（192，iOS 模拟器）、dsh-stock-watch（58）、SDR 外贸获客（24）、3GPP 协议库（14）、dsh-hdc-bridge（12，鸿蒙）。

**⑭ 娱乐/玩物（6+）**：dsh-pet（311）、dsh-ads（533，2005 门户恶搞）与其反制插件 dsh-plugin-anti-ads（11）、galgame 皮肤、鲸鱼娘家族。

**⑮ 官方周边（omdsh-dev）**：DSH-better-sidebar（2.6k）、dsh-genui（293）、dsh-mnemon（169）、dsh-security-audit（13）等 17 个，全适配 rc.1——原生生态里唯一"全绿"的产品线。

---

## 五、重排：最出色的原生插件 Top 10

标准：原生 + 已适配 rc.1 + 不可替代性。DSH 本体不计入。

1. **modlens**（3.5k★）——生态活着的最早原生插件（2026-02），视觉桥定义者
2. **anywhere-labs/deepseek-harness-desktop**（18k★）——原生星数第一，桌面端事实标准
3. **awesome-dsh-plugin**（11.3k★）——策展头牌
4. **dsh-web-ui**（5.5k★）——Web 端皮肤/插件集合
5. **omdsh-dev/DSH-better-sidebar**（2.6k★）——官方侧边栏底座，三方拓展注册机制
6. **dsh-TUI**（2.3k★）——官方公众号收录的终端补位
7. **dsh-market**（1.7k★）——DSH 里的插件市场
8. **AdamPlatin123/awesome-dsh-plugins**（1.3k★）——唯一容器实测目录，选型可信度最高
9. **dsh-agent-teams**（784★）——多 agent 编排
10. **dsh-context**（778★）——上下文洞察与管理

荣誉提及：modsearch（221★，2 月元老，免费搜索）、hairyf 桌面版（907★，Tauri 5MB 工程亮点）、官方 dsh-mnemon（169★，记忆控制平面）、liguobao/deepseek-harness-remote（48★，唯一端到端加密远程方案；作者本人项目，利益相关特此披露）。

出局警示：dsh-anchored-standard（3.7k★）、dsh-pocket（393★）——星数高但未适配 rc.1，印证 v1「star 与维护度不挂钩」。

---

## 六、相对 v1 的结论修订

1. **「记忆选 OpenViking/MemOS」改为分场景**：要现成底座稳定跑，仍可外接 OpenViking/MemOS（但那是选数据库，不是选 DSH 插件）；要看 DSH 原生记忆的演进，跟官方 dsh-mnemon（控制平面路线）与 dsh-memory-evolve / dsh-noema / dsh-memento / dsh-mneme（自进化、可审计、结构化各有侧重）。
2. **原生记忆的竞争格局**：底座之争已经让位（打不过外部平台），原生层在争**治理与整理**——审批门、审计、自我进化、项目记忆沉淀。品类 rc1 率 70% 全场最高：这是当前原生生态里工程态度最认真的赛道。
3. **安全是原生生态最大缺口**：hol-guard 属于外部产品后，原生安全插件无一同时满足 200★+ 和 rc.1 适配。供应链风险敞口不变。
4. **视觉桥、桌面/TUI、策展市场是原生基本盘**：需求由 DSH 特性直接派生（纯文本模型、Web 优先形态、万物皆插件），外部产品进不来。
5. **Provider/订阅类数量最大（90）但质量最稀**（rc1 率 32%），且踩 ToS 红线——原生化并不能洗白灰色属性。

---

## 附录：复现

```bash
python3 scripts/classify_native.py
# 输出三桶统计 + data/native_plugins.jsonl（538 个原生插件）
```

判定规则、`PRODUCT_FIRST` 覆盖名单（40 项）均固化在该脚本内；快照与 v1 共用（2026-08-22）。
