"""Tests for new engines: knowledge, reasoning, discovery."""

import sys
import unittest
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.core import Context, SkillStatus
from framework.engines import KnowledgeEngine, ReasoningEngine, DiscoveryEngine


class TestKnowledgeEngine(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.engine = KnowledgeEngine(path=self.tmp.name)

    def tearDown(self):
        Path(self.tmp.name).unlink(missing_ok=True)

    def test_add_and_get(self):
        ctx = Context()
        ctx.set("action", "add")
        ctx.set("key", "csrf")
        ctx.set("content", "Cross-Site Request Forgery mitigation requires tokens")
        ctx.set("source", "OWASP")
        r = self.engine.run(ctx)
        self.assertEqual(r.status, SkillStatus.SUCCESS)

        ctx2 = Context()
        ctx2.set("action", "get")
        ctx2.set("key", "csrf")
        r2 = self.engine.run(ctx2)
        self.assertEqual(r2.output["entry"]["content"][:10], "Cross-Site")

    def test_search(self):
        ctx = Context()
        ctx.set("action", "add")
        ctx.set("key", "xss")
        ctx.set("content", "Cross-Site Scripting prevention requires output encoding")
        self.engine.run(ctx)

        ctx2 = Context()
        ctx2.set("action", "search")
        ctx2.set("query", "scripting")
        r = self.engine.run(ctx2)
        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertGreater(r.output["count"], 0)


class TestReasoningEngine(unittest.TestCase):
    def test_valid_chain(self):
        ctx = Context()
        ctx.set("premises", [
            "All users have email",
            "Alice is a user",
        ])
        ctx.set("conclusion", "Alice has email")
        r = ReasoningEngine().run(ctx)
        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertTrue(r.output["valid"])

    def test_empty_input_skipped(self):
        r = ReasoningEngine().run(Context())
        self.assertEqual(r.status, SkillStatus.SKIPPED)


class TestDiscoveryEngine(unittest.TestCase):
    def test_scan_directory(self):
        ctx = Context()
        ctx.set("path", str(ROOT / "framework"))
        ctx.set("pattern", "python")
        r = DiscoveryEngine().run(ctx)
        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertGreater(r.output["total_files"], 0)

    def test_invalid_path(self):
        ctx = Context()
        ctx.set("path", "/nonexistent/path/xyz")
        r = DiscoveryEngine().run(ctx)
        self.assertEqual(r.status, SkillStatus.ERROR)


if __name__ == "__main__":
    unittest.main()
