"""
Discovery Engine — structured information discovery
Version: 1.0.0
"""

import re
from pathlib import Path
from typing import List, Dict, Any
from ..core import Skill, SkillResult, SkillStatus, Context


class DiscoveryEngine(Skill):
    name = "discovery"
    version = "1.0.0"
    category = "discovery"
    description = "Discovers files, patterns, and structure in a codebase"

    DEFAULT_PATTERNS = {
        "python": [r"\.py$"],
        "markdown": [r"\.md$"],
        "config": [r"\.(json|ya?ml|toml)$"],
        "docs": [r"README\.md$", r"CHANGELOG\.md$"],
    }

    def run(self, context: Context) -> SkillResult:
        root_path = context.get("path", ".")
        pattern_type = context.get("pattern", "all")

        root = Path(root_path)
        if not root.exists():
            return SkillResult(
                status=SkillStatus.ERROR,
                error=f"Path '{root_path}' not found",
            )

        files = self._scan(root, pattern_type)
        inventory = self._build_inventory(files)

        context.set("discovery_result", inventory)
        return SkillResult(
            status=SkillStatus.SUCCESS,
            output=inventory,
            metadata={"engine": "discovery"},
        )

    def _scan(self, root: Path, pattern_type: str) -> List[Path]:
        files = []
        skip_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv"}

        for path in root.rglob("*"):
            if path.is_file():
                if any(p in path.parts for p in skip_dirs):
                    continue
                if pattern_type == "all" or self._matches(path, pattern_type):
                    files.append(path)

        return sorted(files)

    def _matches(self, path: Path, pattern_type: str) -> bool:
        patterns = self.DEFAULT_PATTERNS.get(pattern_type, [])
        return any(re.search(p, str(path)) for p in patterns)

    def _build_inventory(self, files: List[Path]) -> Dict[str, Any]:
        by_type: Dict[str, int] = {}
        total_size = 0
        for f in files:
            ext = f.suffix or "no-ext"
            by_type[ext] = by_type.get(ext, 0) + 1
            try:
                total_size += f.stat().st_size
            except OSError:
                pass

        return {
            "total_files": len(files),
            "total_size_bytes": total_size,
            "by_extension": by_type,
            "sample": [str(f.relative_to(f.parents[-1])) for f in files[:10]],
        }
