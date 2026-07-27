"""
Orchestrator
Version: 1.0.0
"""

from typing import List, Optional
from .skill import Skill, SkillResult, SkillStatus
from .registry import SkillRegistry
from .context import Context


class Orchestrator:
    """Routes context through one or more skills."""

    def __init__(self, registry: Optional[SkillRegistry] = None):
        self.registry = registry or SkillRegistry()

    def run(self, skill_name: str, context: Context) -> SkillResult:
        skill = self.registry.get(skill_name)
        if not skill:
            return SkillResult(
                status=SkillStatus.ERROR,
                error=f"Skill '{skill_name}' not found",
            )
        if not skill.validate_inputs(context):
            return SkillResult(
                status=SkillStatus.ERROR,
                error=f"Invalid inputs for '{skill_name}'",
            )
        context.log(f"RUN: {skill_name}")
        result = skill.run(context)
        context.log(f"DONE: {skill_name} -> {result.status.value}")
        if result.tokens_used:
            context.add_tokens(result.tokens_used)
        return result

    def run_pipeline(self, names: List[str], context: Context) -> List[SkillResult]:
        results = []
        for name in names:
            r = self.run(name, context)
            results.append(r)
            if r.status == SkillStatus.ERROR:
                break
        return results
