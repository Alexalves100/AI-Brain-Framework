"""
Frontend & A11y Auditor (WCAG 2.1 AA, Clean CSS & Anti-AI Cliché Scanner)
Version: 1.0.0
"""

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class A11yViolation:
    rule_id: str
    category: str      # a11y | clean_css | ai_cliche
    severity: str      # critical | warning | info
    message: str
    snippet: str
    line_number: Optional[int] = None
    fix_recommendation: str = ""


@dataclass
class A11yAuditResult:
    score: int
    passed: bool
    total_violations: int
    violations: List[A11yViolation] = field(default_factory=list)
    ai_cliche_warnings: List[A11yViolation] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": self.score,
            "passed": self.passed,
            "total_violations": self.total_violations,
            "violations": [
                {
                    "rule_id": v.rule_id,
                    "category": v.category,
                    "severity": v.severity,
                    "message": v.message,
                    "snippet": v.snippet,
                    "fix": v.fix_recommendation,
                }
                for v in self.violations
            ],
            "ai_cliche_warnings": [
                {
                    "rule_id": w.rule_id,
                    "message": w.message,
                    "snippet": w.snippet,
                    "fix": w.fix_recommendation,
                }
                for w in self.ai_cliche_warnings
            ],
        }


class A11yAuditor:
    """
    Scans HTML, JSX/TSX, and CSS code for WCAG 2.1 AA accessibility,
    modern CSS best practices, and AI design clichés.
    Zero external dependencies.
    """

    def audit(self, code: str, filename: str = "component.tsx") -> A11yAuditResult:
        violations: List[A11yViolation] = []
        ai_cliches: List[A11yViolation] = []

        lines = code.splitlines()

        # 1. WCAG: Image Missing Alt
        img_pattern = re.compile(r"<img\b(?![^>]*\balt=)[^>]*>", re.IGNORECASE)
        for idx, line in enumerate(lines, start=1):
            for m in img_pattern.finditer(line):
                violations.append(
                    A11yViolation(
                        rule_id="WCAG_IMG_ALT_MISSING",
                        category="a11y",
                        severity="critical",
                        message="Img tag is missing mandatory 'alt' attribute for screen readers.",
                        snippet=m.group(0)[:60],
                        line_number=idx,
                        fix_recommendation="Add alt='Descriptive text' or alt='' for decorative images.",
                    )
                )

        # 2. WCAG: Button without accessible label
        for idx, line in enumerate(lines, start=1):
            if "<button" in line and "</button>" in line:

                if re.search(r"<button\b(?![^>]*\baria-label=)[^>]*>\s*(?:<svg|<i|<span class=)", line, re.IGNORECASE):
                    if not re.search(r"[a-zA-Z0-9]{2,}", re.sub(r"<[^>]+>", "", line)):
                        violations.append(
                            A11yViolation(
                                rule_id="WCAG_BUTTON_NO_LABEL",
                                category="a11y",
                                severity="critical",
                                message="Icon-only button has no text and is missing 'aria-label'.",
                                snippet=line.strip()[:60],
                                line_number=idx,
                                fix_recommendation="Add aria-label='Action name' to the button.",
                            )
                        )

        # 3. Heading Hierarchy Jump (e.g. <h1> followed by <h3>)
        headings = re.findall(r"<h([1-6])\b", code, re.IGNORECASE)
        if headings:
            levels = [int(h) for h in headings]
            for i in range(len(levels) - 1):
                if levels[i + 1] > levels[i] + 1:
                    violations.append(
                        A11yViolation(
                            rule_id="WCAG_HEADING_HIERARCHY_JUMP",
                            category="a11y",
                            severity="warning",
                            message=f"Heading level jumps from <h{levels[i]}> to <h{levels[i + 1]}> without intermediate level.",
                            snippet=f"<h{levels[i]}> -> <h{levels[i + 1]}>",
                            fix_recommendation=f"Use <h{levels[i] + 1}> to maintain accessible document outline.",
                        )
                    )

        # 4. Clean CSS: Z-Index Hell
        z_index_pattern = re.compile(r"z-index:\s*(\d{4,9})|z-\[(\d{4,9})\]", re.IGNORECASE)
        for idx, line in enumerate(lines, start=1):
            z_match = z_index_pattern.search(line)
            if z_match:
                val = z_match.group(1) or z_match.group(2)
                violations.append(
                    A11yViolation(
                        rule_id="CSS_Z_INDEX_HELL",
                        category="clean_css",
                        severity="warning",
                        message=f"Arbitrary high z-index ({val}) detected. Violates modular stacking context.",
                        snippet=line.strip()[:60],
                        line_number=idx,
                        fix_recommendation="Use structured z-index scale (e.g., 10, 20, 50, 100 for modals).",
                    )
                )

        # 5. Clean CSS: Outline None without Focus Ring
        if re.search(r"outline:\s*(?:none|0)", code, re.IGNORECASE) and not re.search(r":focus-visible|focus-visible:", code):
            violations.append(
                A11yViolation(
                    rule_id="CSS_OUTLINE_NONE_NO_FOCUS",
                    category="clean_css",
                    severity="critical",
                    message="Removed default focus outline without providing :focus-visible replacement.",
                    snippet="outline: none / outline: 0",
                    fix_recommendation="Add :focus-visible { outline: 2px solid hsl(var(--ring)); outline-offset: 2px; }",
                )
            )

        # 6. AI Cliché: Purple Glow on Dark
        has_purple = bool(re.search(r"#8b5cf6|#7c3aed|#6366f1|purple-600|violet-500|indigo-500", code, re.IGNORECASE))
        has_dark = bool(re.search(r"bg-black|bg-gray-900|#0f172a|#000000|#000\b", code, re.IGNORECASE))
        if has_purple and has_dark:
            ai_cliches.append(
                A11yViolation(
                    rule_id="AI_CLICHE_PURPLE_DARK",
                    category="ai_cliche",
                    severity="info",
                    message="Generic AI cliché detected: Neon Purple/Violet glow over dark background.",
                    snippet="purple/violet accents on dark background",
                    fix_recommendation="Use calibrated HSL Warm Slate or High-Contrast Monochrome for a professional look.",
                )
            )


        # Calculate Score
        deductions = 0
        for v in violations:
            if v.severity == "critical":
                deductions += 20
            elif v.severity == "warning":
                deductions += 10

        score = max(0, 100 - deductions)
        passed = score >= 70 and not any(v.severity == "critical" for v in violations)

        return A11yAuditResult(
            score=score,
            passed=passed,
            total_violations=len(violations),
            violations=violations,
            ai_cliche_warnings=ai_cliches,
        )
