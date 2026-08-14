"""
Backend-to-Frontend Bridge: Schema to TypeScript SDK & Form Generator
Version: 1.0.0
"""

from typing import Any, Dict, List, Optional


class APIClientGenerator:
    """
    Translates backend Schemas and Models into strictly typed TypeScript interfaces,
    type-safe Fetch API client functions, and accessible React forms.
    Zero external dependencies.
    """

    TYPE_MAPPING = {
        "string": "string",
        "str": "string",
        "integer": "number",
        "int": "number",
        "float": "number",
        "number": "number",
        "boolean": "boolean",
        "bool": "boolean",
        "array": "any[]",
        "list": "any[]",
        "object": "Record<string, any>",
        "dict": "Record<string, any>",
    }

    def generate_typescript_interface(
        self,
        schema_name: str,
        properties: Dict[str, Any],
        required_fields: Optional[List[str]] = None,
    ) -> str:
        """Generates a TypeScript interface declaration from schema properties."""
        req_set = set(required_fields or [])
        lines = [f"export interface {schema_name} {{"]

        for prop_name, prop_spec in properties.items():
            if isinstance(prop_spec, dict):
                p_type = prop_spec.get("type", "string")
                description = prop_spec.get("description")
            elif isinstance(prop_spec, str):
                p_type = prop_spec
                description = None
            else:
                p_type = "any"
                description = None

            ts_type = self.TYPE_MAPPING.get(p_type.lower(), "any")
            is_optional = prop_name not in req_set

            doc = f"  /** {description} */\n" if description else ""
            opt_mark = "?" if is_optional else ""
            lines.append(f"{doc}  {prop_name}{opt_mark}: {ts_type};")

        lines.append("}\n")
        return "\n".join(lines)

    def generate_fetch_client(
        self,
        endpoint_name: str,
        method: str,
        path: str,
        request_type: Optional[str] = None,
        response_type: str = "any",
    ) -> str:
        """Generates a type-safe Fetch API wrapper function."""
        has_body = method.upper() in ["POST", "PUT", "PATCH"]
        req_param = f"payload: {request_type}" if has_body and request_type else ""

        body_clause = ",\n    body: JSON.stringify(payload)" if has_body and request_type else ""

        return f"""export async function {endpoint_name}({req_param}): Promise<{response_type}> {{
  const response = await fetch('{path}', {{
    method: '{method.upper()}',
    headers: {{
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    }}{body_clause},
  }});

  if (!response.ok) {{
    const errorBody = await response.json().catch(() => ({{}}));
    throw new Error(errorBody.message || `API Error: ${{response.status}} ${{response.statusText}}`);
  }}

  return (await response.json()) as {response_type};
}}
"""

    def generate_react_form(
        self,
        schema_name: str,
        properties: Dict[str, Any],
        required_fields: Optional[List[str]] = None,
        submit_endpoint: str = "/api/submit",
    ) -> str:
        """Generates a complete accessible React form component with state management."""
        req_set = set(required_fields or [])

        # Form fields generator
        field_elements = []
        state_initializers = []

        for prop_name, prop_spec in properties.items():
            p_type = prop_spec.get("type", "string") if isinstance(prop_spec, dict) else "string"
            label = prop_name.replace("_", " ").title()
            is_req = prop_name in req_set
            req_attr = " required" if is_req else ""

            input_type = "email" if "email" in prop_name else "number" if p_type in ["integer", "number"] else "text"
            init_val = "0" if p_type in ["integer", "number"] else "''"
            state_initializers.append(f"    {prop_name}: {init_val},")

            field_elements.append(f"""        <div className="flex flex-col gap-1.5">
          <label htmlFor="{prop_name}" className="text-sm font-medium text-foreground">
            {label}{" *" if is_req else ""}
          </label>
          <input
            id="{prop_name}"
            name="{prop_name}"
            type="{input_type}"
            value={{formData.{prop_name}}}
            onChange={{handleChange}}
            className="h-10 px-3 rounded-md border border-input bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"{req_attr}
          />
        </div>""")

        fields_jsx = "\n".join(field_elements)
        state_jsx = "\n".join(state_initializers)

        return f"""import React, {{ useState, FormEvent, ChangeEvent }} from 'react';
import {{ {schema_name} }} from './types';

export const {schema_name}Form: React.FC = () => {{
  const [formData, setFormData] = useState<{schema_name}>({{
{state_jsx}
  }});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {{
    const {{ name, value, type }} = e.target;
    setFormData((prev) => ({{
      ...prev,
      [name]: type === 'number' ? Number(value) : value,
    }}));
  }};

  const handleSubmit = async (e: FormEvent) => {{
    e.preventDefault();
    setIsSubmitting(true);
    setErrorMessage(null);

    try {{
      const res = await fetch('{submit_endpoint}', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(formData),
      }});
      if (!res.ok) throw new Error('Falha ao enviar formulário.');
      alert('Enviado com sucesso!');
    }} catch (err: any) {{
      setErrorMessage(err.message || 'Erro desconhecido');
    }} finally {{
      setIsSubmitting(false);
    }}
  }};

  return (
    <form onSubmit={{handleSubmit}} className="space-y-4 max-w-md p-6 bg-card border border-border rounded-lg shadow-sm">
      <h2 className="text-lg font-semibold text-foreground">Cadastro de {schema_name}</h2>
      {{errorMessage && (
        <div className="p-3 text-sm text-destructive bg-destructive/10 rounded-md" role="alert">
          {{errorMessage}}
        </div>
      )}}
{fields_jsx}
      <button
        type="submit"
        disabled={{isSubmitting}}
        className="w-full h-10 px-4 mt-2 bg-primary text-primary-foreground font-medium rounded-md hover:bg-primary/90 transition-all focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50 cursor-pointer"
      >
        {{isSubmitting ? 'Enviando...' : 'Salvar'}}
      </button>
    </form>
  );
}};
"""
