"""
Unit Tests for DesignTokens & Fluid Typography Calculation
Version: 1.0.0
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.frontend.design_tokens import DesignTokens


class TestDesignTokens(unittest.TestCase):
    def setUp(self):
        self.tokens = DesignTokens()

    def test_calculate_clamp(self):
        clamp_str = self.tokens.calculate_clamp(1.5, 2.5, min_vw_px=320, max_vw_px=1280)
        self.assertTrue(clamp_str.startswith("clamp("))
        self.assertIn("1.500rem", clamp_str)
        self.assertIn("2.500rem", clamp_str)
        self.assertIn("vw", clamp_str)

    def test_generate_css_variables_warm_slate(self):
        css = self.tokens.generate_css_variables("warm_slate")
        self.assertIn("--background:", css)
        self.assertIn("--primary:", css)
        self.assertIn("--ease-spring:", css)
        self.assertIn(":focus-visible", css)

    def test_themes_structure(self):
        self.assertIn("warm_slate", self.tokens.THEMES)
        self.assertIn("editorial", self.tokens.THEMES)
        self.assertIn("tactile_clean", self.tokens.THEMES)


if __name__ == "__main__":
    unittest.main()
