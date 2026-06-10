"""Aggregation: request clues -> IP behavior + timeline metrics.

This is the heart of the story. It turns millions of rows into teachable tables:
- Who behaved suspiciously?
- When did traffic/errors spike?
- Which endpoints/patterns appeared?
"""
from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, List

from .models import IpStats, LogRequest
from .patterns import attack_type_from_flags, detect_request_flags
from .scoring import classify_ip_score, score_request


class AnalysisState:
    """Mutable accumulator for one streaming pass over the log file.

    We intentionally keep only aggregates and small evidence samples. This keeps
    memory usage safe for a ~1.4GB log.
    """

    def __init__(self, max_evidence_per_ip: int = 5, max_global_evidence: int | None = None):
        self.max_evidence_per_ip = max_evidence_per_ip
        self.total_lines = 0
        self.parsed_lines = 0
        self.malformed_lines = 0
        self.status_counts: Counter[int] = Counter()
        self.method_counts: Counter[str] = Counter()
        self.ip_stats: Dict[str, IpStats] = {}
        self.timeline: Dict[str, dict] = {}
        self.endpoint_stats: Dict[str, dict] = {}
        self.all_suspicious_evidence: List[dict] = []
        # Keep global evidence compact during tests and readable in reports.
        # If caller does not specify a global cap, mirror the per-IP cap. The
        # full runner sets a larger global cap while keeping per-IP examples low.
        self.max_global_evidence = max_global_evidence if max_global_evidence is not None else max_evidence_per_ip
        self.endpoints_for_hidden_scan: Counter[str] = Counter()
        self.unique_ips_seen: set[str] = set()  # debug/sample overview only; full run avoids storing normal IPs

    def add_malformed(self) -> None:
        """Record a malformed line without stopping the analysis."""
        self.total_lines += 1
        self.malformed_lines += 1

    def add_request(self, request: LogRequest) -> None:
        """Add one parsed request to all aggregate views."""
        self.total_lines += 1
        self.parsed_lines += 1
        self.status_counts[request.status] += 1
        self.method_counts[request.method] += 1
        # Keep exact unique IP count only for small/debug runs. For full logs with
        # millions of one-off normal IPs, storing every normal IP is expensive and
        # not needed for attacker evidence.
        if self.parsed_lines <= 1_000_000:
            self.unique_ips_seen.add(request.ip)

        flags = detect_request_flags(request)
        request_score = score_request(request)
        # A plain 404 is only a weak clue. Treat a request as timeline/evidence
        # suspicious only when multiple/strong red flags combine to score >= 3
        # (e.g., sensitive endpoint, payload, or server error).
        is_suspicious = request_score.score >= 3
        attack_type = attack_type_from_flags(flags)

        if request_score.score > 0:
            self._update_ip_stats(request, flags, request_score.score)
        self._update_timeline(request, flags, is_suspicious)
        # Endpoint summary should be a true endpoint overview, not only an
        # attack-only view. Bai caught this: normal `/cart` had 200/304/404 in
        # raw log but disappeared from endpoint_summary. Unique endpoints are
        # small (144 in H1), so tracking all endpoint status splits is safe.
        self._update_endpoint_stats(request, flags, attack_type)
        if is_suspicious or request.status >= 500:
            self.endpoints_for_hidden_scan[request.endpoint] += 1

        if is_suspicious and len(self.all_suspicious_evidence) < self.max_global_evidence:
            self.all_suspicious_evidence.append(self._evidence_row(request, request_score.score, flags))

    def _update_ip_stats(self, request: LogRequest, flags: list[str], request_score: int) -> None:
        stats = self.ip_stats.setdefault(request.ip, IpStats(ip=request.ip))
        stats.total_requests += 1
        stats.minute_counts[request.minute] = stats.minute_counts.get(request.minute, 0) + 1
        stats.request_score_total += request_score
        if not stats.first_seen:
            stats.first_seen = request.timestamp.isoformat(sep=" ")
        stats.last_seen = request.timestamp.isoformat(sep=" ")

        if request.status == 404:
            stats.status_404 += 1
        if request.status == 403:
            stats.status_403 += 1
        if request.status == 401:
            stats.status_401 += 1
        if 500 <= request.status <= 599:
            stats.status_500 += 1

        if any(flag in flags for flag in ("path_traversal", "sqli", "xss")):
            stats.payload_hits += 1
        if "sensitive_endpoint" in flags:
            stats.sensitive_hits += 1
        for flag in flags:
            stats.reasons[flag] = stats.reasons.get(flag, 0) + 1

        # Keep only a few strongest examples per IP so reports stay readable.
        if request_score > 0 and len(stats.evidence) < self.max_evidence_per_ip:
            stats.evidence.append(self._evidence_row(request, request_score, flags))

    def _update_timeline(self, request: LogRequest, flags: list[str], is_suspicious: bool) -> None:
        row = self.timeline.setdefault(
            request.minute,
            {
                "minute": request.minute,
                "total_requests": 0,
                "status_2xx": 0,
                "status_3xx": 0,
                "status_4xx": 0,
                "status_5xx": 0,
                "unique_ips_set": set(),
                "suspicious_requests": 0,
            },
        )
        row["total_requests"] += 1
        row["unique_ips_set"].add(request.ip)
        if 200 <= request.status <= 299:
            row["status_2xx"] += 1
        elif 300 <= request.status <= 399:
            row["status_3xx"] += 1
        elif 400 <= request.status <= 499:
            row["status_4xx"] += 1
        elif 500 <= request.status <= 599:
            row["status_5xx"] += 1
        if is_suspicious:
            row["suspicious_requests"] += 1

    def _update_endpoint_stats(self, request: LogRequest, flags: list[str], attack_type: str) -> None:
        row = self.endpoint_stats.setdefault(
            request.endpoint,
            {
                "endpoint": request.endpoint,
                "total_requests": 0,
                "unique_ips_set": set(),
                "status_200": 0,
                "status_302": 0,
                "status_304": 0,
                "status_401": 0,
                "status_403": 0,
                "status_404": 0,
                "status_500": 0,
                "status_504": 0,
                "status_5xx": 0,
                "payload_hits": 0,
                "attack_type": attack_type,
            },
        )
        row["total_requests"] += 1
        row["unique_ips_set"].add(request.ip)
        if request.status in {200, 302, 304, 401, 403, 404, 500, 504}:
            row[f"status_{request.status}"] += 1
        if 500 <= request.status <= 599:
            row["status_5xx"] += 1
        if any(flag in flags for flag in ("path_traversal", "sqli", "xss")):
            row["payload_hits"] += 1
        if row["attack_type"] == "normal" and attack_type != "normal":
            row["attack_type"] = attack_type

    def _ip_behavior_bonus(self, stats: IpStats) -> tuple[int, list[str]]:
        """Add IP-level behavior points beyond individual request scores."""
        bonus = 0
        reasons: list[str] = []
        if stats.status_404 >= 20:
            bonus += 5
            reasons.append("high_404_count")
        elif stats.status_404 >= 5:
            bonus += 3
            reasons.append("moderate_404_count")
        if stats.status_500 >= 5:
            bonus += 4
            reasons.append("high_500_count")
        elif stats.status_500 >= 1:
            bonus += 2
            reasons.append("has_500_error")
        if stats.peak_rpm() >= 100:
            bonus += 4
            reasons.append("high_peak_rpm")
        elif stats.peak_rpm() >= 20:
            bonus += 2
            reasons.append("moderate_peak_rpm")
        if stats.sensitive_hits >= 10:
            bonus += 3
            reasons.append("many_sensitive_hits")
        return bonus, reasons

    def attacker_rows(self) -> list[dict]:
        """Return IP rows sorted by most suspicious first."""
        rows: list[dict] = []
        for ip, stats in self.ip_stats.items():
            bonus, bonus_reasons = self._ip_behavior_bonus(stats)
            score = stats.request_score_total + bonus
            reasons = list(stats.reasons.keys()) + bonus_reasons
            rows.append(
                {
                    "ip": ip,
                    "label": classify_ip_score(score),
                    "score": score,
                    "total_requests": stats.total_requests,
                    "peak_rpm": stats.peak_rpm(),
                    "status_404": stats.status_404,
                    "status_403": stats.status_403,
                    "status_401": stats.status_401,
                    "status_500": stats.status_500,
                    "payload_hits": stats.payload_hits,
                    "sensitive_hits": stats.sensitive_hits,
                    "first_seen": stats.first_seen,
                    "last_seen": stats.last_seen,
                    "evidence_count": len(stats.evidence),
                    "reasons": ";".join(reasons),
                }
            )
        return sorted(rows, key=lambda r: (r["score"], r["total_requests"]), reverse=True)

    def timeline_rows(self) -> list[dict]:
        """Return minute-level rows with a human-readable system state."""
        rows: list[dict] = []
        for minute, row in sorted(self.timeline.items()):
            total = row["total_requests"]
            state = "normal"
            # Conservative state labels: no response-time claims, only traffic/error inference.
            if row["status_5xx"] > 0 and row["suspicious_requests"] > 0:
                state = "down_or_crashing"
            elif row["suspicious_requests"] > 0 or row["status_4xx"] > max(10, total * 0.2):
                state = "suspicious"
            if total >= 1000 and state != "down_or_crashing":
                state = "unstable"
            rows.append(
                {
                    "minute": minute,
                    "total_requests": total,
                    "status_2xx": row["status_2xx"],
                    "status_3xx": row["status_3xx"],
                    "status_4xx": row["status_4xx"],
                    "status_5xx": row["status_5xx"],
                    "unique_ips": len(row["unique_ips_set"]),
                    "suspicious_requests": row["suspicious_requests"],
                    "system_state": state,
                }
            )
        return rows

    def endpoint_rows(self, limit: int = 500) -> list[dict]:
        """Return endpoint summary sorted by suspiciousness and volume."""
        rows = []
        for row in self.endpoint_stats.values():
            rows.append(
                {
                    "endpoint": row["endpoint"],
                    "total_requests": row["total_requests"],
                    "unique_ips": len(row["unique_ips_set"]),
                    "status_200": row["status_200"],
                    "status_302": row["status_302"],
                    "status_304": row["status_304"],
                    "status_401": row["status_401"],
                    "status_403": row["status_403"],
                    "status_404": row["status_404"],
                    "status_500": row["status_500"],
                    "status_504": row["status_504"],
                    "status_5xx": row["status_5xx"],
                    "payload_hits": row["payload_hits"],
                    "attack_type": row["attack_type"],
                }
            )
        rows.sort(key=lambda r: (r["payload_hits"], r["status_5xx"], r["status_404"], r["total_requests"]), reverse=True)
        return rows[:limit]

    def evidence_rows(self) -> list[dict]:
        """Return global suspicious request samples."""
        return self.all_suspicious_evidence

    def hidden_scan_endpoints(self) -> list[str]:
        """Return endpoints worth scanning for hidden clues.

        We include all distinct endpoints seen, but sorted by rarity first because
        signatures/clues are often rare paths rather than common `/products`.
        """
        return [endpoint for endpoint, _count in self.endpoints_for_hidden_scan.most_common()[::-1]]

    @staticmethod
    def _evidence_row(request: LogRequest, score: int, flags: list[str]) -> dict:
        return {
            "line_number": request.line_number,
            "timestamp": request.timestamp.isoformat(sep=" "),
            "ip": request.ip,
            "method": request.method,
            "endpoint": request.endpoint,
            "status": request.status,
            "size": request.size,
            "score": score,
            "reasons": ";".join(flags),
        }
