"""
Tests for SeniorGuidelines and SeniorPromptTemplates.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.prompts import PromptBuilder, SeniorPromptTemplates
from framework.standards.senior_guidelines import SeniorGuidelines


class TestSeniorGuidelines(unittest.TestCase):
    def test_rules_list_populated(self):
        rules = SeniorGuidelines.get_rules_list()
        self.assertGreaterEqual(len(rules), 6)
        rule_ids = [r["id"] for r in rules]
        self.assertIn("SRP-001", rule_ids)
        self.assertIn("GUARD-002", rule_ids)
        self.assertIn("TYPE-003", rule_ids)

    def test_prompt_constraints(self):
        constraints = SeniorGuidelines.get_prompt_constraints()
        self.assertIsInstance(constraints, list)
        self.assertGreater(len(constraints), 4)
        text = " ".join(constraints)
        self.assertIn("SOLID", text)
        self.assertIn("Guard Clauses", text)
        self.assertIn("type hints", text)

    def test_prompt_builder_add_senior_guardrails(self):
        prompt = (
            PromptBuilder()
            .add_role("Senior Python Engineer")
            .add_senior_guardrails()
            .add_task("Create a clean authentication middleware")
            .build()
        )
        self.assertIn("You are Senior Python Engineer.", prompt)
        self.assertIn("Constraints:", prompt)
        self.assertIn("SOLID", prompt)
        self.assertIn("Task:\nCreate a clean authentication middleware", prompt)

    def test_senior_prompt_templates_self_healing(self):
        smells = [{
            "line": 15,
            "symbol": "process_data",
            "severity": "high",
            "message": "Nesting depth is 4.",
            "recommendation": "Use Guard Clauses.",
        }]
        prompt = SeniorPromptTemplates.get_self_healing_refactor_prompt(
            code="def process_data(): pass", smells=smells, score=45
        )
        self.assertIn("CURRENT CLEAN CODE SCORE: 45/100", prompt)
        self.assertIn("Nesting depth is 4.", prompt)
        self.assertIn("Use Guard Clauses.", prompt)


if __name__ == "__main__":
    unittest.main()
