"""
Senior Developer Guidelines and Clean Code Standards
Version: 1.0.0
"""

from typing import Dict, List, Any


class SeniorGuidelines:
    """
    Encapsulates Senior Software Engineering guardrails and Clean Code standards
    inspired by awesome-cursorrules, Aider, and Sourcery.
    """

    RULES = {
        "SRP_SINGLE_RESPONSIBILITY": {
            "id": "SRP-001",
            "name": "Single Responsibility Principle",
            "description": "Functions and methods must do exactly one thing. Max 30 lines per function.",
            "threshold_lines": 30,
        },
        "GUARD_CLAUSES_EARLY_RETURN": {
            "id": "GUARD-002",
            "name": "Guard Clauses & Early Returns",
            "description": "Avoid deep indentation (max nesting depth: 2). Return early on errors or edge cases.",
            "max_nesting": 2,
        },
        "STRICT_TYPE_ANNOTATIONS": {
            "id": "TYPE-003",
            "name": "Strict Type Annotations",
            "description": "All function parameters and return values must have explicit Type Hints.",
            "required": True,
        },
        "DEFENSIVE_ERROR_HANDLING": {
            "id": "ERR-004",
            "name": "Defensive & Explicit Error Handling",
            "description": "Never use bare except: or pass silently. Catch specific exception types.",
            "allow_bare_except": False,
        },
        "PARAMETER_OBJECTS": {
            "id": "PARAM-005",
            "name": "Parameter Limit (Value Objects)",
            "description": "Functions must not accept more than 4 parameters. Group parameters into dataclasses.",
            "max_params": 4,
        },
        "ANTI_LAZY_CODE": {
            "id": "LAZY-006",
            "name": "No Lazy or Incomplete Code",
            "description": "Never leave incomplete placeholder implementations or '# TODO implement later'.",
            "allow_placeholders": False,
        },
        "NO_REDUNDANT_ELSE": {
            "id": "ELSE-007",
            "name": "No Redundant Else After Return",
            "description": "Do not write else/elif blocks after return or raise statements.",
        },
        "NAMING_CONVENTIONS": {
            "id": "NAME-008",
            "name": "Self-Documenting Naming",
            "description": "Use clear, intention-revealing names. Avoid single-letter or cryptic abbreviations.",
        },
    }

    @classmethod
    def get_rules_list(cls) -> List[Dict[str, Any]]:
        """Returns all configured senior rules."""
        return list(cls.RULES.values())

    @classmethod
    def get_prompt_constraints(cls) -> List[str]:
        """
        Returns actionable system prompt constraint bullets
        ready to be injected into PromptBuilder.
        """
        return [
            "Write production-ready, senior-level, modular code following SOLID, DRY, and KISS principles.",
            "Keep functions small and focused on a single responsibility (maximum 30 lines).",
            "Use Guard Clauses (early returns) to eliminate nested if/else statements (maximum nesting depth: 2).",
            "Provide 100% complete type hints (parameters and return types) on all functions and methods.",
            "Never use bare 'except:' or silent 'pass'. Always catch specific exceptions and handle them explicitly.",
            "Limit function parameters to a maximum of 4 (use dataclasses/typed dicts for larger sets).",
            "Do NOT leave lazy placeholders (e.g. '// TODO implement later' or '...'). Write full, working implementations.",
            "Ensure self-documenting naming conventions and concise docstrings explaining why, not just what.",
        ]

    @classmethod
    def get_system_prompt(cls, role_title: str = "Senior Principal Software Engineer") -> str:
        """Generates a complete system prompt header for senior-level AI pair programming."""
        constraints = cls.get_prompt_constraints()
        bullets = "\n".join(f"- {c}" for c in constraints)
        return (
            f"You are a {role_title}.\n"
            "Your objective is to produce clean, maintainable, robust, and readable software.\n\n"
            "MANDATORY ARCHITECTURAL & CLEAN CODE GUARDRAILS:\n"
            f"{bullets}\n"
        )
