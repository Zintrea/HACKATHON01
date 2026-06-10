"""Explainable suspicion scoring.

Teaching point:
    A score is not "truth". It is a reproducible way to prioritize evidence and
    avoid claiming that one signal (like a single 500) proves an attack.
"""
from __future__ import annotations

from .models import LogRequest, RequestScore
from .patterns import detect_request_flags

# Request-level weights. Strong exploit payloads get higher weights than noisy
# but ambiguous signals such as a single 404.
REQUEST_WEIGHTS = {
    "path_traversal": 5,
    "sqli": 5,
    "xss": 5,
    "sensitive_endpoint": 3,
    "server_error": 4,
    "forbidden_or_unauthorized": 2,
    "not_found": 1,
}


def score_request(request: LogRequest) -> RequestScore:
    """Score one request and preserve the reasons behind the score."""
    flags = detect_request_flags(request)
    score = sum(REQUEST_WEIGHTS.get(flag, 0) for flag in flags)
    return RequestScore(score=score, reasons=flags)


def classify_ip_score(score: int) -> str:
    """Map a numeric IP score to a label used in reports/dashboard."""
    if score >= 13:
        return "high_confidence_attacker"
    if score >= 7:
        return "likely_attacker"
    if score >= 3:
        return "suspicious"
    return "normal"
