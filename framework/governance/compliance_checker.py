"""
Compliance Checker — checks compliance with standards
Version: 1.0.0
"""

from pathlib import Path
from typing import Any, Dict


class ComplianceChecker:
    """Checks project compliance with required standards."""

    STANDARDS = {
        "has_readme": "README.md must exist",
        "has_license": "LICENSE must exist",
        "has_tests": "tests/ directory must exist",
        "has_gitignore": ".gitignore must exist",
        "has_security_policy": "SECURITY.md must exist",
        "has_changelog": "CHANGELOG.md must exist",
    }

    def check(self, root: str = ".") -> Dict[str, Any]:
        root_path = Path(root)
        results = {}
        for key, description in self.STANDARDS.items():
            filename = description.split(" must")[0].strip()
            if "/" in filename:
                exists = (root_path / filename).is_dir()
            else:
                exists = (root_path / filename).exists()
            results[key] = {
                "compliant": exists,
                "description": description,
            }

        compliant = sum(1 for r in results.values() if r["compliant"])
        total = len(results)

        return {
            "score": round(compliant / total * 100, 1),
            "compliant": compliant,
            "total": total,
            "details": results,
        }
