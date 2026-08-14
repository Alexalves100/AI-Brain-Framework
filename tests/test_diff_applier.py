"""
Unit Tests for DiffApplier
Version: 1.0.0
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.patchers.diff_applier import DiffApplier

SAMPLE_FILE = """def greet(name):
    print("Hello " + name)

def farewell(name):
    print("Goodbye " + name)
"""


class TestDiffApplier(unittest.TestCase):
    def setUp(self):
        self.applier = DiffApplier()

    def test_apply_search_replace_blocks(self):
        patch = """<<<<<<< SEARCH
def greet(name):
    print("Hello " + name)
=======
def greet(name):
    print(f"Hello, {name}!")
>>>>>>> REPLACE"""

        blocks = self.applier.parse_search_replace_blocks(patch)
        self.assertEqual(len(blocks), 1)

        ok, new_code, errors = self.applier.apply_search_replace_blocks(SAMPLE_FILE, blocks)
        self.assertTrue(ok)
        self.assertEqual(len(errors), 0)
        self.assertIn('print(f"Hello, {name}!")', new_code)

    def test_apply_unified_diff(self):
        diff = """--- a/test.py
+++ b/test.py
@@ -4,3 +4,3 @@
 def farewell(name):
-    print("Goodbye " + name)
+    print(f"Farewell, {name}!")
"""
        ok, new_code, err = self.applier.apply_unified_diff(SAMPLE_FILE, diff)
        self.assertTrue(ok)
        self.assertIsNone(err)
        self.assertIn('print(f"Farewell, {name}!")', new_code)


if __name__ == "__main__":
    unittest.main()
