import unittest

from framework.engines import SaaSManager


class TestSaaSManager(unittest.TestCase):

    def setUp(self):
        self.saas = SaaSManager()
        self.saas.register_tenant("tenant_a", plan="free", name="Tenant Alpha")
        self.saas.register_tenant("tenant_b", plan="pro", name="Tenant Beta")

    def test_tenant_registration_and_retrieval(self):
        t_a = self.saas.get_tenant("tenant_a")
        self.assertIsNotNone(t_a)
        self.assertEqual(t_a.plan, "free")
        self.assertEqual(t_a.name, "Tenant Alpha")

    def test_resolve_tenant_from_headers(self):
        headers_with_id = {"X-Tenant-ID": "tenant_a"}
        self.assertEqual(self.saas.resolve_tenant_from_headers(headers_with_id), "tenant_a")

        headers_with_host = {"Host": "tenant_b.app.com"}
        self.assertEqual(self.saas.resolve_tenant_from_headers(headers_with_host), "tenant_b")

    def test_feature_flags(self):
        self.assertFalse(self.saas.is_feature_enabled("tenant_a", "advanced_analytics"))
        self.saas.enable_feature("tenant_a", "advanced_analytics")
        self.assertTrue(self.saas.is_feature_enabled("tenant_a", "advanced_analytics"))

    def test_quota_checking(self):
        # Free plan API call limit is 1,000
        self.assertTrue(self.saas.check_quota("tenant_a", "api_calls_per_day", 500))
        self.assertFalse(self.saas.check_quota("tenant_a", "api_calls_per_day", 1500))

        # Pro plan API call limit is 100,000
        self.assertTrue(self.saas.check_quota("tenant_b", "api_calls_per_day", 1500))

if __name__ == "__main__":
    unittest.main()
