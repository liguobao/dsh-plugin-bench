#!/usr/bin/env python3
"""Generate audit charts from data/repos.jsonl + data/analysis.json.

Outputs PNGs into charts/. English labels (font-safe), GitHub-embeddable.
Run from repo root: python3 scripts/make_charts.py
"""
import json, os
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# CJK-capable fallback so mixed labels never tofu
for name in ["PingFang SC", "Hiragino Sans GB", "Arial Unicode MS", "Heiti TC"]:
    if name in {f.name for f in font_manager.fontManager.ttflist}:
        plt.rcParams["font.family"] = [name, "DejaVu Sans"]
        break
plt.rcParams["axes.unicode_minus"] = False

C_MAIN, C_ACCENT, C_WARN, C_MUTED = "#2563eb", "#f59e0b", "#dc2626", "#94a3b8"
os.makedirs("charts", exist_ok=True)

repos = [json.loads(l) for l in open("data/repos.jsonl")]
uniq = {r["repo"]: r for r in repos}
rs = list(uniq.values())
ANCHOR = "2026-08-21T07:12:39"

def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"charts/{name}", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote charts/" + name)

# ---- 1. Daily creations + cumulative growth --------------------------------
# The raw set spans 182 distinct creation dates: old repos (often tag-squatters)
# created long before the ecosystem existed. Chart the ecosystem window only.
WINDOW_START = "2026-07-15"
pre = sum(1 for r in rs if r["created"][:10] < WINDOW_START)
daily = Counter(r["created"][:10] for r in rs if r["created"][:10] >= WINDOW_START)
days = sorted(daily)
vals = [daily[d] for d in days]
cum, t = [], 0
for v in vals:
    t += v
    cum.append(t)

fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(days, vals, color=C_MAIN, width=0.7, label="new repos / day")
ax2 = ax.twinx()
ax2.plot(days, cum, color=C_WARN, lw=2, label="cumulative (in window)")
ax2.set_ylabel("cumulative repos", color=C_WARN)
ax.set_ylabel("new repos per day")
ax.set_title(f"dsh-plugin topic: daily repo creation (n={len(rs)-pre} since {WINDOW_START}; "
             f"{pre} older repos predate the window)")
ax.tick_params(axis="x", rotation=60)
ax.annotate("peak 1,508/day", xy=(days.index("2026-08-14"), 1508), xytext=(10, -4),
            textcoords="offset points", fontsize=9, color=C_MUTED)
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper left")
save(fig, "01_daily_creation.png")

# ---- 2. Star pyramid (log) --------------------------------------------------
tiers = [("0 star", 0, 1), ("1-4", 1, 5), ("5-19", 5, 20), ("20-99", 20, 100),
         ("100+", 100, 10**9)]
names = [t[0] for t in tiers]
counts = [sum(1 for r in rs if t[1] <= r["stars"] < t[2]) for t in tiers]
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(names, counts, color=[C_MUTED, C_MUTED, C_MAIN, C_MAIN, C_WARN])
ax.set_yscale("log")
ax.set_ylabel("repos (log scale)")
ax.set_title("star pyramid: 86% of the topic has fewer than 5 stars")
for b, c in zip(bars, counts):
    ax.annotate(f"{c:,}", xy=(b.get_x() + b.get_width() / 2, c), xytext=(0, 3),
                textcoords="offset points", ha="center", fontsize=10)
save(fig, "02_star_pyramid.png")

# ---- 3. rc.1 anchor adaptation by star tier ---------------------------------
pct = []
for _, lo, hi in tiers:
    g = [r for r in rs if lo <= r["stars"] < hi]
    pct.append(100 * sum(1 for r in g if r["pushed"] >= ANCHOR) / len(g))
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(names, pct, color=[C_MUTED, C_MUTED, C_MAIN, C_MAIN, C_WARN])
ax.axhline(20.6, color=C_WARN, ls="--", lw=1.5)
ax.annotate("overall 20.6%", xy=(0.02, 21.5), fontsize=9, color=C_WARN)
ax.set_ylabel("% pushed after rc.1 (2026-08-21T07:12Z)")
ax.set_ylim(0, 70)
ax.set_title("true-activity anchor: share adapted to breaking change, by star tier")
for b, p in zip(bars, pct):
    ax.annotate(f"{p:.0f}%", xy=(b.get_x() + b.get_width() / 2, p), xytext=(0, 3),
                textcoords="offset points", ha="center", fontsize=10)
save(fig, "03_rc1_activity.png")

# ---- 4. Language mix --------------------------------------------------------
lang = Counter(r["lang"] or "(none)" for r in rs)
top = lang.most_common(6)
other = len(rs) - sum(c for _, c in top)
labels = [n for n, _ in top] + ["other"]
lvals = [c for _, c in top] + [other]
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(labels[::-1], lvals[::-1], color=C_MAIN)
ax.set_xlabel("repos")
ax.set_title("language mix: JS+TS = 90% (Cordis plugin system)")
for b, v in zip(bars, lvals[::-1]):
    ax.annotate(f"{v:,}", xy=(v, b.get_y() + b.get_height() / 2), xytext=(4, 0),
                textcoords="offset points", va="center", fontsize=9)
save(fig, "04_languages.png")

# ---- 5. Lifecycle: one-shot vs sustained -------------------------------------
one_shot = sum(1 for r in rs if r["pushed"][:10] <= r["created"][:10])
adapted = sum(1 for r in rs if r["pushed"] >= ANCHOR)
middle = len(rs) - one_shot - adapted
fig, ax = plt.subplots(figsize=(6, 6))
w, _, at = ax.pie(
    [one_shot, middle, adapted],
    labels=[f"one-shot only\n(pushed on creation day)\n{one_shot:,} = {one_shot/len(rs)*100:.0f}%",
            f"active before rc.1\nonly\n{middle:,} = {middle/len(rs)*100:.0f}%",
            f"adapted after rc.1\n{adapted:,} = {adapted/len(rs)*100:.0f}%"],
    colors=[C_MUTED, "#bfdbfe", C_WARN], startangle=90, autopct="",
    wedgeprops=dict(width=0.42), textprops=dict(fontsize=10))
ax.set_title(f"lifecycle split of {len(rs):,} repos\n(rc.1 anchor 2026-08-21)")
save(fig, "05_lifecycle.png")

print("done: 5 charts")
