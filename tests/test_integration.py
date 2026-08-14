"""Integration tests for end-to-end workflows."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework import (
    Context,
    SkillStatus,
    create_default_orchestrator,
)
from framework.core import MetricsCollector
from framework.standards import RateLimiter


class TestFullPipeline(unittest.TestCase):
    def test_brain_security_token_economy(self):
        orch = create_default_orchestrator()
        ctx = Context()
        ctx.set("query", "how to fix sql injection vulnerability")
        ctx.set("code", "execute('SELECT * FROM users WHERE id=' + uid)")
        ctx.set("text", "Claro, vou ajudar. Espero que seja util.")

        results = orch.run_pipeline(
            ["brain", "security", "token_economy"], ctx
        )

        self.assertEqual(len(results), 3)
        self.assertTrue(all(r.status == SkillStatus.SUCCESS for r in results))
        self.assertEqual(results[0].output["routed_to"], "security")
        self.assertGreater(results[1].output["total"], 0)
        self.assertGreater(results[2].output["saved"], 0)

    def test_all_engines_registered(self):
        orch = create_default_orchestrator()
        names = [s.name for s in orch.registry.list()]
        self.assertEqual(len(names), 11)
        self.assertIn("brain", names)
        self.assertIn("security", names)
        self.assertIn("token_economy", names)
        self.assertIn("memory", names)
        self.assertIn("knowledge", names)
        self.assertIn("reasoning", names)
        self.assertIn("discovery", names)
        self.assertIn("ui_design", names)
        self.assertIn("prompt_shield", names)
        self.assertIn("code_patcher", names)
        self.assertIn("fullstack_ui", names)




    def test_pipeline_stops_on_error(self):
        from framework.core import Skill, SkillResult, SkillStatus

        class BrokenSkill(Skill):
            name = "broken"
            category = "test"

            def run(self, context):
                return SkillResult(status=SkillStatus.ERROR, error="boom")

        orch = create_default_orchestrator()
        orch.registry.register(BrokenSkill())
        ctx = Context()
        results = orch.run_pipeline(["brain", "broken", "security"], ctx)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[1].status, SkillStatus.ERROR)


class TestMetricsCollector(unittest.TestCase):
    def test_record_and_get(self):
        mc = MetricsCollector()
        mc.record("op", 10.5)
        mc.record("op", 20.0)
        result = mc.get("op")
        self.assertEqual(result["count"], 2)
        self.assertGreater(result["avg_ms"], 0)

    def test_measure_context_manager(self):
        mc = MetricsCollector()
        with mc.measure("ctx_op"):
            _ = sum(range(1000))
        result = mc.get("ctx_op")
        self.assertEqual(result["count"], 1)

    def test_reset(self):
        mc = MetricsCollector()
        mc.record("x", 5.0)
        mc.reset()
        self.assertEqual(mc.get("x")["count"], 0)


class TestRateLimiter(unittest.TestCase):
    def test_allows_under_limit(self):
        rl = RateLimiter(max_requests=3, window_seconds=1)
        for _ in range(3):
            allowed, remaining = rl.is_allowed("client_a")
            self.assertTrue(allowed)
        self.assertGreaterEqual(remaining, 0)

    def test_blocks_over_limit(self):
        rl = RateLimiter(max_requests=2, window_seconds=10)
        rl.is_allowed("client_b")
        rl.is_allowed("client_b")
        allowed, _ = rl.is_allowed("client_b")
        self.assertFalse(allowed)

    def test_separate_keys(self):
        rl = RateLimiter(max_requests=1, window_seconds=10)
        self.assertTrue(rl.is_allowed("k1")[0])
        self.assertTrue(rl.is_allowed("k2")[0])

    def test_reset(self):
        rl = RateLimiter(max_requests=1, window_seconds=10)
        rl.is_allowed("k")
        rl.reset("k")
        self.assertTrue(rl.is_allowed("k")[0])


class TestEndToEndWebExample(unittest.TestCase):
    def test_simple_website_imports(self):
        examples_path = ROOT / "examples" / "simple_website" / "app.py"
        self.assertTrue(examples_path.exists())
        content = examples_path.read_text(encoding="utf-8")
        self.assertIn("create_default_orchestrator", content)
        self.assertIn("SecurityHeaders", content)
        self.assertIn("InputValidator", content)


if __name__ == "__main__":
    unittest.main()
