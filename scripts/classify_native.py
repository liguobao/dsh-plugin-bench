#!/usr/bin/env python3
"""从 v1 审计数据中分离「DSH 原生插件」与「适配型独立产品」。

输入：data/analysis.json（top 700 README 摘要 + 机器预分类）
      data/repos.jsonl（9,393 仓库元数据，取 created/desc）
输出：data/native_plugins.jsonl（仅原生插件，按 star 降序）

判定规则（详见 report/DSH原生插件整理.md 第一节）：
  1. 时间线：DSH 生态可信起点为 2026-02-01（modlens 2026-02-22 自称
     "first vision plugin for DeepSeek Harness"）。创建早于该日期的仓库
     不可能为 DSH 而建，一律计 adapted。
  2. 定位：仓库名含 dsh/deepseek-harness，或描述/README 摘要以 DSH 为主
     战场；仅把 DSH 列为 N 个运行时之一（"works with DSH, Claude Code,
     OpenClaw, any runtime"）的计 adapted。
  3. 人工复核：头部高星样本逐个过目，PRODUCT_FIRST 为产品优先覆盖名单。
"""
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# DSH 生态可信起点；早于此日期创建的仓库按规则 1 判 adapted
ECOSYSTEM_START = "2026-02-01"

# v0.1.1-rc.1 发布时刻（活跃度锚点，与 v1 报告一致）
RC1 = datetime(2026, 8, 21, 7, 12, 39, tzinfo=timezone.utc)

# 产品优先（独立品牌 / 多平台运行时 / 非 DSH 插件），人工复核判定
PRODUCT_FIRST = {
    # 记忆赛道：先有产品后接 DSH，或把 DSH 列为多运行时之一
    "volcengine/OpenViking", "MemTensor/MemOS", "EverMind-AI/EverOS",
    "mem9-ai/mem9", "mnemon-dev/mnemon", "mindscale-noah/MindMemOS",
    "adoresever/graph-memory", "syncable-dev/memtrace-public",
    "tinqiao-oss/engramory", "Co-Engram/Co-Engram", "Ikalus1988/MisakaNet",
    # 独立产品 / 竞品 harness / 多平台工具
    "nexu-io/open-design", "ruvnet/ruflo", "esengine/DeepSeek-Reasonix",
    "Tencent/WeKnora", "Molunerfinn/PicGo", "nocobase/nocobase",
    "Nagi-ovo/voyager", "tt-a1i/archify", "titanwings/colleague-skill",
    "strukto-ai/mirage", "edison7009/EchoBird", "crafter-station/petdex",
    "hashgraph-online/hol-guard", "Q00/ouroboros", "ZSeven-W/openpencil",
    "Devin-AXIS/iPolloWork", "YaoApp/yao", "whiteguo233/OpenBiliClaw",
    "walkinglabs/learn-harness-engineering", "amruthpillai/reactive-resume",
    "Tiger3807861189/J-Space-Cognition-Suite-System",
    "freestylefly/awesome-gpt-image-2", "TencentCloudBase/CloudBase-AI-Toolkit",
    # 创建于生态起点之后，但定位是自有产品（DSH 仅为支持平台/渠道之一）
    "yejiming/MuseAI", "EthanYoQ/AI-Novel-Writer", "PM-Shawn/Abu-Cowork",
    "text2future/flowix", "alaliqing/claude-paper",
    "ccch1mneyyy/working-activity", "MarioZZJ/cc-notify-hooks",
}


def dsh_linked(repo: str, desc: str, first: str) -> bool:
    name = repo.lower()
    text = (desc + " " + first).lower()
    return (
        "dsh" in name
        or "deepseek-harness" in name
        or "deepseek_harness" in name
        or "deepseek harness" in text
        or "dsh-plugin" in text
        or "dsh plugin" in text
        or "(dsh)" in text
        or "（dsh）" in text
    )


def classify(repo: str, created: str, linked: bool) -> str:
    if repo in PRODUCT_FIRST:
        return "adapted"
    if created < ECOSYSTEM_START:
        return "adapted"
    return "native" if linked else "unrelated"


def main() -> None:
    analysis = json.loads((ROOT / "data/analysis.json").read_text())
    meta = {}
    with open(ROOT / "data/repos.jsonl") as f:
        for line in f:
            r = json.loads(line)
            meta[r["repo"]] = r

    rows = []
    for e in analysis:
        m = meta.get(e["repo"], {})
        pushed = e.get("pushed") or m.get("pushed")
        pd = datetime.fromisoformat(pushed.replace("Z", "+00:00")) if pushed else None
        rows.append(
            dict(
                repo=e["repo"],
                stars=e["stars"],
                cat=e["cat"],
                verdict=e["verdict"],
                first=e["first"][:200],
                created=(m.get("created") or "")[:10],
                desc=(m.get("desc") or "")[:200],
                rc1=bool(pd and pd > RC1),
                cls=classify(e["repo"], (m.get("created") or "")[:10],
                             dsh_linked(e["repo"], m.get("desc") or "", e["first"])),
            )
        )

    native = sorted((r for r in rows if r["cls"] == "native"), key=lambda x: -x["stars"])
    out = ROOT / "data/native_plugins.jsonl"
    with open(out, "w") as f:
        for r in native:
            f.write(json.dumps({k: r[k] for k in ("repo", "stars", "created", "rc1", "cat", "verdict", "desc")},
                               ensure_ascii=False) + "\n")

    counts = Counter(r["cls"] for r in rows)
    stars = {c: sum(r["stars"] for r in rows if r["cls"] == c) for c in counts}
    total = sum(stars.values())
    print(f"native    {counts['native']:4d} repos  {stars['native']:>7}★ ({stars['native'] * 100 // total}%)")
    print(f"adapted   {counts['adapted']:4d} repos  {stars['adapted']:>7}★ ({stars['adapted'] * 100 // total}%)")
    print(f"unrelated {counts['unrelated']:4d} repos  {stars['unrelated']:>7}★ ({stars['unrelated'] * 100 // total}%)")
    print(f"native rc1 follow-up: {sum(1 for r in native if r['rc1'])}/{len(native)}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
