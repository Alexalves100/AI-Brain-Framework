"""
Knowledge Engine — knowledge base management
Version: 1.0.0
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from ..core import Skill, SkillResult, SkillStatus, Context


class KnowledgeEngine(Skill):
    name = "knowledge"
    version = "1.0.0"
    category = "core"
    description = "Persistent knowledge base with search and indexing"

    def __init__(self, path: str = ".knowledge.json", **kwargs):
        super().__init__(**kwargs)
        self.path = Path(path)
        self._kb: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            try:
                self._kb = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                self._kb = {}

    def _save(self) -> None:
        self.path.write_text(
            json.dumps(self._kb, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def add(self, key: str, content: str, tags: Optional[List[str]] = None,
            source: Optional[str] = None) -> None:
        self._kb[key] = {
            "content": content,
            "tags": tags or [],
            "source": source,
        }
        self._save()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        return self._kb.get(key)

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        q = query.lower()
        results = []
        for key, entry in self._kb.items():
            score = sum(
                1 for word in q.split()
                if word in entry["content"].lower() or word in key.lower()
                or any(word in tag.lower() for tag in entry.get("tags", []))
            )
            if score > 0:
                results.append({
                    "key": key,
                    "score": score,
                    "preview": entry["content"][:100],
                    "tags": entry.get("tags", []),
                })
        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:limit]

    def run(self, context: Context) -> SkillResult:
        action = context.get("action", "get")
        key = context.get("key")
        query = context.get("query")

        if action == "add" and key:
            self.add(key, context.get("content", ""),
                    context.get("tags"), context.get("source"))
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={"action": "add", "key": key, "saved": True},
            )

        if action == "get" and key:
            entry = self.get(key)
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={"key": key, "entry": entry},
            )

        if action == "search" and query:
            results = self.search(query, context.get("limit", 5))
            return SkillResult(
                status=SkillStatus.SUCCESS,
                output={"query": query, "results": results, "count": len(results)},
            )

        return SkillResult(
            status=SkillStatus.ERROR,
            error=f"Invalid action '{action}' or missing params",
        )
