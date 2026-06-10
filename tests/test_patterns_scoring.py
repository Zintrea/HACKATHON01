import unittest
from h1_analyzer.models import LogRequest
from h1_analyzer.patterns import detect_request_flags
from h1_analyzer.scoring import score_request, classify_ip_score
from datetime import datetime


def req(endpoint, status=200):
    return LogRequest(
        line_number=1,
        raw="raw",
        timestamp=datetime(2024, 6, 10, 5, 0, 0),
        minute="2024-06-10 05:00",
        ip="6.6.6.6",
        method="GET",
        endpoint=endpoint,
        status=status,
        size=10,
    )


class TestPatternsAndScoring(unittest.TestCase):
    def test_detects_malicious_payloads_and_sensitive_endpoints(self):
        flags = detect_request_flags(req("/search?q=' UNION SELECT password FROM users--", 500))
        self.assertIn("sqli", flags)
        self.assertIn("server_error", flags)

        flags = detect_request_flags(req("/download?file=../../../../etc/passwd", 404))
        self.assertIn("path_traversal", flags)
        self.assertIn("not_found", flags)

        flags = detect_request_flags(req("/.env", 403))
        self.assertIn("sensitive_endpoint", flags)
        self.assertIn("forbidden_or_unauthorized", flags)

    def test_scores_request_with_reasons(self):
        result = score_request(req("/admin?q=<script>alert(1)</script>", 500))
        self.assertGreaterEqual(result.score, 12)
        self.assertIn("xss", result.reasons)
        self.assertIn("sensitive_endpoint", result.reasons)
        self.assertIn("server_error", result.reasons)

    def test_classifies_ip_score_in_explainable_buckets(self):
        self.assertEqual(classify_ip_score(0), "normal")
        self.assertEqual(classify_ip_score(4), "suspicious")
        self.assertEqual(classify_ip_score(9), "likely_attacker")
        self.assertEqual(classify_ip_score(15), "high_confidence_attacker")
