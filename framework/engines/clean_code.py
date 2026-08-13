"""
Clean Code Engine — enforces senior-level clean code standards & self-healing loops
Version: 1.0.0
"""

from typing import Any, Dict, Optional
from ..core import Skill, SkillResult, SkillStatus, Context
from ..analyzers.code_smells import CodeSmellDetector
from ..prompts.senior_prompts import SeniorPromptTemplates
from ..standards.senior_guidelines import SeniorGuidelines


class CleanCodeEngine(Skill):
    name = "clean_code"
    version = "1.0.0"
    category = "quality"
    description = "Audits code against Senior Clean Code standards and generates Self-Healing refactoring instructions"

    def __init__(self, min_passing_score: int = 90, **kwargs):
        super().__init__(**kwargs)
        self.min_passing_score = min_passing_score
        self.detector = CodeSmellDetector()

    def run(self, context: Context) -> SkillResult:
        action = context.get("action", "audit")
        code = context.get("code")
        file_path = context.get("file_path", "")

        if action == "system_prompt":
            role = context.get("role", "Principal Software Architect")
            prompt = SeniorPromptTemplates.get_system_prompt(role=role)
            context.set("clean_code_prompt", prompt)
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={"system_prompt": prompt, "action": "system_prompt"},
                metadata={"engine": "clean_code"},
            )

        if not code or not str(code).strip():
            return SkillResult(
                status=SkillStatus.SKIPPED,
                output={"message": "No code provided for Clean Code analysis"},
            )

        code_str = str(code)
        report = self.detector.analyze_code(code_str, file_path=file_path)

        score = report.get("score", 0)
        smells = report.get("smells", [])
        is_senior = report.get("is_senior_standard", False)

        # Generate Self-Healing refactoring instruction if issues exist
        refactor_instruction = None
        if not is_senior or action == "self_heal":
            refactor_instruction = SeniorPromptTemplates.get_self_healing_refactor_prompt(
                code=code_str, smells=smells, score=score
            )
            context.set("refactor_instruction", refactor_instruction)

        output: Dict[str, Any] = {
            "score": score,
            "min_passing_score": self.min_passing_score,
            "is_senior_standard": is_senior,
            "total_smells": len(smells),
            "type_coverage_pct": report.get("type_coverage_pct", 0),
            "smells": smells,
            "refactor_instruction": refactor_instruction,
            "action": action,
        }

        context.set("clean_code_result", output)

        return SkillResult(
            status=SkillStatus.SUCCESS,
            output=output,
            metadata={"engine": "clean_code", "score": score, "is_senior": is_senior},
        )
