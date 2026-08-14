"""
MCP Tools Registry and Schemas for AI-Brain-Framework
Version: 1.0.0
"""

from typing import Any, Callable, Dict, List

from ..analyzers.code_smells import CodeSmellDetector
from ..analyzers.complexity_analyzer import ComplexityAnalyzer
from ..core.context import Context
from ..engines.clean_code import CleanCodeEngine
from ..engines.security import SecurityEngine
from ..engines.token_economy import TokenEconomyEngine
from ..scanners.ast_scanner import ASTScanner


class MCPToolRegistry:
    """Registry of tools exposed to MCP clients."""

    def __init__(self):
        self.ast_scanner = ASTScanner()
        self.code_smell_detector = CodeSmellDetector()
        self.clean_code_engine = CleanCodeEngine()
        self.security_engine = SecurityEngine()
        self.token_economy_engine = TokenEconomyEngine()
        self.complexity_analyzer = ComplexityAnalyzer()

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Returns the MCP tools specification array."""
        return [
            {
                "name": "clean_code_audit",
                "description": "Audits Python code against Senior Clean Code and SOLID standards. Returns score (0-100), detected smells (deep nesting, missing types, long functions), and self-healing refactoring plan.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The Python source code to audit",
                        },
                        "file_path": {
                            "type": "string",
                            "description": "Optional file path for reporting",
                        },
                    },
                    "required": ["code"],
                },
            },
            {
                "name": "get_symbols_overview",
                "description": "Generates a compact structural AST skeleton (.pyi style) of classes, methods, and type signatures. Replaces bodies with '...' saving 75%+ of tokens while preserving contracts.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The Python source code to summarize into an AST skeleton",
                        },
                        "file_path": {
                            "type": "string",
                            "description": "Optional file path label",
                        },
                    },
                    "required": ["code"],
                },
            },
            {
                "name": "get_symbol_body",
                "description": "Surgically extracts the 100% complete source code of a specific class (e.g. 'AuthService') or method (e.g. 'AuthService.login') without modifying or truncating anything.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The source code containing the target symbol",
                        },
                        "symbol_name": {
                            "type": "string",
                            "description": "Name of class, method, or function (e.g. 'MyClass' or 'MyClass.my_method')",
                        },
                    },
                    "required": ["code", "symbol_name"],
                },
            },
            {
                "name": "security_scan",
                "description": "Audits source code against security vulnerabilities (SQL Injection, XSS, eval, hardcoded secrets, weak hash).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The source code to scan for security vulnerabilities",
                        },
                    },
                    "required": ["code"],
                },
            },
            {
                "name": "compress_tokens",
                "description": "Compresses verbose text or code to minimize token usage using AST skeletons or filler removal.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text or code to compress",
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["auto", "ast_skeleton", "minify", "conversational"],
                            "description": "Compression strategy mode",
                        },
                    },
                    "required": ["text"],
                },
            },
            {
                "name": "analyze_complexity",
                "description": "Calculates cyclomatic and cognitive complexity metrics of source code.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Source code to analyze",
                        },
                    },
                    "required": ["code"],
                },
            },
            {
                "name": "list_symbols",
                "description": "Lists all classes, methods, and functions in a file with line ranges and signatures.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Source code to index",
                        },
                    },
                    "required": ["code"],
                },
            },
        ]

    def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a registered MCP tool by name."""
        handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
            "clean_code_audit": self._handle_clean_code_audit,
            "get_symbols_overview": self._handle_get_symbols_overview,
            "get_symbol_body": self._handle_get_symbol_body,
            "security_scan": self._handle_security_scan,
            "compress_tokens": self._handle_compress_tokens,
            "analyze_complexity": self._handle_analyze_complexity,
            "list_symbols": self._handle_list_symbols,
        }

        handler = handlers.get(name)
        if not handler:
            raise ValueError(f"Unknown tool: '{name}'")

        return handler(arguments)

    def _handle_clean_code_audit(self, args: Dict[str, Any]) -> Dict[str, Any]:
        code = args.get("code", "")
        file_path = args.get("file_path", "")
        ctx = Context()
        ctx.set("code", code)
        ctx.set("file_path", file_path)
        res = self.clean_code_engine.run(ctx)
        return res.output

    def _handle_get_symbols_overview(self, args: Dict[str, Any]) -> Dict[str, Any]:
        code = args.get("code", "")
        file_path = args.get("file_path", "")
        skeleton = self.ast_scanner.get_symbols_overview(code, file_path=file_path)
        orig_len = len(code)
        comp_len = len(skeleton)
        saved = max(0, orig_len - comp_len)
        return {
            "skeleton": skeleton,
            "original_chars": orig_len,
            "compressed_chars": comp_len,
            "saved_chars": saved,
            "savings_ratio": round(saved / orig_len, 3) if orig_len else 0.0,
        }

    def _handle_get_symbol_body(self, args: Dict[str, Any]) -> Dict[str, Any]:
        code = args.get("code", "")
        symbol_name = args.get("symbol_name", "")
        body = self.ast_scanner.get_symbol_body(code, symbol_name)
        if body is None:
            return {"found": False, "symbol": symbol_name, "body": None}
        return {"found": True, "symbol": symbol_name, "body": body}

    def _handle_security_scan(self, args: Dict[str, Any]) -> Dict[str, Any]:
        code = args.get("code", "")
        ctx = Context()
        ctx.set("code", code)
        res = self.security_engine.run(ctx)
        return res.output

    def _handle_compress_tokens(self, args: Dict[str, Any]) -> Dict[str, Any]:
        text = args.get("text", "")
        mode = args.get("mode", "auto")
        ctx = Context()
        ctx.set("text", text)
        ctx.set("mode", mode)
        res = self.token_economy_engine.run(ctx)
        return res.output

    def _handle_analyze_complexity(self, args: Dict[str, Any]) -> Dict[str, Any]:
        code = args.get("code", "")
        cyc = self.complexity_analyzer.cyclomatic_complexity(code)
        cog = self.complexity_analyzer.cognitive_complexity(code)
        lines = code.splitlines()
        non_blank = [line for line in lines if line.strip()]
        return {
            "total_lines": len(lines),
            "code_lines": len(non_blank),
            "cyclomatic_complexity": cyc,
            "cognitive_complexity": cog,
        }

    def _handle_list_symbols(self, args: Dict[str, Any]) -> Dict[str, Any]:
        code = args.get("code", "")
        symbols = self.ast_scanner.list_symbols(code)
        return {"symbols": symbols, "total_symbols": len(symbols)}
