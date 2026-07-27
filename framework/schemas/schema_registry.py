"""
Schema Registry — manages named schemas
Version: 1.0.0
"""

from typing import Dict, List


class SchemaRegistry:
    """Central registry for reusable schemas."""

    DEFAULT_SCHEMAS = {
        "user": {
            "type": "object",
            "required": ["id", "email"],
            "properties": {
                "id": {"type": "string"},
                "email": {"type": "string", "pattern": r"^[^@]+@[^@]+$"},
                "name": {"type": "string", "minLength": 1, "maxLength": 100},
            },
        },
        "skill": {
            "type": "object",
            "required": ["name", "version"],
            "properties": {
                "name": {"type": "string", "minLength": 1, "maxLength": 50},
                "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
                "category": {"type": "string"},
                "description": {"type": "string", "maxLength": 500},
            },
        },
        "engine_result": {
            "type": "object",
            "required": ["status"],
            "properties": {
                "status": {"type": "string"},
                "output": {},
                "error": {"type": "string"},
                "tokens_used": {"type": "integer", "minimum": 0},
            },
        },
    }

    def __init__(self):
        self._schemas: Dict[str, Dict] = dict(self.DEFAULT_SCHEMAS)

    def register(self, name: str, schema: Dict) -> None:
        self._schemas[name] = schema

    def get(self, name: str) -> Dict:
        return self._schemas.get(name, {})

    def list(self) -> List[str]:
        return sorted(self._schemas.keys())
