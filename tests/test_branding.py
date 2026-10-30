"""Branding references: README must point at files that actually exist.
PNGs are checked by path only (they are uploaded via web upload, not
created by tests); text captures must exist on disk."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestBranding(unittest.TestCase):
    def test_readme_answers_agent_phone_plainly(self):
        text = (ROOT / "README.md").read_text()
        self.assertIn("agent-phone / cold-caller", text)
        self.assertIn("agent-phone / cold-caller", text)

    def test_readme_badges(self):
        text = (ROOT / "README.md").read_text()
        for badge in ("Python-3.10", "License-MIT", "Local--first", "Tests-51%20passing", "Status-v1.1", "Dialer-gated"):
            self.assertIn(badge, text, badge)

    def test_referenced_assets_exist(self):
        for rel in ("docs/assets/hero.png", "docs/assets/icon.png",
                    "docs/assets/favicon.png", "docs/assets/workflow.png",
                    "docs/assets/architecture.png"):
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_screenshot_txt_captures_exist(self):
        for rel in ("docs/screenshots/status-leads.txt",
                    "docs/screenshots/scrub-dialprep.txt",
                    "docs/screenshots/qualify-book-packet.txt"):
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_screenshot_pngs_exist(self):
        for rel in ("docs/screenshots/status-leads.png",
                    "docs/screenshots/scrub-dialprep.png",
                    "docs/screenshots/qualify-book-packet.png"):
            self.assertTrue((ROOT / rel).exists(), rel)


if __name__ == "__main__":
    unittest.main()
