"""
Agent Tool-Call Sandbox and Authorization Validator
Inspired by Arcjet and Bastion Security
Version: 1.0.0
"""

import re
from typing import Any, Dict, List, Pattern, Set


class ToolSandbox:
    """
    Validates agent tool execution requests against dangerous parameters,
    destructive actions, and indirect prompt injection.
    Zero external dependencies.
    """

    CRITICAL_TOOLS: Set[str] = {
        "execute_bash",
        "drop_database",
        "delete_database",
        "format_disk",
        "eval_python",
        "send_mass_email",
        "transfer_funds",
    }

    DESTRUCTIVE_COMMAND_PATTERNS: List[Pattern[str]] = [
        re.compile(r"\brm\s+-[rf]{1,2}\s+[\/\*]", re.I),
        re.compile(r"\bdrop\s+(database|table)\b", re.I),
        re.compile(r"\bdelete\s+from\s+[a-zA-Z0-9_]+\s*;\s*$", re.I),
        re.compile(r"\btruncate\s+table\b", re.I),
        re.compile(r"\bformat\s+[c-z]:", re.I),
        re.compile(r"\b(mkfs|dd\s+if=)", re.I),
        re.compile(r"\bos\.(system|popen|remove|rmdir)\s*\(", re.I),
    ]

    INDIRECT_INJECTION_MARKERS: List[Pattern[str]] = [
        re.compile(r"<\s*instruction\s*>", re.I),
        re.compile(r"ignore\s+all\s+previous\s+instructions\s+and\s+execute", re.I),
        re.compile(r"\[SYSTEM:\s*NEW\s*DIRECTIVE\]", re.I),
    ]

    def validate_tool_call(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        user_confirmed: bool = False,
    ) -> Dict[str, Any]:
        """
        Validates if a tool call is safe to execute or requires explicit human confirmation.
        """
        # 1. Check if tool is inherently critical
        if tool_name in self.CRITICAL_TOOLS and not user_confirmed:
            return {
                "decision": "REQUIRES_CONFIRMATION",
                "is_executable": False,
                "reason": f"Tool '{tool_name}' is classified as critical and requires explicit human approval.",
            }

        # 2. Check for destructive payloads inside arguments
        args_text = " ".join(str(v) for v in arguments.values())
        for pattern in self.DESTRUCTIVE_COMMAND_PATTERNS:
            match = pattern.search(args_text)
            if match and not user_confirmed:
                return {
                    "decision": "BLOCKED",
                    "is_executable": False,
                    "reason": f"Destructive command pattern detected in arguments: '{match.group(0)}'",
                }

        # 3. Check for indirect injection in arguments (e.g. fetched from scraped content)
        for pattern in self.INDIRECT_INJECTION_MARKERS:
            match = pattern.search(args_text)
            if match:
                return {
                    "decision": "BLOCKED",
                    "is_executable": False,
                    "reason": f"Indirect prompt injection marker detected in tool payload: '{match.group(0)}'",
                }

        return {
            "decision": "SAFE",
            "is_executable": True,
            "reason": "Tool call passed sandbox security checks.",
        }
