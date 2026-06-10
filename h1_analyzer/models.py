"""Shared data models for the H1 analyzer.

Why this file exists:
- A log analyzer quickly becomes hard to teach if every function passes around
  loose tuples like `(time, ip, endpoint, status)`.
- Dataclasses give every field a name, making the code read like the story we
  want to present: one raw line becomes one `LogRequest`, then scoring produces
  one `RequestScore`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass(frozen=True)
class LogRequest:
    """One parsed access-log request.

    The source log format is:
        timestamp | ip | method | endpoint | status | size

    We keep `raw` and `line_number` because evidence matters. If a judge asks
    "why is this IP suspicious?", we can point back to exact request examples.
    """

    line_number: int
    raw: str
    timestamp: datetime
    minute: str
    ip: str
    method: str
    endpoint: str
    status: int
    size: int


@dataclass(frozen=True)
class RequestScore:
    """Suspicion score for a single request.

    `reasons` are more important than the number itself during presentation:
    they explain *why* the request is suspicious.
    """

    score: int
    reasons: List[str] = field(default_factory=list)


@dataclass
class IpStats:
    """Aggregated behavior for one IP address.

    This is where individual clues become a pattern. A single 404 might be a
    typo; hundreds of 404s across sensitive endpoints become evidence.
    """

    ip: str
    total_requests: int = 0
    status_404: int = 0
    status_403: int = 0
    status_401: int = 0
    status_500: int = 0
    payload_hits: int = 0
    sensitive_hits: int = 0
    request_score_total: int = 0
    first_seen: str = ""
    last_seen: str = ""
    minute_counts: Dict[str, int] = field(default_factory=dict)
    reasons: Dict[str, int] = field(default_factory=dict)
    evidence: List[dict] = field(default_factory=list)

    def peak_rpm(self) -> int:
        """Return peak requests per minute for this IP."""
        return max(self.minute_counts.values(), default=0)
