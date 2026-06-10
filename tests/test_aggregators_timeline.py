import unittest
from datetime import datetime
from h1_analyzer.models import LogRequest
from h1_analyzer.aggregators import AnalysisState
from h1_analyzer.timeline import build_incident_windows


def req(ip, minute, endpoint="/products", status=200):
    ts = datetime.strptime(minute + ":00", "%Y-%m-%d %H:%M:%S")
    return LogRequest(1, "raw", ts, minute[:16], ip, "GET", endpoint, status, 100)


class TestAggregatorsTimeline(unittest.TestCase):
    def test_aggregates_ip_metrics_and_peak_rpm(self):
        state = AnalysisState(max_evidence_per_ip=3)
        for _ in range(5):
            state.add_request(req("1.1.1.1", "2024-06-10 05:00", "/.env", 404))
        state.add_request(req("1.1.1.1", "2024-06-10 05:01", "/search?q=UNION SELECT", 500))

        rows = state.attacker_rows()
        row = rows[0]
        self.assertEqual(row["ip"], "1.1.1.1")
        self.assertEqual(row["total_requests"], 6)
        self.assertEqual(row["status_404"], 5)
        self.assertEqual(row["status_500"], 1)
        self.assertEqual(row["peak_rpm"], 5)
        self.assertGreater(row["score"], 0)
        self.assertLessEqual(len(state.evidence_rows()), 3)

    def test_endpoint_summary_keeps_normal_and_error_status_columns(self):
        state = AnalysisState(max_evidence_per_ip=3)
        state.add_request(req("1.1.1.1", "2024-06-10 05:00", "/cart", 200))
        state.add_request(req("2.2.2.2", "2024-06-10 05:00", "/cart", 304))
        state.add_request(req("3.3.3.3", "2024-06-10 05:00", "/cart", 404))
        state.add_request(req("9.9.9.9", "2024-06-10 05:00", "/cart_", 500))
        state.add_request(req("9.9.9.9", "2024-06-10 05:00", "/cart_", 504))

        rows = {row["endpoint"]: row for row in state.endpoint_rows()}

        self.assertEqual(rows["/cart"]["status_200"], 1)
        self.assertEqual(rows["/cart"]["status_304"], 1)
        self.assertEqual(rows["/cart"]["status_404"], 1)
        self.assertEqual(rows["/cart"]["status_500"], 0)
        self.assertEqual(rows["/cart"]["status_504"], 0)
        self.assertEqual(rows["/cart"]["attack_type"], "normal")
        self.assertEqual(rows["/cart_"]["status_500"], 1)
        self.assertEqual(rows["/cart_"]["status_504"], 1)

    def test_builds_incident_windows_from_abnormal_minutes(self):
        timeline_rows = [
            {"minute": "2024-06-10 05:00", "total_requests": 10, "status_4xx": 0, "status_5xx": 0, "suspicious_requests": 0, "system_state": "normal"},
            {"minute": "2024-06-10 05:01", "total_requests": 200, "status_4xx": 90, "status_5xx": 0, "suspicious_requests": 50, "system_state": "suspicious"},
            {"minute": "2024-06-10 05:02", "total_requests": 300, "status_4xx": 50, "status_5xx": 40, "suspicious_requests": 60, "system_state": "down_or_crashing"},
        ]
        windows = build_incident_windows(timeline_rows)
        self.assertEqual(len(windows), 1)
        self.assertEqual(windows[0]["start_time"], "2024-06-10 05:01")
        self.assertEqual(windows[0]["end_time"], "2024-06-10 05:02")
        self.assertIn("down_or_crashing", windows[0]["states_seen"])
