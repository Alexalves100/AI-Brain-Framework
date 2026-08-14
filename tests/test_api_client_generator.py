"""
Unit Tests for APIClientGenerator (Schema to TypeScript SDK & Form)
Version: 1.0.0
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.frontend.api_client_generator import APIClientGenerator


class TestAPIClientGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = APIClientGenerator()

    def test_generate_typescript_interface(self):
        props = {
            "id": {"type": "integer", "description": "Unique user ID"},
            "name": {"type": "string"},
            "email": {"type": "string"},
            "is_active": {"type": "boolean"},
        }
        res = self.generator.generate_typescript_interface("User", props, required_fields=["id", "email"])
        self.assertIn("export interface User {", res)
        self.assertIn("id: number;", res)
        self.assertIn("name?: string;", res)
        self.assertIn("email: string;", res)
        self.assertIn("is_active?: boolean;", res)
        self.assertIn("/** Unique user ID */", res)

    def test_generate_fetch_client(self):
        res = self.generator.generate_fetch_client("createUser", "POST", "/api/users", "User", "UserResponse")
        self.assertIn("export async function createUser(payload: User): Promise<UserResponse>", res)
        self.assertIn("fetch('/api/users'", res)
        self.assertIn("method: 'POST'", res)

    def test_generate_react_form(self):
        props = {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "age": {"type": "integer"},
        }
        res = self.generator.generate_react_form("Customer", props, required_fields=["name", "email"])
        self.assertIn("export const CustomerForm: React.FC", res)
        self.assertIn("useState<Customer>", res)
        self.assertIn("type=\"email\"", res)
        self.assertIn("type=\"number\"", res)


if __name__ == "__main__":
    unittest.main()
