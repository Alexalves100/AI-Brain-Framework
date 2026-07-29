import unittest
from framework.standards import CSSTokens

class TestCSSTokens(unittest.TestCase):

    def test_css_variables_generation_dark(self):
        css = CSSTokens.generate_css_variables("dark")
        self.assertIn(":root {", css)
        self.assertIn("--color-bg-primary: hsl(222, 47%, 11%);", css)
        self.assertIn("--font-sans:", css)

    def test_css_variables_generation_light(self):
        css = CSSTokens.generate_css_variables("light")
        self.assertIn("--color-bg-primary: hsl(0, 0%, 100%);", css)

    def test_google_fonts_import(self):
        fonts_import = CSSTokens.get_google_fonts_import()
        self.assertTrue(fonts_import.startswith("@import url("))
        self.assertIn("fonts.googleapis.com", fonts_import)

if __name__ == "__main__":
    unittest.main()
