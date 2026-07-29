"""
Metrics Analyzer — aggregates project metrics
Version: 1.0.0
"""

from pathlib import Path
from typing import Dict, Any


class MetricsAnalyzer:
    """Aggregates project-level metrics."""

    def analyze(self, root: str = ".") -> Dict[str, Any]:
        root_path = Path(root)
        skip = {".git", "__pycache__", "node_modules", ".venv", "venv"}

        total_files = 0
        total_lines = 0
        total_size = 0
        by_ext: Dict[str, Dict[str, int]] = {}

        for path in root_path.rglob("*"):
            if not path.is_file():
                continue
            if any(s in path.parts for s in skip):
                continue

            ext = path.suffix or "no-ext"
            total_files += 1

            size = 0
            lines = 0
            try:
                size = path.stat().st_size
                total_size += size
                if ext in (".py", ".js", ".ts", ".md", ".txt"):
                    lines = len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
                    total_lines += lines
            except OSError:
                # Arquivo inacessível: contabiliza apenas presença, não tamanho nem linhas
                pass

            by_ext.setdefault(ext, {"files": 0, "lines": 0, "size": 0})
            by_ext[ext]["files"] += 1
            by_ext[ext]["size"] += size
            by_ext[ext]["lines"] += lines

        return {
            "total_files": total_files,
            "total_lines": total_lines,
            "total_size_bytes": total_size,
            "by_extension": by_ext,
        }
