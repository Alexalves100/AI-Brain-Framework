"""
Prompt Injection, Jailbreak and Steganography Detector
Version: 1.0.0
"""

import re
from typing import Any, Dict, List, Pattern


class InjectionDetector:
    """
    Detects Prompt Injection, Jailbreak attempts, and Delimiter Hijacking in LLM inputs.
    Zero external dependencies.
    """

    # Zero-width / invisible characters used to bypass keyword filters
    ZERO_WIDTH_PATTERN: Pattern[str] = re.compile(
        r"[\u200B-\u200D\u200E\u200F\uFEFF\u00AD\u2060\u2061\u2062\u2063\u2064]"
    )

    INJECTION_PATTERNS: Dict[str, Dict[str, Any]] = {
        "DIRECT_OVERRIDE": {
            "weight": 40,
            "patterns": [
                re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts|rules|commands)", re.I),
                re.compile(r"disregard\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts|rules)", re.I),
                re.compile(r"override\s+(all\s+)?(system|safety|security)\s+(prompts|rules|guidelines)", re.I),
                re.compile(r"forget\s+(all\s+)?(previous|prior|initial)\s+(instructions|context)", re.I),
                re.compile(r"esque[çc]a\s+(todas\s+as\s+)?instru[çc][õo]es\s+(anteriores|acima)", re.I),
                re.compile(r"desconsidere\s+(todas\s+as\s+)?(regras|instru[çc][õo]es)\s+(anteriores|acima)", re.I),
                re.compile(r"ignore\s+(todas\s+as\s+)?(regras|diretrizes)\s+do\s+sistema", re.I),
            ],
            "description": "Direct prompt instruction override",
        },
        "JAILBREAK_PERSONA": {
            "weight": 50,
            "patterns": [
                re.compile(r"\byou\s+are\s+now\s+(dan|an?\s+evil|unfiltered|jailbroken)\b", re.I),
                re.compile(r"\bdo\s+anything\s+now\b", re.I),
                re.compile(r"\bdeveloper\s+mode\s+(output|enabled?|active)\b", re.I),
                re.compile(r"\bbypass\s+(all\s+)?(safety|content|ethical)\s+filters?\b", re.I),
                re.compile(r"\bsem\s+nenhuma\s+restri[çc][ãa]o\s+moral\s+ou\s+[ée]tica\b", re.I),
                re.compile(r"\bresponda\s+como\s+uma\s+ia\s+sem\s+filtros\b", re.I),
                re.compile(r"\bjailbreak\s+mode\s+on\b", re.I),
            ],
            "description": "Jailbreak or persona bypass attack (e.g. DAN)",
        },
        "SYSTEM_EXFILTRATION": {
            "weight": 35,
            "patterns": [
                re.compile(r"(print|show|display|reveal|output|repeat)\s+(your\s+)?(entire\s+)?system\s+prompt", re.I),
                re.compile(r"(repeat|output)\s+all\s+(text|words|instructions)\s+(above|prior)\s+verbatim", re.I),
                re.compile(r"what\s+(are|were)\s+your\s+(exact\s+)?initial\s+instructions", re.I),
                re.compile(r"mostre\s+(seu|o)\s+system\s+prompt(\s+completo)?", re.I),
                re.compile(r"repita\s+as\s+instru[çc][õo]es\s+iniciais\s+palavra\s+por\s+palavra", re.I),
                re.compile(r"quais\s+s[ãa]o\s+suas\s+regras\s+internas\s+secretas", re.I),
            ],
            "description": "System prompt exfiltration attempt",
        },
        "DELIMITER_HIJACK": {
            "weight": 30,
            "patterns": [
                re.compile(r"<\/?(system|assistant|user|im_start|im_end|INST)>", re.I),
                re.compile(r"\[\/?INST\]", re.I),
                re.compile(r"\{\s*\"role\"\s*:\s*\"system\"\s*\}", re.I),
                re.compile(r"```(system|instructions)\b", re.I),
            ],
            "description": "Delimiter hijacking and role boundary breakout",
        },
        "OBFUSCATION_ENCODING": {
            "weight": 25,
            "patterns": [
                re.compile(r"decode\s+(the\s+following\s+)?(base64|hex|rot13|morse)\s+and\s+execute", re.I),
                re.compile(r"decodifique\s+em\s+base64\s+e\s+execute", re.I),
            ],
            "description": "Obfuscated payload execution request",
        },
    }

    def strip_zero_width_chars(self, text: str) -> str:
        """Removes invisible zero-width unicode characters."""
        return self.ZERO_WIDTH_PATTERN.sub("", text)

    def detect(self, text: str) -> Dict[str, Any]:
        """
        Analyzes the text for injection and jailbreak threats.
        Returns safety assessment, threat score (0-100), and findings.
        """
        if not text:
            return {
                "is_safe": True,
                "threat_score": 0,
                "threat_level": "LOW",
                "findings": [],
                "has_zero_width_chars": False,
                "clean_text": "",
            }

        # Check for zero-width characters
        had_zero_width = bool(self.ZERO_WIDTH_PATTERN.search(text))
        clean_text = self.strip_zero_width_chars(text)

        total_score = 0
        findings: List[Dict[str, Any]] = []

        if had_zero_width:
            total_score += 20
            findings.append({
                "type": "ZERO_WIDTH_CHARS",
                "severity": "medium",
                "description": "Hidden zero-width characters detected and removed",
            })

        for threat_type, config in self.INJECTION_PATTERNS.items():
            matched = False
            for pattern in config["patterns"]:
                match = pattern.search(clean_text)
                if match:
                    matched = True
                    matched_snippet = match.group(0)
                    findings.append({
                        "type": threat_type,
                        "severity": "high" if config["weight"] >= 35 else "medium",
                        "description": config["description"],
                        "snippet": matched_snippet,
                    })
                    break

            if matched:
                total_score += config["weight"]

        total_score = min(100, total_score)

        if total_score >= 50:
            threat_level = "CRITICAL"
        elif total_score >= 35:
            threat_level = "HIGH"
        elif total_score > 0:
            threat_level = "MEDIUM"
        else:
            threat_level = "LOW"


        is_safe = total_score < 35

        return {
            "is_safe": is_safe,
            "threat_score": total_score,
            "threat_level": threat_level,
            "findings": findings,
            "has_zero_width_chars": had_zero_width,
            "clean_text": clean_text,
        }
