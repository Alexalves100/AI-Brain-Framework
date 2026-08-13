"""
AST Scanner — semantic symbol analysis and skeleton generation
Version: 1.0.0
"""

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union


class ASTScanner:
    """
    AST-based code intelligence inspired by Serena MCP.
    Extracts structural skeletons, symbols, signatures, and targeted symbol bodies
    without external dependencies (pure Python standard library).
    """

    def __init__(self, keep_docstrings: bool = True, max_docstring_lines: int = 2):
        self.keep_docstrings = keep_docstrings
        self.max_docstring_lines = max_docstring_lines

    def parse_ast(self, code: str) -> Optional[ast.AST]:
        """Safely parses code into an AST tree."""
        try:
            return ast.parse(code)
        except SyntaxError:
            return None

    def get_symbols_overview(self, code: str, file_path: str = "") -> str:
        """
        Generates a compact structural skeleton (.pyi style) of classes,
        functions, methods, and constants, replacing bodies with '...'.
        Preserves decorators, type annotations, and essential docstrings.
        """
        tree = self.parse_ast(code)
        if tree is None:
            # Fallback for non-Python or syntax-error code
            return self._fallback_skeleton(code)

        lines = code.splitlines()
        skeleton_lines: List[str] = []

        if file_path:
            skeleton_lines.append(f"# Symbols overview for: {file_path}")

        # Top-level docstring
        doc = ast.get_docstring(tree)
        if doc and self.keep_docstrings:
            doc_snippet = self._format_docstring(doc, indent=0)
            skeleton_lines.extend(doc_snippet)

        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                # Include imports as they provide critical type/dependency context
                skeleton_lines.append(self._get_raw_node_text(node, lines))
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                # Keep top-level constants / type aliases
                assign_text = self._format_assignment(node, lines)
                if assign_text:
                    skeleton_lines.append(assign_text)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                skeleton_lines.extend(self._format_function_stub(node, lines, indent_level=0))
            elif isinstance(node, ast.ClassDef):
                skeleton_lines.extend(self._format_class_stub(node, lines, indent_level=0))

        result = "\n".join(skeleton_lines)
        return self._normalize_spacing(result)

    def list_symbols(self, code: str) -> List[Dict[str, Any]]:
        """
        Returns a structured index of all classes, methods, and functions.
        """
        tree = self.parse_ast(code)
        if tree is None:
            return []

        symbols: List[Dict[str, Any]] = []
        lines = code.splitlines()

        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                kind = "async_function" if isinstance(node, ast.AsyncFunctionDef) else "function"
                symbols.append({
                    "name": node.name,
                    "kind": kind,
                    "line_start": node.lineno,
                    "line_end": getattr(node, "end_lineno", node.lineno),
                    "signature": self._get_signature_header(node, lines),
                    "docstring": ast.get_docstring(node) or "",
                })
            elif isinstance(node, ast.ClassDef):
                symbols.append({
                    "name": node.name,
                    "kind": "class",
                    "line_start": node.lineno,
                    "line_end": getattr(node, "end_lineno", node.lineno),
                    "signature": f"class {node.name}",
                    "docstring": ast.get_docstring(node) or "",
                })
                # Methods within class
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        m_kind = "async_method" if isinstance(item, ast.AsyncFunctionDef) else "method"
                        symbols.append({
                            "name": f"{node.name}.{item.name}",
                            "kind": m_kind,
                            "line_start": item.lineno,
                            "line_end": getattr(item, "end_lineno", item.lineno),
                            "signature": self._get_signature_header(item, lines),
                            "docstring": ast.get_docstring(item) or "",
                        })

        return symbols

    def get_symbol_body(self, code: str, symbol_name: str) -> Optional[str]:
        """
        Retrieves the exact, complete source code of a specific class or function/method.
        e.g. symbol_name="AuthService" or symbol_name="AuthService.login" or symbol_name="my_func".
        """
        tree = self.parse_ast(code)
        if tree is None:
            return None

        lines = code.splitlines()

        parts = symbol_name.split(".")
        if len(parts) == 1:
            target_name = parts[0]
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == target_name:
                    return self._get_full_node_source(node, lines)
        elif len(parts) == 2:
            class_name, method_name = parts
            for node in tree.body:
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == method_name:
                            return self._get_full_node_source(item, lines)

        return None

    def find_references(self, code: str, symbol_name: str) -> List[Dict[str, Any]]:
        """
        Locates all referencing lines of a symbol in the given code.
        """
        tree = self.parse_ast(code)
        if tree is None:
            return []

        lines = code.splitlines()
        references = []

        target_base = symbol_name.split(".")[-1]

        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == target_base:
                line_no = getattr(node, "lineno", 0)
                if line_no > 0 and line_no <= len(lines):
                    references.append({
                        "line": line_no,
                        "snippet": lines[line_no - 1].strip(),
                    })
            elif isinstance(node, ast.Attribute) and node.attr == target_base:
                line_no = getattr(node, "lineno", 0)
                if line_no > 0 and line_no <= len(lines):
                    references.append({
                        "line": line_no,
                        "snippet": lines[line_no - 1].strip(),
                    })

        # Deduplicate by line number
        unique = []
        seen = set()
        for ref in references:
            if ref["line"] not in seen:
                seen.add(ref["line"])
                unique.append(ref)

        return sorted(unique, key=lambda x: x["line"])

    def minify_code(self, code: str) -> str:
        """
        Minifies code by stripping comments and redundant whitespace,
        retaining valid Python formatting.
        """
        cleaned_lines = []
        for line in code.splitlines():
            # Remove inline comments (simple safe regex)
            stripped = re.sub(r"#.*$", "", line).rstrip()
            if stripped:
                cleaned_lines.append(stripped)

        # Collapse excess empty lines
        compact = "\n".join(cleaned_lines)
        compact = re.sub(r"\n{3,}", "\n\n", compact)
        return compact

    # --- Internal Helpers ---

    def _get_raw_node_text(self, node: ast.AST, lines: List[str]) -> str:
        start = node.lineno - 1
        end = getattr(node, "end_lineno", node.lineno)
        return "\n".join(lines[start:end])

    def _get_full_node_source(self, node: ast.AST, lines: List[str]) -> str:
        # Include decorators if present
        start_line = node.lineno
        if hasattr(node, "decorator_list") and node.decorator_list:
            start_line = min(d.lineno for d in node.decorator_list)

        end_line = getattr(node, "end_lineno", node.lineno)
        return "\n".join(lines[start_line - 1 : end_line])

    def _get_signature_header(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], lines: List[str]) -> str:
        # Extract lines from first decorator or def line up to ':' before body
        start_line = node.lineno
        if node.decorator_list:
            start_line = min(d.lineno for d in node.decorator_list)

        body_start = node.body[0].lineno if node.body else node.lineno
        sig_lines = lines[start_line - 1 : body_start]
        sig_text = "\n".join(sig_lines)
        # Find closing colon of def
        match = re.search(r"(def\s+[\s\S]*?\)):", sig_text)
        if match:
            return match.group(1)
        return lines[node.lineno - 1].strip()

    def _format_docstring(self, doc: str, indent: int = 0) -> List[str]:
        pad = "    " * indent
        doc_lines = doc.strip().splitlines()
        if len(doc_lines) > self.max_docstring_lines:
            doc_lines = doc_lines[: self.max_docstring_lines] + ["..."]

        if len(doc_lines) == 1 and not doc_lines[0].endswith("..."):
            return [f'{pad}"""{doc_lines[0]}"""']

        res = [f'{pad}"""']
        for dl in doc_lines:
            res.append(f"{pad}{dl}")
        res.append(f'{pad}"""')
        return res

    def _format_assignment(self, node: Union[ast.Assign, ast.AnnAssign], lines: List[str]) -> Optional[str]:
        raw = self._get_raw_node_text(node, lines)
        # Keep uppercase constants, __all__, __version__, etc.
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and (target.id.isupper() or target.id.startswith("__")):
                    return raw
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and (node.target.id.isupper() or node.target.id.startswith("__")):
                return raw
        return None

    def _format_function_stub(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], lines: List[str], indent_level: int
    ) -> List[str]:
        pad = "    " * indent_level
        out: List[str] = []

        # Decorators
        for dec in node.decorator_list:
            dec_text = self._get_raw_node_text(dec, lines).strip()
            if not dec_text.startswith("@"):
                dec_text = f"@{dec_text}"
            out.append(f"{pad}{dec_text}")

        # Signature lines
        def_start = node.lineno - 1
        body_start = node.body[0].lineno - 1 if node.body else def_start + 1

        header_lines = lines[def_start:body_start]
        # Reconstruct header indentation
        for idx, hl in enumerate(header_lines):
            stripped = hl.strip()
            if idx == 0:
                out.append(f"{pad}{stripped}")
            else:
                out.append(f"{pad}    {stripped}")

        # Ensure header ends with ':'
        if not out[-1].endswith(":"):
            out[-1] = out[-1] + ":"

        # Docstring
        doc = ast.get_docstring(node)
        if doc and self.keep_docstrings:
            out.extend(self._format_docstring(doc, indent=indent_level + 1))

        # Body replaced with ...
        out.append(f"{pad}    ...")
        return out

    def _format_class_stub(self, node: ast.ClassDef, lines: List[str], indent_level: int) -> List[str]:
        pad = "    " * indent_level
        out: List[str] = []

        # Decorators
        for dec in node.decorator_list:
            dec_text = self._get_raw_node_text(dec, lines).strip()
            if not dec_text.startswith("@"):
                dec_text = f"@{dec_text}"
            out.append(f"{pad}{dec_text}")

        # Class header line
        class_line = lines[node.lineno - 1].strip()
        if not class_line.endswith(":"):
            class_line += ":"
        out.append(f"{pad}{class_line}")

        # Class docstring
        doc = ast.get_docstring(node)
        if doc and self.keep_docstrings:
            out.extend(self._format_docstring(doc, indent=indent_level + 1))

        # Member methods / attributes
        has_members = False
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                has_members = True
                out.extend(self._format_function_stub(item, lines, indent_level=indent_level + 1))
            elif isinstance(item, (ast.Assign, ast.AnnAssign)):
                assign_text = self._format_assignment(item, lines)
                if assign_text:
                    has_members = True
                    out.append(f"{pad}    {assign_text.strip()}")

        if not has_members:
            out.append(f"{pad}    ...")

        return out

    def _normalize_spacing(self, text: str) -> str:
        # Avoid more than 2 consecutive blank lines
        return re.sub(r"\n{3,}", "\n\n", text).strip()

    def _fallback_skeleton(self, text: str) -> str:
        # Simple line-based skeleton fallback for non-python code
        out = []
        for line in text.splitlines():
            if re.match(r"^\s*(class|def|async def|function|export|interface|type)\b", line):
                out.append(line)
        return "\n".join(out) if out else text[:200]
