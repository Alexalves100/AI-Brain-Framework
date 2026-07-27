"""Tests for framework core."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.core import (
    Skill,
    SkillResult,
    SkillStatus,
    SkillRegistry,
    Context,
    Orchestrator,
)


class DummySkill(Skill):
    name = "dummy"
    version = "1.0.0"
    category = "test"

    def run(self, context):
        return SkillResult(
            status=SkillStatus.SUCCESS,
            output={"echo": context.get("input")},
        )


class FailingSkill(Skill):
    name = "failing"
    version = "1.0.0"
    category = "test"

    def run(self, context):
        return SkillResult(
            status=SkillStatus.ERROR,
            error="intentional failure",
        )


class TestSkill(unittest.TestCase):
    def test_run_returns_result(self):
        s = DummySkill()
        ctx = Context()
        ctx.set("input", "hello")
        r = s.run(ctx)
        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertEqual(r.output, {"echo": "hello"})


class TestRegistry(unittest.TestCase):
    def test_register_and_get(self):
        reg = SkillRegistry()
        reg.register(DummySkill())
        self.assertIn("dummy", reg)
        self.assertEqual(reg.get("dummy").name, "dummy")

    def test_register_duplicate_raises(self):
        reg = SkillRegistry()
        reg.register(DummySkill())
        with self.assertRaises(ValueError):
            reg.register(DummySkill())

    def test_list_by_category(self):
        reg = SkillRegistry()
        reg.register(DummySkill())
        self.assertEqual(len(reg.list(category="test")), 1)
        self.assertEqual(len(reg.list(category="other")), 0)


class TestContext(unittest.TestCase):
    def test_set_get_has(self):
        ctx = Context()
        self.assertFalse(ctx.has("x"))
        ctx.set("x", 1)
        self.assertTrue(ctx.has("x"))
        self.assertEqual(ctx.get("x"), 1)
        self.assertEqual(ctx.get("missing", "default"), "default")

    def test_tokens(self):
        ctx = Context()
        ctx.add_tokens(10)
        ctx.add_tokens(5)
        self.assertEqual(ctx.tokens_used, 15)


class TestOrchestrator(unittest.TestCase):
    def test_run_skill(self):
        reg = SkillRegistry()
        reg.register(DummySkill())
        orch = Orchestrator(reg)
        ctx = Context()
        ctx.set("input", "test")
        r = orch.run("dummy", ctx)
        self.assertEqual(r.status, SkillStatus.SUCCESS)

    def test_run_missing_skill(self):
        orch = Orchestrator()
        r = orch.run("missing", Context())
        self.assertEqual(r.status, SkillStatus.ERROR)

    def test_pipeline_stops_on_error(self):
        reg = SkillRegistry()
        reg.register(DummySkill())
        reg.register(FailingSkill())
        orch = Orchestrator(reg)
        results = orch.run_pipeline(["dummy", "failing"], Context())
        self.assertEqual(len(results), 2)
        self.assertEqual(results[1].status, SkillStatus.ERROR)


if __name__ == "__main__":
    unittest.main()
