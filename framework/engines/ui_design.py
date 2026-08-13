"""
UI Design Engine — validates HTML/CSS for accessibility and responsiveness
Version: 1.0.0
"""

import re
from html.parser import HTMLParser
from typing import Any, Dict, List

from ..core import Context, Skill, SkillResult, SkillStatus


class _SemanticChecker(HTMLParser):
    """Collects semantic info from HTML."""

    def __init__(self):
        super().__init__()
        self.tags: List[str] = []
        self.images_without_alt: List[str] = []
        self.inputs_without_label: List[str] = []
        self.headings: List[int] = []
        self._current_input_attrs: Dict[str, str] = {}

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        self.tags.append(tag)

        if tag == "img":
            if not attrs_d.get("alt"):
                self.images_without_alt.append(attrs_d.get("src", "<unknown>"))

        if tag in ("input", "textarea", "select"):
            input_id = attrs_d.get("id")
            input_type = attrs_d.get("type", "text")
            if input_type != "hidden" and input_id:
                self._current_input_attrs[input_id] = attrs_d.get("placeholder", "")
                self.inputs_without_label.append(input_id)

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append(int(tag[1]))

    def handle_endtag(self, tag):
        pass


class UIDesignEngine(Skill):
    name = "ui_design"
    version = "1.0.0"
    category = "engineering"
    description = "Validates HTML for accessibility, semantics, and responsiveness"

    VIEWPORT_PATTERN = re.compile(
        r'<meta[^>]*name=["\']viewport["\'][^>]*content=["\'][^"\']*width=device-width[^"\']*["\']',
        re.I,
    )

    RESPONSIVE_CLASS_PATTERN = re.compile(
        r'class\s*=\s*["\'][^"\']*\b(sm|md|lg|xl|2xl):\w+',
        re.I,
    )

    MEDIA_QUERY_PATTERN = re.compile(r"@media\s*\([^)]*\)", re.I)

    def run(self, context: Context) -> SkillResult:
        html = context.get("html", "")
        css = context.get("css", "")

        if not html and not css:
            return SkillResult(
                status=SkillStatus.SKIPPED,
                output={"reason": "no html or css provided"},
            )

        findings: List[Dict[str, Any]] = []

        if html:
            checker = _SemanticChecker()
            try:
                checker.feed(html)
            except Exception:
                pass

            if not checker.headings:
                findings.append({
                    "type": "semantic.no_heading",
                    "severity": "medium",
                    "message": "No heading tags found",
                })

            if checker.headings and checker.headings[0] != 1:
                findings.append({
                    "type": "semantic.heading_skip",
                    "severity": "low",
                    "message": "First heading should be h1",
                })

            imgs_without_alt = list(checker.images_without_alt)
            img_pattern = re.compile(r"<img\b([^>]*)>", re.I)
            for m in img_pattern.finditer(html):
                attrs = m.group(1)
                if not re.search(r"\balt\s*=", attrs, re.I):
                    src_m = re.search(r'src\s*=\s*["\']([^"\']*)["\']', attrs, re.I)
                    imgs_without_alt.append(src_m.group(1) if src_m else "<unknown>")

            for img in imgs_without_alt:
                findings.append({
                    "type": "a11y.img_missing_alt",
                    "severity": "high",
                    "message": f"Image without alt: {img}",
                })

            if not self.VIEWPORT_PATTERN.search(html):
                findings.append({
                    "type": "responsive.no_viewport_meta",
                    "severity": "high",
                    "message": "Missing responsive viewport meta tag",
                })

            if not self.RESPONSIVE_CLASS_PATTERN.search(html):
                findings.append({
                    "type": "responsive.no_responsive_classes",
                    "severity": "medium",
                    "message": "No responsive utility classes found (sm:/md:/lg:)",
                })

        if css:
            media_count = len(self.MEDIA_QUERY_PATTERN.findall(css))
            if media_count == 0:
                findings.append({
                    "type": "responsive.no_media_queries",
                    "severity": "high",
                    "message": "No media queries in CSS",
                })

        by_severity: Dict[str, int] = {"high": 0, "medium": 0, "low": 0}
        for f in findings:
            by_severity[f["severity"]] = by_severity.get(f["severity"], 0) + 1

        score = max(0, 100 - (by_severity["high"] * 15 + by_severity["medium"] * 5))

        result = {
            "findings": findings,
            "total": len(findings),
            "by_severity": by_severity,
            "score": score,
        }
        context.set("ui_findings", findings)
        return SkillResult(
            status=SkillStatus.SUCCESS,
            output=result,
            metadata={"engine": "ui_design"},
        )
