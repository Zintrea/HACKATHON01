"""Red flag detector for individual requests.

Teaching point:
    This module does NOT decide who the hacker is. It only labels suspicious
    signals on each request. Later modules aggregate these signals per IP/time.
"""
from __future__ import annotations

import re
from urllib.parse import unquote_plus

from .models import LogRequest

# Keep pattern lists near the detector so Bai can explain or tune them quickly.
PATH_TRAVERSAL_PATTERNS = [
    "../",
    "..\\",
    "%2e%2e",
    "%2f",
    "/etc/passwd",
    "/proc/self",
    "windows/win.ini",
]

SQLI_PATTERNS = [
    " union ",
    " select ",
    " or 1=1",
    " or '1'='1",
    "%27",
    "--",
    "/*",
    "sleep(",
]

XSS_PATTERNS = [
    "<script",
    "%3cscript",
    "javascript:",
    "onerror=",
    "onload=",
]

SENSITIVE_ENDPOINTS = [
    "/admin",
    "/admin_dashboard",
    "/login",
    "/api/v1/users",
    "/.env",
    "/config",
    "/config.php",
    "/backup",
    "/backup.zip",
    "/db.sql",
    "/phpmyadmin",
    "/wp-admin",
]


def _normalized_endpoint(endpoint: str) -> str:
    """Lowercase and URL-decode endpoint for easier pattern matching.

    Fast path matters for a 21M-line log: most endpoints contain no encoded
    characters, so we avoid URL decoding unless `%` or `+` appears.
    """
    lowered = endpoint.lower()
    if "%" in lowered or "+" in lowered:
        return unquote_plus(unquote_plus(lowered))
    return lowered


def detect_request_flags(request: LogRequest) -> list[str]:
    """Return red-flag labels for one request.

    Examples of labels: `sqli`, `path_traversal`, `server_error`.
    Multiple labels can appear on the same request.
    """
    endpoint = _normalized_endpoint(request.endpoint)
    flags: list[str] = []

    if any(pattern in endpoint for pattern in PATH_TRAVERSAL_PATTERNS):
        flags.append("path_traversal")

    # A raw single quote is common in SQLi, but it can also appear in normal
    # text. We include it only with broader SQL keywords/operators.
    if any(pattern in endpoint for pattern in SQLI_PATTERNS) or re.search(r"'\s*(or|and)\s+", endpoint):
        flags.append("sqli")

    if any(pattern in endpoint for pattern in XSS_PATTERNS):
        flags.append("xss")

    if any(endpoint.startswith(path) or path in endpoint for path in SENSITIVE_ENDPOINTS):
        flags.append("sensitive_endpoint")

    if request.status == 404:
        flags.append("not_found")
    if request.status in {401, 403}:
        flags.append("forbidden_or_unauthorized")
    if 500 <= request.status <= 599:
        flags.append("server_error")

    return flags


def attack_type_from_flags(flags: list[str]) -> str:
    """Convert red flags into a human-readable attack type for reports."""
    for priority in ["path_traversal", "sqli", "xss", "sensitive_endpoint", "server_error"]:
        if priority in flags:
            return priority
    return "normal"
