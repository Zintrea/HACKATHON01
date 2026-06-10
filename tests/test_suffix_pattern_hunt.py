import csv
import tempfile
import unittest
from pathlib import Path

from suffix_pattern_hunt import base_endpoint, detect_suffix, analyze_suffix_patterns


class TestSuffixPatternHunt(unittest.TestCase):
    def test_detect_suffix_after_known_base_endpoint(self):
        self.assertEqual(base_endpoint("/cart_"), "/cart")
        self.assertEqual(detect_suffix("/cart_"), "_")
        self.assertEqual(base_endpoint("/searchE"), "/search")
        self.assertEqual(detect_suffix("/searchE"), "E")
        self.assertEqual(base_endpoint("/indexE.html"), "/index.html")
        self.assertEqual(detect_suffix("/indexE.html"), "E")
        self.assertEqual(base_endpoint("/api/v1/userA"), "/api/v1/user")
        self.assertEqual(detect_suffix("/api/v1/userA"), "A")
        self.assertIsNone(detect_suffix("/cart"))

    def test_analyze_suffix_patterns_orders_suffixes_and_phrase(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            endpoint_file = out / "endpoint_summary.csv"
            with endpoint_file.open("w", newline="", encoding="utf-8") as f:
                fields = ["endpoint", "total_requests", "unique_ips", "status_200", "status_302", "status_304", "status_401", "status_403", "status_404", "status_500", "status_504", "status_5xx", "payload_hits", "attack_type"]
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows([
                    {"endpoint": "/cart_", "total_requests": "10", "unique_ips": "2", "status_200": "0", "status_302": "0", "status_304": "0", "status_401": "0", "status_403": "0", "status_404": "0", "status_500": "5", "status_504": "5", "status_5xx": "10", "payload_hits": "0", "attack_type": "server_error"},
                    {"endpoint": "/searchE", "total_requests": "9", "unique_ips": "2", "status_200": "0", "status_302": "0", "status_304": "0", "status_401": "0", "status_403": "0", "status_404": "0", "status_500": "9", "status_504": "0", "status_5xx": "9", "payload_hits": "0", "attack_type": "server_error"},
                    {"endpoint": "/productsA", "total_requests": "8", "unique_ips": "2", "status_200": "0", "status_302": "0", "status_304": "0", "status_401": "0", "status_403": "0", "status_404": "0", "status_500": "8", "status_504": "0", "status_5xx": "8", "payload_hits": "0", "attack_type": "server_error"},
                    {"endpoint": "/cart", "total_requests": "100", "unique_ips": "90", "status_200": "90", "status_302": "0", "status_304": "5", "status_401": "0", "status_403": "0", "status_404": "5", "status_500": "0", "status_504": "0", "status_5xx": "0", "payload_hits": "0", "attack_type": "normal"},
                ])
            result = analyze_suffix_patterns(endpoint_file)

            self.assertEqual(result["ordered_suffixes"], ["_", "E", "A"])
            self.assertEqual(result["joined_suffixes"], "_EA")
            self.assertEqual(result["suffix_rows"][0]["suffix"], "_")
            self.assertEqual(result["suffix_rows"][0]["total_5xx"], 10)


if __name__ == "__main__":
    unittest.main()
