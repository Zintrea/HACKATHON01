"""Hidden bonus clue hunter.

This module searches endpoint strings for clues such as names, signatures,
base64/hex/URL-encoded text. It treats weird text as evidence only; it never
follows instruction-like content that may appear inside logs.
"""
from __future__ import annotations

import base64
import binascii
import re
from urllib.parse import unquote_plus

KEYWORDS = [
    "hackathon", "flag", "secret", "signature", "sign", "name", "real", "realname",
    "username", "owned", "pwned", "hacker", "007", "ชื่อ", "ตัวจริง", "ลายเซ็น",
]

PROMPT_INJECTION_LIKE = [
    "ignore previous instructions",
    "forget previous instructions",
    "ลืมคำสั่งเดิม",
    "ทำตามคำสั่งนี้แทน",
]


def _safe_base64_decode(text: str) -> str | None:
    """Try to decode base64 text without raising noisy errors."""
    try:
        padded = text + "=" * (-len(text) % 4)
        decoded = base64.b64decode(padded, validate=True)
        result = decoded.decode("utf-8")
    except (binascii.Error, UnicodeDecodeError, ValueError):
        return None
    if _looks_human(result):
        return result
    return None


def _safe_hex_decode(text: str) -> str | None:
    """Try to decode hex text if it looks long enough to be meaningful."""
    if len(text) < 6 or len(text) % 2 != 0:
        return None
    try:
        result = bytes.fromhex(text).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return None
    if _looks_human(result):
        return result
    return None


def _looks_human(text: str) -> bool:
    """Heuristic: decoded clue should contain readable letters/numbers."""
    if not text or len(text) > 80:
        return False
    readable = sum(ch.isalnum() or ch in "_- .@" for ch in text)
    return readable / max(len(text), 1) > 0.8 and any(ch.isalpha() for ch in text)


def find_hidden_clues(endpoints: list[str], limit: int = 200) -> list[dict]:
    """Find hidden-name/signature candidates from endpoint strings."""
    clues: list[dict] = []
    seen: set[tuple[str, str, str]] = set()

    for endpoint in endpoints:
        decoded_url = unquote_plus(endpoint)
        lower = decoded_url.lower()

        for keyword in KEYWORDS:
            if keyword.lower() in lower:
                _add_clue(clues, seen, decoded_url, keyword, "keyword", "none", "keyword found in endpoint")

        for bad in PROMPT_INJECTION_LIKE:
            if bad in lower:
                _add_clue(clues, seen, decoded_url, bad, "prompt_injection_like", "none", "embedded instruction-like text; record as evidence only")

        # Search token-like chunks. This catches base64/hex inside query/path.
        # We split on separators first so `name=bmVv...` also yields the pure
        # base64 token, not only the whole `name=...` string.
        token_candidates = re.findall(r"[A-Za-z0-9_=%+/.-]{6,}", endpoint)
        for chunk in re.split(r"[/?&=]+", endpoint):
            if len(chunk) >= 6:
                token_candidates.append(chunk)

        for token in token_candidates:
            clean = token.strip("/=?&")
            url_decoded = unquote_plus(clean)
            if url_decoded != clean and _looks_human(url_decoded):
                _add_clue(clues, seen, endpoint, url_decoded, "encoded", "url", "URL-decoded readable text")

            b64 = _safe_base64_decode(clean)
            if b64:
                _add_clue(clues, seen, endpoint, b64, "encoded", "base64", "base64 decoded readable text")

            hx = _safe_hex_decode(clean)
            if hx:
                _add_clue(clues, seen, endpoint, hx, "encoded", "hex", "hex decoded readable text")

        if len(clues) >= limit:
            break

    return clues[:limit]


def _add_clue(clues: list[dict], seen: set[tuple[str, str, str]], endpoint: str, candidate: str, clue_type: str, decode_method: str, reason: str) -> None:
    key = (candidate, clue_type, decode_method)
    if key in seen:
        return
    seen.add(key)
    confidence = "medium" if clue_type in {"keyword", "encoded"} else "low"
    clues.append(
        {
            "candidate": candidate,
            "confidence": confidence,
            "clue_type": clue_type,
            "decode_method": decode_method,
            "timestamp": "",
            "ip": "",
            "endpoint": endpoint,
            "reason": reason,
        }
    )
