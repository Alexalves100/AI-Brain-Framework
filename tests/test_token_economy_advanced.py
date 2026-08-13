"""
Tests for TokenEconomyEngine advanced modes and Serena MCP style features.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.core import Context, SkillStatus
from framework.engines.token_economy import TokenEconomyEngine


SAMPLE_PYTHON_CODE = '''"""Sample database operations module."""

from typing import List, Dict, Any, Optional

DB_TIMEOUT: int = 15
MAX_POOL_SIZE: int = 20

class DatabaseConnection:
    """Manages database connection pool and queries."""

    def __init__(self, uri: str) -> None:
        self.uri = uri
        self._connected = True
        self._pool: List[Any] = []
        self._stats: Dict[str, int] = {"queries": 0, "errors": 0}

    def query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Executes a SQL query and returns raw rows."""
        # Simulated database query execution with validation and logging
        if not self._connected:
            raise RuntimeError("Database is disconnected")
        print(f"Executing: {sql} with {params}")
        self._stats["queries"] += 1
        rows = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        return rows

    def execute_batch(self, statements: List[str]) -> int:
        """Executes multiple statements in a transaction."""
        count = 0
        for stmt in statements:
            self.query(stmt)
            count += 1
        return count

    def close(self) -> None:
        """Closes the connection and flushes pool."""
        self._connected = False
        self._pool.clear()
'''



class TestTokenEconomyAdvanced(unittest.TestCase):
    def setUp(self):
        self.engine = TokenEconomyEngine()

    def test_legacy_conversational_text_mode(self):
        ctx = Context()
        ctx.set("text", "Olá! Claro, vou explicar como funciona. Espero que seja útil.")
        ctx.set("mode", "conversational")
        r = self.engine.run(ctx)

        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertEqual(r.output["strategy"], "conversational")
        self.assertGreater(r.output["saved"], 0)
        self.assertNotIn("Claro,", r.output["text"])

    def test_ast_skeleton_mode_high_savings(self):
        ctx = Context()
        ctx.set("code", SAMPLE_PYTHON_CODE)
        ctx.set("mode", "ast_skeleton")
        r = self.engine.run(ctx)

        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertEqual(r.output["strategy"], "ast_skeleton")
        self.assertGreater(r.output["ratio"], 0.35)
        self.assertGreater(r.output["saved"], 200)

        # Ensure skeleton contains class and method signatures
        self.assertIn("class DatabaseConnection:", r.output["text"])
        self.assertIn("def query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:", r.output["text"])
        # Ensure internal implementation is stubbed
        self.assertNotIn("rows = [{\"id\": 1, \"name\": \"Alice\"}", r.output["text"])

    def test_auto_detects_python_code(self):
        ctx = Context()
        ctx.set("code", SAMPLE_PYTHON_CODE)
        # mode is auto by default
        r = self.engine.run(ctx)

        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertEqual(r.output["strategy"], "ast_skeleton")

    def test_symbol_focus_extraction(self):
        ctx = Context()
        ctx.set("code", SAMPLE_PYTHON_CODE)
        ctx.set("symbol", "DatabaseConnection.query")
        r = self.engine.run(ctx)

        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertEqual(r.output["strategy"], "symbol_focus")
        self.assertIn("def query", r.output["text"])
        self.assertIn("print(f\"Executing: {sql}", r.output["text"])

    def test_symbols_list_mode(self):
        ctx = Context()
        ctx.set("code", SAMPLE_PYTHON_CODE)
        ctx.set("mode", "symbols")
        r = self.engine.run(ctx)

        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertEqual(r.output["strategy"], "list_symbols")
        self.assertGreater(r.output["count"], 0)
        symbol_names = [s["name"] for s in r.output["symbols"]]
        self.assertIn("DatabaseConnection", symbol_names)
        self.assertIn("DatabaseConnection.query", symbol_names)

    def test_minify_mode(self):
        ctx = Context()
        code = "# Comment to strip\nx = 10\n\n\n\ny = 20\n"
        ctx.set("code", code)
        ctx.set("mode", "minify")
        r = self.engine.run(ctx)

        self.assertEqual(r.status, SkillStatus.SUCCESS)
        self.assertEqual(r.output["strategy"], "minify")
        self.assertNotIn("# Comment to strip", r.output["text"])


if __name__ == "__main__":
    unittest.main()
