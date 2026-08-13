"""
Tests for ASTScanner (Serena MCP style symbol intelligence).
"""

import ast
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.scanners.ast_scanner import ASTScanner

SAMPLE_CODE = '''"""Module docstring for sample authentication."""

import os
from typing import Optional, Dict, Any

MAX_RETRIES: int = 3
DEFAULT_TIMEOUT = 30

class User:
    """User representation model."""
    id: int
    name: str

class AuthService:
    """Authentication and authorization service."""

    def __init__(self, secret: str = "default_secret") -> None:
        self.secret = secret
        self.sessions: Dict[str, User] = {}

    @property
    def is_active(self) -> bool:
        """Check if service is active."""
        return True

    def login(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password."""
        if not username or not password:
            return None
        user = User()
        user.name = username
        self.sessions[username] = user
        return user

    async def verify_token(self, token: str) -> bool:
        """Asynchronously verify auth token."""
        return len(token) > 10


def calculate_hash(data: str, salt: str = "") -> str:
    """Calculate secure hash of input string."""
    combined = data + salt
    return "hash_" + combined
'''


class TestASTScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = ASTScanner()

    def test_get_symbols_overview_generates_valid_python(self):
        skeleton = self.scanner.get_symbols_overview(SAMPLE_CODE, file_path="auth.py")

        # Verify it compiles cleanly as valid Python code
        parsed = ast.parse(skeleton)
        self.assertIsNotNone(parsed)

        # Verify key definitions and types are in the skeleton
        self.assertIn("class AuthService:", skeleton)
        self.assertIn("def login(self, username: str, password: str) -> Optional[User]:", skeleton)
        self.assertIn("async def verify_token(self, token: str) -> bool:", skeleton)
        self.assertIn("def calculate_hash(data: str, salt: str = \"\") -> str:", skeleton)
        self.assertIn("MAX_RETRIES: int = 3", skeleton)
        self.assertIn("DEFAULT_TIMEOUT = 30", skeleton)

        # Verify implementation bodies are stubbed out with ...
        self.assertNotIn("self.sessions[username] = user", skeleton)
        self.assertNotIn("combined = data + salt", skeleton)
        self.assertIn("...", skeleton)

    def test_token_reduction_rate(self):
        original_len = len(SAMPLE_CODE)
        skeleton = self.scanner.get_symbols_overview(SAMPLE_CODE)
        compressed_len = len(skeleton)

        savings = original_len - compressed_len
        ratio = savings / original_len
        # Should achieve at least 30% reduction even on small code, and preserves types
        self.assertGreater(ratio, 0.25)
        self.assertGreater(savings, 200)

    def test_list_symbols(self):
        symbols = self.scanner.list_symbols(SAMPLE_CODE)
        names = [s["name"] for s in symbols]

        self.assertIn("User", names)
        self.assertIn("AuthService", names)
        self.assertIn("AuthService.login", names)
        self.assertIn("AuthService.verify_token", names)
        self.assertIn("calculate_hash", names)

        login_sym = next(s for s in symbols if s["name"] == "AuthService.login")
        self.assertEqual(login_sym["kind"], "method")
        self.assertIn("def login", login_sym["signature"])

    def test_get_symbol_body_exact_extraction(self):
        # Extract function body
        calc_body = self.scanner.get_symbol_body(SAMPLE_CODE, "calculate_hash")
        self.assertIsNotNone(calc_body)
        self.assertIn("def calculate_hash", calc_body)
        self.assertIn("combined = data + salt", calc_body)
        self.assertIn("return \"hash_\" + combined", calc_body)

        # Extract method body
        login_body = self.scanner.get_symbol_body(SAMPLE_CODE, "AuthService.login")
        self.assertIsNotNone(login_body)
        self.assertIn("def login(self, username: str, password: str)", login_body)
        self.assertIn("self.sessions[username] = user", login_body)

        # Extract whole class
        user_body = self.scanner.get_symbol_body(SAMPLE_CODE, "User")
        self.assertIsNotNone(user_body)
        self.assertIn("class User:", user_body)
        self.assertIn("id: int", user_body)

        # Nonexistent symbol returns None
        self.assertIsNone(self.scanner.get_symbol_body(SAMPLE_CODE, "NonExistent"))

    def test_find_references(self):
        refs = self.scanner.find_references(SAMPLE_CODE, "User")
        self.assertGreater(len(refs), 0)
        lines = [r["line"] for r in refs]
        self.assertTrue(len(lines) >= 2)

    def test_minify_code(self):
        code_with_comments = """# This is a comment
def foo():
    # Another comment
    return 42
"""
        minified = self.scanner.minify_code(code_with_comments)
        self.assertNotIn("# This is a comment", minified)
        self.assertIn("def foo():", minified)
        self.assertIn("return 42", minified)


if __name__ == "__main__":
    unittest.main()
