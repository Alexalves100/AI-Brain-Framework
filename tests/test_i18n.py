"""Tests for i18n module."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.core import I18n


class TestI18n(unittest.TestCase):
    def test_default_locale(self):
        i18n = I18n()
        self.assertEqual(i18n.locale, "en")

    def test_translate_english(self):
        i18n = I18n(locale="en")
        msg = i18n.t("skill.not_found", name="brain")
        self.assertIn("brain", msg)
        self.assertIn("not found", msg.lower())

    def test_translate_portuguese(self):
        i18n = I18n(locale="pt-BR")
        msg = i18n.t("skill.not_found", name="brain")
        self.assertIn("brain", msg)
        self.assertIn("não encontrada", msg.lower())

    def test_fallback_to_english(self):
        i18n = I18n(locale="pt-BR")
        msg = i18n.t("validation.invalid_email")
        self.assertIn("email", msg.lower())

    def test_unknown_key_returns_key(self):
        i18n = I18n()
        self.assertEqual(i18n.t("unknown.key"), "unknown.key")

    def test_set_locale(self):
        i18n = I18n()
        i18n.set_locale("pt-BR")
        self.assertEqual(i18n.locale, "pt-BR")

    def test_invalid_locale_falls_back(self):
        i18n = I18n(locale="invalid")
        self.assertEqual(i18n.locale, "en")

    def test_available_locales(self):
        locales = I18n.available_locales()
        self.assertIn("en", locales)
        self.assertIn("pt-BR", locales)


if __name__ == "__main__":
    unittest.main()
