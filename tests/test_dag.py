"""
Unit Tests for WorkflowDAG, Kahn's Algorithm & Topological Ordering
Version: 1.0.0
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.core.dag import CyclicDependencyError, WorkflowDAG


class TestWorkflowDAG(unittest.TestCase):
    def test_linear_dag_layers(self):
        dag = WorkflowDAG(name="linear")
        dag.add_node("A", skill_name="security")
        dag.add_node("B", skill_name="token_economy", depends_on=["A"])
        dag.add_node("C", skill_name="brain", depends_on=["B"])

        layers = dag.get_topological_layers()
        self.assertEqual(len(layers), 3)
        self.assertEqual([n.name for n in layers[0]], ["A"])
        self.assertEqual([n.name for n in layers[1]], ["B"])
        self.assertEqual([n.name for n in layers[2]], ["C"])

    def test_diamond_fork_join_layers(self):
        # A -> (B, C) -> D
        dag = WorkflowDAG(name="diamond")
        dag.add_node("A", skill_name="prompt_shield")
        dag.add_node("B", skill_name="security", depends_on=["A"])
        dag.add_node("C", skill_name="token_economy", depends_on=["A"])
        dag.add_node("D", skill_name="brain", depends_on=["B", "C"])

        layers = dag.get_topological_layers()
        self.assertEqual(len(layers), 3)
        self.assertEqual([n.name for n in layers[0]], ["A"])
        self.assertEqual(sorted([n.name for n in layers[1]]), ["B", "C"])
        self.assertEqual([n.name for n in layers[2]], ["D"])

    def test_cyclic_dependency_detection(self):
        # A -> B -> C -> A
        dag = WorkflowDAG(name="cycle")
        dag.add_node("A", skill_name="security", depends_on=["C"])
        dag.add_node("B", skill_name="token_economy", depends_on=["A"])
        dag.add_node("C", skill_name="brain", depends_on=["B"])

        with self.assertRaises(CyclicDependencyError):
            dag.get_topological_layers()

    def test_duplicate_node_name_error(self):
        dag = WorkflowDAG(name="test")
        dag.add_node("A", skill_name="security")
        with self.assertRaises(ValueError):
            dag.add_node("A", skill_name="brain")

    def test_non_existent_dependency_error(self):
        dag = WorkflowDAG(name="test")
        dag.add_node("A", skill_name="security", depends_on=["non_existent"])
        with self.assertRaises(ValueError):
            dag.get_topological_layers()


if __name__ == "__main__":
    unittest.main()
