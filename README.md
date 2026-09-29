# dsh-plugin-bench

DeepSeek Harness（DSH）插件生态的独立基准评估：基于 GitHub API 一手数据枚举 topic，分析活跃度、高星停滞、原生/适配/无关三桶、品类结构与 Release/npm 分发完成度。

本轮快照日期为 **2026-09-30**：实际枚举 16,535 个仓库；复查时 GitHub topic 官方计数为 16,670，覆盖 99.19%。完整结论见 [DSH 插件生态评估报告](report/DSH插件生态评估报告-2026-09-30.md)。

## 最新核心指标

| 指标 | 数值 |
|---|---:|
| 去重仓库 | 16,535 |
| 一次性仓库 | 6,088（36.8%） |
| v0.2.0-rc.1 后有 push | 464（2.8%） |
| 活跃 × 有星 | 354 |
| 原生 × 活跃 × 有星 | 305 |
| star ≥ 10 | 1,264（139 活跃 / 1,125 停滞） |
| README 覆盖 | 2,177 |
| 分发缓存覆盖 | 354 / 354 个活跃有星仓库 |
| npm 已发布 | 223 / 354 个活跃有星仓库 |
| 写好包名但未发布 npm | 79 |
| 远程访问 | 9（1 个 ≥10★） |
| 移动端本机客户端 | 1 |

固定锚点后的新建仓库也会计入“有 push”，因此 2.8% 不是纯粹的存量留存率。更可靠的生态核心口径是 354 个“活跃 × 有星”仓库。

## 主要发现

本轮为自动化统计及初步分类。README 每份最多缓存前 8,000 字符，2,177 份是非空缓存及预分类数量，不是人工完整深读数量；分类规则中的人工标签含历史沿用。分发脚本没有区分请求失败与查无结果，以下“未发布”等负向判断和下载归属仍需复核。锚点后 push 不等于兼容性验证。

- 0–4★ 仓库占 85.3%，生态规模依然由长尾构成。
- 重点判定集合共 4,306 个仓库：原生 3,948、适配型独立产品 87、无关 271；适配型产品仍占据大部分 star。
- 原生活跃仓库贡献 854,767 次 npm 周下载；分发数据已覆盖全部 354 个活跃有星仓库。
- 核心远程访问按“从另一台设备经网络访问并操作正在运行的 DSH”严格统计：9 个活跃仓库、429★；远端工作区开发、实例运维、插件救援及移动端本机客户端均另计。
- 79 个活跃有星仓库写有 package name 却未发布 npm，安装链路仍是明确的生态工程债。
- 新增生产力筛选层：354 个活跃有星候选中筛出 208 个原生生产力工具，按知识检索、文档办公、工程交付、工作流自动化、协作通知、安全访问、模型成本和视觉生产分类。

## 数据文件

| 文件 | 内容 |
|---|---|
| `data/repos.jsonl` | 16,535 条仓库元数据 |
| `data/analysis.json` / `data/digest.txt` | 2,177 份 README 的预分类与摘要 |
| `data/active_set.jsonl` | 354 个活跃有星仓库 |
| `data/active_inventory.json` / `.md` | 活跃品类清单，含分类来源与远程访问分类 |
| `data/classification.jsonl` | 4,306 个重点仓库的原生 / 适配 / 无关明细 |
| `data/native_plugins.jsonl` | 3,948 个原生仓库 |
| `data/dist_check.jsonl` | 354 个活跃仓库的 Release/npm 数据 |
| `data/audit_summary.json` | 报告使用的结构化汇总 |
| `data/productivity_analysis.json` / `.md` | 生产力工具筛选、类别、证据词和分发信号 |

活跃品类使用历史人工标签、本轮人工复核、增量规则和仅元数据判断；`classification_source` 字段保留来源差异。本轮分发数据覆盖全部活跃有星仓库，README 覆盖 Top 2,000 高星仓库及全部活跃有星仓库的并集。

## 图表

| 图 | 内容 |
|---|---|
| ![每日新建仓库](charts/01_daily_creation.png) | 每日创建量与三日移动平均 |
| ![星标分层](charts/02_star_pyramid.png) | star 金字塔 |
| ![v0.2.0-rc.1 活跃率](charts/03_rc1_activity.png) | 各星级段 v0.2.0-rc.1 跟进率 |
| ![语言构成](charts/04_languages.png) | 仓库主语言 |
| ![生命周期](charts/05_lifecycle.png) | 一次性 push 与 v0.2.0-rc.1 跟进交叉 |
| ![活跃品类](charts/06_active_categories.png) | 354 个活跃有星仓库的主要类别与远程访问 |
| ![三桶对比](charts/07_native_adapted.png) | 原生 / 适配 / 无关的仓库数与星标份额 |
| ![远程访问](charts/08_remote_access.png) | 9 个核心远程访问项目的主要技术路线 |

图表可通过 `python3 scripts/make_charts.py` 重新生成。

## 复现

```bash
python3 skills/github-topic-audit/scripts/fetch.py dsh-plugin \
  --out audit-dsh-plugin-20260929 --readme-top 2000

python3 skills/github-topic-audit/scripts/stats.py audit-dsh-plugin-20260929 \
  --anchor-release deepseek-ai/deepseek-harness@dsh-v0.2.0-rc.1

python3 skills/github-topic-audit/scripts/classify_native.py audit-dsh-plugin-20260929 \
  --start 2026-02-01 \
  --kw dsh --kw deepseek-harness --kw 'deepseek harness' --kw deepseek_harness \
  --anchor 2026-09-28T12:36:21Z \
  --product-first data/product_first.txt \
  --exclude deepseek-ai/deepseek-harness \
  --previous data/classification.jsonl \
  --supplement-active-high

python3 scripts/build_active_inventory.py audit-dsh-plugin-20260929 \
  --previous data/active_inventory.json \
  --anchor 2026-09-28T12:36:21Z

python3 skills/github-topic-audit/scripts/check_dist.py audit-dsh-plugin-20260929 \
  --repos audit-dsh-plugin-20260929/active_set.jsonl \
  --native-file audit-dsh-plugin-20260929/native_plugins.jsonl

python3 scripts/build_audit_summary.py audit-dsh-plugin-20260929 \
  --official-count 16670 \
  --official-source 'GitHub Search API 2026-09-30 复查' \
  --anchor 2026-09-28T12:36:21Z \
  --anchor-label v0.2.0-rc.1

python3 scripts/write_audit_report.py \
  audit-dsh-plugin-20260929/audit_summary.json --date 2026-09-30
```

Top 2,000 之外的活跃有星仓库 README 补齐步骤见 `skills/github-topic-audit/SKILL.md` 第 4 步；补齐后需重新运行 `stats.py`。

完整流程与分类边界见 `skills/github-topic-audit/SKILL.md`。

生产力工具专项结果见 [生产力工具插件分析](report/DSH生产力工具插件分析-2026-09-30.md)。

## License

- 本仓库报告与脚本：MIT
- `data/repos.jsonl` 等 GitHub API 元数据及第三方 README 版权归各自作者所有
