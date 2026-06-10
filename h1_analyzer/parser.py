"""Parser: raw text line -> structured `LogRequest`.

Teaching point:
    This is the first step in the story. We cannot reason about hackers from
    unstructured text reliably, so we convert each line into named fields.

Design choice:
    Return `None` for malformed lines instead of crashing. A 21M-line contest
    log may contain a few bad rows; the analyzer should report them, not stop.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from .models import LogRequest


def parse_log_line(line: str, line_number: int) -> Optional[LogRequest]:
    """Parse one NexusCart-style access-log line.

    Expected format:
        2024-06-10 04:17:43 | 39.3.141.152 | POST | /checkout | 200 | 122

    Returns:
        LogRequest when the line is valid, otherwise None.
    """
    raw = line.rstrip("\n\r")
    parts = [part.strip() for part in raw.split(" | ")]
    if len(parts) != 6:
        return None

    timestamp_text, ip, method, endpoint, status_text, size_text = parts
    try:
        # Manual datetime construction is much faster than `strptime` on a
        # 21M-line log while still returning a real datetime for tests/docs.
        timestamp = datetime(
            int(timestamp_text[0:4]),
            int(timestamp_text[5:7]),
            int(timestamp_text[8:10]),
            int(timestamp_text[11:13]),
            int(timestamp_text[14:16]),
            int(timestamp_text[17:19]),
        )
        status = int(status_text)
        size = int(size_text)
    except (ValueError, IndexError):
        return None

    return LogRequest(
        line_number=line_number,
        raw=raw,
        timestamp=timestamp,
        minute=timestamp.strftime("%Y-%m-%d %H:%M"),
        ip=ip,
        method=method.upper(),
        endpoint=endpoint,
        status=status,
        size=size,
    )
