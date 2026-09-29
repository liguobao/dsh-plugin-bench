#!/usr/bin/env python3
"""Write a versioned DSH ecosystem report without overwriting older runs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CATEGORY_NAMES = {
    "session-ui-ux": "会话 / UI 微增强",
    "desktop-client": "桌面客户端",
    "search-web": "搜索 / Web / 浏览器",
    "usage-billing": "用量 / 计费",
    "market-curation": "市场 / 策展",
    "memory-knowledge": "记忆 / 知识",
    "model-provider": "Provider / 路由",
    "orchestration-workflow": "编排 / 工作流",
    "security-governance": "安全 / 治理",
    "skills-presets": "技能 / 预设",
    "vision-multimodal": "视觉 / 多模态",
    "fun-novelty": "娱乐 / 皮肤",
    "remote-access": "远程访问",
    "mobile-client": "移动端本机客户端",
    "vertical-domain": "垂直领域",
    "eng-git-ci": "工程化 / Git / CI",
    "im-notify": "IM / 通知",
    "tui-terminal": "TUI / 终端",
    "file-workspace": "文件 / 工作区",
    "mcp-tooling": "MCP 工具",
    "ide-integration": "IDE 集成",
    "context-management": "上下文管理",
    "voice-audio": "语音 / 音频",
    "other": "其他",
}

ROUTE_NAMES = {
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


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def versioned_path(report_dir: Path, report_date: str) -> Path:
    base = report_dir / f"DSH插件生态评估报告-{report_date}.md"
    if not base.exists():
        return base
    index = 2
    while True:
        candidate = report_dir / f"DSH插件生态评估报告-{report_date}-{index:02d}.md"
        if not candidate.exists():
            return candidate
        index += 1


def distribution_table_row(label: str, row: dict) -> str:
    return (
        f"| {label} | {row['repos']:,} | {row['with_releases']:,} | "
        f"{row['release_downloads']:,} | {row['published_npm']:,} | "
        f"{row['named_unpublished']:,} | {row['npm_weekly']:,} |"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", type=Path)
    parser.add_argument("--date", required=True, help="report date YYYY-MM-DD")
    parser.add_argument("--report-dir", type=Path, default=Path("report"))
    args = parser.parse_args()

    summary = json.loads(args.summary.read_text())
    snapshot = summary["snapshot"]
    scale = summary["scale"]
    activity = summary["activity"]
    high = summary["high_star"]
    classification = summary["classification"]
    distribution = summary["distribution"]
    remote = summary["remote_access"]
    mobile = summary["mobile_client"]
    anchor_label = snapshot.get("anchor_label", "breaking release")
    native_only = snapshot.get("native_only", False)
    classified_total = sum(classification["counts"].values())
    dist_complete = distribution["all_active"]["repos"] == activity["active_starred"]
    dist_all_label = "全部活跃有星" if dist_complete else "已检查活跃有星"

    args.report_dir.mkdir(parents=True, exist_ok=True)
    output = versioned_path(args.report_dir, args.date)

    lines = [
        "# DeepSeek Harness（DSH）插件生态评估报告",
        "",
        f"> {args.date} 独立快照。数据来自 GitHub API 一手抓取；本文件由 `scripts/write_audit_report.py` 生成，历史报告不会被覆盖。",
        "",
        (f"- 原生判定集合：**{snapshot['official']:,}**" if native_only else
         f"- 官方 topic 计数：**{snapshot['official']:,}**"),
        f"- 数据来源：{snapshot.get('official_source', 'GitHub API')}",
        f"- 实际去重枚举：**{snapshot['enumerated']:,}**，覆盖 **{snapshot['coverage'] * 100:.2f}%**",
        f"- README 覆盖：**{snapshot['readmes']:,}**",
        (f"- 原生判定集合：**{classified_total:,}** 个仓库" if native_only else
         f"- 原生 / 适配 / 无关判定覆盖：**{classified_total:,}** 个重点仓库"),
        f"- 活跃锚点：`{snapshot['anchor']}`",
        "- 本轮为自动化统计及初步分类；README 缓存每份最多保留前 8,000 字符，未完成全部摘要的逐条人工复核。下载与预分类不等于完整深读。",
        "",
        "## 一、核心结论",
        "",
        f"1. {anchor_label} 后有 push 的仓库为 **{activity['passed']:,}**，占 {pct(activity['rate'])}；其中“活跃 × 有星” **{activity['active_starred']:,}**，原生活跃 **{activity['native_active_starred']:,}**。",
        f"2. star ≥ 10 共 **{high['total']:,}**：活跃 {high['active']:,}，停滞 {high['stalled']:,}；原生且活跃 {high['native_active']:,}。",
        f"3. 一次性仓库 {scale['one_shot']:,}，占 {pct(scale['one_shot'] / snapshot['enumerated'])}；规模增长仍不能直接等价为可维护供给。",
        ("4. 本报告只在原生集合内比较插件内容、活跃度和分发完成度；非原生仓库不进入任何排名。" if native_only else
         f"4. 三桶分析集合中原生 {classification['counts'].get('native', 0):,}、适配型 {classification['counts'].get('adapted', 0):,}、无关 {classification['counts'].get('unrelated', 0):,}；适配型产品继续支配 star 总量。"),
        f"5. **远程访问已作为独立一级品类统计：{remote['repos']:,} 个活跃仓库，原生 {remote['native']:,}，star ≥ 10 共 {remote['star_10_plus']:,}。** 移动端本机客户端另计 {mobile['repos']:,} 个。",
        "",
        "## 二、漏斗与活跃度",
        "",
        "| 阶段 | 数量 |",
        "|---|---:|",
        (f"| 原生判定集合 | {snapshot['official']:,} |" if native_only else
         f"| 官方 topic | {snapshot['official']:,} |"),
        f"| 精确枚举 | {snapshot['enumerated']:,} |",
        f"| {anchor_label} 后有 push | {activity['passed']:,} |",
        f"| 活跃 × 有星 | {activity['active_starred']:,} |",
        f"| 原生 × 活跃 × 有星 | {activity['native_active_starred']:,} |",
        f"| README 覆盖 | {snapshot['readmes']:,} |",
        "",
        "| 星级 | 通过锚点 | 总数 | 跟进率 |",
        "|---|---:|---:|---:|",
    ]
    for label, row in activity["tiers"].items():
        lines.append(f"| {label} | {row['passed']:,} | {row['total']:,} | {pct(row['rate'])} |")

    lines.extend(
        [
            "",
            "固定锚点会把锚点后新建的一次性项目也计为活跃，因此总活跃率只用于跟进信号；选型更应关注“有星 × 锚点后 push × 可分发”的交集。",
            "",
            "## 三、原生插件范围",
            "",
            (f"本报告只保留已判定为 DSH 原生的仓库，共 **{classified_total:,}** 个。适配产品、蹭标签和其他非原生项目已从全部统计、排名、分发和图表中移除。"
             if native_only else
             f"本节覆盖高星、锚点活跃及历史已判定仓库，共 **{classified_total:,}** 个；不代表对全部 {snapshot['enumerated']:,} 个 topic 仓库逐一完成三桶判定。"),
            "",
            "| 桶 | 仓库数 | star |",
            "|---|---:|---:|",
        ]
    )
    class_rows = (("native", "DSH 原生"),) if native_only else (("native", "DSH 原生"), ("adapted", "适配型独立产品"), ("unrelated", "无关 / 蹭 tag"))
    for key, label in class_rows:
        lines.append(
            f"| {label} | {classification['counts'].get(key, 0):,} | {classification['stars'].get(key, 0):,} |"
        )

    lines.extend(["", "原生活跃头部：", ""])
    for index, row in enumerate(summary["top_native_active"][:12], 1):
        lines.append(f"{index}. `{row['repo']}` — {row['stars']:,}★")

    lines.extend(
        [
            "",
            "## 四、活跃品类结构",
            "",
            "| 品类 | 活跃仓库 | star ≥ 10 | 原生 | star 总量 |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    category_order = list(summary["categories"])
    if "remote-access" in category_order:
        category_order.remove("remote-access")
        category_order.insert(min(12, len(category_order)), "remote-access")
    for category in category_order:
        row = summary["category_details"][category]
        lines.append(
            f"| {CATEGORY_NAMES.get(category, category)} | {row['repos']:,} | "
            f"{row['star_10_plus']:,} | {row['native']:,} | {row['stars']:,} |"
        )

    lines.extend(
        [
            "",
            "`remote-access` 与 `mobile-client` 已拆分：前者仅回答“如何从另一台设备经网络访问并操作正在运行的 DSH”，后者回答“如何在手机本机运行、承载或优化 DSH 客户端”。远端工作区开发、实例运维和外部插件救援不计入核心远程访问。",
            "",
            "## 五、远程访问专项",
            "",
            f"远程访问活跃仓库 **{remote['repos']:,}** 个，总 star **{remote['stars']:,}**；原生 {remote['native']:,}，高星（≥10★）{remote['star_10_plus']:,}。",
            "",
            "### 技术路线",
            "",
            "| 主路线 | 仓库数 |",
            "|---|---:|",
        ]
    )
    for route, count in remote["routes"].items():
        lines.append(f"| {ROUTE_NAMES.get(route, route)} | {count:,} |")

    lines.extend(
        [
            "",
            "### 头部项目",
            "",
            "| 项目 | Star | 原生性 | 主路线 |",
            "|---|---:|---|---|",
        ]
    )
    for row in remote["top"][:15]:
        lines.append(
            f"| `{row['repo']}` | {row['stars']:,} | {row['cls']} | {ROUTE_NAMES.get(row['route'], row['route'])} |"
        )

    remote_all = remote["distribution"]["all"]
    remote_native = remote["distribution"]["native"]
    lines.extend(
        [
            "",
            "### 分发完成度",
            "",
            "| 口径 | 仓库 | 有 Release | Release 下载 | npm 已发布 | 写名未发布 | npm 周下载 |",
            "|---|---:|---:|---:|---:|---:|---:|",
            distribution_table_row(
                "远程访问全部" if remote_all["repos"] == remote["repos"] else "远程访问已检查",
                remote_all,
            ),
            distribution_table_row("远程访问原生", remote_native),
            "",
            (
                "远程访问分发查询已全覆盖。"
                if remote_all["repos"] == remote["repos"]
                else f"远程访问分发查询覆盖 **{remote_all['repos']:,} / {remote['repos']:,}** 个项目。"
            ),
            "",
            "远程访问是高风险能力面：功能比较必须同时看认证、设备撤销、传输加密、隧道/中继明文可见性和自托管能力。`liguobao/ds-harness-remote` 为报告作者相关项目，利益相关特此披露；本报告只核对公开 README 与元数据，不等同于安全审计。",
            "",
            "## 六、全生态分发渠道",
            "",
            "| 口径 | 仓库 | 有 Release | Release 下载 | npm 已发布 | 写名未发布 | npm 周下载 |",
            "|---|---:|---:|---:|---:|---:|---:|",
            distribution_table_row(dist_all_label, distribution["all_active"]),
            distribution_table_row("原生活跃", distribution["native_active"]),
            "",
            (
            "分发脚本已为全部活跃有星仓库生成记录；记录覆盖不代表每次接口请求均成功。"
                if dist_complete
                else f"本轮分发查询仅覆盖 **{distribution['all_active']['repos']:,} / {activity['active_starred']:,}** 个活跃有星仓库；未覆盖项目不计入下载与发布合计。"
            ),
            "",
            ("npm 周下载中位数为 0 时，不能直接解释成无人使用；长尾常通过 GitHub 依赖直装。Release 下载更集中在原生桌面客户端和移动端。"
             if native_only else
             "npm 周下载中位数为 0 时，不能直接解释成无人使用；长尾常通过 GitHub 依赖直装。Release 下载则更偏向桌面应用和适配型独立产品。"),
            "",
            "## 七、高星停滞",
            "",
            (f"star ≥ 10 的原生项目中，锚点后未观察到 push 的有 {high['stalled']:,} 个，其中最后 push 早于锚点 24 小时的有 {high['definite_stalled']:,} 个，锚点前 24 小时内的有 {high['borderline_stalled']:,} 个。这里只列时间信号，不代表已验证不兼容或停止维护。前一组头部如下："
             if native_only else
             f"star ≥ 10 中，锚点后未观察到 push 的项目有 {high['stalled']:,} 个，其中最后 push 早于锚点 24 小时的有 {high['definite_stalled']:,} 个，锚点前 24 小时内的有 {high['borderline_stalled']:,} 个。此处混合原生、适配与无关项目，仅列时间信号，不代表已验证不兼容或停止维护。前一组头部如下："),
            "",
        ]
    )
    for row in high["top_definite"][:12]:
        lines.append(f"- `{row['repo']}` — {row['stars']:,}★，最后 push `{row['pushed']}`")

    lines.extend(
        [
            "",
            "## 八、方法边界与产物",
            "",
            "- 全量元数据通过 star 分桶、ISO 时间戳递归切片与单页叶子抓取，规避 GitHub 1000 条上限和并列排序分页遗漏。",
            f"- 本轮缓存并自动预分类 README {snapshot['readmes']:,} 份，每份最多前 8,000 字符；未完成逐仓深读。",
            "- README 分类仍包含机器辅助增量；`classification_source` 字段区分人工沿用、本轮人工复核、增量规则和仅元数据。",
            "- 分类脚本中的历史人工标签及硬编码覆盖项不代表本轮重新人工核实；品类与原生性结果均属初步判断。",
            "- 分发脚本未分别记录网络失败、限流与不存在；表中未发布、无 Release 及零下载包含待复核项。npm 包名亦未逐一核对仓库归属，下载量不能直接代表插件用户数。",
            "- 锚点后 push 只说明仓库发生推送，不证明已适配；与历史快照比较时，锚点及观察窗口不同，不能直接解释为维护率提升。",
            f"- 纯皮肤可能无需适配 {anchor_label}；固定锚点也会随时间逐渐吸收新建仓库。",
            "- `data/audit_summary.json` 是本报告的结构化数字来源。",
            "- `charts/08_remote_access.png` 为远程访问技术路线图。",
            "",
            "报告与脚本采用 MIT；GitHub 元数据与第三方 README 版权归各自作者所有。",
            "",
        ]
    )

    output.write_text("\n".join(lines))
    print(output)


if __name__ == "__main__":
    main()
