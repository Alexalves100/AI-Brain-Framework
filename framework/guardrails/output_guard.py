"""
Output Guardrails — Protects against System Prompt and Secret Leakage in LLM Responses
Inspired by Guardrails AI
Version: 1.0.0
"""

import json
import re
from typing import Any, Dict, List, Optional, Pattern

from .pii_shield import PIIShield


class OutputGuard:
    """
    Validates and sanitizes LLM output before it reaches the user.
    Prevents leakage of internal instructions, system prompts, and API keys.
    Zero external dependencies.
    """

    PRIVATE_KEY_PATTERN: Pattern[str] = re.compile(
        r"-----BEGIN\s+(RSA|OPENSSH|EC|PGP|ENCRYPTED)?\s*PRIVATE\s+KEY-----", re.I
    )

    def __init__(self):
        self.pii_shield = PIIShield()

    def check_system_prompt_leak(self, output_text: str, system_prompt: str) -> bool:
        """
        Checks if significant consecutive lines from system prompt appear in the output.
        """
        if not system_prompt or not output_text:
            return False

        sys_lines = [line.strip() for line in system_prompt.splitlines() if len(line.strip()) > 30]
        for line in sys_lines:
            if line in output_text:
                return True
        return False

    def validate_and_sanitize(
        self,
        output_text: str,
        system_prompt: Optional[str] = None,
        expected_json_schema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Validates model output against secrets, system prompt leaks, and schema conformance.
        """
        violations: List[Dict[str, Any]] = []
        clean_output = output_text

        # 1. Check for Private Key Leakage
        if self.PRIVATE_KEY_PATTERN.search(output_text):
            violations.append({
                "type": "PRIVATE_KEY_LEAK",
                "severity": "critical",
                "description": "Output contains private cryptographic key material",
            })
            clean_output = self.PRIVATE_KEY_PATTERN.sub("[REDACTED_PRIVATE_KEY]", clean_output)

        # 2. Check for System Prompt Leakage
        if system_prompt and self.check_system_prompt_leak(output_text, system_prompt):
            violations.append({
                "type": "SYSTEM_PROMPT_LEAK",
                "severity": "critical",
                "description": "Output repeats verbatim sentences from the internal system prompt",
            })

        # 3. Check for API Keys & Secrets using PIIShield
        pii_res = self.pii_shield.scan(clean_output)
        if pii_res["has_pii"]:
            secrets = [f for f in pii_res["findings"] if f["type"] in self.pii_shield.SECRETS_PATTERNS]
            if secrets:
                violations.append({
                    "type": "SECRET_KEY_LEAK",
                    "severity": "critical",
                    "description": "Output contains API keys or authentication tokens",
                })
                clean_output = self.pii_shield.anonymize(clean_output)

        # 4. Optional JSON Schema Validation
        if expected_json_schema:
            try:
                parsed = json.loads(clean_output)
                if not isinstance(parsed, dict):
                    violations.append({
                        "type": "SCHEMA_VIOLATION",
                        "severity": "medium",
                        "description": "Output is valid JSON but not a JSON object",
                    })
            except Exception as e:
                violations.append({
                    "type": "INVALID_JSON",
                    "severity": "high",
                    "description": f"Output failed JSON parsing: {str(e)}",
                })

        is_safe = len([v for v in violations if v["severity"] == "critical"]) == 0

        return {
            "is_safe": is_safe,
            "violations": violations,
            "violations_count": len(violations),
            "sanitized_output": clean_output,
        }
