"""
Tests for CodeSmellDetector (AST-based Clean Code analysis).
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.analyzers.code_smells import CodeSmellDetector

CLEAN_CODE_SAMPLE = '''"""Pristine Senior-Level Service."""

from typing import Optional, Dict, Any

RETRY_LIMIT: int = 3

class PaymentProcessor:
    """Processes customer transactions cleanly with guard clauses."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def process(self, amount: float, currency: str) -> Dict[str, Any]:
        """Process payment using guard clauses."""
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        if not currency:
            raise ValueError("Currency is required")

        return {"status": "success", "amount": amount, "currency": currency}
'''


DIRTY_CODE_SAMPLE = '''
# TODO fix this entire function later
def bad_function(a, b, c, d, e):
    if a:
        if b:
            if c:
                if d:
                    print("debug nested")
                    return 9999
                else:
                    return 0
            else:
                return 0
        else:
            return 0
    else:
        try:
            x = 1 / 0
        except:
            pass
        return 0
'''


class TestCodeSmells(unittest.TestCase):
    def setUp(self):
        self.detector = CodeSmellDetector()

    def test_clean_code_passes_senior_standard(self):
        report = self.detector.analyze_code(CLEAN_CODE_SAMPLE, file_path="payment.py")
        self.assertTrue(report["syntax_valid"])
        self.assertTrue(report["is_senior_standard"])
        self.assertGreaterEqual(report["score"], 90)
        self.assertEqual(report["type_coverage_pct"], 100.0)

    def test_detects_nested_guard_clauses_needed(self):
        report = self.detector.analyze_code(DIRTY_CODE_SAMPLE, file_path="dirty.py")
        self.assertFalse(report["is_senior_standard"])
        self.assertLess(report["score"], 60)

        rules = [s["rule"] for s in report["smells"]]
        self.assertIn("GUARD_CLAUSES_EARLY_RETURN", rules)
        self.assertIn("ANTI_LAZY_CODE", rules)
        self.assertIn("PARAMETER_LIMIT", rules)
        self.assertIn("STRICT_TYPE_ANNOTATIONS", rules)
        self.assertIn("DEFENSIVE_ERROR_HANDLING", rules)

    def test_detects_long_function(self):
        long_func = "def very_long():\n" + "\n".join(f"    x_{i} = {i}" for i in range(40)) + "\n    return x_0\n"
        report = self.detector.analyze_code(long_func)
        rules = [s["rule"] for s in report["smells"]]
        self.assertIn("SRP_SINGLE_RESPONSIBILITY", rules)

    def test_detects_redundant_else(self):
        code_with_redundant_else = '''
def check(val: int) -> bool:
    if val > 10:
        return True
    else:
        return False
'''
        report = self.detector.analyze_code(code_with_redundant_else)
        rules = [s["rule"] for s in report["smells"]]
        self.assertIn("NO_REDUNDANT_ELSE", rules)

    def test_syntax_error_handling(self):
        broken_code = "def broken(:"
        report = self.detector.analyze_code(broken_code)
        self.assertFalse(report["syntax_valid"])
        self.assertEqual(report["score"], 0)


if __name__ == "__main__":
    unittest.main()
