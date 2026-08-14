"""
PromptShield & AI Guardrails Engine
Unified Enterprise AI Security Engine for AI-Brain-Framework
Version: 1.0.0
"""

from typing import Any, Dict, Optional

from ..core.context import Context
from ..core.skill import Skill, SkillResult, SkillStatus
from ..guardrails.dialog_rails import DialogRails
from ..guardrails.injection_detector import InjectionDetector
from ..guardrails.output_guard import OutputGuard
from ..guardrails.pii_shield import PIIShield
from ..guardrails.tool_sandbox import ToolSandbox


class PromptShieldEngine(Skill):
    """
    Unified AI Guardrail Engine implementing multi-layered defense-in-depth:
    1. Input Prompt Injection & Jailbreak Scanner
    2. PII & LGPD / GDPR Secret Redactor
    3. Persona & Dialog Rails
    4. Agent Tool-Call Sandbox
    5. Output Leakage & Safety Guard
    Zero external dependencies.
    """

    name = "prompt_shield"
    version = "1.0.0"
    category = "governance"
    description = "Protects LLMs against prompt injection, jailbreaks, PII/secret leaks and unsafe tool calls"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.injection_detector = InjectionDetector()
        self.pii_shield = PIIShield()
        self.dialog_rails = DialogRails()
        self.tool_sandbox = ToolSandbox()
        self.output_guard = OutputGuard()

    def run(self, context: Context) -> SkillResult:
        prompt = context.get("prompt") or context.get("text") or ""
        mode = context.get("action") or context.get("mode") or "enforce"  # enforce | mask | audit
        system_prompt = context.get("system_prompt")
        response_text = context.get("response_text")
        tool_call: Optional[Dict[str, Any]] = context.get("tool_call")

        # 1. Scan Input Injection
        injection_res = self.injection_detector.detect(prompt)

        # 2. Scan & Anonymize PII
        pii_res = self.pii_shield.scan(injection_res["clean_text"])
        sanitized_prompt = self.pii_shield.anonymize(injection_res["clean_text"])

        # 3. Check Dialog & Persona Rails
        dialog_res = self.dialog_rails.check(sanitized_prompt)

        # 4. Optional Tool Sandbox Validation
        tool_sandbox_res = None
        if tool_call and isinstance(tool_call, dict):
            tool_name = tool_call.get("name", "")
            tool_args = tool_call.get("arguments", {})
            user_confirmed = tool_call.get("user_confirmed", False)
            tool_sandbox_res = self.tool_sandbox.validate_tool_call(tool_name, tool_args, user_confirmed)

        # 5. Optional Output Guard Validation
        output_guard_res = None
        if response_text:
            output_guard_res = self.output_guard.validate_and_sanitize(response_text, system_prompt)

        # Determine overall safety
        is_safe = (
            injection_res["is_safe"]
            and dialog_res["is_allowed"]
            and (tool_sandbox_res["is_executable"] if tool_sandbox_res else True)
            and (output_guard_res["is_safe"] if output_guard_res else True)
        )

        should_block = mode == "enforce" and not is_safe

        output = {
            "is_safe": is_safe,
            "mode": mode,
            "blocked": should_block,
            "threat_score": injection_res["threat_score"],
            "threat_level": injection_res["threat_level"],
            "original_prompt": prompt,
            "sanitized_prompt": sanitized_prompt,
            "injection_findings": injection_res["findings"],
            "pii_findings": pii_res["findings"],
            "dialog_violations": dialog_res["violations"],
            "tool_sandbox": tool_sandbox_res,
            "output_guard": output_guard_res,
        }

        context.set("prompt_shield_result", output)
        context.set("clean_prompt", sanitized_prompt)
        if not context.get("query") and sanitized_prompt:
            context.set("query", sanitized_prompt)

        status = SkillStatus.ERROR if should_block else SkillStatus.SUCCESS

        error_msg = "Prompt blocked by PromptShield security policy" if should_block else None

        return SkillResult(
            status=status,
            output=output,
            error=error_msg,
            metadata={"engine": "prompt_shield", "version": self.version},
        )
