"""
Code Scanner — scans source files for issues
Version: 1.0.0
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class CodeScanner:
    """Scans source files for code quality and security issues."""

    PATTERNS = {
        "TODO": re.compile(r"#\s*TODO\b", re.I),
        "FIXME": re.compile(r"#\s*FIXME\b", re.I),
        "XXX": re.compile(r"#\s*XXX\b", re.I),
        "print_debug": re.compile(r"\bprint\s*\(\s*['\"](debug|test|tmp)", re.I),
        "long_line": re.compile(r"^.{121,}$"),
        "broad_except": re.compile(r"except\s*:\s*$"),
        "magic_number": re.compile(r"\b\d{3,}\b"),
    }

    SEVERITY = {
        "TODO": "low",
        "FIXME": "medium",
        "XXX": "medium",
        "print_debug": "low",
        "long_line": "low",
        "broad_except": "high",
        "magic_number": "low",
    }

    def scan_file(self, path: Path) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return findings

        for line_no, line in enumerate(content.splitlines(), 1):
            for name, pattern in self.PATTERNS.items():
                if pattern.search(line):
                    findings.append({
                        "file": str(path),
                        "line": line_no,
                        "type": name,
                        "severity": self.SEVERITY[name],
                        "snippet": line.strip()[:100],
                    })
        return findings

    def scan_directory(self, root: str = ".", extensions: Optional[List[str]] = None) -> Dict[str, Any]:
        exts = extensions or [".py", ".js", ".ts"]
        root_path = Path(root)
        skip = {".git", "__pycache__", "node_modules", ".venv", "venv"}

        all_findings: List[Dict[str, Any]] = []
        files_scanned = 0

        for path in root_path.rglob("*"):
            if not path.is_file():
                continue
            if any(p in path.parts for p in skip):
                continue
            if path.suffix not in exts:
                continue
            files_scanned += 1
            all_findings.extend(self.scan_file(path))

        by_type: Dict[str, int] = {}
        for f in all_findings:
            by_type[f["type"]] = by_type.get(f["type"], 0) + 1

        return {
            "files_scanned": files_scanned,
            "total_findings": len(all_findings),
            "by_type": by_type,
            "findings": all_findings[:100],
        }
