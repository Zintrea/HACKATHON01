#!/usr/bin/env python3
"""Build standalone dashboard data for H1 presentation.

This script converts analyzer outputs into `dashboard/data.js` so the dashboard
can be opened by double-clicking `index.html` without a local server. Browsers
often block `fetch()` from `file://`, so embedding data as a JS variable is the
simplest presentation-safe approach.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
DASHBOARD = ROOT / "dashboard"


def read_csv(name: str, limit: int | None = None) -> list[dict]:
    rows: list[dict] = []
    with (OUTPUT / name).open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            if limit is not None and idx >= limit:
                break
            rows.append(_coerce_numbers(row))
    return rows


def _coerce_numbers(row: dict) -> dict:
    converted = {}
    for key, value in row.items():
        if isinstance(value, str) and value.isdigit():
            converted[key] = int(value)
        else:
            converted[key] = value
    return converted


def pick_endpoint_rows(rows: list[dict]) -> list[dict]:
    """Pick rows that tell the presentation story clearly."""
    important = {"/cart", "/cart_", "/search", "/search_", "/products", "/products_", "/checkout", "/checkout_", "/api/v1/user", "/api/v1/user_", "/index.html", "/index_.html"}
    selected = [row for row in rows if row.get("endpoint") in important]
    seen = {row.get("endpoint") for row in selected}
    # Add top server-error variants if not already present.
    for row in rows:
        if len(selected) >= 24:
            break
        if row.get("endpoint") not in seen and int(row.get("status_5xx", 0)) > 0:
            selected.append(row)
            seen.add(row.get("endpoint"))
    return selected


def build_data() -> dict:
    attackers = read_csv("attacker_ips.csv")
    endpoints = read_csv("endpoint_summary.csv")
    incidents = read_csv("incident_windows.csv")
    suffixes = read_csv("suffix_patterns.csv") if (OUTPUT / "suffix_patterns.csv").exists() else []
    evidence = read_csv("suspicious_requests.csv", limit=80)

    overview = {
        "parsed_lines": 21146397,
        "malformed_lines": 1,
        "suspicious_ips": len(attackers),
        "status_counts": {"200": 10608035, "304": 2581383, "404": 2584078, "500": 2687007, "504": 2685894},
        "suffix_sequence": "".join(row["suffix"] for row in suffixes),
        "note": "No response-time/User-Agent fields; unstable/down windows are inferred from traffic and 5xx patterns.",
    }

    return {
        "overview": overview,
        "attackers": attackers,
        "endpoints": pick_endpoint_rows(endpoints),
        "incidents": incidents[:40],
        "suffixes": suffixes,
        "evidence": evidence,
        "generated_from": {
            "attacker_ips": "output/attacker_ips.csv",
            "endpoint_summary": "output/endpoint_summary.csv",
            "incident_windows": "output/incident_windows.csv",
            "suffix_patterns": "output/suffix_patterns.csv",
            "suspicious_requests": "output/suspicious_requests.csv",
        },
    }


def main() -> int:
    DASHBOARD.mkdir(parents=True, exist_ok=True)
    data = build_data()
    data_js = "window.H1_DASHBOARD_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    (DASHBOARD / "data.js").write_text(data_js, encoding="utf-8")
    print(f"Wrote {DASHBOARD / 'data.js'}")
    print(f"attackers={len(data['attackers'])} endpoints={len(data['endpoints'])} suffixes={len(data['suffixes'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
