"""
Performance metrics for AI-Brain-Framework
Version: 1.0.0
"""

import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Metric:
    name: str
    count: int = 0
    total_ms: float = 0.0
    min_ms: float = float("inf")
    max_ms: float = 0.0

    def record(self, elapsed_ms: float) -> None:
        self.count += 1
        self.total_ms += elapsed_ms
        if elapsed_ms < self.min_ms:
            self.min_ms = elapsed_ms
        if elapsed_ms > self.max_ms:
            self.max_ms = elapsed_ms

    @property
    def avg_ms(self) -> float:
        return self.total_ms / self.count if self.count else 0.0

    def to_dict(self) -> Dict[str, float]:
        return {
            "count": self.count,
            "avg_ms": round(self.avg_ms, 3),
            "min_ms": round(self.min_ms, 3) if self.min_ms != float("inf") else 0,
            "max_ms": round(self.max_ms, 3),
            "total_ms": round(self.total_ms, 3),
        }


class MetricsCollector:
    """Collects performance metrics for skills and operations."""

    def __init__(self) -> None:
        self._metrics: Dict[str, Metric] = {}

    def record(self, name: str, elapsed_ms: float) -> None:
        if name not in self._metrics:
            self._metrics[name] = Metric(name=name)
        self._metrics[name].record(elapsed_ms)

    @contextmanager
    def measure(self, name: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.record(name, elapsed_ms)

    def get(self, name: str) -> Dict[str, float]:
        if name not in self._metrics:
            return {"count": 0, "avg_ms": 0, "min_ms": 0, "max_ms": 0, "total_ms": 0}
        return self._metrics[name].to_dict()

    def all(self) -> Dict[str, Dict[str, float]]:
        return {name: m.to_dict() for name, m in self._metrics.items()}

    def reset(self) -> None:
        self._metrics.clear()
