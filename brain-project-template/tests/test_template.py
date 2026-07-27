"""Tests for brain-project-template."""

import sys
import unittest
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent
FRAMEWORK_DIR = TEMPLATE_DIR.parent
sys.path.insert(0, str(FRAMEWORK_DIR))


class TestTemplateStructure(unittest.TestCase):
    def test_app_py_exists(self):
        self.assertTrue((TEMPLATE_DIR / "app.py").exists())

    def test_config_py_exists(self):
        self.assertTrue((TEMPLATE_DIR / "config.py").exists())

    def test_ai_dir_exists(self):
        self.assertTrue((TEMPLATE_DIR / ".ai").is_dir())

    def test_ai_agents_exists(self):
        self.assertTrue((TEMPLATE_DIR / ".ai" / "AGENTS.md").exists())

    def test_ai_memory_exists(self):
        self.assertTrue((TEMPLATE_DIR / ".ai" / "memory").is_dir())

    def test_ai_policies_exists(self):
        self.assertTrue((TEMPLATE_DIR / ".ai" / "policies").is_dir())

    def test_ai_skills_exists(self):
        self.assertTrue((TEMPLATE_DIR / ".ai" / "skills").is_dir())

    def test_tests_dir_exists(self):
        self.assertTrue((TEMPLATE_DIR / "tests").is_dir())


class TestConfig(unittest.TestCase):
    def test_config_imports(self):
        from config import Config
        self.assertEqual(Config.PROJECT_NAME, "brain-project")
        self.assertEqual(Config.VERSION, "0.1.0")

    def test_config_init_creates_dirs(self):
        from config import Config
        Config.init()
        self.assertTrue(Config.LOGS_DIR.exists())
        self.assertTrue(Config.DATA_DIR.exists())
        self.assertTrue(Config.AI_DIR.exists())


class TestAppImport(unittest.TestCase):
    def test_app_imports(self):
        import app
        self.assertTrue(hasattr(app, "main"))


if __name__ == "__main__":
    unittest.main()
