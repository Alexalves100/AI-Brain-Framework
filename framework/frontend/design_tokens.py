"""
Design Tokens, Themes, Fluid Typography & Tactile Micro-Interactions
Version: 1.0.0
"""

from typing import Any, Dict


class DesignTokens:
    """
    Enterprise-grade design system tokens.
    Provides curated HSL color themes, mathematical fluid typography (clamp),
    tactile elevation shadows, and spring easing curves.
    Zero external dependencies.
    """

    THEMES: Dict[str, Dict[str, Any]] = {
        "warm_slate": {
            "name": "Warm Slate (Modern SaaS)",
            "light": {
                "--background": "0 0% 100%",
                "--foreground": "222 47% 11%",
                "--card": "0 0% 100%",
                "--card-foreground": "222 47% 11%",
                "--popover": "0 0% 100%",
                "--popover-foreground": "222 47% 11%",
                "--primary": "221 83% 53%",
                "--primary-foreground": "210 40% 98%",
                "--secondary": "210 40% 96%",
                "--secondary-foreground": "222 47% 11%",
                "--muted": "210 40% 96%",
                "--muted-foreground": "215 16% 47%",
                "--accent": "210 40% 96%",
                "--accent-foreground": "222 47% 11%",
                "--destructive": "0 84% 60%",
                "--destructive-foreground": "210 40% 98%",
                "--border": "214 32% 91%",
                "--input": "214 32% 91%",
                "--ring": "221 83% 53%",
            },
            "dark": {
                "--background": "224 71% 4%",
                "--foreground": "213 31% 91%",
                "--card": "224 71% 4%",
                "--card-foreground": "213 31% 91%",
                "--popover": "224 71% 4%",
                "--popover-foreground": "215 20% 65%",
                "--primary": "210 40% 98%",
                "--primary-foreground": "222 47% 11%",
                "--secondary": "222 47% 11%",
                "--secondary-foreground": "210 40% 98%",
                "--muted": "223 47% 11%",
                "--muted-foreground": "215 20% 65%",
                "--accent": "216 34% 17%",
                "--accent-foreground": "210 40% 98%",
                "--destructive": "0 63% 31%",
                "--destructive-foreground": "210 40% 98%",
                "--border": "216 34% 17%",
                "--input": "216 34% 17%",
                "--ring": "216 34% 17%",
            },
        },
        "editorial": {
            "name": "Modern Editorial (High-Contrast Financial & Publishing)",
            "light": {
                "--background": "45 29% 97%",
                "--foreground": "20 14% 10%",
                "--card": "0 0% 100%",
                "--card-foreground": "20 14% 10%",
                "--primary": "20 14% 10%",
                "--primary-foreground": "45 29% 97%",
                "--secondary": "40 18% 90%",
                "--secondary-foreground": "20 14% 10%",
                "--muted": "40 18% 90%",
                "--muted-foreground": "25 6% 45%",
                "--accent": "35 30% 85%",
                "--accent-foreground": "20 14% 10%",
                "--destructive": "0 72% 51%",
                "--destructive-foreground": "0 0% 100%",
                "--border": "40 13% 82%",
                "--input": "40 13% 82%",
                "--ring": "20 14% 10%",
            },
            "dark": {
                "--background": "20 14% 8%",
                "--foreground": "45 29% 95%",
                "--card": "20 14% 11%",
                "--card-foreground": "45 29% 95%",
                "--primary": "45 29% 95%",
                "--primary-foreground": "20 14% 8%",
                "--secondary": "20 10% 16%",
                "--secondary-foreground": "45 29% 95%",
                "--muted": "20 10% 16%",
                "--muted-foreground": "30 8% 60%",
                "--accent": "20 10% 20%",
                "--accent-foreground": "45 29% 95%",
                "--destructive": "0 62% 40%",
                "--destructive-foreground": "0 0% 100%",
                "--border": "20 10% 18%",
                "--input": "20 10% 18%",
                "--ring": "45 29% 95%",
            },
        },
        "tactile_clean": {
            "name": "Tactile Clean (1px Precision Micro-Borders)",
            "light": {
                "--background": "0 0% 98%",
                "--foreground": "0 0% 9%",
                "--card": "0 0% 100%",
                "--card-foreground": "0 0% 9%",
                "--primary": "0 0% 9%",
                "--primary-foreground": "0 0% 98%",
                "--secondary": "0 0% 94%",
                "--secondary-foreground": "0 0% 9%",
                "--muted": "0 0% 94%",
                "--muted-foreground": "0 0% 45%",
                "--accent": "0 0% 92%",
                "--accent-foreground": "0 0% 9%",
                "--destructive": "0 84% 60%",
                "--destructive-foreground": "0 0% 98%",
                "--border": "0 0% 88%",
                "--input": "0 0% 88%",
                "--ring": "0 0% 9%",
            },
            "dark": {
                "--background": "0 0% 6%",
                "--foreground": "0 0% 95%",
                "--card": "0 0% 9%",
                "--card-foreground": "0 0% 95%",
                "--primary": "0 0% 95%",
                "--primary-foreground": "0 0% 9%",
                "--secondary": "0 0% 14%",
                "--secondary-foreground": "0 0% 95%",
                "--muted": "0 0% 14%",
                "--muted-foreground": "0 0% 60%",
                "--accent": "0 0% 18%",
                "--accent-foreground": "0 0% 95%",
                "--destructive": "0 62% 40%",
                "--destructive-foreground": "0 0% 95%",
                "--border": "0 0% 16%",
                "--input": "0 0% 16%",
                "--ring": "0 0% 95%",
            },
        },
    }

    EASINGS = {
        "spring": "cubic-bezier(0.16, 1, 0.3, 1)",
        "smooth_out": "cubic-bezier(0, 0, 0.2, 1)",
        "tactile_click": "cubic-bezier(0.4, 0, 0.2, 1)",
    }

    SHADOWS = {
        "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        "md": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
        "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
        "tactile": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
    }

    @staticmethod
    def calculate_clamp(
        min_rem: float,
        max_rem: float,
        min_vw_px: float = 320.0,
        max_vw_px: float = 1280.0,
    ) -> str:
        """
        Calculates mathematical fluid typography clamp(min_rem, preferred_vw, max_rem).
        Formula: clamp(min_rem, (y_intercept)rem + (slope)vw, max_rem)
        """
        min_px = min_rem * 16.0
        max_px = max_rem * 16.0
        slope = (max_px - min_px) / (max_vw_px - min_vw_px)
        y_intercept = (min_px - slope * min_vw_px) / 16.0
        slope_vw = slope * 100.0

        return f"clamp({min_rem:.3f}rem, {y_intercept:.3f}rem + {slope_vw:.3f}vw, {max_rem:.3f}rem)"

    def generate_css_variables(self, theme_name: str = "warm_slate", include_utilities: bool = True) -> str:
        """Generates root CSS stylesheet with CSS custom properties and dark mode."""
        theme = self.THEMES.get(theme_name, self.THEMES["warm_slate"])
        light_vars = "\n  ".join([f"{k}: {v};" for k, v in theme["light"].items()])
        dark_vars = "\n    ".join([f"{k}: {v};" for k, v in theme["dark"].items()])

        css = f"""/* AI-Brain-Framework Design Tokens: {theme['name']} */
:root {{
  /* HSL Color System */
  {light_vars}

  /* Typography Scale (Fluid) */
  --font-display: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: {self.calculate_clamp(1.125, 1.25)};
  --text-xl: {self.calculate_clamp(1.25, 1.5)};
  --text-2xl: {self.calculate_clamp(1.5, 2.0)};
  --text-3xl: {self.calculate_clamp(1.875, 2.5)};
  --text-4xl: {self.calculate_clamp(2.25, 3.25)};

  /* Spacing & Radii */
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: {self.SHADOWS['sm']};
  --shadow-md: {self.SHADOWS['md']};
  --shadow-lg: {self.SHADOWS['lg']};
  --shadow-tactile: {self.SHADOWS['tactile']};

  /* Micro-Interactions & Easings */
  --ease-spring: {self.EASINGS['spring']};
  --ease-out: {self.EASINGS['smooth_out']};
  --ease-click: {self.EASINGS['tactile_click']};
  --transition-tactile: all 0.15s var(--ease-spring);
}}

@media (prefers-color-scheme: dark) {{
  :root {{
    {dark_vars}
  }}
}}

[data-theme="dark"] {{
  {dark_vars}
}}
"""
        if include_utilities:
            css += """
/* Base & Focus Reset */
*, *::before, *::after {
  box-sizing: border-box;
}

body {
  background-color: hsl(var(--background));
  color: hsl(var(--foreground));
  font-family: var(--font-display);
  margin: 0;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

:focus-visible {
  outline: 2px solid hsl(var(--ring));
  outline-offset: 2px;
}
"""
        return css
