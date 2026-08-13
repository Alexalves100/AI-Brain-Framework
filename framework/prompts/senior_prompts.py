"""
Senior Engineering Prompt Templates & Guardrails
Version: 1.0.0
"""

from typing import Any, Dict, List

from ..standards.senior_guidelines import SeniorGuidelines


class SeniorPromptTemplates:
    """
    Standardized Senior Engineer prompts inspired by awesome-cursorrules, Aider, and OpenHands.
    """

    @classmethod
    def get_system_prompt(cls, role: str = "Principal Software Architect") -> str:
        """Returns a high-standard system prompt enforcing clean code and architectural rigor."""
        return SeniorGuidelines.get_system_prompt(role_title=role)

    @classmethod
    def get_self_healing_refactor_prompt(
        cls, code: str, smells: List[Dict[str, Any]], score: int
    ) -> str:
        """
        Builds a targeted refactoring instruction (Aider/Self-Healing style)
        from a list of detected code smells and score.
        """
        issue_bullets = []
        for s in smells:
            line_str = f"Line {s['line']}" if s.get("line") else "Global"
            symbol_str = f" in '{s['symbol']}'" if s.get("symbol") and s['symbol'] not in ("<line>", "<module>") else ""
            issue_bullets.append(
                f"- [{s['severity'].upper()}] {line_str}{symbol_str}: {s['message']}\n  👉 Action: {s['recommendation']}"
            )

        issues_text = "\n".join(issue_bullets) if issue_bullets else "No critical issues detected."

        return (
            "You are a Senior Principal Software Engineer performing an automated Clean Code Refactoring.\n\n"
            f"CURRENT CLEAN CODE SCORE: {score}/100 (Threshold required: >= 90)\n\n"
            "ISSUES & CODE SMELLS REQUIRING CORRECTION:\n"
            f"{issues_text}\n\n"
            "MANDATORY REFACTORING RULES:\n"
            "1. Fix all identified code smells while preserving 100% of the original business logic and behavior.\n"
            "2. Replace nested if/else statements with Guard Clauses (early returns).\n"
            "3. Ensure all functions have explicit Type Hints (parameters and return types).\n"
            "4. Eliminate bare 'except:' statements; catch specific typed exceptions.\n"
            "5. Keep functions concise and single-responsibility.\n\n"
            "ORIGINAL SOURCE CODE TO REFACTOR:\n"
            "```python\n"
            f"{code}\n"
            "```\n\n"
            "Output the pristine, fully-refactored senior-level Python code."
        )

    @classmethod
    def get_feature_implementation_prompt(
        cls, feature_description: str, context_code: str = ""
    ) -> str:
        """
        Builds a senior developer prompt for creating a new feature with clean architecture.
        """
        constraints = SeniorGuidelines.get_prompt_constraints()
        constraints_text = "\n".join(f"- {c}" for c in constraints)

        prompt = (
            "TASK: Implement the following feature at a Senior Staff Engineer standard.\n\n"
            f"FEATURE SPECIFICATION:\n{feature_description}\n\n"
            f"ENGINEERING GUARDRAILS:\n{constraints_text}\n"
        )
        if context_code:
            prompt += f"\nEXISTING ARCHITECTURE CONTEXT:\n```python\n{context_code}\n```\n"

        return prompt
