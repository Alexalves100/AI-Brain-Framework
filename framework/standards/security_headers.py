"""
Security Headers — OWASP recommended HTTP headers
Version: 1.0.0
"""

from typing import Dict


class SecurityHeaders:
    """OWASP recommended security headers for HTTP responses."""

    DEFAULT = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        ),
    }

    @classmethod
    def get(cls) -> Dict[str, str]:
        return dict(cls.DEFAULT)

    @classmethod
    def csp_for_api(cls) -> str:
        return "default-src 'none'; frame-ancestors 'none'"
