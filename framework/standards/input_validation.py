"""
Input Validation — whitelist-based validators
Version: 1.0.0
"""

import re
from typing import Any


class InputValidator:
    """Whitelist-based input validators."""

    EMAIL = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    USERNAME = re.compile(r"^[a-zA-Z0-9_]{3,32}$")
    UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)

    @classmethod
    def email(cls, value: Any) -> bool:
        return isinstance(value, str) and bool(cls.EMAIL.match(value))

    @classmethod
    def slug(cls, value: Any) -> bool:
        return isinstance(value, str) and bool(cls.SLUG.match(value))

    @classmethod
    def username(cls, value: Any) -> bool:
        return isinstance(value, str) and bool(cls.USERNAME.match(value))

    @classmethod
    def uuid(cls, value: Any) -> bool:
        return isinstance(value, str) and bool(cls.UUID.match(value))

    @classmethod
    def length(cls, value: Any, min_len: int = 1, max_len: int = 255) -> bool:
        if not isinstance(value, str):
            return False
        return min_len <= len(value) <= max_len

    @classmethod
    def alphanumeric(cls, value: Any) -> bool:
        return isinstance(value, str) and bool(re.match(r"^[a-zA-Z0-9]+$", value))

    @classmethod
    def no_html(cls, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        return "<" not in value and ">" not in value

    @classmethod
    def sanitize_text(cls, value: str, max_len: int = 1000) -> str:
        if not isinstance(value, str):
            return ""
        cleaned = re.sub(r"[<>]", "", value)
        return cleaned.strip()[:max_len]
