"""
Structure Scanner — scans project structure
Version: 1.0.0
"""

from pathlib import Path
from typing import Dict, Any, List


class StructureScanner:
    """Scans project directory structure."""

    REQUIRED_FILES = ["README.md", "LICENSE", ".gitignore"]
    REQUIRED_DIRS = ["tests", "docs"]

    def scan(self, root: str = ".") -> Dict[str, Any]:
        root_path = Path(root)
        if not root_path.exists():
            return {"error": f"Path '{root}' not found"}

        all_files = []
        all_dirs = []
        skip = {".git", "__pycache__", "node_modules", ".venv", "venv", ".pytest_cache"}

        for p in root_path.rglob("*"):
            if any(s in p.parts for s in skip):
                continue
            if p.is_file():
                all_files.append(p)
            else:
                all_dirs.append(p)

        missing_files = [
            f for f in self.REQUIRED_FILES
            if not (root_path / f).exists()
        ]
        missing_dirs = [
            d for d in self.REQUIRED_DIRS
            if not (root_path / d).is_dir()
        ]

        max_depth = max(
            (len(p.relative_to(root_path).parts) for p in all_files),
            default=0,
        )

        return {
            "total_files": len(all_files),
            "total_dirs": len(all_dirs),
            "max_depth": max_depth,
            "missing_files": missing_files,
            "missing_dirs": missing_dirs,
            "has_tests": (root_path / "tests").is_dir(),
            "has_docs": (root_path / "docs").is_dir(),
            "has_ci": any(
                (root_path / ".github" / "workflows").glob("*.yml")
                if (root_path / ".github" / "workflows").exists()
                else []
            ),
        }
