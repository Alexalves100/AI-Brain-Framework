"""
Token Economy Engine — compresses text and code to optimize token usage
Version: 1.1.0
"""

import ast
import re
from typing import Any, Dict, List, Optional
from ..core import Skill, SkillResult, SkillStatus, Context
from ..scanners.ast_scanner import ASTScanner


class TokenEconomyEngine(Skill):
    name = "token_economy"
    version = "1.1.0"
    category = "context"
    description = "Compresses verbose text and extracts AST code skeletons to optimize token usage (Serena MCP style)"

    FILLER = [
        r"\b(vou|deixa irei)\s+\w+\s+(explicar|ajudar|mostrar)\b",
        r"\b(espero|desejo)\s+que\s+(isso|este|esta)\s+(seja|é)\s+(útil|util|helpful)\b",
        r"\bse\s+precisar\s+de\s+mais\s+ajuda\b",
        r"\b(claro|certo|ok|okay),\s+",
        r"^(oi|olá|hello|hi)[!,.]?\s*",
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ast_scanner = ASTScanner()

    def run(self, context: Context) -> SkillResult:
        # Check if code or text is provided
        code = context.get("code")
        text = context.get("text")
        mode = context.get("mode", "auto")
        symbol = context.get("symbol")
        file_path = context.get("file_path", "")

        # Prioritize code if code-specific mode or symbol is requested, otherwise text if available
        if mode in ("ast_skeleton", "skeleton", "minify", "symbols") or symbol:
            raw_input = code if code is not None else text
        else:
            raw_input = text if text is not None else code

        if raw_input is None or not str(raw_input).strip():
            return SkillResult(status=SkillStatus.SKIPPED, output={"text": ""})

        content_str = str(raw_input)
        original_len = len(content_str)

        # Determine strategy
        if symbol:
            # Target symbol extraction (Progressive Disclosure - Layer 2)
            extracted_body = self.ast_scanner.get_symbol_body(content_str, symbol)
            if extracted_body is None:
                return SkillResult(
                    status=SkillStatus.ERROR,
                    error=f"Symbol '{symbol}' not found in provided code",
                )
            compressed = extracted_body
            strategy = "symbol_focus"

        elif mode in ("ast_skeleton", "skeleton") or (mode == "auto" and self._is_python_code(content_str)):
            # AST Skeleton mode (Serena MCP - Layer 1)
            compressed = self.ast_scanner.get_symbols_overview(content_str, file_path=file_path)
            strategy = "ast_skeleton"

        elif mode == "minify":
            # Code Minification
            compressed = self.ast_scanner.minify_code(content_str)
            strategy = "minify"

        elif mode == "symbols":
            # List symbols index
            symbols_list = self.ast_scanner.list_symbols(content_str)
            context.set("symbols_list", symbols_list)
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={
                    "symbols": symbols_list,
                    "count": len(symbols_list),
                    "strategy": "list_symbols",
                },
                metadata={"engine": "token_economy"},
            )

        else:
            # Conversational text compression (Layer 0 / Legacy mode)
            compressed = content_str
            for pattern in self.FILLER:
                compressed = re.sub(pattern, "", compressed, flags=re.I | re.M)

            compressed = re.sub(r"\n{3,}", "\n\n", compressed)
            compressed = re.sub(r" {2,}", " ", compressed)
            compressed = compressed.strip()
            strategy = "conversational"

        compressed_len = len(compressed)
        savings = max(0, original_len - compressed_len)
        ratio = savings / original_len if original_len else 0.0

        # Update context
        context.set("compressed_text", compressed)
        if code is not None:
            context.set("compressed_code", compressed)

        return SkillResult(
            status=SkillStatus.SUCCESS,
            output={
                "text": compressed,
                "original_len": original_len,
                "compressed_len": compressed_len,
                "saved": savings,
                "ratio": round(ratio, 3),
                "strategy": strategy,
            },
            tokens_used=savings // 4,
            metadata={"engine": "token_economy", "strategy": strategy},
        )

    def _is_python_code(self, text: str) -> bool:
        """Heuristic to detect whether the content is valid Python code."""
        # Quick check for python keywords
        if not re.search(r"\b(def|class|import|from|async def|return)\b", text):
            return False
        try:
            ast.parse(text)
            return True
        except SyntaxError:
            return False
