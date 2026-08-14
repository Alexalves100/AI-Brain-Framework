"""
Structural AST Node Patcher for Targeted Class & Function Replacement
Version: 1.0.0
"""

import ast
from typing import Optional, Tuple


class ASTPatcher:
    """
    Surgically replaces a specific function, method, or class in Python source code
    using AST structural location (inspired by ast-grep).
    Zero external dependencies.
    """

    def find_symbol_range(self, source_code: str, symbol_name: str) -> Tuple[bool, int, int]:
        """
        Finds the 1-indexed (start_line, end_line) of the targeted symbol.
        Supports dotted paths (e.g. "AuthService.login").
        """
        try:
            tree = ast.parse(source_code)
        except Exception:
            return False, -1, -1

        parts = symbol_name.split(".")
        current_scope = tree.body
        target_node: Optional[ast.AST] = None

        for idx, part in enumerate(parts):
            matched = False
            for node in current_scope:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == part:
                    if idx == len(parts) - 1:
                        target_node = node
                        matched = True
                        break
                    elif isinstance(node, ast.ClassDef):
                        current_scope = node.body
                        matched = True
                        break
            if not matched:
                return False, -1, -1

        if not target_node:
            return False, -1, -1

        # Determine start line (accounting for decorators)
        start_line = int(getattr(target_node, "lineno", 1))
        dec_list = getattr(target_node, "decorator_list", None)
        if dec_list:
            first_dec = dec_list[0]
            start_line = min(start_line, int(getattr(first_dec, "lineno", start_line)))

        # Determine end line
        raw_end = getattr(target_node, "end_lineno", None)
        if raw_end is None:
            # Fallback for older python or synthesized nodes: calculate max lineno among children
            end_line = int(max(
                (int(getattr(n, "lineno", start_line)) for n in ast.walk(target_node)),
                default=start_line,
            ))
        else:
            end_line = int(raw_end)

        return True, start_line, end_line


    def replace_symbol(
        self,
        source_code: str,
        symbol_name: str,
        new_symbol_code: str,
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Surgically replaces the symbol definition with new_symbol_code.
        Returns (success, modified_source_code, error_message).
        """
        found, start_line, end_line = self.find_symbol_range(source_code, symbol_name)
        if not found:
            return False, source_code, f"Symbol '{symbol_name}' not found in source code."

        lines = source_code.splitlines(keepends=True)
        # start_line and end_line are 1-indexed
        orig_start_idx = start_line - 1
        orig_end_idx = end_line

        # Detect original indentation of the first line
        target_first_line = lines[orig_start_idx] if orig_start_idx < len(lines) else ""
        target_indent = len(target_first_line) - len(target_first_line.lstrip())

        # Format new symbol lines with matching indentation
        new_lines_raw = new_symbol_code.splitlines(keepends=True)
        if not new_lines_raw:
            return False, source_code, "Replacement code is empty."

        first_raw = new_lines_raw[0]
        raw_indent = len(first_raw) - len(first_raw.lstrip())
        indent_delta = target_indent - raw_indent

        adjusted_new_lines = []
        for line in new_lines_raw:
            if indent_delta > 0 and line.strip():
                adjusted_new_lines.append(" " * indent_delta + line)
            elif indent_delta < 0 and line.startswith(" " * abs(indent_delta)):
                adjusted_new_lines.append(line[abs(indent_delta):])
            else:
                adjusted_new_lines.append(line)

        # Ensure last line ends with newline if necessary
        if adjusted_new_lines and not adjusted_new_lines[-1].endswith(("\n", "\r\n")):
            adjusted_new_lines[-1] = adjusted_new_lines[-1] + "\n"

        modified_lines = lines[:orig_start_idx] + adjusted_new_lines + lines[orig_end_idx:]
        modified_source = "".join(modified_lines)

        # Syntax check on resulting file
        try:
            ast.parse(modified_source)
        except SyntaxError as e:
            return False, source_code, f"SyntaxError in modified code after replacing '{symbol_name}': {str(e)}"

        return True, modified_source, None
