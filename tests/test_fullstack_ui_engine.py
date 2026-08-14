"""
Unit & Integration Tests for FullstackUIEngine & MCP Tools
Version: 1.0.0
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework import Context, SkillStatus, create_default_orchestrator
from framework.engines.fullstack_ui import FullstackUIEngine
from framework.mcp.tools import MCPToolRegistry


class TestFullstackUIEngine(unittest.TestCase):
    def setUp(self):
        self.engine = FullstackUIEngine()
        self.mcp_registry = MCPToolRegistry()

    def test_engine_tokens_action(self):
        ctx = Context()
        ctx.set("action", "tokens")
        ctx.set("theme", "editorial")
        res = self.engine.run(ctx)
        self.assertEqual(res.status, SkillStatus.SUCCESS)
        self.assertIn("css", res.output)
        self.assertIn("--background:", res.output["css"])

    def test_engine_component_action(self):
        ctx = Context()
        ctx.set("action", "component")
        ctx.set("component_type", "card")
        ctx.set("title", "Receita Anual")
        res = self.engine.run(ctx)
        self.assertEqual(res.status, SkillStatus.SUCCESS)
        self.assertIn("Receita Anual", res.output["code"])

    def test_engine_audit_action(self):
        ctx = Context()
        ctx.set("action", "audit")
        ctx.set("code", '<img src="foto.jpg" />')
        res = self.engine.run(ctx)
        self.assertEqual(res.status, SkillStatus.ERROR)
        self.assertFalse(res.output["passed"])


    def test_engine_api_client_action(self):
        ctx = Context()
        ctx.set("action", "api_client")
        ctx.set("schema_name", "Order")
        ctx.set("properties", {"id": "integer", "total": "float"})
        res = self.engine.run(ctx)
        self.assertEqual(res.status, SkillStatus.SUCCESS)
        self.assertIn("export interface Order", res.output["typescript_interface"])

    def test_mcp_frontend_component_scaffold(self):
        res = self.mcp_registry.execute_tool(
            "frontend_component_scaffold",
            {"component_type": "button", "label": "Finalizar"},
        )
        self.assertIn("code", res)
        self.assertIn("Finalizar", res["code"])

    def test_mcp_frontend_a11y_audit(self):
        res = self.mcp_registry.execute_tool(
            "frontend_a11y_audit",
            {"code": "<button aria-label=\"Salvar\"><svg></svg></button>"},
        )
        self.assertTrue(res["passed"])
        self.assertEqual(res["score"], 100)

    def test_mcp_generate_typed_api_client(self):
        res = self.mcp_registry.execute_tool(
            "generate_typed_api_client",
            {"schema_name": "Invoice", "properties": {"amount": "number"}},
        )
        self.assertIn("typescript_interface", res)
        self.assertIn("Invoice", res["typescript_interface"])

    def test_orchestrator_has_fullstack_ui(self):
        orch = create_default_orchestrator()
        self.assertIn("fullstack_ui", orch.registry)


if __name__ == "__main__":
    unittest.main()
