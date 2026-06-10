#!/usr/bin/env python3
"""Hunt endpoint suffix patterns from H1 output.

Why this exists:
    Bai observed that the 19 suspicious IPs hit strange endpoint variants such as
    `/cart_`, `/searchE`, `/productsA`. This script turns that observation into
    a reproducible report.

Input:
    output/endpoint_summary.csv

Output:
    output/suffix_patterns.csv
    output/suffix_pattern_report.md

Teaching story:
    1. Start from endpoint_summary, not raw manual reading.
    2. Compare endpoints against known normal base endpoints.
    3. Extract the extra suffix after the base path.
    4. Sort suffixes by first appearance in endpoint_summary and aggregate 5xx.
    5. Join suffix characters to see whether they form a hidden clue.
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

# Known normal endpoints from the H1 log. Variants are detected by checking
# whether an endpoint starts with one of these bases and has extra characters.
# Longest bases first so `/api/v1/userA` matches `/api/v1/user`, not `/api`.
NORMAL_BASE_ENDPOINTS = [
    "/api/v1/user",
    "/index.html",
    "/checkout",
    "/products",
    "/search",
    "/cart",
]
NORMAL_BASE_ENDPOINTS.sort(key=len, reverse=True)


def base_endpoint(endpoint: str) -> str | None:
    """Return the normal base endpoint for a suspicious variant.

    Handles both simple suffixes (`/cart_`) and pre-extension suffixes
    (`/indexE.html` -> base `/index.html`, suffix `E`).
    """
    # Special case: `/indexE.html` means suffix before `.html`.
    if endpoint.startswith("/index") and endpoint.endswith(".html") and endpoint != "/index.html":
        middle = endpoint[len("/index") : -len(".html")]
        if middle:
            return "/index.html"

    for base in NORMAL_BASE_ENDPOINTS:
        if endpoint.startswith(base) and endpoint != base:
            return base
    return endpoint if endpoint in NORMAL_BASE_ENDPOINTS else None


def detect_suffix(endpoint: str) -> str | None:
    """Extract the extra suffix from an endpoint variant.

    Examples:
        /cart_ -> _
        /searchE -> E
        /indexE.html -> E
        /api/v1/userA -> A
    """
    if endpoint.startswith("/index") and endpoint.endswith(".html") and endpoint != "/index.html":
        middle = endpoint[len("/index") : -len(".html")]
        return middle or None

    base = base_endpoint(endpoint)
    if not base or endpoint == base:
        return None
    return endpoint[len(base) :] or None


def to_int(value: str | int | None) -> int:
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0


def read_endpoint_summary(endpoint_csv: Path) -> list[dict]:
    with endpoint_csv.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def analyze_suffix_patterns(endpoint_csv: Path) -> dict:
    """Aggregate suspicious endpoint variants by suffix.

    The order is based on first appearance in `endpoint_summary.csv`, which is
    sorted by suspicious/error impact from the analyzer. This gives a natural
    clue order: the strongest endpoint-variant group first.
    """
    rows = read_endpoint_summary(endpoint_csv)
    suffix_stats: dict[str, dict] = {}
    examples_by_suffix: dict[str, list[str]] = defaultdict(list)

    for order, row in enumerate(rows, 1):
        endpoint = row.get("endpoint", "")
        suffix = detect_suffix(endpoint)
        base = base_endpoint(endpoint)
        total_5xx = to_int(row.get("status_5xx"))

        # Focus on variants that actually caused server-side errors. Normal
        # endpoints like `/cart` are useful baseline but not suffix clues.
        if not suffix or total_5xx <= 0:
            continue

        stat = suffix_stats.setdefault(
            suffix,
            {
                "suffix": suffix,
                "first_rank": order,
                "joined_order_hint": suffix,
                "endpoint_count": 0,
                "total_requests": 0,
                "total_5xx": 0,
                "status_500": 0,
                "status_504": 0,
                "unique_ips_max": 0,
                "bases_seen": set(),
            },
        )
        stat["first_rank"] = min(stat["first_rank"], order)
        stat["endpoint_count"] += 1
        stat["total_requests"] += to_int(row.get("total_requests"))
        stat["total_5xx"] += total_5xx
        stat["status_500"] += to_int(row.get("status_500"))
        stat["status_504"] += to_int(row.get("status_504"))
        stat["unique_ips_max"] = max(stat["unique_ips_max"], to_int(row.get("unique_ips")))
        if base:
            stat["bases_seen"].add(base)
        if len(examples_by_suffix[suffix]) < 8:
            examples_by_suffix[suffix].append(endpoint)

    suffix_rows = []
    for suffix, stat in suffix_stats.items():
        suffix_rows.append(
            {
                "suffix": suffix,
                "first_rank": stat["first_rank"],
                "endpoint_count": stat["endpoint_count"],
                "total_requests": stat["total_requests"],
                "total_5xx": stat["total_5xx"],
                "status_500": stat["status_500"],
                "status_504": stat["status_504"],
                "unique_ips_max": stat["unique_ips_max"],
                "bases_seen": ";".join(sorted(stat["bases_seen"])),
                "examples": ";".join(examples_by_suffix[suffix]),
            }
        )

    suffix_rows.sort(key=lambda r: (r["first_rank"], -r["total_5xx"]))
    ordered_suffixes = [row["suffix"] for row in suffix_rows]
    joined_suffixes = "".join(ordered_suffixes)

    return {
        "suffix_rows": suffix_rows,
        "ordered_suffixes": ordered_suffixes,
        "joined_suffixes": joined_suffixes,
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = [
        "suffix", "first_rank", "endpoint_count", "total_requests", "total_5xx",
        "status_500", "status_504", "unique_ips_max", "bases_seen", "examples",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, result: dict, endpoint_csv: Path) -> None:
    rows = result["suffix_rows"]
    lines = [
        "# Suffix Pattern Hunt — Endpoint Variants",
        "",
        "> Purpose: ตรวจ endpoint แปลก ๆ ที่เติม suffix หลัง endpoint ปกติ เช่น `/cart_`, `/searchE`, `/productsA` แล้วเรียง suffix เพื่อดู clue ที่อาจซ่อนอยู่",
        "",
        "## Method",
        "",
        f"- Source: `{endpoint_csv}`",
        "- ใช้ `endpoint_summary.csv` เพราะเป็น output ที่รวม endpoint และ status split แล้ว ไม่ต้องไล่อ่าน raw log manual",
        "- เทียบ endpoint กับ base ปกติ: `/cart`, `/search`, `/products`, `/checkout`, `/api/v1/user`, `/index.html`",
        "- ถ้ามีตัวอักษร/สัญลักษณ์ต่อท้าย และ endpoint นั้นมี `status_5xx > 0` จะถือเป็น suspicious suffix variant",
        "- เรียง suffix ตาม `first_rank` คืออันดับแรกที่ suffix นั้นปรากฏใน endpoint_summary ซึ่งถูก sort ตาม impact/error pattern",
        "",
        "## Ordered Suffixes",
        "",
        f"```text\n{result['joined_suffixes']}\n```",
        "",
        "## Suffix Table",
        "",
        "| Order | Suffix | Total 5xx | Status 500 | Status 504 | Endpoint Count | Max Unique IPs | Examples |",
        "|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for idx, row in enumerate(rows, 1):
        examples = row["examples"].replace("|", "\\|")
        lines.append(
            f"| {idx} | `{row['suffix']}` | {row['total_5xx']} | {row['status_500']} | {row['status_504']} | {row['endpoint_count']} | {row['unique_ips_max']} | `{examples}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- ถ้า suffix ที่เรียงได้กลายเป็นคำ/วลี อาจเป็น hidden clue หรือ signature ของ attacker",
            "- ถ้า suffix มีหลาย endpoint ต่อ base เดียวกัน แปลว่า attacker ยิง pattern เป็นชุด ไม่ใช่ path เดี่ยว",
            "- ต้อง validate ต่อด้วย raw evidence หรือ suspicious IP group ก่อนฟันธงว่าเป็น hidden bonus",
            "",
            "## Presentation wording",
            "",
            "> We noticed that suspicious endpoints are not random. They are normal endpoints with added suffix characters. By grouping these suffixes in impact order, the sequence becomes a potential hidden clue and also explains the attack pattern.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze suspicious endpoint suffix patterns from endpoint_summary.csv")
    parser.add_argument("--endpoint-summary", type=Path, default=Path("output/endpoint_summary.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    args = parser.parse_args()

    result = analyze_suffix_patterns(args.endpoint_summary)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "suffix_patterns.csv", result["suffix_rows"])
    write_report(args.output_dir / "suffix_pattern_report.md", result, args.endpoint_summary)

    print("Suffix pattern hunt completed")
    print(f"suffix_count={len(result['suffix_rows'])}")
    print(f"ordered_suffixes={result['joined_suffixes']}")
    print(f"csv={args.output_dir / 'suffix_patterns.csv'}")
    print(f"report={args.output_dir / 'suffix_pattern_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
