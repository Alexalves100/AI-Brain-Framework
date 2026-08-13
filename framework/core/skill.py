"""
Skill base class
Version: 1.0.0
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from .context import Context



class SkillStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class SkillResult:
    status: SkillStatus
    output: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    tokens_used: int = 0


class Skill:
    """Base class for all skills."""

    name: str = "base"
    version: str = "1.0.0"
    category: str = "core"
    description: str = ""

    def __init__(self, **kwargs):
        self.config = kwargs

    def run(self, context: "Context") -> SkillResult:
        """Execute the skill. Override in subclasses."""
        raise NotImplementedError

    def validate_inputs(self, context: "Context") -> bool:
        """Validate required inputs. Override if needed."""
        return True

    def __repr__(self):
        return f"<Skill {self.name} v{self.version}>"
