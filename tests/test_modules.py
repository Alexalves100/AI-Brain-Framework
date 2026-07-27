"""Tests for scanners, analyzers, builders, governance, prompts, schemas."""

import sys
import unittest
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.scanners import CodeScanner, DependencyScanner, StructureScanner
from framework.analyzers import ComplexityAnalyzer, QualityAnalyzer, MetricsAnalyzer
from framework.builders import ProjectBuilder, ModuleBuilder, ConfigBuilder
from framework.governance import PolicyEngine, AuditLog, ComplianceChecker
from framework.prompts import PromptRegistry, PromptBuilder
from framework.schemas import SchemaValidator, SchemaRegistry


class TestCodeScanner(unittest.TestCase):
    def test_scan_file_detects_todo(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w")
        tmp.write("# TODO: fix this\nx = 1\n")
        tmp.close()
        try:
            findings = CodeScanner().scan_file(Path(tmp.name))
            types = [f["type"] for f in findings]
            self.assertIn("TODO", types)
        finally:
            Path(tmp.name).unlink(missing_ok=True)


class TestDependencyScanner(unittest.TestCase):
    def test_scan_requirements(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w")
        tmp.write("requests==2.0.0\nflask>=2.0\n")
        tmp.close()
        try:
            tmpdir = Path(tmp.name).parent
            req = tmpdir / "requirements.txt"
            req.write_text("requests==2.0.0\nflask>=2.0\n")
            result = DependencyScanner().scan_project(str(tmpdir))
            self.assertEqual(result["total_dependencies"], 2)
            self.assertGreater(result["vulnerable_count"], 0)
        finally:
            Path(tmp.name).unlink(missing_ok=True)


class TestStructureScanner(unittest.TestCase):
    def test_scan_detects_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "README.md").write_text("# Test")
            result = StructureScanner().scan(tmpdir)
            self.assertIn("missing_files", result)
            self.assertIn("LICENSE", result["missing_files"])


class TestComplexityAnalyzer(unittest.TestCase):
    def test_cyclomatic(self):
        code = """
def f(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0
"""
        c = ComplexityAnalyzer().cyclomatic_complexity(code)
        self.assertGreaterEqual(c, 3)


class TestQualityAnalyzer(unittest.TestCase):
    def test_clean_file_scores_high(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w")
        tmp.write('"""Module."""\n\n\ndef main():\n    pass\n')
        tmp.close()
        try:
            r = QualityAnalyzer().analyze_file(Path(tmp.name))
            self.assertGreater(r["score"], 50)
        finally:
            Path(tmp.name).unlink(missing_ok=True)


class TestMetricsAnalyzer(unittest.TestCase):
    def test_analyze(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "test.py").write_text("x = 1\n")
            r = MetricsAnalyzer().analyze(tmpdir)
            self.assertGreater(r["total_files"], 0)


class TestProjectBuilder(unittest.TestCase):
    def test_build_creates_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = ProjectBuilder().build("myproj", tmpdir)
            self.assertEqual(result["project"], "myproj")
            self.assertGreater(result["files_created"], 0)


class TestModuleBuilder(unittest.TestCase):
    def test_build_creates_module(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = ModuleBuilder().build("mymod", tmpdir)
            self.assertEqual(result["module"], "mymod")
            self.assertEqual(len(result["files"]), 4)


class TestConfigBuilder(unittest.TestCase):
    def test_env(self):
        out = ConfigBuilder().env({"KEY": "value"})
        self.assertIn("KEY=value", out)

    def test_json(self):
        out = ConfigBuilder().json({"a": 1})
        self.assertIn('"a"', out)


class TestPolicyEngine(unittest.TestCase):
    def test_no_secrets_violation(self):
        pe = PolicyEngine()
        r = pe.check("no_hardcoded_secrets", {"code": "password=secret123"})
        self.assertTrue(r["violated"])

    def test_clean_code_passes(self):
        pe = PolicyEngine()
        r = pe.check("no_hardcoded_secrets", {"code": "x = 1"})
        self.assertFalse(r["violated"])


class TestAuditLog(unittest.TestCase):
    def test_log_and_query(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = str(Path(tmpdir) / "audit.jsonl")
            al = AuditLog(path=log_path)
            al.log("test_event", actor="tester", detail="x")
            results = al.query("test_event")
            self.assertEqual(len(results), 1)


class TestComplianceChecker(unittest.TestCase):
    def test_check(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "README.md").write_text("# Test")
            (Path(tmpdir) / "LICENSE").write_text("MIT")
            r = ComplianceChecker().check(tmpdir)
            self.assertGreater(r["score"], 0)


class TestPromptRegistry(unittest.TestCase):
    def test_render(self):
        pr = PromptRegistry()
        out = pr.render("code_review", code="x = 1")
        self.assertIn("x = 1", out)


class TestPromptBuilder(unittest.TestCase):
    def test_build(self):
        pb = PromptBuilder()
        result = (
            pb.add_role("expert")
            .add_task("review code")
            .add_constraints(["no fluff", "be concise"])
            .build()
        )
        self.assertIn("expert", result)
        self.assertIn("review code", result)


class TestSchemaValidator(unittest.TestCase):
    def test_valid_object(self):
        v = SchemaValidator()
        schema = {
            "type": "object",
            "required": ["name"],
            "properties": {"name": {"type": "string", "minLength": 1}},
        }
        errors = v.validate({"name": "test"}, schema)
        self.assertEqual(errors, [])

    def test_missing_required(self):
        v = SchemaValidator()
        schema = {"type": "object", "required": ["name"]}
        errors = v.validate({}, schema)
        self.assertGreater(len(errors), 0)


class TestSchemaRegistry(unittest.TestCase):
    def test_default_schemas(self):
        sr = SchemaRegistry()
        self.assertIn("user", sr.list())
        self.assertIn("skill", sr.list())


if __name__ == "__main__":
    unittest.main()
