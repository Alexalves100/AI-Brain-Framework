"""
Code Smell Detector & Senior Code Quality Analyzer
Version: 1.0.0
"""

import ast
import re
from typing import Any, Dict, List, Set, Tuple, Union


class CodeSmellDetector:
    """
    AST-based Clean Code Analyzer inspired by Sourcery, Ruff, and Aider.
    Detects anti-patterns, complexity hotspots, and missing senior standards.
    Zero external dependencies.
    """

    ALLOWED_NUMBERS: Set[Union[int, float]] = {0, 1, 2, -1, 10, 100, 200, 201, 204, 400, 401, 403, 404, 500}

    def __init__(
        self,
        max_function_lines: int = 30,
        max_parameters: int = 4,
        max_nesting_depth: int = 2,
        require_type_hints: bool = True,
    ):
        self.max_function_lines = max_function_lines
        self.max_parameters = max_parameters
        self.max_nesting_depth = max_nesting_depth
        self.require_type_hints = require_type_hints

    def analyze_code(self, code: str, file_path: str = "") -> Dict[str, Any]:
        """
        Analyzes source code string and returns a comprehensive Clean Code report.
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "file": file_path,
                "score": 0,
                "syntax_valid": False,
                "error": f"SyntaxError at line {e.lineno}: {e.msg}",
                "smells": [],
                "functions_analyzed": 0,
            }

        lines = code.splitlines()
        smells: List[Dict[str, Any]] = []

        # File-level checks
        if len(lines) > 400:
            smells.append({
                "line": 1,
                "symbol": "<module>",
                "rule": "FILE_TOO_LONG",
                "severity": "medium",
                "message": f"File has {len(lines)} lines (exceeds recommended 400 lines limit). Consider splitting into modules.",
                "recommendation": "Decompose into smaller cohesive modules.",
            })

        # Check for lazy comments
        for idx, line in enumerate(lines, 1):
            if re.search(r"#\s*(TODO|FIXME|XXX|TBD|IMPLEMENTME)\b", line, re.I):
                smells.append({
                    "line": idx,
                    "symbol": "<line>",
                    "rule": "ANTI_LAZY_CODE",
                    "severity": "high",
                    "message": f"Contains lazy placeholder or uncompleted task: '{line.strip()[:60]}'",
                    "recommendation": "Provide full, working implementation without placeholder comments.",
                })

        # Function & Class level AST checks
        func_count = 0
        typed_func_count = 0

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_count += 1
                func_smells, is_typed = self._analyze_function(node, lines)
                smells.extend(func_smells)
                if is_typed:
                    typed_func_count += 1

            elif isinstance(node, ast.Try):
                smells.extend(self._analyze_try_block(node))

            elif isinstance(node, ast.Constant):
                # Magic numbers
                if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                    if node.value not in self.ALLOWED_NUMBERS and hasattr(node, "lineno"):
                        # Skip if in uppercase constant definition or test
                        line_text = lines[node.lineno - 1] if node.lineno <= len(lines) else ""
                        if not re.match(r"^[A-Z0-9_]+\s*[:=]", line_text.strip()):
                            smells.append({
                                "line": node.lineno,
                                "symbol": "<constant>",
                                "rule": "MAGIC_NUMBER",
                                "severity": "low",
                                "message": f"Magic number '{node.value}' used without descriptive constant name.",
                                "recommendation": "Extract to an uppercase named constant (e.g. MAX_TIMEOUT, RETRY_LIMIT).",
                            })

        # Calculate Clean Code Score (100 base)
        penalties = {
            "high": 15,
            "medium": 8,
            "low": 3,
        }
        total_deduction = sum(penalties.get(s["severity"], 5) for s in smells)
        score = max(0, 100 - total_deduction)

        type_coverage_pct = round((typed_func_count / max(func_count, 1)) * 100, 1)

        return {
            "file": file_path,
            "score": score,
            "is_senior_standard": score >= 90 and not any(s["severity"] == "high" for s in smells),
            "syntax_valid": True,
            "total_smells": len(smells),
            "smells": smells,
            "functions_analyzed": func_count,
            "type_coverage_pct": type_coverage_pct,
        }

    def _analyze_function(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], lines: List[str]
    ) -> Tuple[List[Dict[str, Any]], bool]:
        smells: List[Dict[str, Any]] = []

        name = node.name

        start = node.lineno
        end = getattr(node, "end_lineno", node.lineno)
        func_length = end - start + 1

        # 1. Function Length (Single Responsibility)
        if func_length > self.max_function_lines and name != "__init__":
            smells.append({
                "line": start,
                "symbol": name,
                "rule": "SRP_SINGLE_RESPONSIBILITY",
                "severity": "medium",
                "message": f"Function '{name}' is {func_length} lines long (max recommended: {self.max_function_lines}).",
                "recommendation": "Extract sub-tasks into smaller private helper methods.",
            })

        # 2. Parameter count
        args = [a for a in node.args.args if a.arg not in ("self", "cls")]
        if len(args) > self.max_parameters:
            smells.append({
                "line": start,
                "symbol": name,
                "rule": "PARAMETER_LIMIT",
                "severity": "medium",
                "message": f"Function '{name}' accepts {len(args)} parameters (max recommended: {self.max_parameters}).",
                "recommendation": "Group related parameters into a dataclass or typed value object.",
            })

        # 3. Type Annotations
        missing_type_hints = False
        if self.require_type_hints:
            untyped_args = [a.arg for a in args if a.annotation is None]
            if untyped_args:
                missing_type_hints = True
                smells.append({
                    "line": start,
                    "symbol": name,
                    "rule": "STRICT_TYPE_ANNOTATIONS",
                    "severity": "medium",
                    "message": f"Missing type hints for parameter(s): {', '.join(untyped_args)} in '{name}'.",
                    "recommendation": "Add explicit type annotations for all parameters.",
                })
            if node.returns is None and name != "__init__":
                missing_type_hints = True
                smells.append({
                    "line": start,
                    "symbol": name,
                    "rule": "STRICT_TYPE_ANNOTATIONS",
                    "severity": "medium",
                    "message": f"Missing return type annotation on function '{name}'.",
                    "recommendation": "Add explicit return type hint (e.g. '-> None', '-> bool', '-> Result').",
                })

        # 4. Nesting Depth & Guard Clauses
        max_depth = self._calculate_max_nesting(node.body)
        if max_depth > self.max_nesting_depth:
            smells.append({
                "line": start,
                "symbol": name,
                "rule": "GUARD_CLAUSES_EARLY_RETURN",
                "severity": "high",
                "message": f"Function '{name}' has nesting depth of {max_depth} (max recommended: {self.max_nesting_depth}).",
                "recommendation": "Refactor nested if/else statements into Early Returns / Guard Clauses.",
            })

        # 5. Redundant Else after Return / Raise
        for stmt in node.body:
            if isinstance(stmt, ast.If) and stmt.orelse:
                if self._body_always_returns_or_raises(stmt.body):
                    smells.append({
                        "line": stmt.orelse[0].lineno if stmt.orelse else start,
                        "symbol": name,
                        "rule": "NO_REDUNDANT_ELSE",
                        "severity": "low",
                        "message": f"Unnecessary 'else' block after 'return' or 'raise' in '{name}'.",
                        "recommendation": "Remove 'else' indentation and promote inner logic to outer scope.",
                    })

        return smells, not missing_type_hints

    def _analyze_try_block(self, node: ast.Try) -> List[Dict[str, Any]]:
        smells = []
        for handler in node.handlers:
            if handler.type is None:
                smells.append({
                    "line": handler.lineno,
                    "symbol": "<try-except>",
                    "rule": "DEFENSIVE_ERROR_HANDLING",
                    "severity": "high",
                    "message": "Bare 'except:' catch-all hides critical bugs.",
                    "recommendation": "Catch specific exception types (e.g. ValueError, KeyError) instead of bare except.",
                })
            elif isinstance(handler.type, ast.Name) and handler.type.id == "Exception":
                # Catching Base Exception
                # If body is just pass
                if len(handler.body) == 1 and isinstance(handler.body[0], ast.Pass):
                    smells.append({
                        "line": handler.lineno,
                        "symbol": "<try-except>",
                        "rule": "DEFENSIVE_ERROR_HANDLING",
                        "severity": "high",
                        "message": "Silent 'except Exception: pass' swallows unexpected failures.",
                        "recommendation": "Log or handle the exception explicitly instead of silent pass.",
                    })
        return smells

    def _calculate_max_nesting(self, statements: List[ast.stmt], current_depth: int = 1) -> int:
        max_d = current_depth
        for stmt in statements:
            child_stmts = []
            if isinstance(stmt, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                if isinstance(stmt, ast.If):
                    child_stmts.extend(stmt.body)
                    child_stmts.extend(stmt.orelse)
                elif isinstance(stmt, (ast.For, ast.While)):
                    child_stmts.extend(stmt.body)
                    child_stmts.extend(stmt.orelse)
                elif isinstance(stmt, ast.With):
                    child_stmts.extend(stmt.body)
                elif isinstance(stmt, ast.Try):
                    child_stmts.extend(stmt.body)
                    for h in stmt.handlers:
                        child_stmts.extend(h.body)
                    child_stmts.extend(stmt.orelse)
                    child_stmts.extend(stmt.finalbody)

                depth = self._calculate_max_nesting(child_stmts, current_depth + 1)
                if depth > max_d:
                    max_d = depth

        return max_d

    def _body_always_returns_or_raises(self, body: List[ast.stmt]) -> bool:
        if not body:
            return False
        last_stmt = body[-1]
        return isinstance(last_stmt, (ast.Return, ast.Raise))
