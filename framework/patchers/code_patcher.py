"""
Surgical Code Patcher with Auto-Strategy Selection, Syntax Validation & Rollback
Version: 1.0.0
"""

import ast
import difflib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from .ast_patcher import ASTPatcher
from .diff_applier import DiffApplier
from .fuzzy_matcher import FuzzyMatcher


@dataclass
class PatchResult:
    """Consolidated result of a surgical code patch operation."""

    success: bool
    modified_code: str
    original_code: str
    strategy_used: str
    blocks_applied: int = 0
    error: Optional[str] = None
    syntax_valid: bool = True
    diff_summary: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "strategy_used": self.strategy_used,
            "blocks_applied": self.blocks_applied,
            "syntax_valid": self.syntax_valid,
            "error": self.error,
            "diff_summary": self.diff_summary,
        }


class SurgicalCodePatcher:
    """
    Enterprise-grade surgical code patcher for AI agents.
    Provides robust multi-strategy patching, AST node replacement,
    fuzzy matching, post-patch syntax validation, and atomic rollbacks.
    Zero external dependencies.
    """

    def __init__(
        self,
        fuzzy_matcher: Optional[FuzzyMatcher] = None,
        ast_patcher: Optional[ASTPatcher] = None,
        diff_applier: Optional[DiffApplier] = None,
    ):
        self.fuzzy_matcher = fuzzy_matcher or FuzzyMatcher()
        self.ast_patcher = ast_patcher or ASTPatcher()
        self.diff_applier = diff_applier or DiffApplier(self.fuzzy_matcher)

    def _generate_diff(self, original: str, modified: str, filename: str = "target_file") -> str:
        """Generates a readable unified diff summary."""
        orig_lines = original.splitlines(keepends=True)
        mod_lines = modified.splitlines(keepends=True)
        diff = difflib.unified_diff(
            orig_lines,
            mod_lines,
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
            n=3,
        )
        return "".join(diff)

    def patch_string(
        self,
        source_code: str,
        patch_data: str,
        strategy: str = "auto",
        symbol_name: Optional[str] = None,
        is_python: bool = True,
    ) -> PatchResult:
        """
        Surgically patches source_code in-memory using the selected or detected strategy.
        """
        # Determine strategy
        chosen_strategy = strategy
        if strategy == "auto":
            if symbol_name:
                chosen_strategy = "ast_node"
            elif "<<<<<<< SEARCH" in patch_data:
                chosen_strategy = "search_replace"
            elif "@@ -" in patch_data:
                chosen_strategy = "unified_diff"
            else:
                chosen_strategy = "search_replace"

        # 1. AST Node Replacement
        if chosen_strategy == "ast_node":
            if not symbol_name:
                return PatchResult(
                    success=False,
                    modified_code=source_code,
                    original_code=source_code,
                    strategy_used=chosen_strategy,
                    error="Strategy 'ast_node' requires a valid 'symbol_name'.",
                )
            success, modified_code, err = self.ast_patcher.replace_symbol(
                source_code,
                symbol_name,
                patch_data,
            )
            if not success:
                return PatchResult(
                    success=False,
                    modified_code=source_code,
                    original_code=source_code,
                    strategy_used=chosen_strategy,
                    error=err,
                )
            diff = self._generate_diff(source_code, modified_code)
            return PatchResult(
                success=True,
                modified_code=modified_code,
                original_code=source_code,
                strategy_used=chosen_strategy,
                blocks_applied=1,
                diff_summary=diff,
            )

        # 2. Search/Replace Blocks (Aider style)
        elif chosen_strategy == "search_replace":
            blocks = self.diff_applier.parse_search_replace_blocks(patch_data)
            if not blocks:
                # Direct search/replace if only 1 block is given without delimiters
                # or fallback to direct fuzzy match if delimiter missing
                return PatchResult(
                    success=False,
                    modified_code=source_code,
                    original_code=source_code,
                    strategy_used=chosen_strategy,
                    error="No valid '<<<<<<< SEARCH ... ======= ... >>>>>>> REPLACE' blocks found.",
                )

            all_ok, modified_code, errors = self.diff_applier.apply_search_replace_blocks(
                source_code,
                blocks,
            )
            if not all_ok:
                return PatchResult(
                    success=False,
                    modified_code=source_code,
                    original_code=source_code,
                    strategy_used=chosen_strategy,
                    error="; ".join(errors),
                )

        # 3. Unified Diff
        elif chosen_strategy == "unified_diff":
            success, modified_code, err = self.diff_applier.apply_unified_diff(
                source_code,
                patch_data,
            )
            if not success:
                return PatchResult(
                    success=False,
                    modified_code=source_code,
                    original_code=source_code,
                    strategy_used=chosen_strategy,
                    error=err,
                )
        else:
            return PatchResult(
                success=False,
                modified_code=source_code,
                original_code=source_code,
                strategy_used=chosen_strategy,
                error=f"Unknown patch strategy: '{chosen_strategy}'.",
            )

        # Syntax Validation for Python files
        if is_python:
            try:
                ast.parse(modified_code)
            except SyntaxError as e:
                return PatchResult(
                    success=False,
                    modified_code=source_code,
                    original_code=source_code,
                    strategy_used=chosen_strategy,
                    syntax_valid=False,
                    error=f"SyntaxError in code after patch: {str(e)}",
                )

        diff = self._generate_diff(source_code, modified_code)
        return PatchResult(
            success=True,
            modified_code=modified_code,
            original_code=source_code,
            strategy_used=chosen_strategy,
            blocks_applied=len(blocks) if chosen_strategy == "search_replace" else 1,
            diff_summary=diff,
        )

    def patch_file(
        self,
        file_path: str,
        patch_data: str,
        strategy: str = "auto",
        symbol_name: Optional[str] = None,
        dry_run: bool = False,
    ) -> PatchResult:
        """
        Surgically patches a physical file on disk with automatic rollback if errors occur.
        """
        path = Path(file_path)
        if not path.exists():
            return PatchResult(
                success=False,
                modified_code="",
                original_code="",
                strategy_used=strategy,
                error=f"File '{file_path}' does not exist.",
            )

        try:
            original_code = path.read_text(encoding="utf-8")
        except Exception as e:
            return PatchResult(
                success=False,
                modified_code="",
                original_code="",
                strategy_used=strategy,
                error=f"Error reading file '{file_path}': {str(e)}",
            )

        is_python = path.suffix.lower() == ".py"
        res = self.patch_string(
            source_code=original_code,
            patch_data=patch_data,
            strategy=strategy,
            symbol_name=symbol_name,
            is_python=is_python,
        )

        if res.success and not dry_run:
            try:
                path.write_text(res.modified_code, encoding="utf-8")
            except Exception as e:
                return PatchResult(
                    success=False,
                    modified_code=original_code,
                    original_code=original_code,
                    strategy_used=res.strategy_used,
                    error=f"Failed to write patch to disk: {str(e)}",
                )

        return res
