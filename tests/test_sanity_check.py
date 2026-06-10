import csv
import json
import tempfile
import unittest
from pathlib import Path

from sanity_check import run_sanity_checks


class TestSanityCheck(unittest.TestCase):
    def write_csv(self, path, fieldnames, rows):
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def make_minimal_output(self, base: Path):
        base.mkdir(parents=True, exist_ok=True)
        self.write_csv(
            base / "attacker_ips.csv",
            ["ip", "label", "score", "total_requests", "peak_rpm", "status_404", "status_403", "status_401", "status_500", "payload_hits", "sensitive_hits", "first_seen", "last_seen", "evidence_count", "reasons"],
            [{"ip": "9.9.9.9", "label": "high_confidence_attacker", "score": "13", "total_requests": "10", "peak_rpm": "5", "status_404": "0", "status_403": "0", "status_401": "0", "status_500": "10", "payload_hits": "0", "sensitive_hits": "1", "first_seen": "2024-01-01 00:00:00", "last_seen": "2024-01-01 00:01:00", "evidence_count": "1", "reasons": "server_error"}],
        )
        self.write_csv(
            base / "endpoint_summary.csv",
            ["endpoint", "total_requests", "unique_ips", "status_200", "status_302", "status_304", "status_401", "status_403", "status_404", "status_500", "status_504", "status_5xx", "payload_hits", "attack_type"],
            [
                {"endpoint": "/cart", "total_requests": "3", "unique_ips": "3", "status_200": "1", "status_302": "0", "status_304": "1", "status_401": "0", "status_403": "0", "status_404": "1", "status_500": "0", "status_504": "0", "status_5xx": "0", "payload_hits": "0", "attack_type": "normal"},
                {"endpoint": "/cart_", "total_requests": "2", "unique_ips": "1", "status_200": "0", "status_302": "0", "status_304": "0", "status_401": "0", "status_403": "0", "status_404": "0", "status_500": "1", "status_504": "1", "status_5xx": "2", "payload_hits": "0", "attack_type": "server_error"},
            ],
        )
        self.write_csv(
            base / "incident_windows.csv",
            ["start_time", "end_time", "states_seen", "peak_requests", "peak_5xx", "peak_p95_latency_ms", "total_suspicious_requests", "reason"],
            [{"start_time": "2024-01-01 00:00", "end_time": "2024-01-01 00:01", "states_seen": "down_or_crashing", "peak_requests": "10", "peak_5xx": "2", "peak_p95_latency_ms": "1200", "total_suspicious_requests": "2", "reason": "test"}],
        )
        self.write_csv(
            base / "suspicious_requests.csv",
            ["line_number", "timestamp", "ip", "method", "endpoint", "status", "latency_ms", "score", "reasons"],
            [{"line_number": "1", "timestamp": "2024-01-01 00:00:00", "ip": "9.9.9.9", "method": "GET", "endpoint": "/cart_", "status": "500", "latency_ms": "10", "score": "4", "reasons": "server_error"}],
        )
        self.write_csv(
            base / "traffic_timeline.csv",
            ["minute", "total_requests", "status_2xx", "status_3xx", "status_4xx", "status_5xx", "unique_ips", "suspicious_requests", "avg_latency_ms", "p95_latency_ms", "max_latency_ms", "system_state"],
            [{"minute": "2024-01-01 00:00", "total_requests": "5", "status_2xx": "1", "status_3xx": "1", "status_4xx": "1", "status_5xx": "2", "unique_ips": "4", "suspicious_requests": "2", "avg_latency_ms": "500", "p95_latency_ms": "1200", "max_latency_ms": "1500", "system_state": "down_or_crashing"}],
        )
        self.write_csv(
            base / "hidden_bonus_candidates.csv",
            ["candidate", "confidence", "clue_type", "decode_method", "timestamp", "ip", "endpoint", "reason"],
            [],
        )
        (base / "dashboard_data.json").write_text(json.dumps({"overview": {}, "attackers": [], "timeline": [], "incidents": [], "endpoints": [], "evidence": [], "hidden_bonus": []}), encoding="utf-8")
        (base / "h1_summary.md").write_text("# summary", encoding="utf-8")

    def test_sanity_check_passes_for_valid_output_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "output"
            self.make_minimal_output(out)

            result = run_sanity_checks(out)

            self.assertTrue(result.ok)
            self.assertEqual(result.errors, [])
            self.assertTrue(any("/cart and /cart_ are separated" in msg for msg in result.warnings + result.infos))

    def test_sanity_check_fails_when_endpoint_status_columns_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "output"
            self.make_minimal_output(out)
            # Simulate the earlier bug: endpoint summary without normal status columns.
            self.write_csv(
                out / "endpoint_summary.csv",
                ["endpoint", "total_requests", "unique_ips", "status_404", "status_500", "payload_hits", "attack_type"],
                [{"endpoint": "/cart_", "total_requests": "2", "unique_ips": "1", "status_404": "0", "status_500": "2", "payload_hits": "0", "attack_type": "server_error"}],
            )

            result = run_sanity_checks(out)

            self.assertFalse(result.ok)
            self.assertTrue(any("endpoint_summary.csv missing columns" in err for err in result.errors))


if __name__ == "__main__":
    unittest.main()
