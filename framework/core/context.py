"""
Context management with Time-Travel Checkpoints & Transactional Rollback
Version: 1.1.0
"""

import copy
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Context:
    """
    Transactional context object passed between skills and DAG nodes.
    Supports deep state snapshots, time-travel debugging, and rollback.
    """

    data: Dict[str, Any] = field(default_factory=dict)
    tokens_used: int = 0
    history: List[str] = field(default_factory=list)
    _checkpoints: Dict[str, Dict[str, Any]] = field(default_factory=dict, repr=False)
    _checkpoint_order: List[str] = field(default_factory=list, repr=False)

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

    def checkpoint(self, name: Optional[str] = None) -> str:
        """
        Creates an immutable deep snapshot of the current context state.
        Returns the checkpoint identifier.
        """
        cp_name = name or f"checkpoint_{len(self._checkpoint_order) + 1}"
        snapshot = {
            "name": cp_name,
            "timestamp": time.time(),
            "data": copy.deepcopy(self.data),
            "tokens_used": self.tokens_used,
            "history": copy.deepcopy(self.history),
            "keys_count": len(self.data),
        }
        self._checkpoints[cp_name] = snapshot
        if cp_name not in self._checkpoint_order:
            self._checkpoint_order.append(cp_name)
        return cp_name

    def rollback(self, name: Optional[str] = None) -> bool:
        """
        Restores context state to a named checkpoint (or the most recent one).
        Returns True if rollback succeeded, False if checkpoint not found.
        """
        if not self._checkpoint_order:
            return False

        target_name = name or self._checkpoint_order[-1]
        if target_name not in self._checkpoints:
            return False

        snapshot = self._checkpoints[target_name]
        self.data = copy.deepcopy(snapshot["data"])
        self.tokens_used = snapshot["tokens_used"]
        self.history = copy.deepcopy(snapshot["history"])
        return True

    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """Returns the timeline of all registered checkpoints."""
        return [
            {
                "name": name,
                "timestamp": self._checkpoints[name]["timestamp"],
                "keys_count": self._checkpoints[name]["keys_count"],
                "tokens_used": self._checkpoints[name]["tokens_used"],
            }
            for name in self._checkpoint_order
        ]

    def clear_checkpoints(self) -> None:
        """Clears all stored checkpoint snapshots."""
        self._checkpoints.clear()
        self._checkpoint_order.clear()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "tokens_used": self.tokens_used,
            "history_len": len(self.history),
            "checkpoints_count": len(self._checkpoint_order),
        }
