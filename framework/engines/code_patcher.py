"""
Code Patcher Engine Skill
Version: 1.0.0
"""

from typing import Any, Dict, Optional

from ..core.context import Context
from ..core.skill import Skill, SkillResult, SkillStatus
from ..patchers.code_patcher import SurgicalCodePatcher


class CodePatcherEngine(Skill):
    """
    Skill for surgically applying patches to source code files and strings
    with zero external dependencies and automatic syntax rollback.
    """

    name = "code_patcher"
    version = "1.0.0"
    category = "engineering"
    description = "Applies surgical code patches via AST replacement, Search/Replace blocks, or Unified Diffs."

    def __init__(self, patcher: Optional[SurgicalCodePatcher] = None, **kwargs: Any):
        super().__init__(**kwargs)
        self.patcher = patcher or SurgicalCodePatcher()


    def validate_inputs(self, context: Context) -> bool:
        has_file = bool(context.get("file_path"))
        has_source = bool(context.get("source_code") or context.get("code"))
        has_patch = bool(context.get("patch_data") or context.get("patch"))
        return (has_file or has_source) and has_patch

    def run(self, context: Context) -> SkillResult:
        file_path = context.get("file_path")
        source_code = context.get("source_code") or context.get("code")
        patch_data = context.get("patch_data") or context.get("patch", "")
        strategy = context.get("strategy", "auto")
        symbol_name = context.get("symbol_name")
        dry_run = bool(context.get("dry_run", False))

        if file_path:
            result = self.patcher.patch_file(
                file_path=file_path,
                patch_data=patch_data,
                strategy=strategy,
                symbol_name=symbol_name,
                dry_run=dry_run,
            )
        else:
            result = self.patcher.patch_string(
                source_code=source_code,
                patch_data=patch_data,
                strategy=strategy,
                symbol_name=symbol_name,
            )

        output: Dict[str, Any] = result.to_dict()
        if result.success:
            output["modified_code"] = result.modified_code
            context.set("patch_result", output)
            context.set("modified_code", result.modified_code)
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output=output,
                metadata={"engine": self.name, "strategy": result.strategy_used},
            )
        else:
            context.set("patch_result", output)
            return SkillResult(
                status=SkillStatus.ERROR,
                error=result.error or "Failed to apply surgical patch",
                output=output,
                metadata={"engine": self.name},
            )
