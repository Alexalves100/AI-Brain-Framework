import unittest

from framework.standards import JWTAuth, PasswordHasher, RBACManager


class TestAuthAndRBAC(unittest.TestCase):

    def setUp(self):
        self.jwt_auth = JWTAuth(secret_key="secret_test_key_for_unit_tests")
        self.rbac = RBACManager()

    def test_jwt_creation_and_verification_valid(self):
        payload = {"user_id": "usr_123", "role": "admin"}
        token = self.jwt_auth.create_token(payload, expires_in_seconds=60)
        self.assertIsNotNone(token)

        decoded = self.jwt_auth.verify_token(token)
        self.assertIsNotNone(decoded)
        self.assertEqual(decoded["user_id"], "usr_123")
        self.assertEqual(decoded["role"], "admin")

    def test_jwt_verification_invalid_signature(self):
        payload = {"user_id": "usr_123"}
        token = self.jwt_auth.create_token(payload)
        tampered_token = token[:-4] + "xxxx"
        self.assertIsNone(self.jwt_auth.verify_token(tampered_token))

    def test_password_hasher(self):
        password = "MySecr3tPassword!"
        hashed = PasswordHasher.hash_password(password)
        self.assertTrue(PasswordHasher.verify_password(password, hashed))
        self.assertFalse(PasswordHasher.verify_password("WrongPass", hashed))

    def test_rbac_permissions(self):
        self.rbac.add_role("user", ["read"])
        self.rbac.add_role("admin", ["write", "delete"])
        self.rbac.add_child_role("admin", "user")

        self.assertTrue(self.rbac.has_permission("user", "read"))
        self.assertFalse(self.rbac.has_permission("user", "write"))

        # Admin herda 'read' de user
        self.assertTrue(self.rbac.has_permission("admin", "read"))
        self.assertTrue(self.rbac.has_permission("admin", "write"))
        self.assertTrue(self.rbac.has_permission("admin", "delete"))

if __name__ == "__main__":
    unittest.main()
