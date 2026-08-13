"""
AI-Brain-Framework
Version: 1.0.0
Professional framework with digital brain for building websites and web systems.
"""

__version__ = "1.0.0"
__author__ = "AI-Brain-Framework"

from .core import Orchestrator, SkillRegistry, Context, Skill, SkillResult, SkillStatus
from .engines import (
    BrainEngine,
    SecurityEngine,
    TokenEconomyEngine,
    MemoryEngine,
    KnowledgeEngine,
    ReasoningEngine,
    DiscoveryEngine,
    UIDesignEngine,
    CleanCodeEngine,
)
from .standards import SecurityHeaders, InputValidator, SeniorGuidelines
from .scanners import CodeScanner, DependencyScanner, StructureScanner, ASTScanner
from .analyzers import ComplexityAnalyzer, QualityAnalyzer, MetricsAnalyzer, CodeSmellDetector
from .builders import ProjectBuilder, ModuleBuilder, ConfigBuilder
from .governance import PolicyEngine, AuditLog, ComplianceChecker
from .prompts import PromptRegistry, PromptBuilder, SeniorPromptTemplates
from .schemas import SchemaValidator, SchemaRegistry



def create_default_orchestrator() -> Orchestrator:
    """Create an orchestrator pre-loaded with all default engines."""
    registry = SkillRegistry()
    registry.register(BrainEngine())
    registry.register(SecurityEngine())
    registry.register(TokenEconomyEngine())
    registry.register(MemoryEngine())
    registry.register(KnowledgeEngine())
    registry.register(ReasoningEngine())
    registry.register(DiscoveryEngine())
    registry.register(UIDesignEngine())
    return Orchestrator(registry)


__all__ = [
    "Orchestrator",
    "SkillRegistry",
    "Context",
    "Skill",
    "SkillResult",
    "SkillStatus",
    "BrainEngine",
    "SecurityEngine",
    "TokenEconomyEngine",
    "MemoryEngine",
    "KnowledgeEngine",
    "ReasoningEngine",
    "DiscoveryEngine",
    "UIDesignEngine",
    "SecurityHeaders",
    "InputValidator",
    "CodeScanner",
    "DependencyScanner",
    "StructureScanner",
    "ComplexityAnalyzer",
    "QualityAnalyzer",
    "MetricsAnalyzer",
    "ProjectBuilder",
    "ModuleBuilder",
    "ConfigBuilder",
    "PolicyEngine",
    "AuditLog",
    "ComplianceChecker",
    "PromptRegistry",
    "PromptBuilder",
    "SchemaValidator",
    "SchemaRegistry",
    "create_default_orchestrator",
]
