"""
Audit Log — append-only event log
Version: 1.0.0
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List


class AuditLog:
    """Append-only audit log with optional persistence."""

    def __init__(self, path: str = ".audit.jsonl"):
        self.path = Path(path)
        self._events: List[Dict[str, Any]] = []
        if self.path.exists():
            try:
                with self.path.open("r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            self._events.append(json.loads(line))
            except Exception:
                pass

    def log(self, event: str, actor: str = "system", **details) -> Dict[str, Any]:
        entry = {
            "timestamp": time.time(),
            "event": event,
            "actor": actor,
            "details": details,
        }
        self._events.append(entry)
        self._persist(entry)
        return entry

    def _persist(self, entry: Dict[str, Any]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def query(self, event: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        results = self._events
        if event:
            results = [e for e in results if e["event"] == event]
        return results[-limit:]

    def clear(self) -> None:
        self._events.clear()
        if self.path.exists():
            self.path.unlink()
