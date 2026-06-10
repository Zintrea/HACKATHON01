import csv
import json
import tempfile
import unittest
from pathlib import Path
from h1_analyzer.hidden_bonus import find_hidden_clues
from h1_analyzer.runner import run_analysis


class TestHiddenReportsCli(unittest.TestCase):
    def test_hidden_bonus_decodes_url_and_base64_candidates(self):
        endpoints = [
            "/signature/%6e%65%6f",
            "/note?name=bmVvX2hhY2tlcg==",
        ]
        clues = find_hidden_clues(endpoints)
        joined = " ".join(c["candidate"] for c in clues)
        self.assertIn("neo", joined)
        self.assertIn("neo_hacker", joined)

    def test_run_analysis_writes_clear_output_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            log = tmp_path / "sample.log"
            log.write_text("\n".join([
                "2024-06-10 05:00:00 | 1.1.1.1 | GET | /products | 200 | 100",
                "2024-06-10 05:00:01 | 9.9.9.9 | GET | /.env | 404 | 20",
                "2024-06-10 05:00:02 | 9.9.9.9 | GET | /search?q=' UNION SELECT | 500 | 20",
                "2024-06-10 05:01:00 | 9.9.9.9 | GET | /signature/%6e%65%6f | 404 | 20",
            ]), encoding="utf-8")
            out = tmp_path / "out"

            summary = run_analysis(log, out, max_lines=None)

            self.assertEqual(summary["parsed_lines"], 4)
            expected = [
                "attacker_ips.csv",
                "traffic_timeline.csv",
                "incident_windows.csv",
                "endpoint_summary.csv",
                "suspicious_requests.csv",
                "hidden_bonus_candidates.csv",
                "dashboard_data.json",
                "h1_summary.md",
            ]
            for name in expected:
                self.assertTrue((out / name).exists(), name)

            with (out / "attacker_ips.csv").open(newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(rows[0]["ip"], "9.9.9.9")
            self.assertIn(rows[0]["label"], {"likely_attacker", "high_confidence_attacker"})

            with (out / "suspicious_requests.csv").open(newline="", encoding="utf-8") as f:
                suspicious_rows = list(csv.DictReader(f))
            self.assertIn("latency_ms", suspicious_rows[0])
            self.assertNotIn("size", suspicious_rows[0])

            data = json.loads((out / "dashboard_data.json").read_text(encoding="utf-8"))
            self.assertIn("overview", data)
            self.assertIn("attackers", data)
            self.assertIn("timeline", data)
            self.assertIn("Latency field present", data["overview"]["note"])
