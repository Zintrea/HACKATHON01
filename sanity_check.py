#!/usr/bin/env python3
"""Sanity checks for H1 analyzer outputs.

Why this exists:
    Bai correctly noticed that an earlier `endpoint_summary.csv` was misleading:
    it looked like only 500/404 existed because the report was attack-only.

This script is a lightweight guardrail. It checks that the generated output
folder has the expected files, expected columns, readable JSON, and a few
important interpretation invariants such as `/cart` and `/cart_` being separated.
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


REQUIRED_FILES = {
    "attacker_ips.csv",
    "endpoint_summary.csv",
    "incident_windows.csv",
    "suspicious_requests.csv",
    "traffic_timeline.csv",
    "hidden_bonus_candidates.csv",
    "dashboard_data.json",
    "h1_summary.md",
}

EXPECTED_COLUMNS = {
    "attacker_ips.csv": [
        "ip", "label", "score", "total_requests", "peak_rpm", "status_404", "status_403",
        "status_401", "status_500", "payload_hits", "sensitive_hits", "first_seen", "last_seen",
        "evidence_count", "reasons",
    ],
    "endpoint_summary.csv": [
        "endpoint", "total_requests", "unique_ips", "status_200", "status_302", "status_304",
        "status_401", "status_403", "status_404", "status_500", "status_504", "status_5xx",
        "payload_hits", "attack_type",
    ],
    "incident_windows.csv": [
        "start_time", "end_time", "states_seen", "peak_requests", "peak_5xx",
        "peak_p95_latency_ms", "total_suspicious_requests", "reason",
    ],
    "suspicious_requests.csv": [
        "line_number", "timestamp", "ip", "method", "endpoint", "status", "latency_ms", "score", "reasons",
    ],
    "traffic_timeline.csv": [
        "minute", "total_requests", "status_2xx", "status_3xx", "status_4xx", "status_5xx",
        "unique_ips", "suspicious_requests", "avg_latency_ms", "p95_latency_ms", "max_latency_ms", "system_state",
    ],
    "hidden_bonus_candidates.csv": [
        "candidate", "confidence", "clue_type", "decode_method", "timestamp", "ip", "endpoint", "reason",
    ],
}


@dataclass
class SanityResult:
    """Result object returned by `run_sanity_checks` and printed by CLI."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    infos: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def read_header(path: Path) -> list[str]:
    """Read a CSV header safely."""
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            return next(reader)
        except StopIteration:
            return []


def read_rows(path: Path, limit: int | None = None) -> list[dict]:
    """Read CSV rows. Limit is optional because most summary CSVs are small."""
    rows: list[dict] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            if limit is not None and idx >= limit:
                break
            rows.append(row)
    return rows


def to_int(value: str | int | None) -> int:
    """Convert numeric CSV text to int; non-numeric becomes 0 for checks."""
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0


def run_sanity_checks(output_dir: Path) -> SanityResult:
    """Validate output folder shape and key interpretation invariants."""
    output_dir = Path(output_dir)
    result = SanityResult()

    if not output_dir.exists():
        result.errors.append(f"Output directory does not exist: {output_dir}")
        return result

    existing = {path.name for path in output_dir.iterdir() if path.is_file()}
    missing = sorted(REQUIRED_FILES - existing)
    if missing:
        result.errors.append(f"Missing required output files: {', '.join(missing)}")

    # Check stable CSV schemas.
    for filename, expected in EXPECTED_COLUMNS.items():
        path = output_dir / filename
        if not path.exists():
            continue
        header = read_header(path)
        missing_cols = [col for col in expected if col not in header]
        if missing_cols:
            result.errors.append(f"{filename} missing columns: {', '.join(missing_cols)}")
        else:
            result.infos.append(f"{filename} columns OK ({len(header)} columns)")

    # JSON should be parseable and include dashboard sections.
    dashboard_path = output_dir / "dashboard_data.json"
    if dashboard_path.exists():
        try:
            data = json.loads(dashboard_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            result.errors.append(f"dashboard_data.json is not valid JSON: {exc}")
        else:
            for key in ["overview", "attackers", "timeline", "incidents", "endpoints", "evidence", "hidden_bonus"]:
                if key not in data:
                    result.errors.append(f"dashboard_data.json missing key: {key}")
            result.infos.append("dashboard_data.json is readable")

    # Endpoint sanity: `/cart` and `/cart_` are different and should not be merged.
    endpoint_path = output_dir / "endpoint_summary.csv"
    if endpoint_path.exists() and not any("endpoint_summary.csv missing columns" in e for e in result.errors):
        endpoints = {row.get("endpoint", ""): row for row in read_rows(endpoint_path)}
        cart = endpoints.get("/cart")
        cart_ = endpoints.get("/cart_")
        if cart and cart_:
            if to_int(cart.get("status_5xx")) == 0 and to_int(cart_.get("status_5xx")) > 0:
                result.infos.append("/cart and /cart_ are separated: normal cart has no 5xx, cart_ has 5xx")
            else:
                result.warnings.append("/cart and /cart_ exist but their 5xx pattern is not the expected normal-vs-variant split")
        else:
            result.warnings.append("Could not find both /cart and /cart_ in endpoint_summary.csv")

    # Attacker sanity: ranking should not be empty for the current H1 output.
    attacker_path = output_dir / "attacker_ips.csv"
    if attacker_path.exists():
        attackers = read_rows(attacker_path, limit=5)
        if not attackers:
            result.warnings.append("attacker_ips.csv has no rows; check scoring thresholds or input log")
        else:
            result.infos.append(f"attacker_ips.csv has at least {len(attackers)} suspicious rows")

    return result


def print_result(result: SanityResult) -> None:
    """Pretty-print result for CLI usage."""
    print("H1 output sanity check")
    print("status=PASS" if result.ok else "status=FAIL")
    for section, items in [("ERRORS", result.errors), ("WARNINGS", result.warnings), ("INFO", result.infos)]:
        if not items:
            continue
        print(f"\n{section}:")
        for item in items:
            print(f"- {item}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate H1 analyzer output files and schemas.")
    parser.add_argument("output_dir", nargs="?", default="output", type=Path, help="Path to analyzer output directory")
    args = parser.parse_args()

    result = run_sanity_checks(args.output_dir)
    print_result(result)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
