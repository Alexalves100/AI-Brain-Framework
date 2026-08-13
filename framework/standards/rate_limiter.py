"""
Rate Limiter — simple in-memory rate limiting
Version: 1.0.0
"""

import time
from collections import defaultdict
from threading import Lock
from typing import Dict, Optional, Tuple


class RateLimiter:
    """Token-bucket-style rate limiter."""

    def __init__(self, max_requests: int = 60, window_seconds: float = 60.0):
        self.max_requests = max_requests
        self.window = window_seconds
        self._hits: Dict[str, list] = defaultdict(list)
        self._lock = Lock()

    def is_allowed(self, key: str) -> Tuple[bool, int]:
        """Check if a request from `key` is allowed. Returns (allowed, remaining)."""
        now = time.time()
        with self._lock:
            hits = self._hits[key]
            cutoff = now - self.window
            self._hits[key] = [t for t in hits if t > cutoff]

            if len(self._hits[key]) >= self.max_requests:
                return False, 0

            self._hits[key].append(now)
            remaining = self.max_requests - len(self._hits[key])
            return True, remaining

    def reset(self, key: Optional[str] = None) -> None:
        with self._lock:

            if key:
                self._hits.pop(key, None)
            else:
                self._hits.clear()
