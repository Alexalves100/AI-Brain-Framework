"""
Discovery Engine — structured information discovery
Version: 1.1.0
"""

import re
from pathlib import Path
from typing import List, Dict, Any
from ..core import Skill, SkillResult, SkillStatus, Context


class DiscoveryEngine(Skill):
    name = "discovery"
    version = "1.1.0"
    category = "discovery"
    description = "Discovers files, patterns, and structure in a codebase"

    DEFAULT_PATTERNS = {
        "python": [r"\.py$"],
        "markdown": [r"\.md$"],
        "config": [r"\.(json|ya?ml|toml)$"],
        "docs": [r"README\.md$", r"CHANGELOG\.md$"],
    }

    VALID_PATTERNS = ("all", "python", "markdown", "config", "docs")

    def run(self, context: Context) -> SkillResult:
        root_path = context.get("path", ".")
        pattern_type = context.get("pattern", "all")

        if not isinstance(root_path, str) or not root_path:
            return SkillResult(
                status=SkillStatus.ERROR,
                error="path must be a non-empty string",
            )
        if not isinstance(pattern_type, str) or pattern_type not in self.VALID_PATTERNS:
            return SkillResult(
                status=SkillStatus.ERROR,
                error=f"Invalid pattern '{pattern_type}'. Valid: {self.VALID_PATTERNS}",
            )

        root = Path(root_path)
        if not root.exists():
            return SkillResult(
                status=SkillStatus.ERROR,
                error=f"Path '{root_path}' not found",
            )

        files = self._scan(root, pattern_type)
        inventory = self._build_inventory(files, root)

        context.set("discovery_result", inventory)
        return SkillResult(
            status=SkillStatus.SUCCESS,
            output=inventory,
            metadata={"engine": "discovery"},
        )

    def _scan(self, root: Path, pattern_type: str) -> List[Path]:
        files = []
        skip_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv"}

        try:
            iterator = root.rglob("*")
        except OSError as e:
            return files

        for path in iterator:
            try:
                if path.is_file():
                    if any(p in path.parts for p in skip_dirs):
                        continue
                    if pattern_type == "all" or self._matches(path, pattern_type):
                        files.append(path)
            except OSError:
                # Arquivo inacessível: ignora e continua
                continue

        return sorted(files)

    def _matches(self, path: Path, pattern_type: str) -> bool:
        patterns = self.DEFAULT_PATTERNS.get(pattern_type, [])
        return any(re.search(p, str(path)) for p in patterns)

    def _build_inventory(self, files: List[Path], root: Path) -> Dict[str, Any]:
        by_type: Dict[str, int] = {}
        total_size = 0
        sample: List[str] = []
        for f in files:
            ext = f.suffix or "no-ext"
            by_type[ext] = by_type.get(ext, 0) + 1
            try:
                total_size += f.stat().st_size
            except OSError:
                pass
            if len(sample) < 10:
                try:
                    sample.append(str(f.relative_to(root)))
                except ValueError:
                    sample.append(str(f))

        return {
            "total_files": len(files),
            "total_size_bytes": total_size,
            "by_extension": by_type,
            "sample": sample,
        }
