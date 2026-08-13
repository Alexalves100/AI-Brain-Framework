"""
Knowledge Engine — knowledge base management
Version: 1.1.0
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..core import Context, Skill, SkillResult, SkillStatus


class KnowledgeEngine(Skill):
    name = "knowledge"
    version = "1.1.0"
    category = "core"
    description = "Persistent knowledge base with search and indexing"

    VALID_ACTIONS = ("add", "get", "search")

    def __init__(self, path: str = ".knowledge.json", **kwargs):
        super().__init__(**kwargs)
        self.path = Path(path)
        self._kb: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            try:
                loaded = json.loads(self.path.read_text(encoding="utf-8"))
                self._kb = loaded if isinstance(loaded, dict) else {}
            except (json.JSONDecodeError, OSError):
                self._kb = {}

    def _save(self) -> bool:
        """Tenta persistir a KB. Retorna True em sucesso, False em falha."""
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(
                json.dumps(self._kb, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            return True
        except OSError:
            return False

    def add(self, key: str, content: str, tags: Optional[List[str]] = None,
            source: Optional[str] = None) -> bool:
        if not isinstance(key, str) or not key:
            return False
        self._kb[key] = {
            "content": content if isinstance(content, str) else "",
            "tags": tags if isinstance(tags, list) else [],
            "source": source if isinstance(source, str) else None,
        }
        return self._save()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        if not isinstance(key, str):
            return None
        return self._kb.get(key)

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        if not isinstance(query, str) or not query:
            return []
        q = query.lower()
        results = []
        for key, entry in self._kb.items():
            content = entry.get("content", "") if isinstance(entry, dict) else ""
            tags = entry.get("tags", []) if isinstance(entry, dict) else []
            score = sum(
                1 for word in q.split()
                if word in content.lower() or word in key.lower()
                or any(isinstance(tag, str) and word in tag.lower() for tag in tags)
            )
            if score > 0:
                results.append({
                    "key": key,
                    "score": score,
                    "preview": content[:100],
                    "tags": tags,
                })
        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:max(0, limit)]

    def run(self, context: Context) -> SkillResult:
        action = context.get("action", "get")
        key = context.get("key")
        query = context.get("query")

        if not isinstance(action, str) or action not in self.VALID_ACTIONS:
            return SkillResult(
                status=SkillStatus.ERROR,
                error=f"Invalid action '{action}'. Valid: {self.VALID_ACTIONS}",
            )

        if action in ("add", "get"):
            if not isinstance(key, str) or not key:
                return SkillResult(
                    status=SkillStatus.ERROR,
                    error=f"Action '{action}' requires a non-empty string key",
                )

        if action == "add":
            saved = self.add(
                key,
                context.get("content", ""),
                context.get("tags"),
                context.get("source"),
            )
            if not saved:
                return SkillResult(
                    status=SkillStatus.ERROR,
                    error=f"Failed to persist key '{key}'",
                )
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={"action": "add", "key": key, "saved": True},
            )

        if action == "get":
            entry = self.get(key)
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={"key": key, "entry": entry},
            )

        if action == "search":
            if not isinstance(query, str) or not query:
                return SkillResult(
                    status=SkillStatus.ERROR,
                    error="Action 'search' requires a non-empty string query",
                )
            results = self.search(query, context.get("limit", 5))
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={"query": query, "results": results, "count": len(results)},
            )

        return SkillResult(
            status=SkillStatus.ERROR,
            error=f"Unhandled action '{action}'",
        )
