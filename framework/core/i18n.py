"""
Internationalization (i18n) for AI-Brain-Framework
Version: 1.0.0
Simple message translation with locale support.
"""

from typing import Dict


class I18n:
    """Simple key-based message translation."""

    MESSAGES = {
        "en": {
            "skill.not_found": "Skill '{name}' not found",
            "skill.invalid_inputs": "Invalid inputs for '{name}'",
            "skill.run_started": "Running skill '{name}'",
            "skill.run_completed": "Skill '{name}' completed with status '{status}'",
            "pipeline.empty": "Pipeline has no skills",
            "pipeline.stopped": "Pipeline stopped at '{name}' due to error",
            "context.missing_key": "Required key '{key}' missing in context",
            "validation.invalid_email": "Invalid email format",
            "validation.invalid_slug": "Invalid slug format",
            "validation.too_long": "Value exceeds maximum length of {max}",
            "validation.too_short": "Value below minimum length of {min}",
            "security.no_hardcoded_secrets": "Hardcoded secrets are forbidden",
            "security.no_eval": "Use of eval() is forbidden",
            "security.weak_hash": "Weak hash algorithm detected",
            "security.insecure_http": "Insecure HTTP URL detected",
        },
        "pt-BR": {
            "skill.not_found": "Skill '{name}' não encontrada",
            "skill.invalid_inputs": "Entradas inválidas para '{name}'",
            "skill.run_started": "Executando skill '{name}'",
            "skill.run_completed": "Skill '{name}' concluída com status '{status}'",
            "pipeline.empty": "Pipeline não possui skills",
            "pipeline.stopped": "Pipeline interrompida em '{name}' devido a erro",
            "context.missing_key": "Chave obrigatória '{key}' ausente no contexto",
            "validation.invalid_email": "Formato de email inválido",
            "validation.invalid_slug": "Formato de slug inválido",
            "validation.too_long": "Valor excede o comprimento máximo de {max}",
            "validation.too_short": "Valor abaixo do comprimento mínimo de {min}",
            "security.no_hardcoded_secrets": "Segredos hardcoded são proibidos",
            "security.no_eval": "Uso de eval() é proibido",
            "security.weak_hash": "Algoritmo de hash fraco detectado",
            "security.insecure_http": "URL HTTP insegura detectada",
        },
    }

    def __init__(self, locale: str = "en"):
        if locale not in self.MESSAGES:
            locale = "en"
        self.locale = locale

    def t(self, key: str, **kwargs) -> str:
        """Translate a message key with optional formatting."""
        template = self.MESSAGES.get(self.locale, {}).get(
            key,
            self.MESSAGES["en"].get(key, key),
        )
        try:
            return template.format(**kwargs)
        except (KeyError, IndexError):
            return template

    def set_locale(self, locale: str) -> None:
        if locale in self.MESSAGES:
            self.locale = locale

    @classmethod
    def available_locales(cls) -> list:
        return list(cls.MESSAGES.keys())
