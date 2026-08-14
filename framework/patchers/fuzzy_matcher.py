"""
Fuzzy Block Matcher with Whitespace & Indentation Tolerance
Version: 1.0.0
"""

import difflib
from typing import Optional, Tuple


class FuzzyMatcher:
    """
    Locates and replaces target code blocks inside files with tolerance
    to minor indentation, whitespace, and line break variations (inspired by Aider).
    Zero external dependencies.
    """

    def __init__(self, default_threshold: float = 0.8):
        self.default_threshold = default_threshold

    def find_match(
        self,
        original_text: str,
        search_block: str,
        threshold: Optional[float] = None,
    ) -> Tuple[bool, int, int, float]:
        """
        Finds the line range (start_line_0_indexed, end_line_0_indexed) of search_block in original_text.
        Returns (found, start_line, end_line, confidence).
        """
        th = threshold if threshold is not None else self.default_threshold

        # 1. Exact Substring Match
        if search_block in original_text:
            before = original_text[: original_text.index(search_block)]
            start_line = before.count("\n")
            lines_count = search_block.count("\n") + 1
            return True, start_line, start_line + lines_count, 1.0

        orig_lines = original_text.splitlines()
        search_lines = search_block.splitlines()

        if not search_lines or len(search_lines) > len(orig_lines):
            return False, -1, -1, 0.0

        # 2. Normalized Line-by-Line Sliding Window Match
        norm_search = [line.strip() for line in search_lines]
        window_size = len(search_lines)
        best_ratio = 0.0
        best_start = -1

        for i in range(len(orig_lines) - window_size + 1):
            window = [orig_lines[i + j].strip() for j in range(window_size)]
            matcher = difflib.SequenceMatcher(None, window, norm_search)
            ratio = matcher.ratio()

            if ratio > best_ratio:
                best_ratio = ratio
                best_start = i

            if ratio == 1.0:
                break

        if best_ratio >= th and best_start != -1:
            return True, best_start, best_start + window_size, best_ratio

        # 3. Flexible Window Match (window_size ± 2 lines for slight insertions/deletions)
        for offset in (-1, 1, -2, 2):
            w_size = window_size + offset
            if w_size <= 0 or w_size > len(orig_lines):
                continue

            for i in range(len(orig_lines) - w_size + 1):
                window = [orig_lines[i + j].strip() for j in range(w_size)]
                matcher = difflib.SequenceMatcher(None, window, norm_search)
                ratio = matcher.ratio()

                if ratio > best_ratio:
                    best_ratio = ratio
                    best_start = i
                    window_size = w_size

        if best_ratio >= th and best_start != -1:
            return True, best_start, best_start + window_size, best_ratio

        return False, -1, -1, best_ratio

    def replace_block(
        self,
        original_text: str,
        search_block: str,
        replace_block: str,
        threshold: Optional[float] = None,
    ) -> Tuple[bool, str, float]:
        """
        Replaces search_block with replace_block in original_text using fuzzy matching.
        Returns (success, modified_text, confidence).
        """
        # Quick exact replace
        if search_block in original_text:
            return True, original_text.replace(search_block, replace_block, 1), 1.0

        found, start_line, end_line, conf = self.find_match(original_text, search_block, threshold)
        if not found:
            return False, original_text, conf

        orig_lines = original_text.splitlines(keepends=True)
        replace_lines = replace_block.splitlines(keepends=True)

        # Detect indentation of the first line in the target region
        target_first_line = orig_lines[start_line] if start_line < len(orig_lines) else ""
        target_indent = len(target_first_line) - len(target_first_line.lstrip())

        # If replace_lines have no indentation but target had indentation, adjust
        adjusted_replace = []
        search_first_line = search_block.splitlines()[0] if search_block.splitlines() else ""
        search_indent = len(search_first_line) - len(search_first_line.lstrip())
        indent_delta = target_indent - search_indent

        for r_line in replace_lines:
            if indent_delta > 0 and r_line.strip():
                adjusted_replace.append(" " * indent_delta + r_line)
            else:
                adjusted_replace.append(r_line)

        # Rebuild file
        new_lines = orig_lines[:start_line] + adjusted_replace + orig_lines[end_line:]
        result_text = "".join(new_lines)

        return True, result_text, conf
