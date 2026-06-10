"""High-level runner for the H1 analyzer.

This file connects all story steps:
    parse -> detect -> score -> aggregate -> timeline -> hidden bonus -> reports
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from .aggregators import AnalysisState
from .hidden_bonus import find_hidden_clues
from .parser import parse_log_line
from .reports import write_csv, write_json, write_markdown_summary
from .timeline import build_incident_windows


def _compact_timeline_for_dashboard(timeline: list[dict], every_n: int = 240) -> list[dict]:
    """Return a browser-friendly timeline sample.

    The CSV keeps every minute. JSON keeps:
    - regular samples every `every_n` minutes
    - rows where system_state changes
    - top rows with the highest 5xx/suspicious counts

    This avoids creating a huge dashboard JSON while preserving the shape of the
    incident story for presentation.
    """
    keep_indexes: set[int] = set()
    previous_state = None
    for idx, row in enumerate(timeline):
        state = row.get("system_state")
        if idx % every_n == 0 or state != previous_state:
            keep_indexes.add(idx)
        previous_state = state

    # Preserve strongest spikes even if they fall between regular samples.
    ranked = sorted(
        enumerate(timeline),
        key=lambda item: (item[1].get("status_5xx", 0), item[1].get("suspicious_requests", 0), item[1].get("total_requests", 0)),
        reverse=True,
    )
    for idx, _row in ranked[:1000]:
        keep_indexes.add(idx)

    return [timeline[idx] for idx in sorted(keep_indexes)]

ATTACKER_FIELDS = [
    "ip", "label", "score", "total_requests", "peak_rpm", "status_404", "status_403",
    "status_401", "status_500", "payload_hits", "sensitive_hits", "first_seen", "last_seen",
    "evidence_count", "reasons",
]
TIMELINE_FIELDS = [
    "minute", "total_requests", "status_2xx", "status_3xx", "status_4xx", "status_5xx",
    "unique_ips", "suspicious_requests", "system_state",
]
INCIDENT_FIELDS = ["start_time", "end_time", "states_seen", "peak_requests", "peak_5xx", "total_suspicious_requests", "reason"]
ENDPOINT_FIELDS = [
    "endpoint", "total_requests", "unique_ips", "status_200", "status_302", "status_304",
    "status_401", "status_403", "status_404", "status_500", "status_504", "status_5xx",
    "payload_hits", "attack_type",
]
EVIDENCE_FIELDS = ["line_number", "timestamp", "ip", "method", "endpoint", "status", "size", "score", "reasons"]
HIDDEN_FIELDS = ["candidate", "confidence", "clue_type", "decode_method", "timestamp", "ip", "endpoint", "reason"]


def run_analysis(log_path: Path, output_dir: Path, max_lines: Optional[int] = None) -> dict:
    """Run the full analysis and write output files.

    Args:
        log_path: Path to `cart_web.log` or a sample log.
        output_dir: Directory where CSV/JSON/Markdown reports are written.
        max_lines: Optional debug limit. Use this for quick dry-runs.
    """
    log_path = Path(log_path)
    output_dir = Path(output_dir)
    state = AnalysisState(max_evidence_per_ip=5, max_global_evidence=1000)

    with log_path.open("r", encoding="utf-8", errors="replace") as f:
        for line_number, line in enumerate(f, 1):
            if max_lines is not None and line_number > max_lines:
                break
            parsed = parse_log_line(line, line_number)
            if parsed is None:
                state.add_malformed()
            else:
                state.add_request(parsed)

    attackers = state.attacker_rows()
    # Keep normal IPs in CSV too, but dashboard/report focuses on suspicious rows.
    suspicious_attackers = [row for row in attackers if row["label"] != "normal"]
    timeline = state.timeline_rows()
    incidents = build_incident_windows(timeline)
    endpoints = state.endpoint_rows()
    evidence = state.evidence_rows()
    hidden = find_hidden_clues(state.hidden_scan_endpoints())

    overview = {
        "source_log": str(log_path),
        "parsed_lines": state.parsed_lines,
        "malformed_lines": state.malformed_lines,
        "unique_ips": len(state.unique_ips_seen) if state.parsed_lines <= 1_000_000 else "not_tracked_for_full_run",
        "suspicious_ips": len(suspicious_attackers),
        "status_counts": dict(sorted(state.status_counts.items())),
        "note": "No response-time/User-Agent fields in this log; unstable windows are inferred from traffic/error spikes.",
    }

    write_csv(output_dir / "attacker_ips.csv", suspicious_attackers, ATTACKER_FIELDS)
    write_csv(output_dir / "traffic_timeline.csv", timeline, TIMELINE_FIELDS)
    write_csv(output_dir / "incident_windows.csv", incidents, INCIDENT_FIELDS)
    write_csv(output_dir / "endpoint_summary.csv", endpoints, ENDPOINT_FIELDS)
    write_csv(output_dir / "suspicious_requests.csv", evidence, EVIDENCE_FIELDS)
    write_csv(output_dir / "hidden_bonus_candidates.csv", hidden, HIDDEN_FIELDS)
    write_json(
        output_dir / "dashboard_data.json",
        {
            "overview": overview,
            "attackers": suspicious_attackers[:100],
            # Dashboard JSON should be compact enough for a browser demo.
            # Full minute-by-minute data remains available in traffic_timeline.csv.
            "timeline": _compact_timeline_for_dashboard(timeline),
            "incidents": incidents,
            "endpoints": endpoints[:100],
            "evidence": evidence[:300],
            "hidden_bonus": hidden,
        },
    )
    write_markdown_summary(output_dir / "h1_summary.md", overview, suspicious_attackers, incidents, hidden)
    return overview
