"""
Complexity Analyzer — analyzes code complexity
Version: 1.0.0
"""

import re
from pathlib import Path
from typing import Any, Dict


class ComplexityAnalyzer:
    """Analyzes cyclomatic and cognitive complexity of source files."""

    KEYWORDS = re.compile(
        r"\b(if|elif|else|for|while|and|or|except|case|when)\b"
    )

    def cyclomatic_complexity(self, content: str) -> int:
        return 1 + len(self.KEYWORDS.findall(content))

    def cognitive_complexity(self, content: str) -> int:
        score = 0
        nesting = 0
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            nesting += stripped.count("(") - stripped.count(")")
            if self.KEYWORDS.search(stripped):
                score += 1 + max(0, nesting // 2)
        return score

    def analyze_file(self, path: Path) -> Dict[str, Any]:
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return {"file": str(path), "error": "cannot read"}

        lines = content.splitlines()
        non_blank = [line for line in lines if line.strip()]


        return {
            "file": str(path),
            "total_lines": len(lines),
            "code_lines": len(non_blank),
            "cyclomatic": self.cyclomatic_complexity(content),
            "cognitive": self.cognitive_complexity(content),
            "comment_ratio": round(
                (len(lines) - len(non_blank)) / max(len(lines), 1), 3
            ),
        }

    def analyze_directory(self, root: str = ".") -> Dict[str, Any]:
        root_path = Path(root)
        skip = {".git", "__pycache__", "node_modules", ".venv", "venv"}

        results = []
        for path in root_path.rglob("*.py"):
            if any(s in path.parts for s in skip):
                continue
            results.append(self.analyze_file(path))

        if not results:
            return {"files": 0, "avg_cyclomatic": 0, "avg_cognitive": 0}

        avg_cyc = sum(r.get("cyclomatic", 0) for r in results) / len(results)
        avg_cog = sum(r.get("cognitive", 0) for r in results) / len(results)

        return {
            "files": len(results),
            "avg_cyclomatic": round(avg_cyc, 2),
            "avg_cognitive": round(avg_cog, 2),
            "max_cyclomatic": max((r.get("cyclomatic", 0) for r in results), default=0),
            "results": results[:50],
        }
