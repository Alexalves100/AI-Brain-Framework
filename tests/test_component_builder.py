"""
Unit Tests for ComponentBuilder (Multi-Stack Component Scaffolds)
Version: 1.0.0
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.frontend.component_builder import ComponentBuilder


class TestComponentBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = ComponentBuilder()

    def test_build_react_button(self):
        code = self.builder.build_button(label="Enviar", variant="primary", stack="react_tailwind")
        self.assertIn("export const Button", code)
        self.assertIn("aria-label=\"Enviar\"", code)
        self.assertIn("isLoading", code)
        self.assertIn("active:scale-[0.98]", code)

    def test_build_vanilla_button(self):
        code = self.builder.build_button(label="Comprar", variant="primary", stack="vanilla")
        self.assertIn("<button type=\"button\" class=\"btn btn-primary", code)
        self.assertIn("aria-label=\"Comprar\"", code)
        self.assertIn(":focus-visible", code)

    def test_build_react_card(self):
        code = self.builder.build_card(title="Dashboard", subtitle="Visão geral", stack="react_tailwind")
        self.assertIn("export const Card", code)
        self.assertIn("<article", code)
        self.assertIn("Dashboard", code)

    def test_build_react_input(self):
        code = self.builder.build_input(label="Senha", input_id="pwd", input_type="password", stack="react_tailwind")
        self.assertIn("export const InputField", code)
        self.assertIn("htmlFor={id}", code)
        self.assertIn("aria-invalid", code)


if __name__ == "__main__":
    unittest.main()
