#!/usr/bin/env python3
"""Build the community content map and productivity layer for a topic audit.

The content map is the census: every enumerated repository gets one broad
content family. The productivity layer is a narrower recommendation set built
from active, starred, native repositories with README evidence.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


FAMILIES = {
    "client-and-shell": ["desktop", "桌面", "client", "客户端", "launcher", "electron", "tauri", "web app"],
    "model-and-provider": ["model", "模型", "provider", "ollama", "vllm", "router", "route", "inference", "oauth", "api key"],
    "knowledge-and-context": ["memory", "记忆", "knowledge", "知识", "rag", "embedding", "retrieval", "context", "上下文"],
    "search-and-web": ["search", "搜索", "browser", "浏览器", "web search", "scrape", "crawler", "网页"],
    "engineering-and-delivery": ["git", "commit", "review", "ci", "lint", "debug", "deploy", "build", "test", "代码", "开发"],
    "workflow-and-agents": ["workflow", "工作流", "automation", "自动化", "pipeline", "orchestration", "subagent", "multi-agent", "编排"],
    "documents-and-office": ["office", "docx", "pdf", "pptx", "xlsx", "excel", "word", "文档", "报告", "resume", "简历"],
    "communication-and-notify": ["notification", "通知", "telegram", "slack", "discord", "wechat", "微信", "飞书", "email", "calendar", "日历"],
    "security-and-remote": ["security", "安全", "permission", "权限", "secret", "encrypt", "加密", "sandbox", "remote", "远程", "relay", "tunnel", "ssh"],
    "visual-and-media": ["vision", "视觉", "image", "图像", "ocr", "screenshot", "video", "audio", "音频", "design", "设计"],
    "market-and-skills": ["market", "市场", "plugin manager", "插件管理", "skill", "技能", "prompt", "提示词", "awesome", "curated"],
    "ui-and-theme": ["theme", "主题", "skin", "皮肤", "sidebar", "侧边栏", "statusline", "tui", "wallpaper", "壁纸"],
    "fun-and-novelty": ["pet", "桌宠", "meme", "joke", "toy", "roleplay", "galgame", "小游戏", "娱乐"],
    "vertical-domain": ["finance", "金融", "trading", "股票", "legal", "法律", "medical", "医疗", "education", "教育", "robot", "量化"],
}


def family(text: str) -> tuple[str, list[str]]:
    text = text.lower()
    scores = {name: [kw for kw in kws if kw in text] for name, kws in FAMILIES.items()}
    scores = {name: hits for name, hits in scores.items() if hits}
    if not scores:
        return "unclassified-or-low-signal", []
    name = max(scores, key=lambda key: len(scores[key]))
    return name, scores[name][:8]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.open() if line.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("audit_dir", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    out = args.out or args.audit_dir / "plugin_landscape.json"

    repos = read_jsonl(args.audit_dir / "repos.jsonl")
    active = {row["repo"] for row in read_jsonl(args.audit_dir / "active_set.jsonl")}
    classified = {row["repo"]: row.get("cls", "unclassified") for row in read_jsonl(args.audit_dir / "classification.jsonl")}
    productivity = json.loads((args.audit_dir / "productivity_analysis.json").read_text())
    productive = {row["repo"]: row for row in productivity["all"]}
    analysis_rows = json.loads((args.audit_dir / "analysis.json").read_text())
    analysis = {row["repo"]: row for row in analysis_rows}

    records = []
    for row in repos:
        repo = row["repo"]
        evidence = " ".join([repo, row.get("desc") or "", " ".join(analysis.get(repo, {}).get("first", "").split())])
        content_family, signals = family(evidence)
        records.append({
            "repo": repo,
            "stars": row["stars"],
            "pushed": row["pushed"],
            "content_family": content_family,
            "content_signals": signals,
            "active_starred": repo in active,
            "classification": classified.get(repo, "unclassified"),
            "productive": repo in productive,
            "productivity_category": productive.get(repo, {}).get("category"),
        })

    family_counts = Counter(row["content_family"] for row in records)
    active_records = [row for row in records if row["active_starred"]]
    summary = {
        "scope": {"enumerated": len(records), "active_starred": len(active_records), "productive_native": len(productive)},
        "content_families": dict(family_counts.most_common()),
        "active_content_families": dict(Counter(row["content_family"] for row in active_records).most_common()),
        "classification": dict(Counter(row["classification"] for row in active_records).most_common()),
        "productivity_categories": productivity["categories"],
        "records": records,
    }
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    md = out.with_suffix(".md")
    lines = [
        "# DSH 插件社区内容地图与生产力筛选",
        "",
        f"全量枚举 **{len(records):,}** 个仓库；活跃且有星 **{len(active_records):,}** 个；生产力筛选 **{len(productive):,}** 个原生插件。",
        "",
        "内容地图回答社区在做什么，生产力筛选回答哪些项目值得进入工作工具候选集。两者分开统计，避免主题、市场目录和适配产品遮蔽真正的插件能力。",
        "",
        "## 全社区内容地图",
        "",
        "| 内容家族 | 全量仓库 | 活跃有星 |",
        "|---|---:|---:|",
    ]
    for name, count in summary["content_families"].items():
        lines.append(f"| {name} | {count:,} | {summary['active_content_families'].get(name, 0):,} |")
    lines += ["", "## 生产力类别", "", "| 类别 | 原生生产力插件 |", "|---|---:|"]
    for name, count in productivity["categories"].items():
        lines.append(f"| {name} | {count:,} |")
    lines += ["", "## 生产力工具判定", "", "".join([
        "纳入条件：活跃、有星、原生，且 README 或元数据中至少出现两个具体的重复工作信号。",
        "主题、娱乐、市场目录和单纯桌面壳不进入生产力主榜；适配产品单独保留在社区地图中。",
    ])]
    md.write_text("\n".join(lines) + "\n")
    print(f"enumerated={len(records)} active_starred={len(active_records)} productive_native={len(productive)}")
    print(f"wrote {out} and {md}")


if __name__ == "__main__":
    main()
