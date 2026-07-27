"""Tests for UI Design Engine."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.core import Context, SkillStatus
from framework.engines import UIDesignEngine


class TestUIDesignEngine(unittest.TestCase):
    def test_clean_html_scores_high(self):
        html = """
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Test</title>
</head>
<body>
  <h1>Title</h1>
  <img src="x.png" alt="description">
  <div class="sm:text-sm md:text-base lg:text-lg">responsive</div>
</body>
</html>
"""
        css = """
@media (max-width: 640px) { .x { display: none; } }
@media (min-width: 1024px) { .y { display: block; } }
"""
        ctx = Context()
        ctx.set("html", html)
        ctx.set("css", css)
        result = UIDesignEngine().run(ctx)
        self.assertEqual(result.status, SkillStatus.SUCCESS)
        self.assertGreaterEqual(result.output["score"], 80)

    def test_missing_viewport_lowers_score(self):
        html = "<html><body><h1>Title</h1</body</html>"
        ctx = Context()
        ctx.set("html", html)
        ctx.set("css", "@media (max-width: 640px) {}")
        result = UIDesignEngine().run(ctx)
        findings = result.output["findings"]
        types = [f["type"] for f in findings]
        self.assertIn("responsive.no_viewport_meta", types)

    def test_image_without_alt_detected(self):
        html = '<html><head><meta name="viewport" content="width=device-width</head><body><h1>T</h1><img src="x.png</body</html>'
        ctx = Context()
        ctx.set("html", html)
        ctx.set("css", "@media (max-width: 640px) {}")
        result = UIDesignEngine().run(ctx)
        types = [f["type"] for f in result.output["findings"]]
        self.assertIn("a11y.img_missing_alt", types)

    def test_no_media_queries_detected(self):
        html = '<html><body><h1>Title</h1</body</html>'
        ctx = Context()
        ctx.set("html", html)
        ctx.set("css", ".x { color: red; }")
        result = UIDesignEngine().run(ctx)
        types = [f["type"] for f in result.output["findings"]]
        self.assertIn("responsive.no_media_queries", types)

    def test_no_heading_detected(self):
        html = '<html><body><p>No heading here</p</body</html>'
        ctx = Context()
        ctx.set("html", html)
        ctx.set("css", "@media (max-width: 640px) {}")
        result = UIDesignEngine().run(ctx)
        types = [f["type"] for f in result.output["findings"]]
        self.assertIn("semantic.no_heading", types)

    def test_empty_input_skipped(self):
        result = UIDesignEngine().run(Context())
        self.assertEqual(result.status, SkillStatus.SKIPPED)


if __name__ == "__main__":
    unittest.main()
