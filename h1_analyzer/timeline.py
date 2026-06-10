"""Incident-window builder.

The analyzer first creates one row per minute. This module merges adjacent
non-normal minutes into presentation-friendly windows.
"""
from __future__ import annotations


def build_incident_windows(timeline_rows: list[dict]) -> list[dict]:
    """Merge adjacent suspicious/unstable/down minutes into incident windows."""
    windows: list[dict] = []
    current: dict | None = None

    for row in timeline_rows:
        state = row.get("system_state", "normal")
        abnormal = state != "normal"
        if not abnormal:
            if current:
                windows.append(current)
                current = None
            continue

        if current is None:
            current = {
                "start_time": row["minute"],
                "end_time": row["minute"],
                "states_seen": state,
                "peak_requests": row["total_requests"],
                "peak_5xx": row["status_5xx"],
                "total_suspicious_requests": row.get("suspicious_requests", 0),
                "reason": "traffic/error/suspicious-request spike inferred from log metrics",
            }
        else:
            current["end_time"] = row["minute"]
            states = set(current["states_seen"].split(";"))
            states.add(state)
            current["states_seen"] = ";".join(sorted(states))
            current["peak_requests"] = max(current["peak_requests"], row["total_requests"])
            current["peak_5xx"] = max(current["peak_5xx"], row["status_5xx"])
            current["total_suspicious_requests"] += row.get("suspicious_requests", 0)

    if current:
        windows.append(current)
    return windows
