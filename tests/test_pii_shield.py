"""
Unit Tests for PIIShield (LGPD, Deterministic CPF & Luhn Verification)
Version: 1.0.0
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.guardrails.pii_shield import PIIShield


class TestPIIShield(unittest.TestCase):
    def setUp(self):
        self.shield = PIIShield()

    def test_valid_cpf(self):
        # Known valid CPF (example algorithmically valid test sequence)
        # Using a valid CPF generator logic: 11144477735 is mathematically valid
        self.assertTrue(self.shield.validate_cpf("11144477735"))
        self.assertTrue(self.shield.validate_cpf("111.444.777-35"))

        # Invalid CPFs
        self.assertFalse(self.shield.validate_cpf("11111111111"))
        self.assertFalse(self.shield.validate_cpf("12345678900"))

    def test_luhn_credit_card(self):
        # Known valid 16-digit test card: 4532015112830366
        self.assertTrue(self.shield.validate_luhn("4532015112830366"))
        self.assertTrue(self.shield.validate_luhn("4532-0151-1283-0366"))
        self.assertFalse(self.shield.validate_luhn("4532015112830367"))

    def test_scan_and_anonymize(self):
        text = (
            "Cliente João, email: joao.silva@empresa.com.br, CPF: 111.444.777-35, "
            "Cartão: 4532-0151-1283-0366, Chave OpenAI: sk-1234567890abcdef1234567890abcdef."
        )
        scan_res = self.shield.scan(text)
        self.assertTrue(scan_res["has_pii"])
        self.assertEqual(scan_res["total_entities"], 4)


        anonymized = self.shield.anonymize(text, mask_type="tag")
        self.assertIn("[REDACTED_EMAIL]", anonymized)
        self.assertIn("[REDACTED_CPF]", anonymized)
        self.assertIn("[REDACTED_CREDIT_CARD]", anonymized)
        self.assertIn("[REDACTED_OPENAI_KEY]", anonymized)
        self.assertNotIn("joao.silva@empresa.com.br", anonymized)
        self.assertNotIn("111.444.777-35", anonymized)


if __name__ == "__main__":
    unittest.main()
