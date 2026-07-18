import unittest
from pathlib import Path

from api_app import health, root


class DemoSurfaceTests(unittest.TestCase):
    def test_health_advertises_the_demo_control_plane(self):
        response = health()

        self.assertTrue(response["ok"])
        self.assertEqual(response["surface"], "demo-control-plane")
        self.assertEqual(response["web"], "/web/")

    def test_root_exposes_the_judge_routes(self):
        response = root()

        self.assertEqual(response["web"], "/web/")
        self.assertEqual(response["agent_context"], "/agent/context")

    def test_web_ui_is_served_and_uses_the_protected_chat_contract(self):
        page = (Path(__file__).resolve().parents[1] / "web_ui" / "index.html").read_text(encoding="utf-8")
        self.assertIn("NerTzh Metrics Control Plane", page)
        self.assertIn('X-Control-Token', page)
        self.assertIn("sessionStorage", page)
        self.assertIn('"/agent/context', page)
        self.assertNotIn("setInterval(", page)
        self.assertNotIn("cdn.jsdelivr.net", page)
        self.assertNotIn("Math.random", page)
        self.assertIn("persisted", page.lower())


if __name__ == "__main__":
    unittest.main()
