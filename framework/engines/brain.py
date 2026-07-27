"""
Brain Engine — central cognitive orchestration
Version: 1.0.0
"""

from typing import Dict, Any
from ..core import Skill, SkillResult, SkillStatus, Context


class BrainEngine(Skill):
    name = "brain"
    version = "1.0.0"
    category = "core"
    description = "Routes context to the appropriate skill"

    KEYWORDS = {
        "security": ["csrf", "xss", "sql", "cookie", "header", "vulnerability", "auth"],
        "performance": ["slow", "lag", "memory", "cpu", "cache", "optimize"],
        "architecture": ["design", "pattern", "structure", "module", "decouple"],
        "documentation": ["doc", "readme", "guide", "tutorial"],
        "testing": ["test", "coverage", "spec", "assert"],
    }

    def run(self, context: Context) -> SkillResult:
        query = (context.get("query") or "").lower()
        if not query:
            return SkillResult(
                status=SkillStatus.SKIPPED,
                output={"routed_to": None, "reason": "empty query"},
            )

        scores: Dict[str, int] = {}
        for category, words in self.KEYWORDS.items():
            scores[category] = sum(1 for w in words if w in query)

        routed_to = max(scores, key=scores.get) if any(scores.values()) else "general"
        context.set("routed_category", routed_to)
        context.set("category_scores", scores)

        return SkillResult(
            status=SkillStatus.SUCCESS,
            output={"routed_to": routed_to, "scores": scores},
            metadata={"engine": "brain"},
        )
