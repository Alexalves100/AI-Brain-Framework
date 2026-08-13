"""
Schema Validator — validates data against schemas
Version: 1.0.0
"""

from typing import Any, Dict, List


class SchemaValidator:
    """Validates dictionaries against simple JSON-Schema-like definitions."""

    def validate(self, data: Any, schema: Dict[str, Any]) -> List[str]:
        errors = []

        expected_type = schema.get("type")
        if expected_type:
            if not self._check_type(data, expected_type):
                errors.append(f"expected type '{expected_type}', got '{type(data).__name__}'")

        if expected_type == "object" and isinstance(data, dict):
            required = schema.get("required", [])
            for field in required:
                if field not in data:
                    errors.append(f"missing required field '{field}'")

            properties = schema.get("properties", {})
            for key, value in data.items():
                if key in properties:
                    errors.extend(self.validate(value, properties[key]))

        if expected_type == "array" and isinstance(data, list):
            items_schema = schema.get("items")
            if items_schema:
                for i, item in enumerate(data):
                    item_errors = self.validate(item, items_schema)
                    errors.extend([f"[{i}] {e}" for e in item_errors])

        if expected_type == "string" and isinstance(data, str):
            if "minLength" in schema and len(data) < schema["minLength"]:
                errors.append(f"string shorter than {schema['minLength']}")
            if "maxLength" in schema and len(data) > schema["maxLength"]:
                errors.append(f"string longer than {schema['maxLength']}")
            if "pattern" in schema:
                import re
                if not re.search(schema["pattern"], data):
                    errors.append("string does not match pattern")

        return errors

    def _check_type(self, data: Any, expected: str) -> bool:
        type_map: Dict[str, Any] = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict,
            "null": type(None),
        }
        if expected in type_map:
            target_type = type_map[expected]
            if isinstance(target_type, tuple):
                return isinstance(data, target_type)
            return isinstance(data, target_type)
        return True


    def is_valid(self, data: Any, schema: Dict[str, Any]) -> bool:
        return len(self.validate(data, schema)) == 0
