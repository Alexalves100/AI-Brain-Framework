"""
High-End Multi-Stack UI Component Builder (Vanilla, React TSX, Vue)
Version: 1.0.0
"""

from typing import Optional


class ComponentBuilder:
    """
    Builds production-grade, accessible, and tactile UI components
    without AI clichés (supports Vanilla HTML5/CSS, React Next.js TSX + Tailwind, and Vue 3).
    Zero external dependencies.
    """

    def build_button(
        self,
        label: str = "Continuar",
        variant: str = "primary",  # primary | secondary | destructive | outline | ghost
        size: str = "md",          # sm | md | lg
        stack: str = "react_tailwind",
        with_loading_state: bool = True,
        aria_label: Optional[str] = None,
    ) -> str:
        """Builds a tactile button with all interaction states."""
        effective_aria = aria_label or label

        if stack == "react_tailwind":
            return f"""import React, {{ ButtonHTMLAttributes, forwardRef }} from 'react';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {{
  variant?: 'primary' | 'secondary' | 'destructive' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(({{
  children = '{label}',
  variant = '{variant}',
  size = '{size}',
  isLoading = false,
  disabled,
  className = '',
  ...props
}}, ref) => {{
  const baseStyles = 'inline-flex items-center justify-center font-medium transition-all duration-150 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none active:scale-[0.98] select-none cursor-pointer';

  const variants = {{
    primary: 'bg-primary text-primary-foreground hover:bg-primary/90 focus-visible:ring-primary shadow-sm',
    secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80 focus-visible:ring-secondary',
    destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90 focus-visible:ring-destructive shadow-sm',
    outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground focus-visible:ring-ring',
    ghost: 'hover:bg-accent hover:text-accent-foreground focus-visible:ring-ring',
  }};

  const sizes = {{
    sm: 'h-8 px-3 text-xs gap-1.5',
    md: 'h-10 px-4 text-sm gap-2',
    lg: 'h-12 px-6 text-base gap-2.5',
  }};

  return (
    <button
      ref={{ref}}
      aria-label="{effective_aria}"
      disabled={{disabled || isLoading}}
      className={{`${{baseStyles}} ${{variants[variant]}} ${{sizes[size]}} ${{className}}`}}
      {{...props}}
    >
      {{isLoading ? (
        <>
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          <span>Carregando...</span>
        </>
      ) : (
        children
      )}}
    </button>
  );
}});

Button.displayName = 'Button';
"""

        # Vanilla HTML5 + Modern CSS
        return f"""<!-- HTML5 Accessible Button Component -->
<button type="button" class="btn btn-{variant} btn-{size}" aria-label="{effective_aria}">
  <span class="btn-spinner" aria-hidden="true"></span>
  <span class="btn-label">{label}</span>
</button>

<style>
.btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display, inherit);
  font-weight: 500;
  border-radius: var(--radius-md, 0.375rem);
  border: 1px solid transparent;
  cursor: pointer;
  user-select: none;
  transition: var(--transition-tactile, all 0.15s ease);
  outline: none;
}}

.btn:focus-visible {{
  outline: 2px solid hsl(var(--ring));
  outline-offset: 2px;
}}

.btn:active:not(:disabled) {{
  transform: scale(0.98);
}}

.btn:disabled {{
  opacity: 0.5;
  cursor: not-allowed;
}}

/* Sizes */
.btn-sm {{ height: 2rem; padding: 0 0.75rem; font-size: var(--text-xs, 0.75rem); gap: 0.375rem; }}
.btn-md {{ height: 2.5rem; padding: 0 1rem; font-size: var(--text-sm, 0.875rem); gap: 0.5rem; }}
.btn-lg {{ height: 3rem; padding: 0 1.5rem; font-size: var(--text-base, 1rem); gap: 0.625rem; }}

/* Variants */
.btn-primary {{
  background-color: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
  box-shadow: var(--shadow-sm);
}}
.btn-primary:hover:not(:disabled) {{
  filter: brightness(0.95);
}}

.btn-outline {{
  background-color: transparent;
  border-color: hsl(var(--border));
  color: hsl(var(--foreground));
}}
.btn-outline:hover:not(:disabled) {{
  background-color: hsl(var(--accent));
}}
</style>
"""

    def build_card(
        self,
        title: str = "Visão Geral",
        subtitle: str = "Acompanhe suas métricas em tempo real",
        stack: str = "react_tailwind",
    ) -> str:
        """Builds a high-end card container with tactile borders and elevation."""
        if stack == "react_tailwind":
            return f"""import React, {{ HTMLAttributes }} from 'react';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {{
  title?: string;
  subtitle?: string;
  headerAction?: React.ReactNode;
}}

export const Card: React.FC<CardProps> = ({{
  title = '{title}',
  subtitle = '{subtitle}',
  headerAction,
  children,
  className = '',
  ...props
}}) => {{
  return (
    <article
      className={{`bg-card text-card-foreground rounded-lg border border-border/80 shadow-sm transition-all duration-200 hover:border-border hover:shadow-md ${{className}}`}}
      {{...props}}
    >
      <header className="p-6 border-b border-border/50 flex items-start justify-between">
        <div>
          <h3 className="font-semibold text-lg tracking-tight text-foreground">{{title}}</h3>
          {{subtitle && <p className="text-sm text-muted-foreground mt-1">{{subtitle}}</p>}}
        </div>
        {{headerAction && <div className="ml-4">{{headerAction}}</div>}}
      </header>
      <div className="p-6">
        {{children}}
      </div>
    </article>
  );
}};
"""

        # Vanilla HTML5 + CSS
        return f"""<!-- HTML5 Semantic Card Component -->
<article class="card">
  <header class="card-header">
    <h3 class="card-title">{title}</h3>
    <p class="card-subtitle">{subtitle}</p>
  </header>
  <div class="card-body">
    <!-- Card Content Here -->
  </div>
</article>

<style>
.card {{
  background-color: hsl(var(--card));
  color: hsl(var(--card-foreground));
  border-radius: var(--radius-lg, 0.5rem);
  border: 1px solid hsl(var(--border) / 0.8);
  box-shadow: var(--shadow-sm);
  transition: var(--transition-tactile, all 0.2s ease);
}}

.card:hover {{
  border-color: hsl(var(--border));
  box-shadow: var(--shadow-md);
}}

.card-header {{
  padding: 1.5rem;
  border-bottom: 1px solid hsl(var(--border) / 0.5);
}}

.card-title {{
  margin: 0;
  font-size: var(--text-lg, 1.125rem);
  font-weight: 600;
  letter-spacing: -0.015em;
}}

.card-subtitle {{
  margin: 0.25rem 0 0;
  font-size: var(--text-sm, 0.875rem);
  color: hsl(var(--muted-foreground));
}}

.card-body {{
  padding: 1.5rem;
}}
</style>
"""

    def build_input(
        self,
        label: str = "E-mail Corporativo",
        input_id: str = "email_input",
        input_type: str = "email",
        placeholder: str = "voce@empresa.com",
        stack: str = "react_tailwind",
    ) -> str:
        """Builds an accessible form input with label and helper text."""
        if stack == "react_tailwind":
            return f"""import React, {{ InputHTMLAttributes, forwardRef }} from 'react';

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {{
  label: string;
  error?: string;
  helperText?: string;
}}

export const InputField = forwardRef<HTMLInputElement, InputProps>(({{
  label = '{label}',
  id = '{input_id}',
  type = '{input_type}',
  placeholder = '{placeholder}',
  error,
  helperText,
  className = '',
  ...props
}}, ref) => {{
  return (
    <div className="w-full flex flex-col gap-1.5">
      <label htmlFor={{id}} className="text-sm font-medium text-foreground select-none">
        {{label}}
      </label>
      <input
        ref={{ref}}
        id={{id}}
        type={{type}}
        placeholder={{placeholder}}
        aria-invalid={{!!error}}
        aria-describedby={{error ? `${{id}}-error` : helperText ? `${{id}}-helper` : undefined}}
        className={{`h-10 w-full rounded-md border bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${{
          error ? 'border-destructive focus-visible:ring-destructive' : 'border-input hover:border-border'
        }} ${{className}}`}}
        {{...props}}
      />
      {{error ? (
        <p id={{`${{id}}-error`}} className="text-xs text-destructive mt-0.5" role="alert">
          {{error}}
        </p>
      ) : helperText ? (
        <p id={{`${{id}}-helper`}} className="text-xs text-muted-foreground mt-0.5">
          {{helperText}}
        </p>
      ) : null}}
    </div>
  );
}});

InputField.displayName = 'InputField';
"""

        # Vanilla HTML5 + CSS
        return f"""<!-- HTML5 Accessible Input Component -->
<div class="input-group">
  <label for="{input_id}" class="input-label">{label}</label>
  <input
    id="{input_id}"
    type="{input_type}"
    placeholder="{placeholder}"
    class="input-field"
  />
</div>

<style>
.input-group {{
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  width: 100%;
}}

.input-label {{
  font-size: var(--text-sm, 0.875rem);
  font-weight: 500;
  color: hsl(var(--foreground));
}}

.input-field {{
  height: 2.5rem;
  width: 100%;
  border-radius: var(--radius-md, 0.375rem);
  border: 1px solid hsl(var(--input));
  background-color: hsl(var(--background));
  padding: 0 0.75rem;
  font-size: var(--text-sm, 0.875rem);
  color: hsl(var(--foreground));
  transition: var(--transition-tactile, all 0.15s ease);
  outline: none;
}}

.input-field:focus-visible {{
  outline: 2px solid hsl(var(--ring));
  outline-offset: 2px;
}}
</style>
"""
