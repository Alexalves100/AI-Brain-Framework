"""
Prompt Builder — composes prompts from parts
Version: 1.0.0
"""

from typing import List


class PromptBuilder:
    """Builds prompts from composable parts."""

    def __init__(self):
        self.parts: List[str] = []

    def add_role(self, role: str) -> "PromptBuilder":
        self.parts.append(f"You are {role}.")
        return self

    def add_context(self, context: str) -> "PromptBuilder":
        self.parts.append(f"Context:\n{context}")
        return self

    def add_task(self, task: str) -> "PromptBuilder":
        self.parts.append(f"Task:\n{task}")
        return self

    def add_constraints(self, constraints: List[str]) -> "PromptBuilder":
        self.parts.append("Constraints:\n" + "\n".join(f"- {c}" for c in constraints))
        return self

    def add_format(self, format_spec: str) -> "PromptBuilder":
        self.parts.append(f"Output format:\n{format_spec}")
        return self

    def add_examples(self, examples: List[str]) -> "PromptBuilder":
        self.parts.append("Examples:\n" + "\n".join(examples))
        return self

    def build(self) -> str:
        return "\n\n".join(self.parts)
