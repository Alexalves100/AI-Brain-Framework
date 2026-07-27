"""
Policy Engine — enforces governance policies
Version: 1.0.0
"""

from typing import List, Dict, Any


class PolicyEngine:
    """Enforces governance policies with declarative rules."""

    DEFAULT_POLICIES = {
        "no_hardcoded_secrets": {
            "severity": "critical",
            "description": "No hardcoded secrets in code",
        },
        "require_input_validation": {
            "severity": "high",
            "description": "All inputs must be validated",
        },
        "require_security_headers": {
            "severity": "medium",
            "description": "HTTP responses must include security headers",
        },
        "require_tests": {
            "severity": "medium",
            "description": "All modules must have tests",
        },
    }

    def __init__(self, policies: Dict[str, Dict[str, Any]] = None):
        self.policies = policies or self.DEFAULT_POLICIES

    def check(self, policy_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if policy_name not in self.policies:
            return {"violated": False, "reason": "policy not found"}

        policy = self.policies[policy_name]

        if policy_name == "no_hardcoded_secrets":
            code = context.get("code", "")
            has_secret = any(
                marker in code.lower()
                for marker in ["password=", "api_key=", "secret="]
            )
            return {
                "violated": has_secret,
                "severity": policy["severity"],
                "description": policy["description"],
            }

        if policy_name == "require_input_validation":
            has_validation = context.get("has_validation", False)
            return {
                "violated": not has_validation,
                "severity": policy["severity"],
                "description": policy["description"],
            }

        if policy_name == "require_security_headers":
            has_headers = context.get("has_security_headers", False)
            return {
                "violated": not has_headers,
                "severity": policy["severity"],
                "description": policy["description"],
            }

        if policy_name == "require_tests":
            has_tests = context.get("has_tests", False)
            return {
                "violated": not has_tests,
                "severity": policy["severity"],
                "description": policy["description"],
            }

        return {"violated": False}

    def check_all(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [self.check(name, context) for name in self.policies]
