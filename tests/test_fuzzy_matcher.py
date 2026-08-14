"""
Unit Tests for FuzzyMatcher
Version: 1.0.0
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.patchers.fuzzy_matcher import FuzzyMatcher

SAMPLE_FILE = """def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total

def print_receipt(order):
    print("Order ID:", order.id)
    print("Total:", order.total)
"""


class TestFuzzyMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = FuzzyMatcher()

    def test_exact_match_replace(self):
        search = """def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total"""

        replace = """def calculate_total(items):
    return sum(item.price for item in items)"""

        success, new_text, conf = self.matcher.replace_block(SAMPLE_FILE, search, replace)
        self.assertTrue(success)
        self.assertEqual(conf, 1.0)
        self.assertIn("return sum(item.price", new_text)

    def test_fuzzy_match_whitespace_tolerance(self):
        # Slightly different whitespace/indentation in search block
        search_with_spaces = (
            "  def calculate_total(items):\n"
            "      total = 0\n"
            "      for item in items:\n"
            "          total += item.price\n"
            "      return total"
        )


        replace = """def calculate_total(items):
    return sum(item.price for item in items)"""

        success, new_text, conf = self.matcher.replace_block(SAMPLE_FILE, search_with_spaces, replace)
        self.assertTrue(success)
        self.assertGreaterEqual(conf, 0.8)
        self.assertIn("return sum(item.price", new_text)

    def test_unmatched_block_returns_false(self):
        search = "def completely_unrelated_function():\n    pass"
        replace = "def replacement(): pass"
        success, new_text, conf = self.matcher.replace_block(SAMPLE_FILE, search, replace)
        self.assertFalse(success)
        self.assertEqual(new_text, SAMPLE_FILE)


if __name__ == "__main__":
    unittest.main()
