# dsh-plugin-bench

DeepSeek Harness（DSH / dsh）插件生态的独立基准评估仓库：一份基于 GitHub 一手数据（非目录站转述）的全量生态评估报告，外加一套可复用于**任何 GitHub topic 生态**的审计 Skill。

- 评估日期：2026-08-22
- 数据快照：`data/repos.jsonl`（9,393 个 `dsh-plugin` topic 仓库元数据，覆盖率 89%）
- 深读范围：star ≥ 10 的全部 700 个仓库 README（`data/digest.txt` 为逐个分类结果）

## 核心发现（TL;DR）

| 指标 | 数值 |
|---|---|
| topic 仓库总数（官方计数） | 10,529 |
| 真实可用内核估算 | 500–900 个 |
| star < 5 的仓库占比 | 86% |
| 只在创建当天推送过一次 | 48.3% |
| **rc.1 破坏性变更后的真活跃率** | **20.6%**（1,932/9,393） |
| 100★+ 头部插件 rc.1 跟进率 | 59.4%（四成头部已停滞） |

关键结论：

1. **活跃度要用"破坏性变更锚点"衡量**，不能用"近三天有 push"（该口径为 38.7%，严重高估）。以 v0.1.1-rc.1（2026-08-21T07:12Z）为锚，仅 20.6% 的仓库跟进。
2. **star 榜单不可直接选型**：reactive-resume（41k★）、PicGo（27k★）、NocoBase（23.7k★）等知名无关项目靠打 topic 标签占据榜首（"蹭 tag"），top 700 中约 15% 属此类或空壳。
3. **最强四条产品线**：记忆/知识库、视觉桥接（DeepSeek V4 纯文本 → 配眼睛）、订阅/Provider 接入、远程/移动访问；安全类是被低估的洼地；桌面壳与用量挂件已严重同质化。
4. **大量高星项目已停滞**：EverOS（12.3k★）、petdex（3.9k★）、dsh-pocket（393★）等未适配 rc.1，详见报告"stalled despite stars"名单。

## 统计图

| 图 | 内容 |
|---|---|
| ![daily creation](charts/01_daily_creation.png) | 每日新建仓库数 + 累计曲线（2026-07-15 起；更早的 300+ 个为蹭 tag 的老仓库） |
| ![star pyramid](charts/02_star_pyramid.png) | 星标金字塔（对数轴）：86% 的仓库 star < 5 |
| ![rc.1 activity](charts/03_rc1_activity.png) | 各星级段的 rc.1 破坏性变更跟进率：头部也仅 59% |
| ![languages](charts/04_languages.png) | 语言构成：JS+TS 合计 90% |
| ![lifecycle](charts/05_lifecycle.png) | 生命周期拆分：48% 一次性仓库 / 31% rc.1 前停滞 / 21% 真活跃 |

图表由 `scripts/make_charts.py` 从 `data/repos.jsonl` 重新生成：`python3 scripts/make_charts.py`

## 仓库结构

```
├── report/
│   └── DSH插件生态评估报告.md   # 完整评估报告（品类全景/活跃度/Remote 专项/建议）
├── data/
│   ├── repos.jsonl              # 9,393 仓库元数据快照（GitHub API 抓取）
│   ├── stats.txt                # 全量统计（星标金字塔/语言/一次性比率/锚点活跃率）
│   ├── digest.txt               # 700 个 README 的一行式摘要+分类（人工校正基础）
│   └── analysis.json            # 机器预分类结构化结果
├── charts/                      # 统计图（scripts/make_charts.py 生成）
├── scripts/
│   └── make_charts.py           # 从 data/ 重新生成全部图表
└── skills/github-topic-audit/   # 可复用审计 Skill（见下）
```

> 注：700 个第三方仓库的 README 全文**不**入库（体积与再分发考虑），`data/` 保留元数据与本仓库产出的分析；用 Skill 脚本可随时重新抓取复现。

## Skill：github-topic-audit

把本次评估的方法固化成了可复用的 Agent Skill，适用于任何 GitHub topic 生态（`claude-plugins`、`vscode-extension`、任意平台插件生态……）：

```bash
# 1) 枚举全量仓库 + 下载 top README（自动绕过搜索 API 1000 条/查询上限：
#    star 分桶 + 创建日期递归二分）
python3 skills/github-topic-audit/scripts/fetch.py <topic> --readme-top 700

# 2) 统计 + 分类预跑（--anchor-release 指定破坏性变更版本作为活跃度锚点）
python3 skills/github-topic-audit/scripts/stats.py audit-<topic> \
    --anchor-release <owner>/<repo>@<tag>

# 3) 人工逐行校正 digest.txt 后按 references/classification.md 的报告骨架成文
```

方法要点（都踩过坑）：

- **搜索上限陷阱**：GitHub Search 单查询硬上限 1000 条，分页无效；必须按 star 桶切分，仍超限的桶按创建日期递归二分。
- **活跃度锚点**：以核心平台最新破坏性变更 release 的 `published_at` 为分界统计 `pushed`，比"近 N 天有推送"严格且可复现。
- **分类必须人工复核**：关键词预分类必然过度合并（实测 253/700 被吸进一个桶），digest 逐行读、逐个纠偏才是评估本身。
- **诚实边界**：长尾（star<10）只做元数据统计并明说，不假装读过全部 README。

Skill 也可安装到用户级目录直接触发：`cp -r skills/github-topic-audit ~/.agents/skills/`

## 复现

```bash
gh auth status   # 需要已认证的 gh CLI
python3 skills/github-topic-audit/scripts/fetch.py dsh-plugin --readme-top 700
python3 skills/github-topic-audit/scripts/stats.py audit-dsh-plugin \
    --anchor 2026-08-21T07:12:39Z
```

## License

- 本仓库分析报告与脚本：MIT
- `data/repos.jsonl` 为 GitHub API 公开元数据快照，版权归各仓库所有者
