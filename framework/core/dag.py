"""
Directed Acyclic Graph (DAG) Workflow Engine with Kahn's Algorithm & Conditional Edges
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from .context import Context
from .skill import SkillResult


class CyclicDependencyError(Exception):
    """Raised when a cycle or self-referential loop is detected in the DAG topology."""
    pass


@dataclass
class DAGNode:
    """
    Represents a single executable node in the workflow graph.
    """

    name: str
    skill_name: Optional[str] = None
    action: Optional[Callable[[Context], SkillResult]] = None
    depends_on: List[str] = field(default_factory=list)
    condition: Optional[Callable[[Context], bool]] = None
    compensate: Optional[Callable[[Context], None]] = None
    retries: int = 0
    retry_delay: float = 0.0
    requires_human_approval: bool = False

    def __post_init__(self):
        if not self.skill_name and not self.action:
            raise ValueError(f"Node '{self.name}' must have either 'skill_name' or 'action' defined.")


@dataclass
class ConditionalEdge:
    """
    Represents dynamic routing from a source node to target nodes based on output evaluation.
    """

    source_node: str
    router: Callable[[SkillResult, Context], str]
    routes: Dict[str, str]  # e.g. {"safe": "brain_node", "unsafe": "quarantine_node"}


class WorkflowDAG:
    """
    Directed Acyclic Graph (DAG) for orchestrating complex agentic and business workflows.
    Includes cycle detection, layer-based parallel scheduling, and dynamic routing.
    Zero external dependencies.
    """

    def __init__(self, name: str = "default_dag"):
        self.name = name
        self.nodes: Dict[str, DAGNode] = {}
        self.conditional_edges: Dict[str, List[ConditionalEdge]] = {}

    def add_node(
        self,
        name: str,
        skill_name: Optional[str] = None,
        action: Optional[Callable[[Context], SkillResult]] = None,
        depends_on: Optional[List[str]] = None,
        condition: Optional[Callable[[Context], bool]] = None,
        compensate: Optional[Callable[[Context], None]] = None,
        retries: int = 0,
        retry_delay: float = 0.0,
        requires_human_approval: bool = False,
    ) -> "WorkflowDAG":
        """Adds an executable node to the DAG."""
        if name in self.nodes:
            raise ValueError(f"Node with name '{name}' already exists in DAG '{self.name}'.")

        deps = depends_on or []
        node = DAGNode(
            name=name,
            skill_name=skill_name,
            action=action,
            depends_on=deps,
            condition=condition,
            compensate=compensate,
            retries=retries,
            retry_delay=retry_delay,
            requires_human_approval=requires_human_approval,
        )
        self.nodes[name] = node
        return self

    def add_conditional_edge(
        self,
        source_node: str,
        router: Callable[[SkillResult, Context], str],
        routes: Dict[str, str],
    ) -> "WorkflowDAG":
        """Adds a conditional branch routing from a source node to destination nodes."""
        edge = ConditionalEdge(source_node=source_node, router=router, routes=routes)
        if source_node not in self.conditional_edges:
            self.conditional_edges[source_node] = []
        self.conditional_edges[source_node].append(edge)
        return self

    def get_topological_layers(self) -> List[List[DAGNode]]:
        """
        Computes the execution layers using Kahn's Algorithm.
        Nodes within the same layer can be safely executed in parallel.
        Raises CyclicDependencyError if any loop or circular dependency is found.
        """
        # Validate that all dependencies exist
        for node in self.nodes.values():
            for dep in node.depends_on:
                if dep not in self.nodes:
                    raise ValueError(f"Node '{node.name}' depends on non-existent node '{dep}'.")

        in_degree: Dict[str, int] = {name: len(node.depends_on) for name, node in self.nodes.items()}
        dependents: Dict[str, List[str]] = {name: [] for name in self.nodes}
        for name, node in self.nodes.items():
            for dep in node.depends_on:
                dependents[dep].append(name)

        # Nodes with in-degree 0 form the first layer
        current_layer_names: List[str] = [name for name, deg in in_degree.items() if deg == 0]
        layers: List[List[DAGNode]] = []
        visited_count = 0

        while current_layer_names:
            current_layer_names.sort()  # Deterministic execution order
            layer_nodes = [self.nodes[name] for name in current_layer_names]
            layers.append(layer_nodes)
            visited_count += len(current_layer_names)

            next_layer_names: List[str] = []
            for name in current_layer_names:
                for dependent in dependents[name]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        next_layer_names.append(dependent)

            current_layer_names = next_layer_names

        if visited_count != len(self.nodes):
            unvisited = [name for name, deg in in_degree.items() if deg > 0]
            raise CyclicDependencyError(
                f"Cyclic dependency detected in DAG '{self.name}'. Unresolved nodes: {unvisited}"
            )

        return layers

    def validate(self) -> None:
        """Validates the DAG structure and topology."""
        self.get_topological_layers()

    def __len__(self) -> int:
        return len(self.nodes)

    def __repr__(self) -> str:
        return f"<WorkflowDAG name='{self.name}' nodes={len(self.nodes)}>"
