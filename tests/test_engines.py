"""Tests for framework engines."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.core import Context, SkillStatus
from framework.engines import (
    BrainEngine,
    SecurityEngine,
    TokenEconomyEngine,
    MemoryEngine,
)
from framework.standards import SecurityHeaders, InputValidator


class TestBrainEngine(unittest.TestCase):
    def test_routes_security_query(self):
        ctx = Context()
        ctx.set("query", "how to fix sql injection vulnerability")
        r = BrainEngine().run(ctx)
        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertEqual(r.output["routed_to"], "security")

    def test_routes_performance_query(self):
        ctx = Context()
        ctx.set("query", "the app is slow and needs cache")
        r = BrainEngine().run(ctx)
        self.assertEqual(r.output["routed_to"], "performance")

    def test_empty_query_skipped(self):
        r = BrainEngine().run(Context())
        self.assertEqual(r.status, SkillStatus.SKIPPED)


class TestSecurityEngine(unittest.TestCase):
    def test_detects_sql_injection(self):
        ctx = Context()
        ctx.set("code", 'execute("SELECT * FROM users WHERE id=" + uid)')
        r = SecurityEngine().run(ctx)
        types = [f["type"] for f in r.output["findings"]]
        self.assertIn("SQL Injection", types)

    def test_detects_eval(self):
        ctx = Context()
        ctx.set("code", "result = eval(user_input)")
        r = SecurityEngine().run(ctx)
        types = [f["type"] for f in r.output["findings"]]
        self.assertIn("Eval Usage", types)

    def test_clean_code_no_findings(self):
        ctx = Context()
        ctx.set("code", "x = 1 + 2")
        r = SecurityEngine().run(ctx)
        self.assertEqual(r.output["total"], 0)


class TestTokenEconomyEngine(unittest.TestCase):
    def test_removes_filler(self):
        ctx = Context()
        ctx.set("text", "Claro, vou ajudar com isso. Espero que seja útil.")
        r = TokenEconomyEngine().run(ctx)
        self.assertGreater(r.output["saved"], 0)

    def test_empty_text_skipped(self):
        r = TokenEconomyEngine().run(Context())
        self.assertEqual(r.status, SkillStatus.SKIPPED)


class TestMemoryEngine(unittest.TestCase):
    def test_set_and_get(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            m = MemoryEngine(path=path)
            ctx = Context()
            ctx.set("action", "set")
            ctx.set("key", "name")
            ctx.set("value", "AI-Brain")
            m.run(ctx)

            ctx2 = Context()
            ctx2.set("action", "get")
            ctx2.set("key", "name")
            r = m.run(ctx2)
            self.assertEqual(r.output["value"], "AI-Brain")
        finally:
            Path(path).unlink(missing_ok=True)


class TestSecurityHeaders(unittest.TestCase):
    def test_returns_owasp_headers(self):
        h = SecurityHeaders.get()
        self.assertEqual(h["X-Frame-Options"], "DENY")
        self.assertEqual(h["X-Content-Type-Options"], "nosniff")
        self.assertIn("Content-Security-Policy", h)


class TestInputValidator(unittest.TestCase):
    def test_email(self):
        self.assertTrue(InputValidator.email("a@b.co"))
        self.assertFalse(InputValidator.email("not-an-email"))

    def test_slug(self):
        self.assertTrue(InputValidator.slug("hello-world"))
        self.assertFalse(InputValidator.slug("Hello World"))

    def test_no_html(self):
        self.assertTrue(InputValidator.no_html("plain text"))
        self.assertFalse(InputValidator.no_html("<script>"))

    def test_sanitize(self):
        self.assertEqual(InputValidator.sanitize_text("<b>hi</b>"), "bhi/b")


if __name__ == "__main__":
    unittest.main()
