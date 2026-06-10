import json
import unittest
from pathlib import Path


class TestStaticDashboard(unittest.TestCase):
    def test_dashboard_files_exist_and_data_is_embedded(self):
        root = Path(__file__).resolve().parents[1]
        dashboard = root / "dashboard"

        self.assertTrue((dashboard / "index.html").exists())
        self.assertTrue((dashboard / "styles.css").exists())
        self.assertTrue((dashboard / "app.js").exists())
        self.assertTrue((dashboard / "data.js").exists())

        html = (dashboard / "index.html").read_text(encoding="utf-8")
        self.assertIn("data.js", html)
        self.assertIn("app.js", html)

        data_text = (dashboard / "data.js").read_text(encoding="utf-8")
        prefix = "window.H1_DASHBOARD_DATA = "
        self.assertTrue(data_text.startswith(prefix))
        data = json.loads(data_text[len(prefix):].rstrip().rstrip(";"))
        self.assertIn("overview", data)
        self.assertIn("attackers", data)
        self.assertNotIn("suffixes", data)
        self.assertGreaterEqual(len(data["attackers"]), 1)
        self.assertNotIn("suffix_sequence", data["overview"])

        app = (dashboard / "app.js").read_text(encoding="utf-8")
        html = (dashboard / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("Suffix clue", app)
        self.assertNotIn("renderSuffixes", app)
        self.assertNotIn("Ordered endpoint suffixes", app)
        self.assertNotIn("Suffix pattern sequence", html)


if __name__ == "__main__":
    unittest.main()
