"""
Memory Engine — persistent key-value memory
Version: 1.0.0
"""

import json
from pathlib import Path
from typing import Any, Optional
from ..core import Skill, SkillResult, SkillStatus, Context


class MemoryEngine(Skill):
    name = "memory"
    version = "1.0.0"
    category = "core"
    description = "Persistent key-value memory with snapshot support"

    def __init__(self, path: str = ".memory.json", **kwargs):
        super().__init__(**kwargs)
        self.path = Path(path)
        self._store: dict = {}
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            try:
                self._store = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                self._store = {}

    def _save(self) -> None:
        self.path.write_text(
            json.dumps(self._store, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value
        self._save()

    def delete(self, key: str) -> None:
        self._store.pop(key, None)
        self._save()

    def snapshot(self) -> dict:
        return dict(self._store)

    def run(self, context: Context) -> SkillResult:
        action = context.get("action", "get")
        key = context.get("key")
        value = context.get("value")

        if action == "get" and key:
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={"key": key, "value": self.get(key)},
            )
        if action == "set" and key:
            self.set(key, value)
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={"key": key, "saved": True},
            )
        if action == "delete" and key:
            self.delete(key)
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
            error=f"Invalid action '{action}' or missing key",
        )
