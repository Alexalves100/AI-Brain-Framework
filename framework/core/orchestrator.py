"""
Orchestrator with Linear Pipelines & Stateful DAG Workflows
Version: 1.2.0
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from .context import Context
from .dag import DAGNode, WorkflowDAG
from .registry import SkillRegistry
from .skill import SkillResult, SkillStatus


@dataclass
class DAGExecutionResult:
    """Consolidated result of a DAG workflow execution."""

    status: SkillStatus
    node_results: Dict[str, SkillResult] = field(default_factory=dict)
    executed_nodes: List[str] = field(default_factory=list)
    skipped_nodes: List[str] = field(default_factory=list)
    failed_node: Optional[str] = None
    rollback_performed: bool = False
    compensated_nodes: List[str] = field(default_factory=list)
    checkpoints_created: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "executed_nodes": self.executed_nodes,
            "skipped_nodes": self.skipped_nodes,
            "failed_node": self.failed_node,
            "rollback_performed": self.rollback_performed,
            "compensated_nodes": self.compensated_nodes,
            "total_nodes_executed": len(self.executed_nodes),
        }


class Orchestrator:
    """
    Routes context through one or more skills or complex DAG workflows.
    Supports parallel layer execution, conditional branching, time-travel checkpoints,
    and automatic Saga compensation rollback.
    """

    def __init__(self, registry: Optional[SkillRegistry] = None):
        self.registry = registry or SkillRegistry()

    @staticmethod
    def _validate_inputs(skill_name: Any, context: Any) -> Optional[SkillResult]:
        """Validates input parameters."""
        if not isinstance(skill_name, str) or not skill_name.strip():
            return SkillResult(
                status=SkillStatus.ERROR,
                error="skill_name must be a non-empty string",
            )
        if context is None:
            return SkillResult(
                status=SkillStatus.ERROR,
                error="context must not be None",
            )
        if not isinstance(context, Context):
            return SkillResult(
                status=SkillStatus.ERROR,
                error="context must be an instance of Context",
            )
        return None

    def run(self, skill_name: str, context: Context) -> SkillResult:
        """Executes a single skill by name."""
        validation_error = self._validate_inputs(skill_name, context)
        if validation_error is not None:
            return validation_error

        skill = self.registry.get(skill_name)
        if not skill:
            return SkillResult(
                status=SkillStatus.ERROR,
                error=f"Skill '{skill_name}' not found",
            )
        if not skill.validate_inputs(context):
            return SkillResult(
                status=SkillStatus.ERROR,
                error=f"Invalid inputs for '{skill_name}'",
            )
        context.log(f"RUN: {skill_name}")
        result = skill.run(context)
        context.log(f"DONE: {skill_name} -> {result.status.value}")
        if result.tokens_used:
            context.add_tokens(result.tokens_used)
        return result

    def run_pipeline(self, names: List[str], context: Context) -> List[SkillResult]:
        """Executes a linear sequence of skills."""
        if not isinstance(names, list):
            return [
                SkillResult(
                    status=SkillStatus.ERROR,
                    error="names must be a list of skill names",
                )
            ]
        validation_error = self._validate_inputs(names[0] if names else "", context)
        if validation_error is not None and validation_error.error and "skill_name" in validation_error.error:
            return [validation_error]

        results: List[SkillResult] = []
        for name in names:
            r = self.run(name, context)
            results.append(r)
            if r.status == SkillStatus.ERROR:
                break
        return results

    def _execute_node_with_retries(self, node: DAGNode, context: Context) -> SkillResult:
        """Executes a single node handling retries and custom actions."""
        max_attempts = max(1, node.retries + 1)
        last_result: Optional[SkillResult] = None

        for attempt in range(1, max_attempts + 1):
            try:
                if node.action:
                    res = node.action(context)
                elif node.skill_name:
                    res = self.run(node.skill_name, context)
                else:
                    return SkillResult(status=SkillStatus.ERROR, error=f"Node '{node.name}' has no skill or action")

                if res.status != SkillStatus.ERROR:
                    return res
                last_result = res
            except Exception as e:
                last_result = SkillResult(status=SkillStatus.ERROR, error=f"Exception in node '{node.name}': {str(e)}")

            if attempt < max_attempts and node.retry_delay > 0:
                time.sleep(node.retry_delay)

        return last_result or SkillResult(status=SkillStatus.ERROR, error=f"Node '{node.name}' failed after {max_attempts} attempts")

    def run_dag(
        self,
        dag: WorkflowDAG,
        context: Context,
        parallel: bool = False,
        max_workers: int = 4,
        auto_rollback_on_error: bool = True,
    ) -> DAGExecutionResult:
        """
        Executes a WorkflowDAG with Kahn topological layers, conditional branching,
        state checkpoints, and Saga compensation rollback on failure.
        """
        initial_cp = context.checkpoint(f"dag_{dag.name}_start")
        checkpoints_created: List[str] = [initial_cp]

        try:
            layers = dag.get_topological_layers()
        except Exception as e:
            return DAGExecutionResult(
                status=SkillStatus.ERROR,
                failed_node=None,
                rollback_performed=False,
                node_results={"_topology": SkillResult(status=SkillStatus.ERROR, error=str(e))},
            )

        executed_nodes: List[str] = []
        skipped_nodes: Set[str] = set()
        node_results: Dict[str, SkillResult] = {}
        compensations_to_run: List[Tuple[str, Callable[[Context], None]]] = []

        for layer_idx, layer in enumerate(layers):
            layer_cp = context.checkpoint(f"dag_{dag.name}_layer_{layer_idx}")
            checkpoints_created.append(layer_cp)

            # Filter nodes ready to execute in this layer
            nodes_to_run: List[DAGNode] = []
            for node in layer:
                # If any predecessor was skipped or failed, skip this node
                predecessors_skipped = any(dep in skipped_nodes for dep in node.depends_on)
                predecessors_failed = any(
                    dep in node_results and node_results[dep].status == SkillStatus.ERROR
                    for dep in node.depends_on
                )

                if predecessors_skipped or predecessors_failed:
                    skipped_nodes.add(node.name)
                    node_results[node.name] = SkillResult(
                        status=SkillStatus.SKIPPED,
                        output={"reason": "predecessor skipped or failed"},
                    )
                    continue

                # Check node condition predicate
                if node.condition and not node.condition(context):
                    skipped_nodes.add(node.name)
                    node_results[node.name] = SkillResult(
                        status=SkillStatus.SKIPPED,
                        output={"reason": "condition predicate evaluated to false"},
                    )
                    continue

                # Check Human-in-the-Loop approval
                if node.requires_human_approval and not context.get("human_approved", False):
                    skipped_nodes.add(node.name)
                    node_results[node.name] = SkillResult(
                        status=SkillStatus.SKIPPED,
                        output={"reason": "waiting for human approval"},
                    )
                    continue

                nodes_to_run.append(node)

            if not nodes_to_run:
                continue

            # Layer Execution: Parallel or Sequential
            layer_failed = False
            failed_node_name: Optional[str] = None

            if parallel and len(nodes_to_run) > 1:
                with ThreadPoolExecutor(max_workers=min(max_workers, len(nodes_to_run))) as executor:
                    futures = {
                        executor.submit(self._execute_node_with_retries, node, context): node
                        for node in nodes_to_run
                    }
                    for fut in as_completed(futures):
                        node = futures[fut]
                        try:
                            res = fut.result()
                            node_results[node.name] = res
                            if res.status == SkillStatus.ERROR:
                                layer_failed = True
                                failed_node_name = node.name
                            else:
                                executed_nodes.append(node.name)
                                if node.compensate:
                                    compensations_to_run.append((node.name, node.compensate))
                        except Exception as ex:
                            layer_failed = True
                            failed_node_name = node.name
                            node_results[node.name] = SkillResult(status=SkillStatus.ERROR, error=str(ex))
            else:
                for node in nodes_to_run:
                    res = self._execute_node_with_retries(node, context)
                    node_results[node.name] = res
                    if res.status == SkillStatus.ERROR:
                        layer_failed = True
                        failed_node_name = node.name
                        break
                    executed_nodes.append(node.name)
                    if node.compensate:
                        compensations_to_run.append((node.name, node.compensate))

            # Handle Layer Failure with Saga Compensations and Rollback
            if layer_failed:
                compensated_nodes: List[str] = []
                if auto_rollback_on_error:
                    # Run compensations in reverse order
                    for name, comp in reversed(compensations_to_run):
                        try:
                            comp(context)
                            compensated_nodes.append(name)
                        except Exception:
                            pass
                    context.rollback(initial_cp)

                return DAGExecutionResult(
                    status=SkillStatus.ERROR,
                    node_results=node_results,
                    executed_nodes=executed_nodes,
                    skipped_nodes=list(skipped_nodes),
                    failed_node=failed_node_name,
                    rollback_performed=auto_rollback_on_error,
                    compensated_nodes=compensated_nodes,
                    checkpoints_created=checkpoints_created,
                )

            # Evaluate conditional edges for nodes in this layer
            for node in nodes_to_run:
                if node.name in dag.conditional_edges:
                    for edge in dag.conditional_edges[node.name]:
                        res = node_results[node.name]
                        try:
                            chosen_key = edge.router(res, context)
                            target_node = edge.routes.get(chosen_key)
                            # Mark non-chosen route destinations as skipped
                            for r_key, r_target in edge.routes.items():
                                if r_key != chosen_key and r_target != target_node:
                                    skipped_nodes.add(r_target)
                        except Exception:
                            pass

        return DAGExecutionResult(
            status=SkillStatus.SUCCESS,
            node_results=node_results,
            executed_nodes=executed_nodes,
            skipped_nodes=list(skipped_nodes),
            failed_node=None,
            rollback_performed=False,
            compensated_nodes=[],
            checkpoints_created=checkpoints_created,
        )
