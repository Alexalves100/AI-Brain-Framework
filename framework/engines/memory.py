"""
Memory Engine — persistent key-value memory
Version: 1.1.0
"""

import json
from pathlib import Path
from typing import Any, Optional
from ..core import Skill, SkillResult, SkillStatus, Context


class MemoryEngine(Skill):
    name = "memory"
    version = "1.1.0"
    category = "core"
    description = "Persistent key-value memory with snapshot support"

    VALID_ACTIONS = ("get", "set", "delete", "snapshot")

    def __init__(self, path: str = ".memory.json", **kwargs):
        super().__init__(**kwargs)
        self.path = Path(path)
        self._store: dict = {}
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            try:
                self._store = json.loads(self.path.read_text(encoding="utf-8"))
                if not isinstance(self._store, dict):
                    self._store = {}
            except (json.JSONDecodeError, OSError):
                self._store = {}

    def _save(self) -> bool:
        """Tenta persistir o store. Retorna True em sucesso, False em falha."""
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(
                json.dumps(self._store, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            return True
        except OSError:
            return False

    def get(self, key: str, default: Any = None) -> Any:
        if not isinstance(key, str):
            return default
        return self._store.get(key, default)

    def set(self, key: str, value: Any) -> bool:
        if not isinstance(key, str) or not key:
            return False
        self._store[key] = value
        return self._save()

    def delete(self, key: str) -> bool:
        if not isinstance(key, str):
            return False
        self._store.pop(key, None)
        return self._save()

    def snapshot(self) -> dict:
        return dict(self._store)

    def run(self, context: Context) -> SkillResult:
        action = context.get("action", "get")
        key = context.get("key")
        value = context.get("value")

        if not isinstance(action, str) or action not in self.VALID_ACTIONS:
            return SkillResult(
                status=SkillStatus.ERROR,
                error=f"Invalid action '{action}'. Valid: {self.VALID_ACTIONS}",
            )

        if action in ("get", "set", "delete"):
            if not isinstance(key, str) or not key:
                return SkillResult(
                    status=SkillStatus.ERROR,
                    error=f"Action '{action}' requires a non-empty string key",
                )

        if action == "get":
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={"key": key, "value": self.get(key)},
            )
        if action == "set":
            saved = self.set(key, value)
            if not saved:
                return SkillResult(
                    status=SkillStatus.ERROR,
                    error=f"Failed to persist key '{key}'",
                )
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={"key": key, "saved": True},
            )
        if action == "delete":
            deleted = self.delete(key)
            if not deleted:
                return SkillResult(
                    status=SkillStatus.ERROR,
                    error=f"Failed to persist deletion of '{key}'",
                )
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={"key": key, "deleted": True},
            )
        if action == "snapshot":
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={"snapshot": self.snapshot()},
            )
        return SkillResult(
            status=SkillStatus.ERROR,
            error=f"Unhandled action '{action}'",
        )
