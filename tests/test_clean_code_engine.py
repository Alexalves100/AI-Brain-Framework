"""
Tests for CleanCodeEngine.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.core import Context, SkillStatus
from framework.engines.clean_code import CleanCodeEngine

SAMPLE_CLEAN = '''"""Clean Module."""
from typing import List

def get_active_users(users: List[dict]) -> List[dict]:
    """Filter active users."""
    if not users:
        return []
    return [u for u in users if u.get("active")]
'''

SAMPLE_DIRTY = '''
# FIXME unfinished logic
def dirty_func(a, b, c, d, e):
    if a:
        if b:
            return 1
    return 0
'''


class TestCleanCodeEngine(unittest.TestCase):
    def setUp(self):
        self.engine = CleanCodeEngine()

    def test_clean_code_audit(self):
        ctx = Context()
        ctx.set("code", SAMPLE_CLEAN)
        r = self.engine.run(ctx)

        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertTrue(r.output["is_senior_standard"])
        self.assertGreaterEqual(r.output["score"], 90)
        self.assertEqual(r.output["total_smells"], 0)
        self.assertIsNone(r.output["refactor_instruction"])

    def test_dirty_code_triggers_self_healing_instruction(self):
        ctx = Context()
        ctx.set("code", SAMPLE_DIRTY)
        r = self.engine.run(ctx)

        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertFalse(r.output["is_senior_standard"])
        self.assertLess(r.output["score"], 90)
        self.assertGreater(r.output["total_smells"], 0)
        self.assertIsNotNone(r.output["refactor_instruction"])
        self.assertIn("REFACTORING", r.output["refactor_instruction"])

    def test_system_prompt_action(self):
        ctx = Context()
        ctx.set("action", "system_prompt")
        r = self.engine.run(ctx)

        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertIn("MANDATORY ARCHITECTURAL", r.output["system_prompt"])

    def test_empty_code_skipped(self):
        ctx = Context()
        r = self.engine.run(ctx)
        self.assertEqual(r.status, SkillStatus.SKIPPED)


if __name__ == "__main__":
    unittest.main()
