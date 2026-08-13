"""
Dependency Scanner — scans project dependencies
Version: 1.0.0
"""

import re
from pathlib import Path
from typing import Any, Dict, List


class DependencyScanner:
    """Scans project dependencies from common manifest files."""

    PYTHON_PATTERN = re.compile(r"^\s*([a-zA-Z0-9_.-]+)\s*([>=<~!]=?)\s*([\S]+)", re.M)
    NPM_PATTERN = re.compile(r'"([@a-zA-Z0-9_./-]+)":\s*"([^"]+)"')

    KNOWN_VULNERABLE = {
        "django": ["1.0", "1.1", "1.2"],
        "flask": ["0.1", "0.2"],
        "requests": ["2.0.0"],
    }

    def scan_python(self, content: str) -> List[Dict[str, Any]]:
        deps = []
        for m in self.PYTHON_PATTERN.finditer(content):
            name, _op, version = m.group(1), m.group(2), m.group(3)
            if name.lower() in ("python", "pip"):

                continue
            deps.append({
                "name": name,
                "version": version,
                "ecosystem": "pypi",
                "vulnerable": self._is_vulnerable(name, version),
            })
        return deps

    def scan_npm(self, content: str) -> List[Dict[str, Any]]:
        deps = []
        try:
            import json
            data = json.loads(content)
            for name, version in data.get("dependencies", {}).items():
                deps.append({
                    "name": name,
                    "version": version.lstrip("^~"),
                    "ecosystem": "npm",
                    "vulnerable": self._is_vulnerable(name, version),
                })
        except Exception:
            for m in self.NPM_PATTERN.finditer(content):
                deps.append({
                    "name": m.group(1),
                    "version": m.group(2).lstrip("^~"),
                    "ecosystem": "npm",
                    "vulnerable": self._is_vulnerable(m.group(1), m.group(2)),
                })
        return deps

    def _is_vulnerable(self, name: str, version: str) -> bool:
        bad = self.KNOWN_VULNERABLE.get(name.lower(), [])
        return any(version.startswith(v) for v in bad)

    def scan_project(self, root: str = ".") -> Dict[str, Any]:
        root_path = Path(root)
        all_deps: List[Dict[str, Any]] = []

        for filename in ["requirements.txt", "pyproject.toml", "Pipfile"]:
            f = root_path / filename
            if f.exists():
                content = f.read_text(encoding="utf-8", errors="ignore")
                all_deps.extend(self.scan_python(content))

        pkg = root_path / "package.json"
        if pkg.exists():
            content = pkg.read_text(encoding="utf-8", errors="ignore")
            all_deps.extend(self.scan_npm(content))

        vulnerable = [d for d in all_deps if d["vulnerable"]]

        return {
            "total_dependencies": len(all_deps),
            "vulnerable_count": len(vulnerable),
            "vulnerable": vulnerable,
            "all": all_deps,
        }
