#!/usr/bin/env python3
"""Build a productivity-tool view from an existing topic audit.

The ecosystem audit answers "what is in the topic?". This pass answers
"which plugins help someone do recurring work?" It deliberately keeps the
scope narrow and reports excluded categories instead of ranking everything.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


CATEGORIES = {
    "knowledge-research": [
        "memory", "knowledge", "知识", "记忆", "rag", "retrieval", "search",
        "搜索", "检索", "context", "上下文", "deepread", "citation", "文献",
    ],
    "documents-office": [
        "office", "docx", "pdf", "pptx", "xlsx", "excel", "word", "文档",
        "简历", "resume", "slide", "presentation", "报告", "table", "spreadsheet",
    ],
    "engineering-delivery": [
        "git", "commit", "pull request", "review", "ci", "lint", "test",
        "debug", "bug", "build", "deploy", "release", "checkpoint", "backup",
        "工程", "代码", "开发", "部署", "测试", "审查",
    ],
    "workflow-automation": [
        "workflow", "工作流", "automation", "自动化", "pipeline", "编排",
        "orchestration", "scheduler", "task", "任务", "subagent", "multi-agent",
    ],
    "communication-collaboration": [
        "notification", "通知", "telegram", "slack", "discord", "wechat", "微信",
        "dingtalk", "飞书", "lark", "email", "mail", "calendar", "日历",
    ],
    "security-access": [
        "security", "安全", "permission", "权限", "secret", "加密", "encrypt",
        "sandbox", "audit", "审计", "remote", "远程", "tunnel", "relay", "ssh",
    ],
    "model-cost": [
        "provider", "model", "模型", "router", "route", "ollama", "vllm", "oauth",
        "api key", "token", "usage", "用量", "cost", "费用", "billing", "预算",
    ],
    "visual-production": [
        "ocr", "image", "图像", "vision", "截图", "screenshot", "video", "音频",
        "audio", "transcription", "转写", "design", "设计", "canvas",
    ],
}

# These are the terms that carry meaning for a productivity claim. Generic
# words such as "tool", "agent", "build", and "model" are only supporting
# evidence and cannot qualify a project by themselves.
STRONG = {
    "knowledge-research": ["memory", "knowledge", "知识库", "rag", "retrieval", "检索", "citation", "文献", "deepread"],
    "documents-office": ["docx", "pdf", "pptx", "xlsx", "excel", "word", "文档", "简历", "resume", "spreadsheet"],
    "engineering-delivery": ["git", "commit", "pull request", "code review", "ci", "lint", "debug", "deploy", "checkpoint", "backup", "代码审查", "部署", "测试报告"],
    "workflow-automation": ["workflow", "工作流", "automation", "自动化", "pipeline", "orchestration", "scheduler", "subagent", "multi-agent"],
    "communication-collaboration": ["notification", "通知", "telegram", "slack", "discord", "wechat", "微信", "dingtalk", "飞书", "calendar", "日历"],
    "security-access": ["security", "安全", "permission", "权限", "secret", "加密", "encrypt", "sandbox", "audit", "审计", "remote", "远程", "tunnel", "relay", "ssh"],
    "model-cost": ["provider", "router", "ollama", "vllm", "oauth", "api key", "token", "usage", "用量", "cost", "费用", "billing", "预算"],
    "visual-production": ["ocr", "vision", "截图", "screenshot", "video", "音频", "audio", "transcription", "转写", "design", "设计", "canvas"],
}

EXCLUDED = {
    "theme-and-ui": ["theme", "主题", "skin", "皮肤", "wallpaper", "sidebar", "statusline"],
    "fun-and-novelty": ["pet", "桌宠", "meme", "joke", "toy", "roleplay", "galgame", "小游戏"],
    "catalog-and-market": ["market", "市场", "plugin manager", "插件管理", "awesome", "curated"],
    "standalone-shell": ["desktop client", "桌面客户端", "launcher", "electron", "tauri"],
}


def text_for(repo: str, row: dict, readmes: Path) -> str:
    parts = [row.get("desc") or ""]
    readme = readmes / (repo.replace("/", "_") + ".md")
    if readme.exists():
        parts.append(readme.read_text(encoding="utf-8", errors="ignore")[:12000])
    return " ".join(parts).lower()


def hits(text: str, keywords: list[str]) -> list[str]:
    return [kw for kw in keywords if kw.lower() in text]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("audit_dir", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--min-stars", type=int, default=1)
    args = ap.parse_args()
    out = args.out or args.audit_dir / "productivity_analysis.json"

    repos = {json.loads(line)["repo"]: json.loads(line) for line in (args.audit_dir / "repos.jsonl").open()}
    active = {json.loads(line)["repo"] for line in (args.audit_dir / "active_set.jsonl").open()}
    classes = {json.loads(line)["repo"]: json.loads(line).get("cls") for line in (args.audit_dir / "classification.jsonl").open()}
    dist = {json.loads(line)["repo"]: json.loads(line) for line in (args.audit_dir / "dist_check.jsonl").open()}
    candidates = [repo for repo in active if repos[repo]["stars"] >= args.min_stars]

    included = []
    excluded = Counter()
    for repo in candidates:
        row = repos[repo]
        classification = classes.get(repo, "unclassified")
        if classification != "native":
            excluded["adapted-or-unrelated"] += 1
            continue
        text = text_for(repo, row, args.audit_dir / "readmes")
        category_hits = {name: hits(text, words) for name, words in CATEGORIES.items()}
        category_hits = {name: values for name, values in category_hits.items() if values}
        strong_hits = {name: hits(text, words) for name, words in STRONG.items()}
        strong_hits = {name: values for name, values in strong_hits.items() if values}
        excluded_hits = {name: hits(text, words) for name, words in EXCLUDED.items()}
        excluded_hits = {name: values for name, values in excluded_hits.items() if values}
        if any(name in excluded_hits for name in ("theme-and-ui", "fun-and-novelty")) and not any(name in strong_hits for name in ("security-access", "knowledge-research", "documents-office", "engineering-delivery", "workflow-automation")):
            excluded["theme-or-fun"] += 1
            continue
        score = sum(min(len(values), 3) for values in category_hits.values())
        # A productivity claim needs recurring work signals, not a single
        # generic word such as "tool" or "agent".
        productive = score >= 2 and bool(category_hits) and bool(strong_hits)
        if not productive and excluded_hits:
            excluded[" / ".join(sorted(excluded_hits))] += 1
        if not productive:
            continue
        category = max(strong_hits, key=lambda name: len(strong_hits[name]))
        d = dist.get(repo, {})
        included.append({
            "repo": repo,
            "stars": row["stars"],
            "pushed": row["pushed"],
            "category": category,
            "evidence": sorted(set(category_hits[category]))[:8],
            "all_categories": sorted(category_hits),
            "native": True,
            "classification": classification,
            "has_release": d.get("releases", 0) > 0,
            "npm_published": bool(d.get("npm_exists")),
            "npm_weekly": d.get("npm_weekly") or 0,
            "release_downloads": d.get("rel_downloads", 0),
        })

    included.sort(key=lambda item: (-item["stars"], item["repo"]))
    summary = {
        "scope": {
            "candidates": len(candidates),
            "productive": len(included),
            "native_productive": sum(item["native"] for item in included),
            "min_stars": args.min_stars,
            "definition": "Recurring work support with at least two concrete productivity signals in metadata or README.",
        },
        "categories": dict(Counter(item["category"] for item in included).most_common()),
        "distribution": {
            "with_release": sum(item["has_release"] for item in included),
            "npm_published": sum(item["npm_published"] for item in included),
            "npm_weekly": sum(item["npm_weekly"] for item in included),
            "release_downloads": sum(item["release_downloads"] for item in included),
        },
        "excluded_signals": dict(excluded.most_common()),
        "top": included[:50],
        "all": included,
    }
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    md = out.with_suffix(".md")
    lines = [
        "# 生产力工具插件分析",
        "",
        f"候选集合：{len(candidates)} 个活跃且有星仓库；生产力工具：{len(included)} 个；其中原生插件：{summary['scope']['native_productive']} 个。",
        "",
        "判定要求至少命中两个具体工作信号，并结合 README 语境；主题、娱乐、市场目录和单纯桌面壳单独排除。结果是筛选和排序依据，不等于人工功能验收。",
        "",
        "## 类别分布",
        "",
        "| 类别 | 插件数 |",
        "|---|---:|",
    ]
    for category, count in summary["categories"].items():
        lines.append(f"| {category} | {count} |")
    lines += ["", "## 生产力工具头部", "", "| 项目 | Star | 类别 | 原生 | npm 周下载 | Release 下载 |", "|---|---:|---|---|---:|---:|"]
    for item in included[:30]:
        lines.append(f"| `{item['repo']}` | {item['stars']:,} | {item['category']} | {'是' if item['native'] else '否'} | {item['npm_weekly']:,} | {item['release_downloads']:,} |")
    lines += ["", "## 复核提示", "", "- 先按类别查看 README 和安装方式，再判断是否适合纳入默认插件集合。", "- `npm_weekly` 和 Release 下载只说明分发信号，不代表活跃用户数。", "- 生产力类别仍需人工复核同质化复制、误命中和 README 夸大描述。"]
    md.write_text("\n".join(lines) + "\n")
    print(f"candidates={len(candidates)} productive={len(included)} native={summary['scope']['native_productive']}")
    print(f"wrote {out} and {md}")


if __name__ == "__main__":
    main()
