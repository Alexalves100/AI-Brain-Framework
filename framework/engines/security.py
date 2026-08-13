"""
Security Engine — security auditing
Version: 1.0.0
"""

import re
from typing import Any, Dict, List

from ..core import Context, Skill, SkillResult, SkillStatus


class SecurityEngine(Skill):
    name = "security"
    version = "1.0.0"
    category = "governance"
    description = "Audits code/config for security issues"

    PATTERNS = [
        ("SQL Injection", re.compile(r"(execute|query)\s*\(\s*['\"].*\+|['\"].*\+.*\)", re.I)),
        ("SQL String Concat", re.compile(r"\b(SELECT|INSERT|UPDATE|DELETE)\b.*\+", re.I)),
        ("XSS Risk", re.compile(r"innerHTML\s*=|document\.write\(", re.I)),
        ("Hardcoded Secret", re.compile(r"(password|api_key|secret)\s*=\s*['\"][^'\"]{8,}", re.I)),
        ("Eval Usage", re.compile(r"\beval\s*\(", re.I)),
        ("Weak Hash", re.compile(r"\b(md5|sha1)\s*\(", re.I)),
        ("Insecure HTTP", re.compile(r"http://(?!localhost|127\.)", re.I)),
    ]

    SEVERITY = {
        "SQL Injection": "critical",
        "SQL String Concat": "high",
        "XSS Risk": "high",
        "Hardcoded Secret": "critical",
        "Eval Usage": "high",
        "Weak Hash": "medium",
        "Insecure HTTP": "medium",
    }

    def run(self, context: Context) -> SkillResult:
        code = context.get("code", "")
        if not code:
            return SkillResult(status=SkillStatus.SKIPPED, output={"findings": []})

        findings: List[Dict[str, Any]] = []
        for name, pattern in self.PATTERNS:
            matches = pattern.findall(code)
            count = len(matches) if matches else 0
            if count:
                findings.append({
                    "type": name,
                    "severity": self.SEVERITY[name],
                    "count": count,
                })

        context.set("security_findings", findings)
        return SkillResult(
            status=SkillStatus.SUCCESS,
            output={"findings": findings, "total": len(findings)},
            metadata={"engine": "security"},
        )
