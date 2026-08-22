# DeepSeek Harness（DSH/dsh）插件生态评估报告

- **评估日期**：2026-08-22
- **数据来源**：GitHub API 实测抓取（非目录站转述）
- **枚举范围**：`dsh-plugin` topic 全量仓库，官方计数 10,529 个，实际去重枚举 **9,393 个**（覆盖率 89%，缺口为评估当日新建仓库）
- **深度阅读**：star ≥ 10 的全部 **700 个仓库 README 逐个阅读分类**（机器预分类 + 人工逐行校正）
- **活跃度口径**：以官方 **v0.1.1-rc.1**（2026-08-21 07:12 UTC 发布，含破坏性变更）发布时间为分界，`pushed ≥ 该时间` 记为"已适配/真活跃"
- **修订记录**：v1.1（2026-08-22 晚）——剔除适配型独立产品，见下方特别声明

---

## ⚠️ 特别声明：关于"擦边"插件的处理

本报告初版把两类仓库与真正的 DSH 原生插件混排在同一张榜上：

1. **适配型独立产品（62 个，占 top 700 星数的 61%）**：先有产品/品牌、后顺手接入或贴上 `dsh-plugin` 标签的仓库——OpenViking（火山引擎通用上下文库）、MemOS / EverOS / mem9 / mnemon（通用记忆产品）、ruflo（Claude Code/Codex 元 harness）、open-design、WeKnora、PicGo、NocoBase、hol-guard、EchoBird 等。它们的兴衰不由 DSH 生态决定，出现在"DSH 插件"榜单里只会扭曲选型判断——初版 star 榜前 11 名（除 DSH 本体）全部属于此类。
2. **蹭 tag / 无关 / 空壳（103 个）**：reactive-resume、Aria 等与 DSH 毫无关系的知名项目靠打标签引流。

**v1.1 已做三件事**：正文品类全景、榜单与选型建议中的上述仓库已移除或降为数据点标注；判定规则固化为 `scripts/classify_native.py`（三桶：native 538 / adapted 62 / unrelated 103）；纯原生视角的完整目录与重排 Top 10 见姊妹篇 **[DSH原生插件整理.md](DSH原生插件整理.md)**，机器可读清单为 `data/native_plugins.jsonl`。

> 剔除 ≠ 否定价值：OpenViking/MemOS 作为外接记忆底座依然可用，但那是"选数据库"，不是"选 DSH 插件"。本报告此后的推荐默认只面向 DSH 原生插件；第三节/第四节的生态级统计（总量、rc.1 活跃率）仍基于全量 9,393 仓库，不受剔除影响。

---

## 一、核心结论（TL;DR）

1. **规模**：全网带 `dsh-plugin` 标签的仓库 10,529 个，但真实可用的内核约 **500–900 个**；86% 的仓库 star 不足 5，48.3% 只在创建当天推送过一次。
2. **活跃度**：按 rc.1 破坏性变更衡量的"真活跃率"为 **20.6%**（1,932/9,393）。此前"近三天有 push"口径（38.7%）严重高估了生态健康度。**头部插件（100★+）也只有 59.4% 在 rc.1 发布后 36 小时内跟进。**
3. **品类**：修正后共 11 条真实产品线，最强四条是**记忆/知识库、视觉桥接、远程/移动访问、桌面/TUI 交互层**；安全类是被低估的洼地；桌面客户端与用量挂件已经严重同质化。
4. **质量分布**（top 700 人工判定）：真生产力约 45–50%，有用但同质化约 25%，纯玩物约 10%，蹭 tag / 无关 / 空壳约 15%。**v1.1 重整后另识别出 62 个适配型独立产品（占 61% 的星），已连同蹭 tag 项一并移出正文推荐——star 榜单含大量寄生标签（reactive-resume、PicGo、NocoBase、OpenViking、ruflo 等），按 star 选型会被误导。**
5. **选型建议**：三个指标判断插件可信度——① 是否适配最新 rc；② 作者是否持续 push；③ 是否被实测型目录（AdamPlatin123/awesome-dsh-plugins 或 dsh-plugin-hub 验证集）收录。

---

## 二、方法论

| 步骤 | 做法 | 局限声明 |
|---|---|---|
| 全量枚举 | GitHub Search API 按 star 分桶 + 按创建日期按天切片，绕过单查询 1000 条上限 | 剩余 ~1,100 个当日新建仓库未覆盖 |
| README 深读 | star ≥ 10 的 700 个仓库，下载 README 前 6,000 字节逐个阅读 | 低于 10★ 的约 8,700 个仅做元数据统计（其中 48% 为一次性推送，逐个阅读边际价值极低） |
| 分类 | 关键词机器预分类 + 人工逐行校正（修正了 git-eng 类目误判 253 处中的大多数） | 部分长尾仓库分类基于描述而非全文 |
| 活跃判定 | rc.1 发布时间戳前后是否有 push | 皮肤类插件可能不受 API 破坏影响、无需跟进，故"未适配"是风险指标而非死亡判决 |

---

## 三、规模与增长

### 3.1 增长曲线

生态从 2026 年 7 月底萌芽，至今不到一个月。创建峰值在 8/14（单日 1,508 个），评估前两日（8/20）仍有 917 个/天。

| 日期 | 新建仓库数 |
|---|---|
| 08-12 | ~300 |
| 08-13 | 639 |
| 08-14 | **1,508**（峰） |
| 08-15 | 1,385 |
| 08-16 | 1,289 |
| 08-17 | 953 |
| 08-18 | 671 |
| 08-19 | 872 |
| 08-20 | 917 |
| 08-21 | 513 |
| 08-22（半天） | 113 |

### 3.2 星标金字塔

| 星级段 | 数量 | 占比 |
|---|---|---|
| 100★+ | 180 | 1.9% |
| 20–99★ | 249 | 2.7% |
| 5–19★ | 869 | 9.3% |
| 1–4★ | 3,592 | 38.2% |
| 0★ | 4,503 | 47.9% |

### 3.3 其他特征

- **语言**：JavaScript 5,440 + TypeScript 2,975（合计 ~90%，Cordis 插件体系决定），Python 378、Rust 78、PowerShell 64。
- **一次性仓库**：48.3%（4,533/9,393）只在创建当天有 push。
- **归档**：仅 25 个——没有人"退出"，只是不再回来。
- **无描述**：10.4%。

---

## 四、活跃度：rc.1 试金石

v0.1.1-rc.1（2026-08-21 07:12 UTC）带来破坏性变更。以其发布时间为分界统计 push 时间：

| 星级段 | 已跟进 rc.1 | 真活跃率 |
|---|---|---|
| 100★+ | 107/180 | **59.4%** |
| 20–99★ | 108/249 | 43.4% |
| 5–19★ | 226/869 | 26.0% |
| 1–4★ | 709/3,592 | 19.7% |
| 0★ | 782/4,503 | 17.4% |
| **全量** | **1,932/9,393** | **20.6%** |

**要点**：

- 头部也有四成未跟进——star 数与维护度并不挂钩。
- 已明显掉队的高星项目：▲EverOS（12.3k★）、▲petdex（3.9k★）、dsh-anchored-standard（3.7k★）、dsh-pocket（393★）、▲graph-memory（565★）、PPT-Design-Skill（442★，多平台 skill）。带 ▲ 者为适配型独立产品，仅作活跃度数据点保留，不列入插件目录。
- 全生态真正跟得上版本节奏的估算为 **700–900 个**（"有星"与"已适配"的交集）；其中 DSH 原生插件的 rc.1 跟进率为 44%（236/538），显著健康于全量。

---

## 五、品类全景（11 条产品线，基于 700 个 README 人工校正；v1.1 起仅收录 DSH 原生插件）

### ① 记忆/知识库 —— 生态最强主线（原生约 14 个，全部创建于 2026-08-05 之后，rc.1 跟进率 70% 为全场最高）
dsh-memory-evolve（218★，五轨记忆 + git 分支感知 + 后台自进化）、官方 dsh-mnemon（169★，三层控制平面 + 9 个可插拔 provider）、dsh-noema（121★）、dsh-memento（59★，写审批门 + 审计轨迹）、dsh-meow-memory（33★，七层 SQL）、dsh-mneme（32★，autoDream 自整理）、dsh-memoir（18★，项目记忆沉淀）、dsh-knowledge（10★，RAG）等。
（OpenViking、MemOS、EverOS、mem9、mnemon、MindMemOS、graph-memory、memtrace、engramory、MisakaNet、Co-Engram 等 11 个为通用记忆产品/泛 host 协议，已按特别声明移出——它们是可外接的底座，不是 DSH 插件赛道的参与者。）

### ② 视觉桥接 —— 因 DeepSeek V4 纯文本而爆发（12 个，纯原生赛道）
modlens（3.5k★，旗舰，2026-02 元老）、dsh-vision-router（936★，内置免费视觉 API）、dsh-vision-toolkit（805★）、dsh-browser（383★，Chrome 侧边栏）、picturereader（32★）、OCR/视频理解系列。"给纯文本大脑配眼睛"从第一天就是 DSH 独有需求，外部产品进不来。

### ③ 订阅/Provider 接入 —— 灰色地带（90 个，rc1 率 32% 全场最低）
dsh-codex-oauth（14★）、dsh-codex-connect（39★）、dsh-coding-subscription-oauth（11★）、dsh-clawrouter（19★）、dockyard-dsh（74★，macOS 账号池）——把 ChatGPT/Claude/Grok 订阅接进 DSH。需求真实，踩 ToS 红线；原生视角下这一类数量最大但质量最稀。（EchoBird 为多平台产品，已移出。）

### ④ 桌面客户端/启动器 —— 高度同质化（30 个）
anywhere-labs/deepseek-harness-desktop（18k★，**原生星数第一**）领先；其后十余个功能雷同的 Electron/Tauri 壳。hairyf 桌面版（907★）与 xtxo/dsh-ui（Rust，10★）是小体量工程亮点。

### ⑤ 远程/移动访问（18 个，正在洗牌）
详见第七节专项分析。

### ⑥ 用量计费（25 个，同质化）
TokenLedger（130★，中继站归因）、dsh-cost-meter（153★）、dsh-usage-stats（105★）、dsh-damage-pulse（83★，扣血动画）、dsh-green-meter（52★，能耗/碳排放）。前两三名之后均在重复造轮子。

### ⑦ 安全 —— 少而精，被低估（约 13 个原生）
dsh-pentest（189★）、dsh-auto-mode（116★，安全自动授权）、dsh-undo-savepoint（112★，崩溃救援）、dsh-auto-review（73★，第二模型复核审批）、dsh-plugin-guard（29★）、dsh-permission-rules（27★）、官方 dsh-security-audit（13★）、dsh-plugin-anti-ads（11★）。在"万物皆插件、供应链风险极大"的架构下属于刚需洼地。（hol-guard、openguardrails 为通用 agent 安全产品/协议，已移出；剔除后原生安全无一是 200★+ 且适配 rc.1 的，缺口更刺眼。）

### ⑧ IM 接入（9 个）
dsh-im（470★，9 渠道）、飞书家族（dsh-lark 系列官方 1 + 社区 5+ 个）、QQ bot、dsh-notifier（56★）。中文生态特色显著。（cc-notify-hooks 为四端通用通知，已移出。）

### ⑨ 垂直领域技能 —— 最长尾
招聘 copilot（41★）、法律诉讼可视化、外贸 SDR（Xuxchloris 24★，九阶段 SOP + 人工审批）、3GPP 通信协议库（14★）、dsh-ios（192★，iOS 模拟器）、dsh-hdc-bridge（12★，鸿蒙）、量子计算、机器人、Godot/Blender/Garmin。"一切皆插件"的承诺在垂直方向兑现得最好。（A 股实盘 hyqibot/A-share-Ai 为 2025-11 的自有量化产品贴牌，已移出。）

### ⑩ 策展/收录/插件市场 —— 最内卷的品类（原生约 35 个，v1.1 专项扩充）

按形态分五类：

**a. 静态 awesome 列表（人工精选，11 个）**：awesome-dsh-plugin（11.3k★，头牌，已发展成 org + awesome-dsh-plugin.com 网站，形成事实目录标准）、0xsline（809★）、Zhiyuan-Fan（254★）、libukai（184★，终极指南）、Dominic789654（180★）、beancookie（95★）、Alex-Yanggg（76★）、kejixiaoliang（24★）、white0dew（13★）、jiji262（13★）等。
**b. 自动发现 + 验证管道（可信度更高，8 个）**：AdamPlatin123/awesome-dsh-plugins（1.3k★，唯一 k8s 容器实测、四档判定）、bruc3van（261★，脚本每日抓取 + 人工逐个核实、明示反蹭 tag）、imsai-sh（156★，store+hub 收录 3,100+）、hikariming/dshfind（203★，原理学习+市场）、Oh-My-DSH（68★，每 4 小时自动同步）、ZASENJC/dsh-plugins-store（64★，自动分类+验证）、whyihaveyou/dsh-suite（44★，每小时刷新）、YELEBAI（20★，验证 + 自维护 Registry）。
**c. 装进 DSH 的一键市场插件（13 个）**：dsh-market（1.7k★，旗舰）、bradeGithub/DSH-Plugins-Marketplace（135★）、Sanqi-normal/dsh-webui-market-plugin（99★，直接浏览 awesome-dsh-plugin 目录）、zat-dsh-engine（77★，可视化市场）、awesome-dsh-plugin/dsh-find-plugin（75★，"找插件的插件"，agent 内实时搜 GitHub topic）、Noob-stupid/dsh-plugin-hub（67★，管理面板+市场）、LX2000WASD（62★，Web UI 管理器）、2BingLing/dsh-market（51★，1,500+ 五维评分+中文搜索）、Ericwong5021（24★）、alexchenzl（21★）、dshplugin/dsh-plugin-hub（17★，自称收录 4,310/人工验证 3,112）、sliverp（16★）、w2112515（12★）。
**d. 垂类市场（2 个）**：dsh-skin-market（71★，皮肤市场+评分+人工审核，嵌入设置页）、dsh-meme-hub（31★，meme 策展）。
**e. 官方配套（1 个）**：omdsh-dev/dsh-plugin-check（27★，检查插件"hub 收录状态"——官方工具承认收录体系的存在）。

⚠️ 本品类内部同样有寄生者：**Anil-matcha/awesome-dsh-plugin（973★）创建于 2023-05，早于 DSH 诞生两年，系老仓库改名蹭热度**，且未跟进 rc.1，勿当作正经目录使用；另 Awesome-AI-Pedia（227★，泛 AI 百科）、EverMind-AI/SkillCorpus（92★，EverOS 厂商的 SKILL 基建）、ru-marketplace-mcp（68★，俄罗斯电商 MCP）均为无关蹭 tag。

**可信度排序**：容器实测（AdamPlatin123）＞ 自动抓取 + 人工核实（bruc3van 等）＞ 纯自动同步（Oh-My-DSH 等）＞ 纯静态列表（第 5 名之后的 awesome 无存在必要）。收录数量口径普遍虚高（自称 1,500–4,310 不等，均大于真实可用内核的 500–900），选型看验证手段而非收录量。

### ⑪ 官方周边（omdsh-dev，原 dsh-external）
dsh-deep-research、dsh-genui、DSH-better-sidebar（2.6k★）、dsh-toolkit、dsh-notification、plugin-template、dsh-plugin-check 等 17 个，质量稳定、全部适配 rc.1，是新用户起步最优解——也是原生生态里唯一"全绿"的产品线。

---

## 六、生产力 vs 玩具 vs 蹭 tag（top 700 人工判定，v1.1 增补适配型一档）

| 判定 | 占比 | 说明 |
|---|---|---|
| 真生产力 | ~45–50% | 记忆、视觉桥、远程、计费、安全、IM、垂直技能、深度研究 |
| 有用但同质化 | ~25% | 桌面壳、会话管理、侧边栏、余额挂件——同类第 5 名之后无存在必要 |
| 纯玩物 | ~10%（60–70 个） | 桌宠家族、动漫皮肤（鲸鱼娘/流萤/终末地/赛博朋克/QQ2006）、meme、五子棋、竹知了（2.8k★）、SillyTavern 角色扮演家族。文化现象大于工具价值 |
| **适配型独立产品（v1.1 新增）** | **62 个 / 61% 星** | OpenViking、ruflo、open-design、MemOS、WeKnora、hol-guard 等"先有产品后接入/贴牌"，已移出正文推荐 |
| 蹭 tag / 无关 / 空壳 | ~15%（103 个） | reactive-resume（41k★ 简历工具）、PicGo（27k★ 图床）、NocoBase（23.7k★ 低代码）、Aria（C++ 框架）等知名无关项目打标签引流；另有大量模板与 AI 生成 stub |

**star 榜单不可直接作为选型依据**：剔除 DSH 本体后，star 前 11 名全部是适配型或蹭 tag，第一个原生插件（anywhere-labs 桌面端）要数到第 12 名。

---

## 七、Remote 品类专项

约 20 个真实项目。rc.1 试金石下正在洗牌：

| 项目 | Star | rc.1 适配 | 技术路线 |
|---|---|---|---|
| dsh-pocket | 393 | ✗ | 手机扫码同屏 |
| dsh-remote-web-gateway | 116 | ✓ | Web 网关 |
| dsh-mobile-apk | 112 | ✓ | APK 打包 |
| dsh-mobile (saya-ch) | 101 | ✗ | 原生 App（Alpha） |
| **liguobao/deepseek-harness-remote** | **48** | **✓** | **中继 + 端到端加密，多客户端（浏览器/VS Code/Android）** |
| xgone/dsh-remote | 42 | ✓ | LAN 认证层 |
| DeepSeekHarnessRemoteGateway | 19 | ✗ | sidecar 网关 |
| 其余（dsh-tether、dsh-phone、dsh-lan-gate 等） | ≤18 | 部分 | P2P / FRP / Tailscale 教程流 |

**判断**：按 rc.1 活跃标准，品类内仍在牌桌上的前 3–4 名为 dsh-remote-web-gateway、dsh-mobile-apk、liguobao/deepseek-harness-remote、xgone/dsh-remote。其中 liguobao 版本是**唯一实现端到端加密 + 中继不可见明文 + 只读文件预览 + 设备级撤销**的方案，安全模型最完整；短板为中继不可自托管（信任模型最大扣分项）与 Host/客户端版本耦合较紧（0.3.28 客户端仅兼容 0.3.15 Host 基本功能）。

---

## 八、最出色的插件（原生 + 活跃 + 不可替代；v1.1 重排，标准：DSH 原生 + 已适配 rc.1 + 不可替代性）

1. **modlens**（3.5k★，已适配）——纯文本模型视觉桥，定位精准；2026-02 创建，活着的最早原生插件。
2. **anywhere-labs/deepseek-harness-desktop**（18k★，已适配）——原生星数第一，桌面端事实标准。
3. **awesome-dsh-plugin**（11.3k★，已适配）——策展头牌。
4. **dsh-web-ui**（5.5k★，已适配）——Web 端皮肤与插件集合。
5. **omdsh-dev/DSH-better-sidebar**（2.6k★，官方）——侧边栏底座，支持三方拓展注册。
6. **dsh-TUI**（2.3k★，已适配）——Claude Code 风终端补位，官方公众号收录。
7. **dsh-market**（1.7k★，已适配）——DSH 内置插件市场。
8. **AdamPlatin123/awesome-dsh-plugins**（1.3k★，已适配）——唯一容器级实测目录，选型可信度最高。
9. **dsh-agent-teams**（784★，已适配）——多 agent 编排。
10. **dsh-context**（778★，已适配）——上下文洞察与管理。

荣誉提及：modsearch（221★，2 月元老，免费搜索）、hairyf 桌面版（907★，Tauri 5MB）、官方 dsh-mnemon（169★，记忆控制平面）、liguobao/deepseek-harness-remote（48★，唯一端到端加密远程方案——作者本人项目，利益相关特此披露）。
omdsh-dev 官方全家桶（17 个）整体全适配 rc.1，可视为第 0 名。

（v1 初版榜单中的 OpenViking、ruflo、hol-guard/openguardrails 经重整确认为适配型独立产品，已移出；open-design 90k★ 同理，属"被 DSH 适配的独立产品"，不计入排名。）

---

## 九、风险与建议

**生态级风险**：
1. **供应链风险**：插件可覆盖工具、沙箱、模型层，且市场类插件直接执行安装——运行时防护的装机量（无论原生还是外部产品）远低于风险敞口；v1.1 剔除 hol-guard 后，原生安全插件无一同时满足 200★+ 与 rc.1 适配。
2. **维护断层**：48% 一次性仓库 + rc.1 后 40% 头部未跟进，一个月后的下一次破坏性变更预计还会淘汰一批。
3. **灰色 Provider 插件**随时可能因官方收紧而批量失效。

**给使用者的建议**：
- 起步用 omdsh-dev 官方线 + awesome-dsh-plugin 精选；核心生产力选已适配 rc.1 的原生头部（记忆选官方 dsh-mnemon 或 dsh-memory-evolve，视觉选 modlens，用量选 TokenLedger，安全装 dsh-undo-savepoint / 官方 dsh-security-audit）。若愿意外接通用底座（OpenViking/MemOS），那是选数据库而非选插件，注意另行评估其 DSH 桥接层的维护状态。
- 避开：同质化区（第 5 个以后的桌面壳/余额挂件）、未适配 rc.1 的停滞项目、纯 star 导向的榜单、以及一切"顺手打个 dsh-plugin 标签"的适配型仓库。

**给插件作者的建议**：
- 竞争最不充分的三条线：安全审计、企业治理（权限/合规/审计日志）、自托管中继（remote 品类的共同短板）。
- 跟进 rc 节奏本身就是竞争力信号：适配日志写进 README 能直接转化为信任。

---

## 附录：数据快照与产物

- 抓取时间：2026-08-22（UTC+8 下午）；v1.1 修订同日晚间
- 工具：GitHub Search/Repos API（gh CLI），全量 9,393 仓库元数据 + 700 README
- rc.1 分界时间戳：2026-08-21T07:12:39Z
- 仓库内数据产物：`data/repos.jsonl`（元数据）、`data/analysis.json`（700 个机器预分类）、`data/digest.txt`（一行式摘要）、`data/native_plugins.jsonl`（v1.1 原生清单，538 个）
- 分类复现：`python3 scripts/classify_native.py`（三桶规则 + 40 项产品优先覆盖名单）
- 姊妹篇：[DSH原生插件整理.md](DSH原生插件整理.md)（纯原生视角的目录、Top 10 与结论修订）
