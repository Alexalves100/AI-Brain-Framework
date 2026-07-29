"""
OpenAPI 3.0 Generator Module.
Gera a documentação interativa e especificação técnica OpenAPI 3.0 / Swagger JSON
para APIs REST sem dependências externas.
"""
import json
from typing import Dict, Any, List, Optional

class OpenAPIGenerator:
    """Gerador automático de especificações OpenAPI 3.0."""

    def __init__(self, title: str = "AI-Brain API", version: str = "1.0.0", description: str = ""):
        self.spec: Dict[str, Any] = {
            "openapi": "3.0.3",
            "info": {
                "title": title,
                "version": version,
                "description": description or "Documentação de API gerada com AI-Brain-Framework",
            },
            "paths": {},
            "components": {
                "securitySchemes": {
                    "BearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                        "description": "Autenticação via Token JWT no header Authorization",
                    }
                },
                "schemas": {},
            },
        }

    def add_path(
        self,
        path: str,
        method: str,
        summary: str,
        responses: Dict[str, Any],
        parameters: Optional[List[Dict[str, Any]]] = None,
        request_body: Optional[Dict[str, Any]] = None,
        security_required: bool = True,
        tags: Optional[List[str]] = None,
    ) -> None:
        """Adiciona uma rota e seu método HTTP à especificação OpenAPI."""
        method_lower = method.lower()
        if path not in self.spec["paths"]:
            self.spec["paths"][path] = {}

        operation: Dict[str, Any] = {
            "summary": summary,
            "responses": responses,
        }

        if tags:
            operation["tags"] = tags
        if parameters:
            operation["parameters"] = parameters
        if request_body:
            operation["requestBody"] = request_body
        if security_required:
            operation["security"] = [{"BearerAuth": []}]

        self.spec["paths"][path][method_lower] = operation

    def add_schema(self, name: str, schema_def: Dict[str, Any]) -> None:
        """Adiciona um schema reutilizável em components.schemas."""
        self.spec["components"]["schemas"][name] = schema_def

    def to_dict(self) -> Dict[str, Any]:
        """Retorna o dicionário completo no formato OpenAPI 3.0."""
        return self.spec

    def to_json(self, indent: int = 2) -> str:
        """Retorna a string JSON formatada da especificação OpenAPI 3.0."""
        return json.dumps(self.spec, indent=indent, ensure_ascii=False)
