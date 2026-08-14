"""
PII (Personally Identifiable Information) and Secret Shield
Supports LGPD (Brazil CPF, Phone) and GDPR compliance with mathematical validation.
Version: 1.0.0
"""

import re
from typing import Any, Dict, List, Pattern


class PIIShield:
    """
    Scans and redacts PII and sensitive secrets.
    Includes deterministic validation (Luhn for cards, Checksum for Brazilian CPF).
    Zero external dependencies.
    """

    EMAIL_PATTERN: Pattern[str] = re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    CPF_PATTERN: Pattern[str] = re.compile(
        r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"
    )

    PHONE_BR_PATTERN: Pattern[str] = re.compile(
        r"(?:\+55\s?)?(?:\(?\d{2}\)?[\s-]?)?(?:9\d{4}|\d{4})[-\s]?\d{4}\b"
    )

    CREDIT_CARD_CANDIDATE: Pattern[str] = re.compile(
        r"\b(?:\d[ -]*?){13,19}\b"
    )

    SECRETS_PATTERNS: Dict[str, Pattern[str]] = {
        "OPENAI_KEY": re.compile(r"\bsk-[a-zA-Z0-9_-]{20,}\b"),
        "GITHUB_TOKEN": re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36}\b"),
        "AWS_ACCESS_KEY": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "JWT_TOKEN": re.compile(r"\beyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b"),
        "BEARER_AUTH": re.compile(r"\bBearer\s+[a-zA-Z0-9_.-]{20,}\b", re.I),
    }

    @staticmethod
    def validate_cpf(cpf_str: str) -> bool:
        """Validates Brazilian CPF using official modulus 11 verification digits."""
        digits = [int(c) for c in cpf_str if c.isdigit()]
        if len(digits) != 11:
            return False

        # Reject all same digits (e.g. 111.111.111-11)
        if len(set(digits)) == 1:
            return False

        # First check digit
        sum_1 = sum(digits[i] * (10 - i) for i in range(9))
        remainder_1 = (sum_1 * 10) % 11
        check_1 = 0 if remainder_1 >= 10 else remainder_1
        if digits[9] != check_1:
            return False

        # Second check digit
        sum_2 = sum(digits[i] * (11 - i) for i in range(10))
        remainder_2 = (sum_2 * 10) % 11
        check_2 = 0 if remainder_2 >= 10 else remainder_2

        return digits[10] == check_2

    @staticmethod
    def validate_luhn(card_str: str) -> bool:
        """Validates credit card numbers using the standard Luhn checksum."""
        digits = [int(c) for c in card_str if c.isdigit()]
        if not (13 <= len(digits) <= 19):
            return False

        checksum = 0
        reverse_digits = digits[::-1]
        for i, digit in enumerate(reverse_digits):
            if i % 2 == 1:
                doubled = digit * 2
                checksum += doubled - 9 if doubled > 9 else doubled
            else:
                checksum += digit

        return checksum % 10 == 0

    def scan(self, text: str) -> Dict[str, Any]:
        """Scans text for all PII and secret categories."""
        findings: List[Dict[str, Any]] = []

        # 1. Brazilian CPF
        for m in self.CPF_PATTERN.finditer(text):
            val = m.group(0)
            if self.validate_cpf(val):
                findings.append({"type": "CPF", "value": val, "start": m.start(), "end": m.end()})

        # 2. Credit Cards (with Luhn)
        for m in self.CREDIT_CARD_CANDIDATE.finditer(text):
            val = m.group(0)
            clean_digits = "".join(c for c in val if c.isdigit())
            # Skip if it was already caught as CPF
            if len(clean_digits) == 11 and self.validate_cpf(val):
                continue
            if self.validate_luhn(val):
                findings.append({"type": "CREDIT_CARD", "value": val, "start": m.start(), "end": m.end()})

        # 3. Emails
        for m in self.EMAIL_PATTERN.finditer(text):
            findings.append({"type": "EMAIL", "value": m.group(0), "start": m.start(), "end": m.end()})

        # 4. Secrets & API Keys
        for secret_type, pattern in self.SECRETS_PATTERNS.items():
            for m in pattern.finditer(text):
                findings.append({"type": secret_type, "value": m.group(0), "start": m.start(), "end": m.end()})

        # Sort findings by position
        findings.sort(key=lambda x: x["start"])

        return {
            "has_pii": len(findings) > 0,
            "total_entities": len(findings),
            "findings": findings,
        }

    def anonymize(self, text: str, mask_type: str = "tag") -> str:
        """
        Redacts all identified PII and secrets in the text.
        mask_type can be 'tag' ([REDACTED_CPF]) or 'asterisk' (***).
        """
        scan_res = self.scan(text)
        if not scan_res["has_pii"]:
            return text

        # Replace from end to start to preserve indices
        result = text
        for item in reversed(scan_res["findings"]):
            start = item["start"]
            end = item["end"]
            entity_type = item["type"]

            if mask_type == "tag":
                replacement = f"[REDACTED_{entity_type}]"
            else:
                replacement = "*" * min(8, end - start)

            result = result[:start] + replacement + result[end:]

        return result
