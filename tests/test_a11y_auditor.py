"""
Unit Tests for A11yAuditor (WCAG 2.1 AA, Clean CSS & Anti-AI Clichés)
Version: 1.0.0
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.frontend.a11y_auditor import A11yAuditor


class TestA11yAuditor(unittest.TestCase):
    def setUp(self):
        self.auditor = A11yAuditor()

    def test_clean_accessible_code(self):
        code = """
        <button aria-label="Fechar Modal">
          <svg aria-hidden="true"></svg>
        </button>
        <img src="logo.png" alt="Logotipo da Empresa" />
        <h1>Título Principal</h1>
        <h2>Subtítulo</h2>
        """
        res = self.auditor.audit(code)
        self.assertTrue(res.passed)
        self.assertEqual(res.total_violations, 0)
        self.assertEqual(res.score, 100)

    def test_detect_image_missing_alt(self):
        code = '<img src="foto.jpg" class="rounded" />'
        res = self.auditor.audit(code)
        self.assertFalse(res.passed)
        rule_ids = [v.rule_id for v in res.violations]
        self.assertIn("WCAG_IMG_ALT_MISSING", rule_ids)

    def test_detect_icon_button_no_label(self):
        code = '<button class="p-2"><svg></svg></button>'
        res = self.auditor.audit(code)
        self.assertFalse(res.passed)
        rule_ids = [v.rule_id for v in res.violations]
        self.assertIn("WCAG_BUTTON_NO_LABEL", rule_ids)

    def test_detect_heading_hierarchy_jump(self):
        code = "<h1>Header 1</h1><h3>Header 3</h3>"
        res = self.auditor.audit(code)
        rule_ids = [v.rule_id for v in res.violations]
        self.assertIn("WCAG_HEADING_HIERARCHY_JUMP", rule_ids)

    def test_detect_z_index_hell(self):
        code = ".modal { z-index: 99999; }"
        res = self.auditor.audit(code)
        rule_ids = [v.rule_id for v in res.violations]
        self.assertIn("CSS_Z_INDEX_HELL", rule_ids)

    def test_detect_ai_cliche_purple_on_dark(self):
        code = '<div class="bg-black text-white"><button class="bg-purple-600">Click</button></div>'
        res = self.auditor.audit(code)
        cliche_ids = [w.rule_id for w in res.ai_cliche_warnings]
        self.assertIn("AI_CLICHE_PURPLE_DARK", cliche_ids)


if __name__ == "__main__":
    unittest.main()
