"""
Token Economy Engine — compresses text to reduce token usage
Version: 1.0.0
"""

import re
from ..core import Skill, SkillResult, SkillStatus, Context


class TokenEconomyEngine(Skill):
    name = "token_economy"
    version = "1.0.0"
    category = "context"
    description = "Compresses verbose text into compact form"

    FILLER = [
        r"\b(vou|deixa irei)\s+\w+\s+(explicar|ajudar|mostrar)\b",
        r"\b(espero|desejo)\s+que\s+(isso|este|esta)\s+(seja|é)\s+(útil|util|helpful)\b",
        r"\bse\s+precisar\s+de\s+mais\s+ajuda\b",
        r"\b(claro|certo|ok|okay),\s+",
        r"^(oi|olá|hello|hi)[!,.]?\s*",
    ]

    def run(self, context: Context) -> SkillResult:
        text = context.get("text", "")
        if not text:
            return SkillResult(status=SkillStatus.SKIPPED, output={"text": ""})

        original_len = len(text)
        compressed = text
        for pattern in self.FILLER:
            compressed = re.sub(pattern, "", compressed, flags=re.I | re.M)

        compressed = re.sub(r"\n{3,}", "\n\n", compressed)
        compressed = re.sub(r" {2,}", " ", compressed)
        compressed = compressed.strip()

        savings = original_len - len(compressed)
        ratio = savings / original_len if original_len else 0

        context.set("compressed_text", compressed)
        return SkillResult(
            status=SkillStatus.SUCCESS,
            output={
                "text": compressed,
                "original_len": original_len,
                "compressed_len": len(compressed),
                "saved": savings,
                "ratio": round(ratio, 3),
            },
            tokens_used=savings // 4,
            metadata={"engine": "token_economy"},
        )
