"""
Unit Tests for Transactional Context & Time-Travel Checkpoints
Version: 1.0.0
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.core.context import Context


class TestTransactionalContext(unittest.TestCase):
    def test_checkpoint_and_rollback(self):
        ctx = Context()
        ctx.set("counter", 10)
        ctx.set("user", {"name": "Alice", "role": "admin"})

        # Snapshot 1
        cp1 = ctx.checkpoint("initial_state")
        self.assertEqual(cp1, "initial_state")

        # Mutate state
        ctx.set("counter", 25)
        ctx.get("user")["name"] = "Bob"
        ctx.set("new_key", "value")

        self.assertEqual(ctx.get("counter"), 25)
        self.assertEqual(ctx.get("user")["name"], "Bob")

        # Rollback to initial
        success = ctx.rollback("initial_state")
        self.assertTrue(success)

        # Verify deep state restoration
        self.assertEqual(ctx.get("counter"), 10)
        self.assertEqual(ctx.get("user")["name"], "Alice")
        self.assertFalse(ctx.has("new_key"))

    def test_multiple_checkpoints_timeline(self):
        ctx = Context()
        ctx.set("step", 0)

        ctx.checkpoint("cp_0")
        ctx.set("step", 1)
        ctx.checkpoint("cp_1")
        ctx.set("step", 2)
        ctx.checkpoint("cp_2")

        timeline = ctx.list_checkpoints()
        self.assertEqual(len(timeline), 3)
        self.assertEqual([t["name"] for t in timeline], ["cp_0", "cp_1", "cp_2"])

        # Rollback to step 1
        ctx.rollback("cp_1")
        self.assertEqual(ctx.get("step"), 1)

        # Rollback to most recent when name is None (should be cp_2)
        ctx.rollback()
        self.assertEqual(ctx.get("step"), 2)

    def test_rollback_on_empty_checkpoints(self):
        ctx = Context()
        self.assertFalse(ctx.rollback("non_existent"))

    def test_clear_checkpoints(self):
        ctx = Context()
        ctx.checkpoint("cp1")
        self.assertEqual(len(ctx.list_checkpoints()), 1)
        ctx.clear_checkpoints()
        self.assertEqual(len(ctx.list_checkpoints()), 0)


if __name__ == "__main__":
    unittest.main()
