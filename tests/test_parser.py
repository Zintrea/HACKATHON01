import unittest
from h1_analyzer.parser import parse_log_line


class TestParser(unittest.TestCase):
    def test_parse_valid_log_line_into_typed_request(self):
        line = "2024-06-10 04:17:43 | 39.3.141.152 | POST | /checkout | 200 | 122"

        req = parse_log_line(line, line_number=7)

        self.assertEqual(req.line_number, 7)
        self.assertEqual(req.timestamp.isoformat(sep=" "), "2024-06-10 04:17:43")
        self.assertEqual(req.minute, "2024-06-10 04:17")
        self.assertEqual(req.ip, "39.3.141.152")
        self.assertEqual(req.method, "POST")
        self.assertEqual(req.endpoint, "/checkout")
        self.assertEqual(req.status, 200)
        self.assertEqual(req.latency_ms, 122)
        self.assertFalse(hasattr(req, "size"))

    def test_malformed_line_returns_none_instead_of_crashing(self):
        self.assertIsNone(parse_log_line("not a real access log", line_number=1))
