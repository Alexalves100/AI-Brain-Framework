import unittest

from framework.core import EventBus


class TestEventBus(unittest.TestCase):

    def setUp(self):
        self.bus = EventBus()

    def test_publish_subscribe(self):
        received_data = []

        def handler_a(data):
            received_data.append(f"A:{data}")

        def handler_b(data):
            received_data.append(f"B:{data}")

        self.bus.subscribe("user_created", handler_a)
        self.bus.subscribe("user_created", handler_b)

        called_count = self.bus.publish("user_created", "usr_100")
        self.assertEqual(called_count, 2)
        self.assertIn("A:usr_100", received_data)
        self.assertIn("B:usr_100", received_data)

    def test_unsubscribe(self):
        received = []

        def handler(data):
            received.append(data)

        self.bus.subscribe("order_placed", handler)
        self.bus.publish("order_placed", "order_1")
        self.assertEqual(len(received), 1)

        unsub_ok = self.bus.unsubscribe("order_placed", handler)
        self.assertTrue(unsub_ok)

        self.bus.publish("order_placed", "order_2")
        self.assertEqual(len(received), 1)

if __name__ == "__main__":
    unittest.main()
