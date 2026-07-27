"""Tests for structured logging."""

import io
import json
import logging
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.core import get_logger


class TestStructuredLogger(unittest.TestCase):
    def test_logger_returns_logger(self):
        logger = get_logger("test_logger_a")
        self.assertIsInstance(logger, logging.Logger)

    def test_log_emits_json(self):
        logger = get_logger("test_logger_b")
        for h in list(logger.handlers):
            logger.removeHandler(h)

        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        from framework.core import StructuredFormatter
        handler.setFormatter(StructuredFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        logger.info("hello", extra={"key": "value"})

        output = stream.getvalue().strip()
        data = json.loads(output)
        self.assertEqual(data["message"], "hello")
        self.assertEqual(data["level"], "INFO")
        self.assertEqual(data["key"], "value")

    def test_log_to_file(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "test.log")
            logger = get_logger("test_logger_c", log_file=path)
            logger.info("file message")
            for h in list(logger.handlers):
                h.flush()
                h.close()
                logger.removeHandler(h)

            content = Path(path).read_text(encoding="utf-8")
            self.assertIn("file message", content)


if __name__ == "__main__":
    unittest.main()
