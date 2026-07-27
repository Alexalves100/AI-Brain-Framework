"""
Config Builder — generates configuration files
Version: 1.0.0
"""

from typing import Dict, Any


class ConfigBuilder:
    """Generates configuration files in various formats."""

    def toml(self, data: Dict[str, Any]) -> str:
        lines = []
        for key, value in data.items():
            lines.append(f"[{key}]")
            if isinstance(value, dict):
                for k, v in value.items():
                    lines.append(f'{k} = "{v}"')
            else:
                lines.append(f'value = "{value}"')
            lines.append("")
        return "\n".join(lines)

    def env(self, data: Dict[str, Any]) -> str:
        return "\n".join(f"{k}={v}" for k, v in data.items())

    def yaml(self, data: Dict[str, Any]) -> str:
        lines = []
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{key}:")
                for k, v in value.items():
                    lines.append(f"  {k}: {v}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)

    def json(self, data: Dict[str, Any]) -> str:
        import json
        return json.dumps(data, indent=2, ensure_ascii=False)
