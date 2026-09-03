# dsh-plugin-bench

DeepSeek Harness（DSH）插件生态的独立基准评估：基于 GitHub API 一手数据枚举 topic，分析活跃度、高星停滞、原生/适配/无关三桶、品类结构与 Release/npm 分发完成度。

本轮快照日期为 **2026-09-03**：实际枚举 13,321 个仓库。枚举期间 GitHub 搜索各星级分桶合计同为 13,321；结束时的官方计数复查因未获网络权限而未执行。完整结论见 [DSH 插件生态评估报告](report/DSH插件生态评估报告.md)。

## 最新核心指标

| 指标 | 数值 |
|---|---:|
| 去重仓库 | 13,321 |
| 一次性仓库 | 5,624（42.2%） |
| v0.1.2-alpha.4 后有 push | 1,503（11.3%） |
| 活跃 × 有星 | 1,050 |
| 原生 × 活跃 × 有星 | 929 |
| star ≥ 10 | 984（303 活跃 / 681 停滞） |
| README 覆盖 | 700 |
| 分发缓存覆盖 | 521 / 1,050 个活跃有星仓库 |
| npm 已发布 | 264 / 521 个已检查仓库 |
| 写好包名但未发布 npm | 149 |
| 远程访问 | 8（5 个 ≥10★） |
| 移动端本机客户端 | 5 |

固定锚点后的新建仓库也会计入“有 push”，因此 11.3% 不是纯粹的存量留存率。更可靠的生态核心口径是 1,050 个“活跃 × 有星”仓库。

## 主要发现

- 0–4★ 仓库占 85.7%，生态规模依然由长尾构成。
- 重点判定集合共 2,877 个仓库：原生 2,588、适配型独立产品 86、无关 203；适配型产品仍占据大部分 star。
- 原生活跃仓库在已检查样本中贡献 487,022 次 npm 周下载；分发数据仅覆盖 521 / 1,050 个活跃有星仓库，不外推为全量。
- 核心远程访问按“从另一台设备经网络访问并操作正在运行的 DSH”严格统计：8 个活跃仓库、1,353★，覆盖局域网/Web 网关、认证代理、Cloudflare Tunnel、托管 Relay 和 P2P 优先网络；远端工作区开发、实例运维、插件救援及移动端本机客户端均另计。
- 已检查项目中，149 个仓库写有 package name 却未发布 npm，安装链路仍是明确的生态工程债。

## 数据文件

| 文件 | 内容 |
|---|---|
| `data/repos.jsonl` | 13,321 条仓库元数据 |
| `data/analysis.json` / `data/digest.txt` | 700 份 README 的预分类与摘要 |
| `data/active_set.jsonl` | 1,050 个活跃有星仓库 |
| `data/active_inventory.json` / `.md` | 活跃品类清单，含分类来源与远程访问分类 |
| `data/classification.jsonl` | 2,877 个重点仓库的原生 / 适配 / 无关明细 |
| `data/native_plugins.jsonl` | 2,588 个原生仓库 |
| `data/dist_check.jsonl` | 521 个活跃仓库的缓存 Release/npm 数据 |
| `data/audit_summary.json` | 报告使用的结构化汇总 |

活跃品类使用历史人工标签、本轮人工复核、增量规则和仅元数据判断；`classification_source` 字段保留来源差异。本轮未能联网补齐全部 README 与分发数据，报告对覆盖范围作了明确标注。

## 图表

| 图 | 内容 |
|---|---|
| ![每日新建仓库](charts/01_daily_creation.png) | 每日创建量与三日移动平均 |
| ![星标分层](charts/02_star_pyramid.png) | star 金字塔 |
| ![alpha.4 活跃率](charts/03_rc1_activity.png) | 各星级段 v0.1.2-alpha.4 跟进率 |
| ![语言构成](charts/04_languages.png) | 仓库主语言 |
| ![生命周期](charts/05_lifecycle.png) | 一次性 push 与 alpha.4 跟进交叉 |
| ![活跃品类](charts/06_active_categories.png) | 1,050 个活跃有星仓库的前 12 类 + 远程访问 |
| ![三桶对比](charts/07_native_adapted.png) | 原生 / 适配 / 无关的仓库数与星标份额 |
| ![远程访问](charts/08_remote_access.png) | 8 个核心远程访问项目的主要技术路线 |

图表可通过 `python3 scripts/make_charts.py` 重新生成。

## 复现

```bash
python3 skills/github-topic-audit/scripts/fetch.py dsh-plugin \
  --out audit-dsh-plugin-20260903 --readme-top 700

python3 skills/github-topic-audit/scripts/stats.py audit-dsh-plugin-20260903 \
  --anchor 2026-09-01T15:45:07Z

python3 skills/github-topic-audit/scripts/classify_native.py audit-dsh-plugin-20260903 \
  --start 2026-02-01 \
  --kw dsh --kw deepseek-harness --kw 'deepseek harness' --kw deepseek_harness \
  --anchor 2026-09-01T15:45:07Z \
  --product-first data/product_first.txt \
  --exclude deepseek-ai/deepseek-harness \
  --previous data/classification.jsonl \
  --supplement-active-high

python3 scripts/build_active_inventory.py audit-dsh-plugin-20260903 \
  --previous data/active_inventory.json \
  --anchor 2026-09-01T15:45:07Z

python3 scripts/build_audit_summary.py audit-dsh-plugin-20260903 \
  --official-count 13321 \
  --official-source '枚举期间 GitHub 搜索各星级分桶合计；结束时复查未获网络权限' \
  --anchor 2026-09-01T15:45:07Z \
  --anchor-label v0.1.2-alpha.4

# 每次生成独立报告；同日重复运行自动追加 -02、-03……
python3 scripts/write_audit_report.py \
  audit-dsh-plugin-20260903/audit_summary.json --date 2026-09-03
```

完整流程与分类边界见 `skills/github-topic-audit/SKILL.md`。

## License

- 本仓库报告与脚本：MIT
- `data/repos.jsonl` 等 GitHub API 元数据及第三方 README 版权归各自作者所有
