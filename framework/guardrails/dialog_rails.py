"""
Dialog Rails — Persona and Topic Lock
Inspired by NVIDIA NeMo Guardrails
Version: 1.0.0
"""

import re
from typing import Any, Dict, List, Optional, Pattern


class DialogRails:
    """
    Enforces persona locking and topic compliance.
    Prevents roleplay subversions and malicious persona shifts.
    Zero external dependencies.
    """

    PERSONA_SUBVERSION_PATTERNS: List[Pattern[str]] = [
        re.compile(r"from\s+now\s+on[,\s]+(you\s+will\s+)?(act|behave|pretend|roleplay)\s+as", re.I),
        re.compile(r"agora\s+voc[êe]\s+[ée]\s+(um|uma)\s+(ia\s+sem\s+regras|hacker|vil[ãa]o)", re.I),
        re.compile(r"simule\s+que\s+voc[êe]\s+[ée]\s+um\s+criminoso", re.I),
        re.compile(r"pretend\s+you\s+have\s+no\s+(morals|ethics|rules)", re.I),
        re.compile(r"in\s+this\s+hypothetical\s+story[,\s]+you\s+are\s+an\s+evil\s+ai", re.I),
        re.compile(r"roleplay\s+as\s+a\s+(black\s+hat|terrorist|criminal)", re.I),
    ]

    FORBIDDEN_HARMFUL_TOPICS: Dict[str, Pattern[str]] = {
        "MALWARE_CREATION": re.compile(
            r"(write|generate|create|crie)\s+(a\s+)?(ransomware|keylogger|trojan|worm|rootkit)", re.I
        ),
        "CREDENTIAL_HARVESTING": re.compile(
            r"(how\s+to\s+phish|create\s+phishing\s+page|roubar\s+senhas)", re.I
        ),
        "EXPLOIT_PAYLOAD": re.compile(
            r"(generate|escreva)\s+(a\s+)?zero[- ]day\s+exploit\s+payload", re.I
        ),
    }

    def check(self, text: str, allowed_topics: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Validates whether input violates persona integrity or enters forbidden topics.
        """
        violations: List[Dict[str, Any]] = []

        # 1. Persona Lock Check
        for pattern in self.PERSONA_SUBVERSION_PATTERNS:
            match = pattern.search(text)
            if match:
                violations.append({
                    "category": "PERSONA_SUBVERSION",
                    "severity": "critical",
                    "snippet": match.group(0),
                    "description": "Attempt to hijack or alter the AI system persona",
                })
                break

        # 2. Harmful Topics Check
        for topic_name, pattern in self.FORBIDDEN_HARMFUL_TOPICS.items():
            match = pattern.search(text)
            if match:
                violations.append({
                    "category": topic_name,
                    "severity": "critical",
                    "snippet": match.group(0),
                    "description": f"Attempt to engage in forbidden topic: {topic_name}",
                })

        # 3. Allowed Topics Restriction (if configured)
        if allowed_topics and not violations:
            text_lower = text.lower()
            topic_matched = any(topic.lower() in text_lower for topic in allowed_topics)
            if not topic_matched:
                violations.append({
                    "category": "OFF_TOPIC",
                    "severity": "medium",
                    "description": "Input does not match any authorized domain topic",
                })

        is_allowed = len([v for v in violations if v["severity"] == "critical"]) == 0

        return {
            "is_allowed": is_allowed,
            "violations_count": len(violations),
            "violations": violations,
        }
