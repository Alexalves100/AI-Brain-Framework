"""
Prompt Registry — manages prompt templates
Version: 1.0.0
"""

from typing import Dict, List


class PromptRegistry:
    """Central registry for prompt templates."""

    DEFAULT_PROMPTS = {
        "code_review": "Review the following code for issues:\n\n{code}",
        "refactor": "Refactor this code to improve quality:\n\n{code}",
        "document": "Generate documentation for:\n\n{code}",
        "test": "Generate unit tests for:\n\n{code}",
        "explain": "Explain what this code does:\n\n{code}",
        "security_audit": "Audit this code for security issues:\n\n{code}",
    }

    def __init__(self):
        self._prompts: Dict[str, str] = dict(self.DEFAULT_PROMPTS)

    def register(self, name: str, template: str) -> None:
        self._prompts[name] = template

    def get(self, name: str) -> str:
        return self._prompts.get(name, "")

    def render(self, name: str, **kwargs) -> str:
        template = self.get(name)
        try:
            return template.format(**kwargs)
        except KeyError:
            return template

    def list(self) -> List[str]:
        return sorted(self._prompts.keys())
