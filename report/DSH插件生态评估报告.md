# DeepSeek Harness（DSH/dsh）插件生态评估报告

- **评估日期**：2026-08-22
- **数据来源**：GitHub API 实测抓取（非目录站转述）
- **枚举范围**：`dsh-plugin` topic 全量仓库，官方计数 10,529 个，实际去重枚举 **9,393 个**（覆盖率 89%，缺口为评估当日新建仓库）
- **深度阅读**：star ≥ 10 的全部 **700 个仓库 README 逐个阅读分类**（机器预分类 + 人工逐行校正）
- **活跃度口径**：以官方 **v0.1.1-rc.1**（2026-08-21 07:12 UTC 发布，含破坏性变更）发布时间为分界，`pushed ≥ 该时间` 记为"已适配/真活跃"

---

## 一、核心结论（TL;DR）

1. **规模**：全网带 `dsh-plugin` 标签的仓库 10,529 个，但真实可用的内核约 **500–900 个**；86% 的仓库 star 不足 5，48.3% 只在创建当天推送过一次。
2. **活跃度**：按 rc.1 破坏性变更衡量的"真活跃率"为 **20.6%**（1,932/9,393）。此前"近三天有 push"口径（38.7%）严重高估了生态健康度。**头部插件（100★+）也只有 59.4% 在 rc.1 发布后 36 小时内跟进。**
3. **品类**：修正后共 11 条真实产品线，最强四条是**记忆/知识库、视觉桥接、订阅/Provider 接入、远程/移动访问**；安全类是被低估的洼地；桌面客户端与用量挂件已经严重同质化。
4. **质量分布**（top 700 人工判定）：真生产力约 45–50%，有用但同质化约 25%，纯玩物约 10%，蹭 tag / 无关 / 空壳约 15%。**star 榜单含大量寄生标签（reactive-resume、PicGo、NocoBase 等知名无关项目），按 star 选型会被误导。**
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
- 已明显掉队的高星项目：EverOS（12.3k★）、petdex（3.9k★）、dsh-anchored-standard（3.7k★）、dsh-pocket（393★）、graph-memory（565★）、PPT-Design-Skill（442★）。
- 全生态真正跟得上版本节奏的估算为 **700–900 个**（"有星"与"已适配"的交集）。

---

## 五、品类全景（11 条产品线，基于 700 个 README 人工校正）

### ① 记忆/知识库 —— 生态最强主线（25+ 个）
OpenViking（31.8k★，火山引擎出品）、MemOS（10.9k★）、EverOS（12.3k★，未适配 rc.1）、mem9、mnemon、MindMemOS、dsh-mneme、dsh-mnemon、engramory、dsh-memento、MisakaNet（Git 化失败记忆）、Co-Engram 等。模型厂商直接下场，说明这是公认痛点。

### ② 视觉桥接 —— 因 DeepSeek V4 纯文本而爆发（20+ 个）
modlens（3.5k★，旗舰）、agent-vision-toolkit（1.1k★）、dsh-vision-router（936★）、dsh-vision-toolkit（805★）、picturereader、OCR/视频理解系列。"给纯文本大脑配眼睛"是刚需。

### ③ 订阅/Provider 接入 —— 灰色地带（15+ 个）
dsh-codex-oauth、EchoBird（3.1k★）、dsh-codex-connect、coding-subscription-oauth、dsh-clawrouter、dockyard（账号池）——把 ChatGPT/Claude/Grok 订阅接进 DSH。需求真实，踩 ToS 红线。

### ④ 桌面客户端/启动器 —— 高度同质化（15+ 个）
anywhere-labs/deepseek-harness-desktop（18k★）领先；其后十余个功能雷同的 Electron/Tauri 壳。xtxo/dsh-ui 用 Rust 做到 8.7MB 是唯一工程亮点。

### ⑤ 远程/移动访问（约 20 个，正在洗牌）
详见第七节专项分析。

### ⑥ 用量计费（25+ 个，同质化）
TokenLedger、dsh-cost-meter、dsh-usage-stats、dsh-damage-pulse（扣血动画）、dsh-green-meter（能耗/碳排放）。前两三名之后均在重复造轮子。

### ⑦ 安全 —— 少而精，被低估（12 个）
hol-guard（agent 防病毒，459★）、dsh-pentest（189★）、dsh-undo-savepoint、openguardrails、dsh-security-audit、dsh-plugin-guard。在"万物皆插件、供应链风险极大"的架构下属于刚需洼地。

### ⑧ IM 接入（20+ 个）
dsh-im（470★，9 渠道）、飞书家族（dsh-lark 系列 6+ 个）、QQ bot、通知钩子（cc-notify-hooks 支持 11 渠道）。中文生态特色显著。

### ⑨ 垂直领域技能 —— 最长尾
A股实盘交易（hyqibot/A-share-Ai、KCNyu/clawock 真实券商账户）、招聘 copilot、法律诉讼可视化、外贸 SDR、3GPP 通信协议库、量子计算、机器人、HarmonyOS/iOS/Godot/Blender/Garmin。"一切皆插件"的承诺在垂直方向兑现得最好。

### ⑩ 策展/插件市场（30+ 个，本身已内卷成品类）
awesome-dsh-plugin（11.3k★）、AdamPlatin123/awesome-dsh-plugins（1.3k★，唯一做 k8s 容器实测）、dsh-plugin-hub（自称收录 4,310、人工验证 3,112）、0xsline、libukai、dshfind 等。

### ⑪ 官方周边（omdsh-dev，原 dsh-external）
dsh-deep-research、dsh-genui、dsh-toolkit、dsh-notification、plugin-template、dsh-plugin-check 等 17 个，质量稳定、全部适配 rc.1，是新用户起步最优解。

---

## 六、生产力 vs 玩具 vs 蹭 tag（top 700 人工判定）

| 判定 | 占比 | 说明 |
|---|---|---|
| 真生产力 | ~45–50% | 记忆、视觉桥、远程、计费、安全、IM、垂直技能、深度研究 |
| 有用但同质化 | ~25% | 桌面壳、会话管理、侧边栏、余额挂件——同类第 5 名之后无存在必要 |
| 纯玩物 | ~10%（60–70 个） | 桌宠家族、动漫皮肤（鲸鱼娘/流萤/终末地/赛博朋克/QQ2006）、meme、五子棋、竹知了（2.8k★）、SillyTavern 角色扮演家族。文化现象大于工具价值 |
| 蹭 tag / 无关 / 空壳 | ~15% | reactive-resume（41k★ 简历工具）、PicGo（27k★ 图床）、NocoBase（23.7k★ 低代码）、Aria（C++ 框架）等知名无关项目打标签引流；另有大量模板与 AI 生成 stub |

**star 榜单不可直接作为选型依据。**

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

## 八、最出色的插件（原生 + 活跃 + 不可替代）

1. **modlens**（3.5k★，已适配）——纯文本模型视觉桥，定位精准。
2. **OpenViking**（31.8k★，已适配）——记忆方向事实标准候选，厂商背书。
3. **ruflo**（68.8k★，已适配）——多 agent 编排 meta-harness，最像"平台"的项目。
4. **omdsh-dev 全家桶**——官方血统、文档完备、全适配 rc.1。
5. **hol-guard / openguardrails**——agent 运行时防护，方向稀缺。
6. **AdamPlatin123/awesome-dsh-plugins**——唯一容器级实测目录，选型可信度最高。

（open-design 90k★ 为设计工具类头部，但属"被 DSH 适配的独立产品"，不计入原生插件排名。）

---

## 九、风险与建议

**生态级风险**：
1. **供应链风险**：插件可覆盖工具、沙箱、模型层，且市场类插件直接执行安装——hol-guard 一类运行时防护的装机量远低于风险敞口。
2. **维护断层**：48% 一次性仓库 + rc.1 后 40% 头部未跟进，一个月后的下一次破坏性变更预计还会淘汰一批。
3. **灰色 Provider 插件**随时可能因官方收紧而批量失效。

**给使用者的建议**：
- 起步用 omdsh-dev 官方线 + awesome-dsh-plugin 精选；核心生产力选已适配 rc.1 的头部（记忆选 OpenViking/MemOS，视觉选 modlens，用量选 TokenLedger，安全装 hol-guard）。
- 避开：同质化区（第 5 个以后的桌面壳/余额挂件）、未适配 rc.1 的停滞项目、纯 star 导向的榜单。

**给插件作者的建议**：
- 竞争最不充分的三条线：安全审计、企业治理（权限/合规/审计日志）、自托管中继（remote 品类的共同短板）。
- 跟进 rc 节奏本身就是竞争力信号：适配日志写进 README 能直接转化为信任。

---

## 附录：数据快照

- 抓取时间：2026-08-22（UTC+8 下午）
- 工具：GitHub Search/Repos API（gh CLI），全量 9,393 仓库元数据 + 700 README
- rc.1 分界时间戳：2026-08-21T07:12:39Z
- 原始数据：`/tmp/dsh-audit/repos.jsonl`（元数据）、`/tmp/dsh-audit/readmes/`（README 全文）、`/tmp/dsh-audit/readme_analysis.json`（分类结果）
