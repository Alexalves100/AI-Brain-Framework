"""
Unit & Integration Tests for SurgicalCodePatcher, CodePatcherEngine & MCP Tool
Version: 1.0.0
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework import Context, SkillStatus, create_default_orchestrator
from framework.engines.code_patcher import CodePatcherEngine
from framework.mcp.tools import MCPToolRegistry
from framework.patchers.code_patcher import SurgicalCodePatcher

SAMPLE_CODE = """def add_numbers(a, b):
    return a + b

def multiply_numbers(a, b):
    return a * b
"""


class TestSurgicalCodePatcher(unittest.TestCase):
    def setUp(self):
        self.patcher = SurgicalCodePatcher()
        self.mcp_registry = MCPToolRegistry()

    def test_patch_string_search_replace(self):
        patch = """<<<<<<< SEARCH
def add_numbers(a, b):
    return a + b
=======
def add_numbers(a: int, b: int) -> int:
    return a + b
>>>>>>> REPLACE"""

        res = self.patcher.patch_string(SAMPLE_CODE, patch, strategy="auto")
        self.assertTrue(res.success)
        self.assertEqual(res.strategy_used, "search_replace")
        self.assertTrue(res.syntax_valid)
        self.assertIn("def add_numbers(a: int, b: int) -> int:", res.modified_code)

    def test_patch_string_ast_node_strategy(self):
        new_func = """def multiply_numbers(a: int, b: int) -> int:
    # Optimized multiply
    return a * b"""

        res = self.patcher.patch_string(
            SAMPLE_CODE,
            new_func,
            strategy="ast_node",
            symbol_name="multiply_numbers",
        )
        self.assertTrue(res.success)
        self.assertEqual(res.strategy_used, "ast_node")
        self.assertIn("def multiply_numbers(a: int, b: int) -> int:", res.modified_code)

    def test_syntax_error_rollback(self):
        invalid_patch = """<<<<<<< SEARCH
def add_numbers(a, b):
    return a + b
=======
def add_numbers(a, b:
    invalid syntax here
>>>>>>> REPLACE"""

        res = self.patcher.patch_string(SAMPLE_CODE, invalid_patch, strategy="search_replace")
        self.assertFalse(res.success)
        self.assertFalse(res.syntax_valid)
        self.assertIn("SyntaxError", res.error)

    def test_patch_file_with_dry_run(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tf:
            tf.write(SAMPLE_CODE)
            tf_path = tf.name

        try:
            patch = """<<<<<<< SEARCH
def add_numbers(a, b):
    return a + b
=======
def add_numbers(a, b):
    return (a + b) * 1
>>>>>>> REPLACE"""

            # Dry run should NOT write to disk
            res_dry = self.patcher.patch_file(tf_path, patch, dry_run=True)
            self.assertTrue(res_dry.success)
            content_disk = Path(tf_path).read_text(encoding="utf-8")
            self.assertEqual(content_disk, SAMPLE_CODE)

            # Real run DOES write to disk
            res_real = self.patcher.patch_file(tf_path, patch, dry_run=False)
            self.assertTrue(res_real.success)
            content_disk_updated = Path(tf_path).read_text(encoding="utf-8")
            self.assertIn("(a + b) * 1", content_disk_updated)
        finally:
            Path(tf_path).unlink(missing_ok=True)

    def test_code_patcher_engine_skill(self):
        engine = CodePatcherEngine()
        ctx = Context()
        ctx.set("code", SAMPLE_CODE)
        ctx.set("patch", """<<<<<<< SEARCH
def add_numbers(a, b):
    return a + b
=======
def add_numbers(a, b):
    return sum([a, b])
>>>>>>> REPLACE""")

        self.assertTrue(engine.validate_inputs(ctx))
        res = engine.run(ctx)
        self.assertEqual(res.status, SkillStatus.SUCCESS)
        self.assertIn("sum([a, b])", res.output["modified_code"])

    def test_mcp_tool_apply_surgical_patch(self):
        patch = """<<<<<<< SEARCH
def add_numbers(a, b):
    return a + b
=======
def add_numbers(a, b):
    return a + b + 0
>>>>>>> REPLACE"""

        res = self.mcp_registry.execute_tool(
            "apply_surgical_patch",
            {"code": SAMPLE_CODE, "patch_data": patch},
        )
        self.assertTrue(res["success"])
        self.assertIn("diff_summary", res)

    def test_orchestrator_has_code_patcher(self):
        orch = create_default_orchestrator()
        self.assertIn("code_patcher", orch.registry)


if __name__ == "__main__":
    unittest.main()
