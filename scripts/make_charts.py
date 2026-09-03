#!/usr/bin/env python3
"""为 DSH 插件生态评估报告生成中文图表。

输入：data/repos.jsonl、data/analysis.json、data/active_inventory.json
输出：charts/*.png
运行：python3 scripts/make_charts.py
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter, MultipleLocator

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CHART_DIR = ROOT / "charts"
CHART_DIR.mkdir(exist_ok=True)

AUDIT_SUMMARY = json.loads((DATA_DIR / "audit_summary.json").read_text(encoding="utf-8"))
ANCHOR = AUDIT_SUMMARY["snapshot"]["anchor"]
ANCHOR_LABEL = AUDIT_SUMMARY["snapshot"].get("anchor_label", "breaking release")
ANCHOR_DT = datetime.fromisoformat(ANCHOR.replace("Z", "+00:00"))
WINDOW_START = date(2026, 7, 15)

# 统一视觉系统：深蓝为主色，金色只承担关键强调，避免默认彩虹色。
INK = "#19324D"
TEXT = "#34495E"
MUTED = "#718096"
GRID = "#E7EDF3"
BLUE = "#2F6BFF"
BLUE_DARK = "#1F4EB8"
BLUE_MID = "#7FA6FF"
BLUE_LIGHT = "#DCE7FF"
GOLD = "#F2B84B"
ORANGE = "#E9873A"
GREY = "#B8C4D0"
GREY_LIGHT = "#E8EDF2"
WHITE = "#FFFFFF"


def configure_style() -> None:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in ("Noto Sans CJK SC", "WenQuanYi Zen Hei", "WenQuanYi Micro Hei", "PingFang SC", "Hiragino Sans GB", "Heiti SC", "Arial Unicode MS"):
        if name in available:
            plt.rcParams["font.family"] = [name, "DejaVu Sans"]
            break
    plt.rcParams.update(
        {
            "axes.unicode_minus": False,
            "figure.facecolor": WHITE,
            "axes.facecolor": WHITE,
            "axes.edgecolor": GRID,
            "axes.labelcolor": MUTED,
            "xtick.color": MUTED,
            "ytick.color": TEXT,
            "text.color": TEXT,
            "font.size": 11,
            "axes.titleweight": "normal",
            "axes.titlesize": 20,
            "axes.labelsize": 11,
            "legend.frameon": False,
            "savefig.facecolor": WHITE,
        }
    )


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def unique_repos() -> list[dict]:
    rows = load_jsonl(DATA_DIR / "repos.jsonl")
    return list({row["repo"]: row for row in rows}.values())


def chart_canvas(title: str, subtitle: str, *, height: float = 6.4):
    fig, ax = plt.subplots(figsize=(12, height))
    fig.subplots_adjust(left=0.105, right=0.95, top=0.76, bottom=0.17)
    fig.text(0.07, 0.93, title, fontsize=22, color=INK)
    fig.text(0.07, 0.875, subtitle, fontsize=11.5, color=MUTED)
    return fig, ax


def clean_axes(ax, *, grid: str | None = "y") -> None:
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="both", length=0, pad=8)
    if grid:
        ax.grid(axis=grid, color=GRID, linewidth=0.8, zorder=0)


def footer(fig, source: str) -> None:
    fig.text(0.07, 0.045, source, fontsize=9.2, color=MUTED)


def save(fig, filename: str) -> None:
    path = CHART_DIR / filename
    fig.savefig(path, dpi=180, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    print(f"已生成 {path.relative_to(ROOT)}")


def pct(value: int, total: int, digits: int = 1) -> str:
    return f"{value / total * 100:.{digits}f}%"


configure_style()
repos = unique_repos()
repo_total = len(repos)


# 01｜每日创建量：柱形显示每日新增，3 日均线压低单日噪声。
daily = Counter(
    datetime.fromisoformat(row["created"].replace("Z", "+00:00")).date()
    for row in repos
    if row["created"][:10] >= WINDOW_START.isoformat()
)
last_day = max(daily)
days: list[date] = []
cursor = WINDOW_START
while cursor <= last_day:
    days.append(cursor)
    cursor += timedelta(days=1)
values = [daily.get(day, 0) for day in days]
moving_avg = [sum(values[max(0, i - 2) : i + 1]) / min(3, i + 1) for i in range(len(values))]
peak_i = max(range(len(values)), key=values.__getitem__)

fig, ax = chart_canvas(
    "生态在 8 月中旬集中爆发",
    f"{WINDOW_START.isoformat()}—{last_day.isoformat()}｜柱：每日新建仓库；线：3 日移动平均",
)
bar_colors = [GOLD if i == peak_i else BLUE_LIGHT for i in range(len(days))]
ax.bar(days, values, width=0.78, color=bar_colors, edgecolor=WHITE, linewidth=0.5, zorder=2)
ax.plot(days, moving_avg, color=BLUE_DARK, linewidth=2.5, zorder=3)
ax.scatter(days[-1], moving_avg[-1], s=42, color=BLUE_DARK, zorder=4)
ax.annotate(
    f"峰值 {values[peak_i]:,} 个",
    xy=(days[peak_i], values[peak_i]),
    xytext=(0, 17),
    textcoords="offset points",
    ha="center",
    fontsize=11,
    fontweight="normal",
    color=INK,
)
ax.axvline(ANCHOR_DT.date(), color=ORANGE, linestyle=(0, (4, 4)), linewidth=1.4, zorder=1)
ax.text(
    ANCHOR_DT.date() - timedelta(days=0.25),
    max(values) * 0.73,
    f"{ANCHOR_LABEL} 发布",
    ha="right",
    color=ORANGE,
    fontsize=10,
    fontweight="normal",
)
ax.set_ylabel("新建仓库数")
ax.set_ylim(0, max(values) * 1.18)
ax.set_xlim(days[0] - timedelta(days=0.6), days[-1] + timedelta(days=0.6))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
ax.yaxis.set_major_locator(MultipleLocator(300))
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
clean_axes(ax, grid="y")
footer(fig, f"数据：GitHub API 仓库快照（n={repo_total:,}）；窗口内仓库 n={sum(values):,}")
save(fig, "01_daily_creation.png")


# 02｜星标金字塔：用零基线横条呈现真实数量，不使用对数轴夸大头部。
tiers = [
    ("0 星", 0, 1),
    ("1–4 星", 1, 5),
    ("5–19 星", 5, 20),
    ("20–99 星", 20, 100),
    ("100 星以上", 100, 10**12),
]
tier_labels = [item[0] for item in tiers]
tier_counts = [sum(1 for row in repos if lo <= row["stars"] < hi) for _, lo, hi in tiers]

fig, ax = chart_canvas(
    f"{(tier_counts[0] + tier_counts[1]) / repo_total:.0%} 的仓库不足 5 星",
    "按仓库当前 star 数分层｜横条从零起点绘制，标签同时给出数量与全量占比",
)
colors = [BLUE_DARK, BLUE, BLUE_MID, BLUE_LIGHT, GOLD]
bars = ax.barh(tier_labels[::-1], tier_counts[::-1], color=colors[::-1], height=0.6, zorder=2)
for bar, count in zip(bars, tier_counts[::-1]):
    ax.text(
        count + repo_total * 0.012,
        bar.get_y() + bar.get_height() / 2,
        f"{count:,}  ·  {pct(count, repo_total)}",
        va="center",
        fontsize=11,
        fontweight="normal",
        color=INK,
    )
ax.set_xlabel("仓库数")
ax.set_xlim(0, max(tier_counts) * 1.28)
ax.xaxis.set_major_locator(MultipleLocator(1000))
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x / 1000:.0f}k" if x else "0"))
clean_axes(ax, grid="x")
footer(fig, f"数据：GitHub API 仓库快照（n={repo_total:,}）；不足 5 星共 {tier_counts[0] + tier_counts[1]:,} 个")
save(fig, "02_star_pyramid.png")


# 03｜锚点活跃率：点线图强调“星越多，跟进率越高”，同时保留总体基准。
activity_rows = []
for label, lo, hi in tiers:
    group = [row for row in repos if lo <= row["stars"] < hi]
    active = sum(1 for row in group if row["pushed"] >= ANCHOR)
    activity_rows.append((label, active, len(group), active / len(group) * 100))

fig, ax = chart_canvas(
    "高星不等于持续维护",
    f"以 {ANCHOR_LABEL} 破坏性变更为锚｜点表示各星级段在发布后仍有 push 的比例",
)
y = list(range(len(activity_rows)))
rates = [row[3] for row in activity_rows]
for yi, rate in zip(y, rates):
    ax.hlines(yi, 0, rate, color=BLUE_LIGHT, linewidth=7, zorder=1)
ax.scatter(rates[:-1], y[:-1], s=115, color=BLUE, edgecolor=WHITE, linewidth=1.6, zorder=3)
ax.scatter(rates[-1], y[-1], s=135, color=GOLD, edgecolor=WHITE, linewidth=1.6, zorder=4)
overall = sum(row[1] for row in activity_rows) / repo_total * 100
ax.axvline(overall, color=ORANGE, linestyle=(0, (4, 4)), linewidth=1.5, zorder=0)
ax.text(overall + 1, len(y) - 0.25, f"全量 {overall:.1f}%", color=ORANGE, fontsize=10)
for yi, (_, active, total, rate) in enumerate(activity_rows):
    ax.text(rate + 1.5, yi, f"{rate:.1f}%  ({active:,}/{total:,})", va="center", color=INK, fontsize=10.5)
ax.set_yticks(y, [row[0] for row in activity_rows])
ax.set_xlabel(f"{ANCHOR_LABEL} 发布后有 push 的仓库占比")
ax.set_xlim(0, 70)
ax.xaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
clean_axes(ax, grid="x")
footer(fig, f"数据：GitHub API 仓库快照（n={repo_total:,}）；锚点：{ANCHOR_DT:%Y-%m-%d %H:%M} UTC")
save(fig, "03_rc1_activity.png")


# 04｜语言构成：直接标出数量和占比，突出 Cordis 体系中的 JS/TS 双核心。
language_counts = Counter(row.get("lang") or "未识别" for row in repos)
top_languages = language_counts.most_common(6)
other_count = repo_total - sum(value for _, value in top_languages)
language_names = [name for name, _ in top_languages] + ["其他"]
language_values = [value for _, value in top_languages] + [other_count]
js_ts = language_counts["JavaScript"] + language_counts["TypeScript"]

fig, ax = chart_canvas(
    f"JavaScript 与 TypeScript 构成 {js_ts / repo_total:.0%} 的生态",
    "按仓库主语言统计｜其余语言合并为“其他”，避免低频类别干扰主要结构",
)
language_colors = [BLUE_DARK, BLUE, GOLD] + [GREY] * (len(language_values) - 3)
bars = ax.barh(language_names[::-1], language_values[::-1], color=language_colors[::-1], height=0.6, zorder=2)
for bar, value in zip(bars, language_values[::-1]):
    ax.text(
        value + repo_total * 0.011,
        bar.get_y() + bar.get_height() / 2,
        f"{value:,}  ·  {pct(value, repo_total)}",
        va="center",
        fontsize=10.5,
        color=INK,
    )
ax.set_xlabel("仓库数")
ax.set_xlim(0, max(language_values) * 1.24)
ax.xaxis.set_major_locator(MultipleLocator(1000))
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x / 1000:.0f}k" if x else "0"))
clean_axes(ax, grid="x")
footer(fig, f"数据：GitHub API 仓库快照（n={repo_total:,}）；JS + TS 共 {js_ts:,} 个，占 {pct(js_ts, repo_total)}")
save(fig, "04_languages.png")


# 05｜生命周期交叉：旧版环图把“创建日一次性 push”与“锚点后有 push”误当成互斥。
# 新图使用 2×2 交叉结果，既保留一次性比例，也不重复计算锚点后的新仓库。
one_shot = {row["repo"] for row in repos if row["pushed"][:10] <= row["created"][:10]}
rc1_active = {row["repo"] for row in repos if row["pushed"] >= ANCHOR}
life_rows = [
    ("创建日后仍持续推送", repo_total - len(one_shot)),
    ("仅在创建日推送", len(one_shot)),
]
life_inactive = [
    len({row["repo"] for row in repos} - one_shot - rc1_active),
    len(one_shot - rc1_active),
]
life_active = [
    len(rc1_active - one_shot),
    len(rc1_active & one_shot),
]

fig, ax = chart_canvas(
    f"{life_active[0] / repo_total:.1%} 同时满足“持续推送”与“跟进 {ANCHOR_LABEL}”",
    f"一次性推送与 {ANCHOR_LABEL} 跟进状态交叉｜两项口径存在重叠，因此采用 2×2 结构而非环图",
)
y = [0, 1]
row_totals = [row[1] for row in life_rows]
inactive_share = [value / total * 100 for value, total in zip(life_inactive, row_totals)]
active_share = [value / total * 100 for value, total in zip(life_active, row_totals)]
ax.barh(y, inactive_share, color=GREY_LIGHT, edgecolor=WHITE, height=0.52, label=f"{ANCHOR_LABEL} 后无 push", zorder=2)
ax.barh(y, active_share, left=inactive_share, color=BLUE, edgecolor=WHITE, height=0.52, label=f"{ANCHOR_LABEL} 后有 push", zorder=2)
for yi, (inactive, active, total) in enumerate(zip(life_inactive, life_active, row_totals)):
    ax.text(inactive / total * 50, yi, f"{inactive:,}\n{inactive / total:.1%}", ha="center", va="center", color=TEXT, fontsize=10)
    if active / total * 100 >= 8:
        ax.text(
            inactive / total * 100 + active / total * 50,
            yi,
            f"{active:,}\n{active / total:.1%}",
            ha="center",
            va="center",
            color=WHITE,
            fontsize=10,
            fontweight="normal",
        )
ax.set_yticks(y, [f"{label}\n共 {total:,} 个" for label, total in life_rows])
ax.set_xlabel("组内占比")
ax.set_xlim(0, 100)
ax.xaxis.set_major_locator(MultipleLocator(20))
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.03), ncol=2)
clean_axes(ax, grid="x")
footer(fig, f"数据：GitHub API 仓库快照（n={repo_total:,}）；持续推送且 {ANCHOR_LABEL} 后活跃 {life_active[0]:,} 个")
save(fig, "05_lifecycle.png")


# 06｜活跃品类：旧人工标签 + 本轮机器辅助增量，展示头部 12 类。
active_inventory = json.loads((DATA_DIR / "active_inventory.json").read_text(encoding="utf-8"))
category_counts = Counter(row["cat"] for row in active_inventory)
category_names = {
    "session-ui-ux": "会话 / Web UI 微增强",
    "search-web": "搜索 / 网页 / 浏览器",
    "desktop-client": "桌面客户端 / 启动器",
    "market-curation": "插件市场 / 目录",
    "model-provider": "订阅 / Provider / 路由",
    "orchestration-workflow": "编排 / 多 Agent / 工作流",
    "usage-billing": "用量 / 计费",
    "memory-knowledge": "记忆 / 知识库",
    "eng-git-ci": "工程化 / Git / CI",
    "vertical-domain": "垂直领域",
    "skills-presets": "技能包 / 预设",
    "security-governance": "安全 / 权限 / 治理",
    "vision-multimodal": "视觉 / 多模态",
    "fun-novelty": "趣味 / 玩具",
    "other": "其他",
    "remote-access": "远程访问",
    "mobile-client": "移动端本机客户端",
}
top_categories = category_counts.most_common(12)
shown_categories = {name for name, _ in top_categories}
if "remote-access" in category_counts and "remote-access" not in shown_categories:
    top_categories.append(("remote-access", category_counts["remote-access"]))
other_categories = len(active_inventory) - sum(value for _, value in top_categories)
category_labels = [category_names.get(name, name) for name, _ in top_categories]
category_values = [value for _, value in top_categories]

fig, ax = chart_canvas(
    "会话体验是最大需求，但生态高度碎片化",
    f"“活跃 × 有星”{len(active_inventory):,} 个仓库｜数量前 12 类 + 远程访问；其余类别共 {other_categories} 个",
    height=7.4,
)
category_colors = [
    ORANGE if name == "remote-access" else GOLD if i == 0 else BLUE if i < 5 else BLUE_LIGHT
    for i, (name, _) in enumerate(top_categories)
]
bars = ax.barh(category_labels[::-1], category_values[::-1], color=category_colors[::-1], height=0.58, zorder=2)
for bar, value in zip(bars, category_values[::-1]):
    ax.text(value + 3, bar.get_y() + bar.get_height() / 2, f"{value:,}", va="center", color=INK, fontsize=10.5)
ax.set_xlabel("仓库数")
ax.set_xlim(0, max(category_values) * 1.15)
ax.xaxis.set_major_locator(MultipleLocator(25))
clean_axes(ax, grid="x")
footer(fig, f"数据：data/active_inventory.json（n={len(active_inventory):,}；旧人工标签 + 增量机器辅助分类）")
save(fig, "06_active_categories.png")


# 07｜原生 / 适配 / 无关：直接使用本轮完整三桶明细。
classified = load_jsonl(DATA_DIR / "classification.jsonl")

classes = ["native", "adapted", "unrelated"]
class_labels = ["DSH 原生", "适配型独立产品", "蹭 tag / 无关"]
class_colors = [BLUE, GOLD, GREY]
repo_counts = [sum(1 for row in classified if row["cls"] == cls) for cls in classes]
star_counts = [sum(row["stars"] for row in classified if row["cls"] == cls) for cls in classes]

fig, ax = chart_canvas(
    f"适配型产品只占 {repo_counts[1] / sum(repo_counts):.0%}，却拿走 {star_counts[1] / sum(star_counts):.0%} 的星",
    f"README 覆盖的 {len(classified):,} 个仓库｜同一三桶口径比较仓库数量与星标总量",
)
series = [("仓库数量", repo_counts), ("星标总量", star_counts)]
for yi, (label, values) in enumerate(series):
    total = sum(values)
    left = 0.0
    for value, color, class_label in zip(values, class_colors, class_labels):
        share = value / total * 100
        ax.barh(yi, share, left=left, color=color, height=0.5, edgecolor=WHITE, linewidth=1.5, zorder=2)
        value_label = f"{value:,}" if label == "仓库数量" else f"{value / 1000:.0f}k★"
        if share >= 15:
            segment_text = f"{class_label}\n{share:.1f}% · {value_label}"
        elif share >= 7:
            segment_text = f"{share:.1f}%\n{value_label}"
        elif share >= 4:
            segment_text = f"{share:.1f}%"
        else:
            segment_text = ""
        if segment_text:
            ax.text(left + share / 2, yi, segment_text, ha="center", va="center", color=WHITE if color != GOLD else INK, fontsize=10)
        left += share
ax.set_yticks([0, 1], [f"仓库数量\n{len(classified):,} 个", f"星标总量\n{sum(star_counts) / 1000:.0f}k★"])
ax.set_xlim(0, 100)
ax.set_xlabel("构成占比")
ax.xaxis.set_major_locator(MultipleLocator(20))
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in class_colors]
ax.legend(handles, class_labels, loc="lower center", bbox_to_anchor=(0.5, 1.03), ncol=3)
clean_axes(ax, grid="x")
footer(fig, "数据：data/classification.jsonl；DSH 本体按报告口径排除")
save(fig, "07_native_adapted.png")


# 08｜远程访问：按主要连接路线拆分，移动端本机运行不计入此图。
audit_summary = AUDIT_SUMMARY
remote = audit_summary["remote_access"]
route_names = {
    "lan-gateway": "局域网 / Web 网关",
    "cloudflare-tunnel": "Cloudflare Tunnel",
    "reverse-proxy-self-hosted": "反向代理 / 自托管",
    "vpn-overlay": "Tailscale / Overlay VPN",
    "hosted-e2ee-relay": "托管 E2EE 中继",
    "hosted-relay": "托管 Relay",
    "e2ee-pairing": "E2EE 配对传输",
    "peer-to-peer": "P2P",
    "third-party-tunnel": "第三方隧道",
    "generic-remote": "其他 / 未明确",
}
route_rows = sorted(remote["routes"].items(), key=lambda item: item[1])
route_labels = [route_names.get(name, name) for name, _ in route_rows]
route_values = [value for _, value in route_rows]

fig, ax = chart_canvas(
    f"远程访问成为独立产品线：{remote['repos']:,} 个活跃仓库",
    f"按 README / 仓库描述的主技术路线归类｜原生 {remote['native']:,} 个；star ≥ 10 共 {remote['star_10_plus']:,} 个",
    height=6.8,
)
bars = ax.barh(route_labels, route_values, color=[ORANGE if value == max(route_values) else BLUE_LIGHT for value in route_values], height=0.58)
for bar, value in zip(bars, route_values):
    ax.text(value + 0.5, bar.get_y() + bar.get_height() / 2, f"{value:,}", va="center", color=INK)
ax.set_xlabel("仓库数")
ax.set_xlim(0, max(route_values) * 1.2)
ax.xaxis.set_major_locator(MultipleLocator(5))
clean_axes(ax, grid="x")
remote_dist = remote["distribution"]["all"]
footer(
    fig,
    f"数据：data/audit_summary.json；分发缓存覆盖 {remote_dist['repos']:,}/{remote['repos']:,}，有 Release {remote_dist['with_releases']:,}，已发布 npm {remote_dist['published_npm']:,}",
)
save(fig, "08_remote_access.png")


print("完成：共生成 8 张中文图表")
