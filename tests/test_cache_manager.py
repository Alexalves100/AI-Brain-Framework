import unittest
import time
from framework.standards import CacheManager

class TestCacheManager(unittest.TestCase):

    def setUp(self):
        self.cache = CacheManager(default_ttl_seconds=2)

    def test_set_and_get_valid(self):
        self.cache.set("user:1", {"name": "Alice"})
        val = self.cache.get("user:1")
        self.assertEqual(val, {"name": "Alice"})

    def test_expiration_ttl(self):
        self.cache.set("temp", "value", ttl_seconds=1)
        self.assertEqual(self.cache.get("temp"), "value")
        time.sleep(1.1)
        self.assertIsNone(self.cache.get("temp"))

    def test_hit_and_miss_stats(self):
        self.cache.set("key1", "val1")
        self.cache.get("key1")  # Hit
        self.cache.get("key2")  # Miss

        stats = self.cache.get_stats()
        self.assertEqual(stats["hits"], 1)
        self.assertEqual(stats["misses"], 1)
        self.assertEqual(stats["hit_rate_pct"], 50.0)

    def test_cached_decorator(self):
        call_count = 0

        @self.cache.cached(ttl_seconds=5)
        def expensive_computation(x, y):
            nonlocal call_count
            call_count += 1
            return x + y

        res1 = expensive_computation(5, 10)
        res2 = expensive_computation(5, 10)

        self.assertEqual(res1, 15)
        self.assertEqual(res2, 15)
        self.assertEqual(call_count, 1)  # Chamado apenas 1 vez devido ao cache

if __name__ == "__main__":
    unittest.main()
