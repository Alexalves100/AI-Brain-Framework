"""
Context management
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Context:
    """Minimal context object passed between skills."""

    data: Dict[str, Any] = field(default_factory=dict)
    tokens_used: int = 0
    history: list = field(default_factory=list)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value

    def has(self, key: str) -> bool:
        return key in self.data

    def add_tokens(self, n: int) -> None:
        self.tokens_used += n

    def log(self, entry: str) -> None:
        self.history.append(entry)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "tokens_used": self.tokens_used,
            "history_len": len(self.history),
        }
