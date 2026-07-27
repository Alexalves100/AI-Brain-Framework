"""
Reasoning Engine — structured reasoning with explicit premises
Version: 1.0.0
"""

from typing import List, Dict, Any
from ..core import Skill, SkillResult, SkillStatus, Context


class ReasoningEngine(Skill):
    name = "reasoning"
    version = "1.0.0"
    category = "core"
    description = "Structured reasoning with explicit premises and conclusions"

    def run(self, context: Context) -> SkillResult:
        premises: List[str] = context.get("premises", [])
        conclusion: str = context.get("conclusion", "")

        if not premises or not conclusion:
            return SkillResult(
                status=SkillStatus.SKIPPED,
                output={"reason": "missing premises or conclusion"},
            )

        chain = []
        for i, premise in enumerate(premises, 1):
            chain.append({
                "step": i,
                "premise": premise,
                "validated": len(premise.strip()) > 0,
            })

        confidence = self._compute_confidence(premises, conclusion)
        valid = confidence >= 0.5

        result = {
            "chain": chain,
            "conclusion": conclusion,
            "confidence": round(confidence, 2),
            "valid": valid,
        }
        context.set("reasoning_result", result)
        return SkillResult(
            status=SkillStatus.SUCCESS,
            output=result,
            metadata={"engine": "reasoning"},
        )

    def _compute_confidence(self, premises: List[str], conclusion: str) -> float:
        if not premises:
            return 0.0
        premise_words = set()
        for p in premises:
            premise_words.update(p.lower().split())
        conclusion_words = set(conclusion.lower().split())
        if not conclusion_words:
            return 0.0
        overlap = len(premise_words & conclusion_words)
        return min(1.0, overlap / len(conclusion_words))
