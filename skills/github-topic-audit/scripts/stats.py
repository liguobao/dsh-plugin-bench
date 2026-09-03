#!/usr/bin/env python3
"""Stats, activity anchor, and README classification pre-pass for a topic audit.

Usage:
  python3 stats.py <audit-dir> [--anchor ISO_TS | --anchor-release owner/repo@tag]

Reads <audit-dir>/repos.jsonl and <audit-dir>/readmes/*.md, writes:
  <audit-dir>/stats.txt        - full metadata statistics
  <audit-dir>/digest.txt       - one line per README-read repo, for MANUAL review
  <audit-dir>/analysis.json    - machine pre-classification (must be corrected by hand)

The digest is the point: classification keywords over-merge (e.g. "test"/"verify"
throw half the ecosystem into one bucket). Always read digest.txt line by line and
correct categories/verdicts before writing any report.
"""
import argparse, glob, json, os, subprocess
from collections import Counter
from datetime import datetime

CAT_RULES = [
    ("memory-knowledge", ["memory", "记忆", "knowledge", "知识库", "rag", "embedding", "context database"]),
    ("context-search", ["context", "上下文", "search", "搜索", "retrieval", "web search", "deepread", "file mount"]),
    ("model-provider", ["ollama", "vllm", "llm", "model", "模型", "router", "route", "inference", "oauth", "api key", "provider", "subscription", "订阅"]),
    ("remote-access", ["remote", "远程", "relay", "中继", "gateway", "网关", "tunnel", "隧道", "tailscale", "frp", "cloudflare", "局域网", "lan access", "reverse proxy", "扫码"]),
    ("mobile-client", ["android", "apk", "ios", "mobile client", "mobile app", "webview", "手机端", "移动端"]),
    ("ui-theme", ["theme", "主题", "skin", "皮肤", "catppuccin", "wallpaper", "sidebar", "侧边栏", "tui", "statusline"]),
    ("fun-novelty", ["pet", "桌宠", "宠物", "meme", "梗图", "toy", "companion", "看板娘", "galgame", "roleplay", "角色扮演"]),
    ("security", ["security", "安全", "audit", "审计", "secret", "poison", "guard", "encrypt", "加密", "permission", "权限", "sandbox"]),
    ("eng-quality", ["git", "commit", "review", "评审", "ci", "action", "checkpoint", "lint", "testing framework", "bugfix", "build"]),
    ("orchestration", ["orchestr", "swarm", "multi-agent", "team", "协作", "subagent", "workflow", "工作流", "pipeline", "task board", "看板"]),
    ("office-docs", ["office", "docx", "pdf", "pptx", "xlsx", "excel", "word", "文档", "resume", "简历", "slide", "ppt"]),
    ("notify-im", ["notif", "通知", "telegram", "slack", "discord", "wechat", "微信", "dingtalk", "飞书", "lark", "qq", "email"]),
    ("voice-audio", ["voice", "语音", "audio", "音频", "tts", "asr", "speech"]),
    ("vision", ["vision", "视觉", "图像", "image", "多模态", "ocr", "看图", "screenshot"]),
    ("market-curation", ["market", "市场", "hub", "plugin manager", "插件管理", "registry", "awesome", "curated"]),
    ("skills-pack", ["skill", "技能", "prompt", "提示词"]),
    ("desktop-client", ["desktop", "桌面", "client", "客户端", "launcher", "启动器", "electron", "tauri", "vscode", "ide", "editor"]),
    ("usage-billing", ["token", "usage", "用量", "billing", "计费", "cost", "费用", "budget", "预算", "balance", "余额"]),
    ("vertical-domain", ["金融", "股票", "trading", "legal", "法律", "hr", "招聘", "sales", "medical", "教育", "quantum", "robot", "harmonyos", "ios dev"]),
]
# deliberately narrow: prevents the "everything is eng-quality" over-merge
TOY_KW = ["pet", "桌宠", "宠物", "meme", "joke", "整活", "toy", "娱乐", "皮肤", "skin", "彩蛋",
          "easter", "挂机", "看板娘", "galgame", "wallpaper", "壁纸", "小游戏", "minigame"]
PROD_KW = ["memory", "记忆", "security", "安全", "audit", "审计", "ci", "pipeline", "benchmark",
           "enterprise", "企业", "workflow", "工作流", "knowledge", "知识", "检索", "token",
           "review", "评审", "checkpoint", "备份", "remote", "远程", "权限", "permission"]

def cat_of(text):
    t = text.lower()
    scores = {c: sum(1 for k in kws if k in t) for c, kws in CAT_RULES}
    scores = {c: s for c, s in scores.items() if s}
    return max(scores, key=scores.get) if scores else "uncategorized"

def verdict_of(text, desc):
    t = (text[:3000] + " " + (desc or "").lower()).lower()
    toy = sum(1 for k in TOY_KW if k in t)
    prod = sum(1 for k in PROD_KW if k in t)
    if toy >= 2 and toy > prod: return "toy"
    if prod >= 2 and prod > toy: return "productive"
    return "mixed"

def resolve_anchor(args):
    if args.anchor:
        return args.anchor
    if args.anchor_release:
        repo, tag = args.anchor_release.split("@")
        r = subprocess.run(["gh", "api", f"repos/{repo}/releases/tags/{tag}"],
                           capture_output=True, text=True)
        return json.loads(r.stdout)["published_at"]
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audit_dir")
    ap.add_argument("--anchor", help="ISO timestamp of breaking-change release")
    ap.add_argument("--anchor-release", help="owner/repo@tag to fetch published_at from")
    args = ap.parse_args()

    repos = {}
    for l in open(os.path.join(args.audit_dir, "repos.jsonl")):
        r = json.loads(l)
        repos.setdefault(r["repo"], r)
    rs = list(repos.values())
    anchor = resolve_anchor(args)
    out = []
    P = out.append

    P(f"total unique repos: {len(rs)}")
    for lo, hi, name in [(100, 10**9, "100+"), (20, 100, "20-99"), (5, 20, "5-19"), (1, 5, "1-4"), (-1, 1, "0")]:
        P(f"stars {name}: {sum(1 for r in rs if lo <= r['stars'] < hi)}")
    P(f"languages: {Counter(r['lang'] for r in rs if r['lang']).most_common(6)}")
    dead = sum(1 for r in rs if r["pushed"][:10] <= r["created"][:10])
    P(f"one-shot (pushed only on creation day): {dead}/{len(rs)} = {dead/len(rs)*100:.1f}%")
    P(f"no description: {sum(1 for r in rs if not r['desc'])}/{len(rs)}")
    P(f"archived: {sum(1 for r in rs if r['archived'])}")
    if anchor:
        P(f"\nactivity anchor (breaking change @ {anchor}):")
        for lo, hi, name in [(100, 10**9, "100+"), (20, 100, "20-99"), (5, 20, "5-19"), (1, 5, "1-4"), (-1, 1, "0")]:
            g = [r for r in rs if lo <= r["stars"] < hi]
            a = sum(1 for r in g if r["pushed"] >= anchor)
            P(f"  {name}: {a}/{len(g)} = {a/len(g)*100:.1f}%" if g else f"  {name}: 0/0")
        a_all = sum(1 for r in rs if r["pushed"] >= anchor)
        P(f"  OVERALL: {a_all}/{len(rs)} = {a_all/len(rs)*100:.1f}%")

    # README classification pre-pass
    results = []
    rd = os.path.join(args.audit_dir, "readmes")
    for f in sorted(glob.glob(rd + "/*.md")):
        # GitHub owners cannot contain underscores, while repository names can.
        # Only the first underscore is our owner/repo filename separator.
        repo = os.path.basename(f)[:-3].replace("_", "/", 1)
        r = repos.get(repo, {})
        txt = open(f, encoding="utf-8", errors="ignore").read()
        if not txt.strip():
            continue
        lines = [l.strip() for l in txt.splitlines()
                 if l.strip() and not l.strip().startswith(("<", "[!", "---", "|", "#"))][:2]
        results.append({
            "repo": repo, "stars": r.get("stars", 0), "pushed": r.get("pushed", ""),
            "adapted": bool(anchor and r.get("pushed", "") >= anchor),
            "cat": cat_of(txt[:3000] + " " + (r.get("desc") or "")),
            "verdict": verdict_of(txt, r.get("desc")),
            "first": " ".join(lines)[:110].rstrip(),
        })
    results.sort(key=lambda x: -x["stars"])

    P(f"\nREADME-read repos: {len(results)}")
    P(f"category pre-pass (NEEDS MANUAL CORRECTION via digest.txt):")
    for c, n in Counter(r["cat"] for r in results).most_common():
        P(f"  {c:20s} {n}")
    if anchor:
        P("category x anchor cross-tab (maintenance discipline by category):")
        for c, n in Counter(r["cat"] for r in results).most_common():
            g = [r for r in results if r["cat"] == c]
            a = sum(1 for r in g if r["pushed"] >= anchor)
            P(f"  {c:20s} {a}/{n} = {a/n*100:.0f}%")

    with open(os.path.join(args.audit_dir, "analysis.json"), "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    with open(os.path.join(args.audit_dir, "digest.txt"), "w") as f:
        for r in results:
            line = (
                f"[{r['stars']:>6}*|{r['cat'][:14]:14s}|{r['verdict'][:4]:4s}|"
                f"anc:{'Y' if r['adapted'] else '-'}] {r['repo']} :: {r['first']}"
            )
            f.write(line.rstrip() + "\n")

    open(os.path.join(args.audit_dir, "stats.txt"), "w").write("\n".join(out) + "\n")
    print("\n".join(out))
    print(f"\nwrote: stats.txt, analysis.json, digest.txt ({len(results)} rows to review manually)")

if __name__ == "__main__":
    main()
