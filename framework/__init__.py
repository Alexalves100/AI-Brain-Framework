"""
AI-Brain-Framework
Version: 1.0.0
Professional framework with digital brain for building websites and web systems.
"""

__version__ = "1.0.0"
__author__ = "AI-Brain-Framework"

from .analyzers import CodeSmellDetector, ComplexityAnalyzer, MetricsAnalyzer, QualityAnalyzer
from .builders import ConfigBuilder, ModuleBuilder, ProjectBuilder
from .core import (
    Context,
    CyclicDependencyError,
    DAGExecutionResult,
    DAGNode,
    Orchestrator,
    Skill,
    SkillRegistry,
    SkillResult,
    SkillStatus,
    WorkflowDAG,
)
from .engines import (
    BrainEngine,
    CleanCodeEngine,
    CodePatcherEngine,
    DiscoveryEngine,
    FullstackUIEngine,
    KnowledgeEngine,
    MemoryEngine,
    PromptShieldEngine,
    ReasoningEngine,
    SecurityEngine,
    TokenEconomyEngine,
    UIDesignEngine,
)
from .frontend import (
    A11yAuditor,
    A11yAuditResult,
    A11yViolation,
    APIClientGenerator,
    ComponentBuilder,
    DesignTokens,
)
from .governance import AuditLog, ComplianceChecker, PolicyEngine
from .guardrails import DialogRails, InjectionDetector, OutputGuard, PIIShield, ToolSandbox
from .mcp import JsonRpcMessage, MCPServer, MCPToolRegistry
from .patchers import ASTPatcher, DiffApplier, FuzzyMatcher, PatchResult, SurgicalCodePatcher
from .prompts import PromptBuilder, PromptRegistry, SeniorPromptTemplates
from .scanners import ASTScanner, CodeScanner, DependencyScanner, StructureScanner
from .schemas import SchemaRegistry, SchemaValidator
from .standards import InputValidator, SecurityHeaders, SeniorGuidelines


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
    registry.register(PromptShieldEngine())
    registry.register(CodePatcherEngine())
    registry.register(FullstackUIEngine())
    return Orchestrator(registry)





__all__ = [
    "Orchestrator",
    "DAGExecutionResult",
    "DAGNode",
    "WorkflowDAG",
    "CyclicDependencyError",
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
    "CleanCodeEngine",
    "PromptShieldEngine",
    "CodePatcherEngine",
    "FullstackUIEngine",
    "DesignTokens",
    "ComponentBuilder",
    "A11yAuditor",
    "A11yAuditResult",
    "A11yViolation",
    "APIClientGenerator",
    "SurgicalCodePatcher",
    "ASTPatcher",
    "FuzzyMatcher",
    "DiffApplier",
    "PatchResult",
    "SecurityHeaders",
    "InputValidator",


    "SeniorGuidelines",
    "CodeScanner",
    "DependencyScanner",
    "StructureScanner",
    "ASTScanner",
    "ComplexityAnalyzer",
    "QualityAnalyzer",
    "MetricsAnalyzer",
    "CodeSmellDetector",
    "InjectionDetector",
    "PIIShield",
    "DialogRails",
    "ToolSandbox",
    "OutputGuard",
    "ProjectBuilder",
    "ModuleBuilder",
    "ConfigBuilder",
    "PolicyEngine",
    "AuditLog",
    "ComplianceChecker",
    "PromptRegistry",
    "PromptBuilder",
    "SeniorPromptTemplates",
    "SchemaValidator",
    "SchemaRegistry",
    "MCPServer",
    "MCPToolRegistry",
    "JsonRpcMessage",
    "create_default_orchestrator",
]



