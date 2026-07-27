"""
Quality Analyzer — measures code quality metrics
Version: 1.0.0
"""

import re
from pathlib import Path
from typing import Dict, Any


class QualityAnalyzer:
    """Measures code quality via heuristics."""

    def analyze_file(self, path: Path) -> Dict[str, Any]:
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return {"file": str(path), "score": 0}

        score = 100
        issues = []

        if len(content.splitlines()) > 500:
            score -= 10
            issues.append("file too long")

        if "TODO" in content:
            score -= 5
            issues.append("contains TODO")
        if "FIXME" in content:
            score -= 10
            issues.append("contains FIXME")
        if "print(" in content and "test" not in str(path):
            score -= 3
            issues.append("contains print statement")

        if re.search(r"except\s*:", content):
            score -= 15
            issues.append("bare except")

        if re.search(r"^\s*pass\s*$", content, re.M):
            score -= 5
            issues.append("contains pass")

        docstring_count = len(re.findall(r'"""', content))
        if docstring_count < 2 and "test" not in str(path):
            score -= 5
            issues.append("missing module docstring")

        return {
            "file": str(path),
            "score": max(0, score),
            "issues": issues,
            "lines": len(content.splitlines()),
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
            return {"files": 0, "avg_score": 0}

        avg = sum(r["score"] for r in results) / len(results)

        return {
            "files": len(results),
            "avg_score": round(avg, 2),
            "min_score": min(r["score"] for r in results),
            "max_score": max(r["score"] for r in results),
            "results": results[:50],
        }
