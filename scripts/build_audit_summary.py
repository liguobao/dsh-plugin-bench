#!/usr/bin/env python3
"""Build a compact, reproducible summary from one GitHub topic audit run."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.open() if line.strip()]


def distribution(rows: list[dict]) -> dict:
    releases = [row for row in rows if row["releases"] > 0]
    packages = [row for row in rows if row["npm_name"]]
    published = [row for row in packages if row["npm_exists"]]
    weekly = sorted((row["npm_weekly"] or 0 for row in published), reverse=True)
    return {
        "repos": len(rows),
        "with_releases": len(releases),
        "release_downloads": sum(row["rel_downloads"] for row in releases),
        "zero_download_releases": sum(row["rel_downloads"] == 0 for row in releases),
        "with_package_name": len(packages),
        "published_npm": len(published),
        "named_unpublished": len(packages) - len(published),
        "npm_weekly": sum(weekly),
        "npm_weekly_median": weekly[len(weekly) // 2] if weekly else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_dir", type=Path)
    parser.add_argument("--official-count", type=int, required=True)
    parser.add_argument("--anchor", required=True, help="breaking-release ISO timestamp")
    parser.add_argument("--anchor-label", default="breaking release")
    parser.add_argument("--official-source", default="GitHub API end-of-run query")
    parser.add_argument("--native-only", action="store_true", help="keep only repositories classified as native")
    parser.add_argument("--native-file", type=Path, default=None, help="native_plugins.jsonl when --native-only is set")
    parser.add_argument("--output", type=Path, default=None, help="summary output path")
    args = parser.parse_args()
    anchor = args.anchor

    repos = jsonl(args.audit_dir / "repos.jsonl")
    native_names = None
    if args.native_only:
        native_path = args.native_file or (args.audit_dir / "native_plugins.jsonl")
        native_names = {row["repo"] for row in jsonl(native_path)}
        repos = [row for row in repos if row["repo"] in native_names]
    meta = {row["repo"]: row for row in repos}
    active = [row for row in repos if row["stars"] >= 1 and row["pushed"] >= anchor]
    active_names = {row["repo"] for row in active}
    inventory = json.loads((args.audit_dir / "active_inventory.json").read_text())
    categories = {row["repo"]: row["cat"] for row in inventory}
    inventory_by_repo = {row["repo"]: row for row in inventory}
    classified = jsonl(args.audit_dir / "classification.jsonl")
    if args.native_only:
        classified = [row for row in classified if row.get("cls") == "native"]
    class_by_repo = {row["repo"]: row["cls"] for row in classified}

    anchor_dt = datetime.fromisoformat(anchor.replace("Z", "+00:00"))
    definite_cutoff = (anchor_dt - timedelta(days=1)).isoformat().replace("+00:00", "Z")
    high = [row for row in repos if row["stars"] >= 10]
    high_active = [row for row in high if row["pushed"] >= anchor]
    high_stalled = [row for row in high if row["pushed"] < anchor]
    definite = sorted(
        (row for row in high_stalled if row["pushed"] < definite_cutoff),
        key=lambda row: -row["stars"],
    )
    borderline = sorted(
        (row for row in high_stalled if row["pushed"] >= definite_cutoff),
        key=lambda row: -row["stars"],
    )

    native_active = [row for row in active if class_by_repo.get(row["repo"]) == "native"]
    top_native = sorted(native_active, key=lambda row: -row["stars"])[:15]
    owner_counts = Counter(row["repo"].split("/", 1)[0] for row in active)
    cat_counts = Counter(categories.get(row["repo"], "unclassified") for row in active)
    high_cat = Counter(categories.get(row["repo"], "unclassified") for row in active if row["stars"] >= 10)
    tail_cat = Counter(categories.get(row["repo"], "unclassified") for row in active if row["stars"] < 10)

    dist_rows = [row for row in jsonl(args.audit_dir / "dist_check.jsonl") if row["repo"] in active_names]
    dist_by_repo = {row["repo"]: row for row in dist_rows}
    native_names = {row["repo"] for row in native_active}
    native_dist = [row for row in dist_rows if row["repo"] in native_names]

    category_details = {}
    for category, count in cat_counts.most_common():
        category_rows = [row for row in active if categories.get(row["repo"]) == category]
        category_dist = [dist_by_repo[row["repo"]] for row in category_rows if row["repo"] in dist_by_repo]
        category_details[category] = {
            "repos": count,
            "stars": sum(row["stars"] for row in category_rows),
            "star_10_plus": sum(row["stars"] >= 10 for row in category_rows),
            "native": sum(class_by_repo.get(row["repo"]) == "native" for row in category_rows),
            "adapted": sum(class_by_repo.get(row["repo"]) == "adapted" for row in category_rows),
            "unrelated": sum(class_by_repo.get(row["repo"]) == "unrelated" for row in category_rows),
            "distribution": distribution(category_dist),
        }

    remote_rows = [row for row in active if categories.get(row["repo"]) == "remote-access"]
    remote_names = {row["repo"] for row in remote_rows}
    remote_native = [row for row in remote_rows if class_by_repo.get(row["repo"]) == "native"]
    remote_dist = [row for row in dist_rows if row["repo"] in remote_names]
    remote_native_names = {row["repo"] for row in remote_native}
    remote_native_dist = [row for row in remote_dist if row["repo"] in remote_native_names]
    remote_routes = Counter(
        inventory_by_repo[row["repo"]].get("remote_route", "generic-remote")
        for row in remote_rows
    )

    mobile_rows = [row for row in active if categories.get(row["repo"]) == "mobile-client"]
    mobile_names = {row["repo"] for row in mobile_rows}
    mobile_dist = [row for row in dist_rows if row["repo"] in mobile_names]

    star_tiers = {
        "100+": sum(row["stars"] >= 100 for row in repos),
        "20-99": sum(20 <= row["stars"] < 100 for row in repos),
        "5-19": sum(5 <= row["stars"] < 20 for row in repos),
        "1-4": sum(1 <= row["stars"] < 5 for row in repos),
        "0": sum(row["stars"] == 0 for row in repos),
    }
    activity_tiers = {}
    for label, lo, hi in (("100+", 100, 10**12), ("20-99", 20, 100), ("5-19", 5, 20), ("1-4", 1, 5), ("0", 0, 1)):
        group = [row for row in repos if lo <= row["stars"] < hi]
        passed = sum(row["pushed"] >= anchor for row in group)
        activity_tiers[label] = {"passed": passed, "total": len(group), "rate": passed / len(group)}

    class_counts = Counter(row["cls"] for row in classified)
    class_stars = Counter()
    for row in classified:
        class_stars[row["cls"]] += row["stars"]

    summary = {
        "snapshot": {
            "enumerated": len(repos),
            "official": args.official_count,
            "official_source": args.official_source,
            "coverage": len(repos) / args.official_count,
            "readmes": len(json.loads((args.audit_dir / "analysis.json").read_text())),
            "anchor": anchor,
            "anchor_label": args.anchor_label,
            "native_only": args.native_only,
        },
        "scale": {
            "star_tiers": star_tiers,
            "one_shot": sum(row["pushed"][:10] <= row["created"][:10] for row in repos),
            "languages": Counter(row.get("lang") or "Unknown" for row in repos).most_common(8),
        },
        "activity": {
            "passed": sum(row["pushed"] >= anchor for row in repos),
            "rate": sum(row["pushed"] >= anchor for row in repos) / len(repos),
            "tiers": activity_tiers,
            "active_starred": len(active),
            "native_active_starred": len(native_active),
        },
        "high_star": {
            "total": len(high),
            "active": len(high_active),
            "stalled": len(high_stalled),
            "native": sum(class_by_repo.get(row["repo"]) == "native" for row in high),
            "native_active": sum(
                class_by_repo.get(row["repo"]) == "native" and row["pushed"] >= anchor
                for row in high
            ),
            "definite_stalled": len(definite),
            "borderline_stalled": len(borderline),
            "top_definite": definite[:15],
            "top_borderline": borderline[:10],
        },
        "classification": {
            "counts": dict(class_counts),
            "stars": dict(class_stars),
            "first_native_rank": next(
                index + 1
                for index, row in enumerate(sorted(classified, key=lambda row: -row["stars"]))
                if row["cls"] == "native"
            ),
        },
        "categories": dict(cat_counts.most_common()),
        "category_details": category_details,
        "tier_categories": {
            "active_10_plus": dict(high_cat.most_common()),
            "active_1_9": dict(tail_cat.most_common()),
        },
        "top_native_active": top_native,
        "owner_concentration": owner_counts.most_common(15),
        "remote_access": {
            "repos": len(remote_rows),
            "stars": sum(row["stars"] for row in remote_rows),
            "star_10_plus": sum(row["stars"] >= 10 for row in remote_rows),
            "native": len(remote_native),
            "routes": dict(remote_routes.most_common()),
            "distribution": {
                "all": distribution(remote_dist),
                "native": distribution(remote_native_dist),
            },
            "top": [
                {
                    **row,
                    "cls": class_by_repo.get(row["repo"], "unclassified"),
                    "route": inventory_by_repo[row["repo"]].get("remote_route", "generic-remote"),
                }
                for row in sorted(remote_rows, key=lambda item: -item["stars"])[:25]
            ],
        },
        "mobile_client": {
            "repos": len(mobile_rows),
            "stars": sum(row["stars"] for row in mobile_rows),
            "star_10_plus": sum(row["stars"] >= 10 for row in mobile_rows),
            "native": sum(class_by_repo.get(row["repo"]) == "native" for row in mobile_rows),
            "distribution": distribution(mobile_dist),
            "top": sorted(mobile_rows, key=lambda item: -item["stars"])[:15],
        },
        "distribution": {
            "all_active": distribution(dist_rows),
            "native_active": distribution(native_dist),
        },
    }
    output_path = args.output or (args.audit_dir / "audit_summary.json")
    output_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
