"""
Design System Tokens Generator.
Fornece tokens de design visual, paletas HSL, variáveis CSS e reset tipográfico
para aplicações Web, Mobile e Websites profissionais sem dependências externas.
"""

class CSSTokens:
    """Provedor de tokens de design system em CSS nativo."""

    THEMES = {
        "dark": {
            "bg_primary": "hsl(222, 47%, 11%)",
            "bg_secondary": "hsl(217, 33%, 17%)",
            "bg_surface": "hsl(217, 33%, 22%)",
            "text_primary": "hsl(210, 40%, 98%)",
            "text_secondary": "hsl(215, 20%, 65%)",
            "accent": "hsl(250, 84%, 67%)",
            "accent_hover": "hsl(250, 84%, 75%)",
            "border": "hsl(217, 20%, 28%)",
            "success": "hsl(142, 71%, 45%)",
            "warning": "hsl(38, 92%, 50%)",
            "error": "hsl(0, 84%, 60%)",
        },
        "light": {
            "bg_primary": "hsl(0, 0%, 100%)",
            "bg_secondary": "hsl(210, 40%, 96%)",
            "bg_surface": "hsl(210, 40%, 98%)",
            "text_primary": "hsl(222, 47%, 11%)",
            "text_secondary": "hsl(215, 16%, 47%)",
            "accent": "hsl(250, 84%, 54%)",
            "accent_hover": "hsl(250, 84%, 62%)",
            "border": "hsl(214, 32%, 91%)",
            "success": "hsl(142, 76%, 36%)",
            "warning": "hsl(38, 92%, 50%)",
            "error": "hsl(0, 84%, 60%)",
        }
    }

    TYPOGRAPHY = {
        "font_family_sans": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "font_family_heading": "'Outfit', 'Inter', sans-serif",
        "font_family_mono": "'Fira Code', monospace",
        "font_import_url": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap",
    }

    SPACING = {
        "xs": "0.25rem",
        "sm": "0.5rem",
        "md": "1rem",
        "lg": "1.5rem",
        "xl": "2rem",
        "2xl": "3rem",
    }

    BORDER_RADIUS = {
        "sm": "0.375rem",
        "md": "0.5rem",
        "lg": "0.75rem",
        "full": "9999px",
    }

    @classmethod
    def generate_css_variables(cls, theme: str = "dark") -> str:
        """Gera um bloco de variáveis CSS :root para o tema selecionado."""
        selected_theme = cls.THEMES.get(theme, cls.THEMES["dark"])
        lines = ["/* AI-Brain-Framework Design Tokens */", ":root {"]

        for key, val in selected_theme.items():
            css_var = f"  --color-{key.replace('_', '-')}: {val};"
            lines.append(css_var)

        for key, val in cls.SPACING.items():
            lines.append(f"  --space-{key}: {val};")

        for key, val in cls.BORDER_RADIUS.items():
            lines.append(f"  --radius-{key}: {val};")

        lines.append(f"  --font-sans: {cls.TYPOGRAPHY['font_family_sans']};")
        lines.append(f"  --font-heading: {cls.TYPOGRAPHY['font_family_heading']};")
        lines.append(f"  --font-mono: {cls.TYPOGRAPHY['font_family_mono']};")
        lines.append("}")
        return "\n".join(lines)

    @classmethod
    def get_google_fonts_import(cls) -> str:
        """Retorna o import CSS para as fontes padrão Google Fonts."""
        return f"@import url('{cls.TYPOGRAPHY['font_import_url']}');"
