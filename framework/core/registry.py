"""
Skill Registry
Version: 1.0.0
"""

from typing import Dict, List, Optional

from .skill import Skill


class SkillRegistry:
    """Central registry for all skills."""

    def __init__(self):
        self._skills: Dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        if skill.name in self._skills:
            raise ValueError(f"Skill '{skill.name}' already registered")
        self._skills[skill.name] = skill

    def unregister(self, name: str) -> None:
        self._skills.pop(name, None)

    def get(self, name: str) -> Optional[Skill]:
        return self._skills.get(name)

    def list(self, category: Optional[str] = None) -> List[Skill]:
        skills = list(self._skills.values())
        if category:
            skills = [s for s in skills if s.category == category]
        return sorted(skills, key=lambda s: s.name)

    def categories(self) -> List[str]:
        return sorted({s.category for s in self._skills.values()})


    def __len__(self):
        return len(self._skills)

    def __contains__(self, name: str):
        return name in self._skills
