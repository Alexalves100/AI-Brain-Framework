"""
Orchestrator
Version: 1.1.0
"""

from typing import List, Optional
from .skill import Skill, SkillResult, SkillStatus
from .registry import SkillRegistry
from .context import Context


class Orchestrator:
    """Routes context through one or more skills."""

    def __init__(self, registry: Optional[SkillRegistry] = None):
        self.registry = registry or SkillRegistry()

    @staticmethod
    def _validate_inputs(skill_name, context) -> Optional[SkillResult]:
        """Valida parâmetros de entrada. Retorna SkillResult de erro ou None se OK."""
        if not isinstance(skill_name, str) or not skill_name.strip():
            return SkillResult(
                status=SkillStatus.ERROR,
                error="skill_name must be a non-empty string",
            )
        if context is None:
            return SkillResult(
                status=SkillStatus.ERROR,
                error="context must not be None",
            )
        if not isinstance(context, Context):
            return SkillResult(
                status=SkillStatus.ERROR,
                error="context must be an instance of Context",
            )
        return None

    def run(self, skill_name: str, context: Context) -> SkillResult:
        validation_error = self._validate_inputs(skill_name, context)
        if validation_error is not None:
            return validation_error

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
        if not isinstance(names, list):
            return [
                SkillResult(
                    status=SkillStatus.ERROR,
                    error="names must be a list of skill names",
                )
            ]
        validation_error = self._validate_inputs(names[0] if names else "", context)
        # Apenas valida context aqui; nomes são validados em run()
        if validation_error is not None and "skill_name" in validation_error.error:
            return [validation_error]

        results = []
        for name in names:
            r = self.run(name, context)
            results.append(r)
            if r.status == SkillStatus.ERROR:
                break
        return results
