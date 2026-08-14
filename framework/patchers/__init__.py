"""
Surgical Code Patcher Module
Version: 1.0.0
"""

from .ast_patcher import ASTPatcher
from .code_patcher import PatchResult, SurgicalCodePatcher
from .diff_applier import DiffApplier, SearchReplaceBlock
from .fuzzy_matcher import FuzzyMatcher

__all__ = [
    "SurgicalCodePatcher",
    "PatchResult",
    "ASTPatcher",
    "FuzzyMatcher",
    "DiffApplier",
    "SearchReplaceBlock",
]
