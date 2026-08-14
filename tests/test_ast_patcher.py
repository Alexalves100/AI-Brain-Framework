"""
Unit Tests for ASTPatcher
Version: 1.0.0
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.patchers.ast_patcher import ASTPatcher

SAMPLE_CLASS_CODE = """class PaymentService:
    def __init__(self, gateway):
        self.gateway = gateway

    def process_payment(self, amount, card_token):
        # Old processing logic
        return self.gateway.charge(amount, card_token)

    def refund_payment(self, transaction_id):
        return self.gateway.refund(transaction_id)
"""


class TestASTPatcher(unittest.TestCase):
    def setUp(self):
        self.patcher = ASTPatcher()

    def test_find_symbol_range(self):
        found, start, end = self.patcher.find_symbol_range(SAMPLE_CLASS_CODE, "PaymentService.process_payment")
        self.assertTrue(found)
        self.assertEqual(start, 5)
        self.assertEqual(end, 7)

    def test_replace_method_surgically(self):
        new_method = """    def process_payment(self, amount, card_token):
        # New secure processing logic with validation
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return self.gateway.charge_secure(amount, card_token)"""

        success, mod_code, err = self.patcher.replace_symbol(
            SAMPLE_CLASS_CODE,
            "PaymentService.process_payment",
            new_method,
        )
        self.assertTrue(success)
        self.assertIsNone(err)
        self.assertIn("charge_secure", mod_code)
        self.assertIn("def refund_payment", mod_code)
        self.assertIn("class PaymentService:", mod_code)

    def test_replace_non_existent_symbol(self):
        success, mod_code, err = self.patcher.replace_symbol(
            SAMPLE_CLASS_CODE,
            "PaymentService.non_existent_method",
            "def foo(): pass",
        )
        self.assertFalse(success)
        self.assertIn("not found", err)


if __name__ == "__main__":
    unittest.main()
