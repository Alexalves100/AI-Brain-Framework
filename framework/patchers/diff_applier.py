"""
Unified Diff & Search/Replace Block Parser and Applier
Version: 1.0.0
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

from .fuzzy_matcher import FuzzyMatcher


@dataclass
class SearchReplaceBlock:
    search: str
    replace: str


class DiffApplier:
    """
    Parses and applies Search/Replace block formats and standard Unified Diffs.
    Zero external dependencies.
    """

    SEARCH_REPLACE_PATTERN = re.compile(
        r"<{5,9}\s*SEARCH\s*\n(.*?)\n={5,9}\s*\n(.*?)\n>{5,9}\s*REPLACE",
        re.DOTALL,
    )

    def __init__(self, fuzzy_matcher: Optional[FuzzyMatcher] = None):
        self.fuzzy_matcher = fuzzy_matcher or FuzzyMatcher()

    def parse_search_replace_blocks(self, patch_text: str) -> List[SearchReplaceBlock]:
        """Extracts all SEARCH/REPLACE blocks from a patch text."""
        blocks: List[SearchReplaceBlock] = []
        for match in self.SEARCH_REPLACE_PATTERN.finditer(patch_text):
            search_content = match.group(1)
            replace_content = match.group(2)
            blocks.append(SearchReplaceBlock(search=search_content, replace=replace_content))
        return blocks

    def apply_search_replace_blocks(
        self,
        original_text: str,
        blocks: List[SearchReplaceBlock],
    ) -> Tuple[bool, str, List[str]]:
        """
        Applies a list of SEARCH/REPLACE blocks sequentially to original_text.
        Returns (all_succeeded, modified_text, errors).
        """
        current_text = original_text
        errors: List[str] = []

        for idx, block in enumerate(blocks):
            success, new_text, conf = self.fuzzy_matcher.replace_block(
                current_text,
                block.search,
                block.replace,
            )
            if not success:
                errors.append(f"Block #{idx + 1} could not be matched (confidence: {conf:.2f}).")
            else:
                current_text = new_text

        all_ok = len(errors) == 0
        return all_ok, current_text, errors

    def apply_unified_diff(
        self,
        original_text: str,
        diff_text: str,
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Applies a standard Unified Diff to original_text.
        Returns (success, modified_text, error_message).
        """
        orig_lines = original_text.splitlines()
        diff_lines = diff_text.splitlines()

        hunk_header_re = re.compile(r"^@@\s*-(\d+)(?:,(\d+))?\s+\+(\d+)(?:,(\d+))?\s+@@")

        result_lines = list(orig_lines)
        line_offset = 0
        hunk_found = False

        i = 0
        while i < len(diff_lines):
            line = diff_lines[i]
            m = hunk_header_re.match(line)
            if m:
                hunk_found = True
                orig_start = int(m.group(1)) - 1  # 0-indexed
                # Parse hunk lines
                i += 1
                hunk_orig: List[str] = []
                hunk_new: List[str] = []

                while i < len(diff_lines) and not hunk_header_re.match(diff_lines[i]):
                    hline = diff_lines[i]
                    if hline.startswith("---") or hline.startswith("+++"):
                        i += 1
                        continue
                    if hline.startswith("-"):
                        hunk_orig.append(hline[1:])
                    elif hline.startswith("+"):
                        hunk_new.append(hline[1:])
                    elif hline.startswith(" "):
                        hunk_orig.append(hline[1:])
                        hunk_new.append(hline[1:])
                    elif not hline:
                        # empty context line
                        hunk_orig.append("")
                        hunk_new.append("")
                    i += 1

                # Search where hunk_orig fits near (orig_start + line_offset)
                search_block = "\n".join(hunk_orig)
                replace_block = "\n".join(hunk_new)
                current_content = "\n".join(result_lines)

                success, updated_content, _ = self.fuzzy_matcher.replace_block(
                    current_content,
                    search_block,
                    replace_block,
                )
                if not success:
                    return False, original_text, f"Failed to apply hunk starting at line {orig_start + 1}"

                result_lines = updated_content.splitlines()
                line_offset += len(hunk_new) - len(hunk_orig)
            else:
                i += 1

        if not hunk_found:
            return False, original_text, "No valid unified diff hunks found in input."

        final_text = "\n".join(result_lines)
        if original_text.endswith("\n") and not final_text.endswith("\n"):
            final_text += "\n"

        return True, final_text, None
