"""
Fullstack & Frontend UI Engine Skill
Version: 1.0.0
"""

from typing import Any

from ..core.context import Context
from ..core.skill import Skill, SkillResult, SkillStatus
from ..frontend.a11y_auditor import A11yAuditor
from ..frontend.api_client_generator import APIClientGenerator
from ..frontend.component_builder import ComponentBuilder
from ..frontend.design_tokens import DesignTokens


class FullstackUIEngine(Skill):
    """
    Skill for fullstack UI/UX development:
    - Generates fluid Design Tokens & Themes
    - Builds production-grade accessible components (Vanilla, React TSX, Vue)
    - Audits frontend code for WCAG 2.1 AA and AI clichés
    - Generates typed TypeScript SDKs and forms from schemas
    Zero external dependencies.
    """

    name = "fullstack_ui"
    version = "1.0.0"
    category = "engineering"
    description = "Generates accessible multi-stack components, design tokens, audits A11y, and creates TypeScript API clients."

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.design_tokens = DesignTokens()
        self.component_builder = ComponentBuilder()
        self.a11y_auditor = A11yAuditor()
        self.api_client_generator = APIClientGenerator()

    def validate_inputs(self, context: Context) -> bool:
        # Accepts any of action, component_type, code, or schema
        return True

    def run(self, context: Context) -> SkillResult:
        action = context.get("action", "component")  # component | tokens | audit | api_client

        if action == "tokens":
            theme = context.get("theme", "warm_slate")
            css = self.design_tokens.generate_css_variables(theme)
            output = {"theme": theme, "css": css}
            context.set("tokens_css", css)
            return SkillResult(status=SkillStatus.SUCCESS, output=output, metadata={"engine": self.name})

        elif action == "component":
            comp_type = context.get("component_type", "button")  # button | card | input
            stack = context.get("stack", "react_tailwind")        # react_tailwind | vanilla | vue
            label = context.get("label", "Continuar")
            variant = context.get("variant", "primary")

            if comp_type == "card":
                title = context.get("title", "Visão Geral")
                subtitle = context.get("subtitle", "Métricas em tempo real")
                code = self.component_builder.build_card(title=title, subtitle=subtitle, stack=stack)
            elif comp_type == "input":
                label = context.get("label", "E-mail")
                code = self.component_builder.build_input(label=label, stack=stack)
            else:
                code = self.component_builder.build_button(label=label, variant=variant, stack=stack)

            output = {"component_type": comp_type, "stack": stack, "code": code}
            context.set("component_code", code)
            return SkillResult(status=SkillStatus.SUCCESS, output=output, metadata={"engine": self.name})

        elif action == "audit":
            code = context.get("code", "")
            filename = context.get("filename", "component.tsx")
            res = self.a11y_auditor.audit(code, filename)
            output = res.to_dict()
            context.set("a11y_audit", output)
            status = SkillStatus.SUCCESS if res.passed else SkillStatus.ERROR
            return SkillResult(status=status, output=output, metadata={"engine": self.name})


        elif action == "api_client":
            schema_name = context.get("schema_name", "Model")
            properties = context.get("properties", {})
            required_fields = context.get("required_fields", [])
            ts_interface = self.api_client_generator.generate_typescript_interface(schema_name, properties, required_fields)
            fetch_client = self.api_client_generator.generate_fetch_client(f"create{schema_name}", "POST", f"/api/{schema_name.lower()}s", schema_name, schema_name)
            form_code = self.api_client_generator.generate_react_form(schema_name, properties, required_fields)

            output = {
                "typescript_interface": ts_interface,
                "fetch_client": fetch_client,
                "react_form": form_code,
            }
            context.set("api_client", output)
            return SkillResult(status=SkillStatus.SUCCESS, output=output, metadata={"engine": self.name})

        return SkillResult(status=SkillStatus.ERROR, error=f"Unknown action: '{action}'", metadata={"engine": self.name})
