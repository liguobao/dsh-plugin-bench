#!/usr/bin/env python3
"""Build the current active×starred inventory, preserving manual prior labels.

Existing manually reviewed labels are carried forward for repositories that
remain active. New repositories are assigned a narrower, ordered heuristic
category and explicitly marked as machine-assisted rather than hand-reviewed.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


DIRECT = {
    "memory-knowledge": "memory-knowledge",
    "context-search": "search-web",
    "model-provider": "model-provider",
    "remote-access": "remote-access",
    "remote-mobile": "remote-access",
    "mobile-client": "mobile-client",
    "security": "security-governance",
    "orchestration": "orchestration-workflow",
    "office-docs": "vertical-domain",
    "notify-im": "im-notify",
    "voice-audio": "voice-audio",
    "vision": "vision-multimodal",
    "market-curation": "market-curation",
    "skills-pack": "skills-presets",
    "desktop-client": "desktop-client",
    "usage-billing": "usage-billing",
    "fun-novelty": "fun-novelty",
    "ui-theme": "session-ui-ux",
    "vertical-domain": "vertical-domain",
}

MANUAL_CATEGORY_OVERRIDES = {
    "gychen-NJU/dsh-overleaf": "vertical-domain",
    "sperictao/dsh-pro-max": "desktop-client",
}

RULES = [
    ("fun-novelty", r"\bpet\b|桌宠|宠物|galgame|wallpaper|壁纸|meme|小游戏|companion"),
    ("memory-knowledge", r"memory|记忆|knowledge|知识库|\brag\b|embedding|engram"),
    ("vision-multimodal", r"vision|视觉|image|图像|多模态|\bocr\b|screenshot"),
    ("security-governance", r"security|安全|audit|审计|secret|guard|sandbox|permission|权限|pentest|authentication|authorization|认证|访问密码|access control"),
    ("remote-access", r"remote access|remote control|remote client|remote host|远程访问|远程控制|远程使用|远程连接|远控|remote relay|中继服务|tunnel|隧道|tailscale|zerotier|\bfrp\b|cpolar|cloudflare tunnel|局域网|lan access|reverse proxy|扫码|\bp2p\b|peer.to.peer"),
    ("mobile-client", r"mobile client|mobile app|mobile companion|mobile shell|android (?:client|app|companion|shell)|android 客户端|安卓壳|webview ui|手机端(?:适配|客户端|ui)|移动端(?:适配|客户端|ui)|harmonyos 原生客户端|harmony 客户端"),
    ("im-notify", r"notify|通知|telegram|slack|discord|wechat|微信|钉钉|飞书|\bqq\b|email"),
    ("usage-billing", r"token|usage|用量|billing|计费|cost|费用|budget|预算|balance|余额"),
    ("market-curation", r"market|市场|registry|awesome|curated|插件目录|插件管理"),
    ("orchestration-workflow", r"orchestrat|swarm|multi-agent|agent team|subagent|workflow|工作流|pipeline|task board"),
    ("search-web", r"search|搜索|browser|浏览器|web access|网页|retrieval|爬虫"),
    ("desktop-client", r"desktop|桌面|electron|tauri|launcher|启动器|desktop client"),
    ("tui-terminal", r"\btui\b|terminal|终端|statusline|状态栏"),
    ("ide-integration", r"vscode|visual studio|\bide\b|editor integration"),
    ("mcp-tooling", r"\bmcp\b|model context protocol"),
    ("file-workspace", r"workspace|工作区|file manager|文件管理|@file|filesystem"),
    ("context-management", r"context|上下文|compress|压缩|compact"),
    ("session-ui-ux", r"web ui|webui|sidebar|侧边栏|theme|主题|skin|皮肤|composer|panel|widget|timeline|界面|会话"),
    ("skills-presets", r"\bskill\b|技能|preset|预设|prompt|提示词"),
    ("model-provider", r"provider|subscription|订阅|router|路由|model|模型|oauth|api relay|ollama|vllm"),
    ("vertical-domain", r"finance|trading|股票|金融|legal|法律|medical|医疗|教育|小说|视频|office|ppt|excel|word|pdf"),
    ("eng-git-ci", r"\bgit\b|commit|review|\bci\b|lint|test|checkpoint|build|debug|deploy"),
    ("tutorial-docs", r"tutorial|教程|handbook|手册|course|课程|learn"),
]


def remote_or_mobile(repo: str, text: str) -> str | None:
    repo_lower = repo.lower()
    lower = text.lower()
    remote_repo = r"remote|relay|tether|winrm|lan.access|tailscale|zerotier|web.gateway"
    remote_text = r"remote access|remote control|remote client|remote host|remote web|remote workspace|远程访问|远程控制|远程使用|远程连接|远程操控|远程工作区|远端机器|远控|remote relay|中继服务|dispatch.{0,40}from (?:your )?phone|从手机.{0,30}(?:派发|调度)|tunnel|隧道|tailscale|zerotier|\bfrp\b|cpolar|cloudflare tunnel|局域网|lan access|reverse proxy|扫码|\bp2p\b|peer.to.peer|ssh tunnel"
    mobile = r"mobile client|mobile app|mobile companion|mobile shell|android (?:client|app|companion|shell)|android 客户端|安卓壳|webview ui|手机端(?:适配|客户端|ui)|移动端(?:适配|客户端|ui)|harmonyos 原生客户端|harmony 客户端"
    if re.search(remote_repo, repo_lower, re.I) or re.search(remote_text, lower, re.I):
        return "remote-access"
    if "mobile" in repo_lower or re.search(mobile, lower, re.I):
        return "mobile-client"
    return None


def route_from_text(text: str) -> str | None:
    lower = text.lower()
    if re.search(r"\bp2p\b|peer.to.peer|no server|无服务器", lower, re.I):
        return "peer-to-peer"
    if (
        re.search(r"hosted.{0,40}relay|托管.{0,20}中继", lower, re.I)
        and re.search(r"end.to.end encrypt|端到端加密", lower, re.I)
    ):
        return "hosted-e2ee-relay"
    routes = [
        ("hosted-relay", r"cloud.{0,20}relay|云端.{0,20}(?:relay|中继)|hosted.{0,20}relay"),
        ("e2ee-pairing", r"end.to.end encrypt|端到端加密"),
        ("cloudflare-tunnel", r"cloudflare|cloudflared|quick tunnel"),
        ("reverse-proxy-self-hosted", r"reverse proxy|反向代理|nginx|\bfrp\b|ssh tunnel|自托管|self.host"),
        ("vpn-overlay", r"tailscale|zerotier|headscale"),
        ("third-party-tunnel", r"cpolar|ngrok|localtunnel"),
        ("lan-gateway", r"局域网|\blan\b|扫码|qr code|web gateway|web 网关"),
    ]
    for route, pattern in routes:
        if re.search(pattern, lower, re.I):
            return route
    return None


def remote_route(primary_text: str, readme: str) -> str:
    route = route_from_text(primary_text)
    if route:
        return route
    route = route_from_text(readme)
    if route:
        return route
    return "generic-remote"


def classify_new(repo: str, machine_cat: str, text: str, verdict: str) -> str:
    lower = text.lower()
    if machine_cat == "ui-theme" and verdict == "toy":
        return "fun-novelty"
    if re.search(r"theme|skin|主题|皮肤", lower, re.I):
        return "session-ui-ux"
    if machine_cat == "model-provider":
        if re.search(r"security|安全分析|malware|pentest|攻防|审计", lower, re.I):
            return "security-governance"
        return "model-provider"
    if machine_cat in {"remote-access", "remote-mobile", "mobile-client"}:
        remote_mobile = remote_or_mobile(repo, text)
        if remote_mobile:
            return remote_mobile
    if machine_cat not in {
        "eng-quality", "remote-access",
        "remote-mobile", "mobile-client", "uncategorized",
    }:
        return DIRECT.get(machine_cat, "other")
    for category, pattern in RULES:
        if re.search(pattern, lower, re.I):
            return category
    return "other"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_dir", type=Path)
    parser.add_argument("--previous", type=Path, required=True)
    parser.add_argument("--anchor", required=True, help="breaking-release ISO timestamp")
    args = parser.parse_args()

    meta = {
        row["repo"]: row
        for row in (json.loads(line) for line in (args.audit_dir / "repos.jsonl").open())
    }
    previous = {row["repo"]: row["cat"] for row in json.loads(args.previous.read_text())}
    analysis = {
        row["repo"]: row
        for row in json.loads((args.audit_dir / "analysis.json").read_text())
    }

    rows = []
    for repo, item in meta.items():
        if item["stars"] < 1 or item["pushed"] < args.anchor:
            continue
        summary = analysis.get(repo, {})
        readme_path = args.audit_dir / "readmes" / f"{repo.replace('/', '_')}.md"
        readme = readme_path.read_text(errors="ignore") if readme_path.exists() else ""
        evidence_text = " ".join(
            (repo, item.get("desc") or "", summary.get("first") or "")
        )
        if repo in previous:
            category = previous[repo]
            if category == "remote-mobile":
                category = remote_or_mobile(repo, evidence_text) or classify_new(
                    repo,
                    summary.get("cat", "uncategorized"),
                    evidence_text,
                    summary.get("verdict", "mixed"),
                )
                source = "manual-carry-forward-remote-retag"
            else:
                source = "manual-carry-forward"
        else:
            category = classify_new(
                repo,
                summary.get("cat", "uncategorized"),
                evidence_text,
                summary.get("verdict", "mixed"),
            )
            source = "incremental-heuristic" if summary else "metadata-only"
        if repo in MANUAL_CATEGORY_OVERRIDES:
            category = MANUAL_CATEGORY_OVERRIDES[repo]
            source = "manual-current-review"
        row = {
            "repo": repo,
            "stars": item["stars"],
            "cat": category,
            "classification_source": source,
        }
        if category == "remote-access":
            row["remote_route"] = remote_route(evidence_text, readme)
        rows.append(row)

    rows.sort(key=lambda row: (-row["stars"], row["repo"].lower()))
    (args.audit_dir / "active_inventory.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=1) + "\n"
    )

    counts = Counter(row["cat"] for row in rows)
    sources = Counter(row["classification_source"] for row in rows)
    lines = [
        f"# 活跃 × 有星插件清单（{len(rows):,} 个）",
        "",
        f"> 口径：stars ≥ 1 且 pushed ≥ {args.anchor}。",
        f"> 分类来源：上一轮人工分类沿用 {sources['manual-carry-forward']:,} 个；"
        f"远程旧标签重分 {sources['manual-carry-forward-remote-retag']:,} 个；"
        f"本轮 README 机器辅助增量 {sources['incremental-heuristic']:,} 个；"
        f"本轮人工复核覆盖 {sources['manual-current-review']:,} 个；"
        f"仅元数据 {sources['metadata-only']:,} 个。增量分类尚未逐仓人工复核。",
        "",
    ]
    for category, count in counts.most_common():
        lines.extend((f"## {category} — {count} 个", ""))
        for row in (row for row in rows if row["cat"] == category):
            lines.append(
                f"- ★{row['stars']:,} `{row['repo']}` ({row['classification_source']})"
            )
        lines.append("")
    (args.audit_dir / "active_inventory.md").write_text("\n".join(lines))

    print(f"active inventory: {len(rows)}")
    print("sources:", dict(sources))
    print("categories:")
    for category, count in counts.most_common():
        print(f"  {category:24s} {count}")


if __name__ == "__main__":
    main()
