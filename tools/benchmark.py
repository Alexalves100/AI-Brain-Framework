"""
Benchmark suite for AI-Brain-Framework
Version: 1.0.0
Measures performance of all engines and modules.
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework import create_default_orchestrator, Context
from framework.core import MetricsCollector


def benchmark(name: str, func, iterations: int = 1000) -> dict:
    """Run `func` `iterations` times and return stats."""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        elapsed_ms = (time.perf_counter() - start) * 1000
        times.append(elapsed_ms)

    times.sort()
    return {
        "name": name,
        "iterations": iterations,
        "min_ms": round(times[0], 4),
        "max_ms": round(times[-1], 4),
        "avg_ms": round(sum(times) / len(times), 4),
        "p50_ms": round(times[len(times) // 2], 4),
        "p95_ms": round(times[int(len(times) * 0.95)], 4),
        "p99_ms": round(times[int(len(times) * 0.99)], 4),
    }


def main():
    orch = create_default_orchestrator()
    ctx = Context()
    ctx.set("query", "sql injection vulnerability")
    ctx.set("code", "execute('SELECT * FROM users WHERE id=' + uid)")
    ctx.set("text", "Claro, vou ajudar. Espero que seja util.")

    print("=" * 60)
    print("AI-Brain-Framework Benchmark")
    print("=" * 60)

    benchmarks = []

    benchmarks.append(benchmark(
        "brain",
        lambda: orch.run("brain", Context(data={"query": "test"})),
        iterations=1000,
    ))

    benchmarks.append(benchmark(
        "security",
        lambda: orch.run("security", Context(data={"code": "x = 1"})),
        iterations=1000,
    ))

    benchmarks.append(benchmark(
        "token_economy",
        lambda: orch.run("token_economy", Context(data={"text": "hello world"})),
        iterations=1000,
    ))

    benchmarks.append(benchmark(
        "full_pipeline",
        lambda: orch.run_pipeline(
            ["brain", "security", "token_economy"],
            Context(data={"query": "x", "code": "x", "text": "x"}),
        ),
        iterations=500,
    ))

    print(f"\n{'Engine':<20} {'Avg ms':>10} {'P95 ms':>10} {'P99 ms':>10} {'Min ms':>10}")
    print("-" * 60)
    for b in benchmarks:
        print(
            f"{b['name']:<20} "
            f"{b['avg_ms']:>10.4f} "
            f"{b['p95_ms']:>10.4f} "
            f"{b['p99_ms']:>10.4f} "
            f"{b['min_ms']:>10.4f}"
        )

    print("\n" + "=" * 60)
    print("Done.")


if __name__ == "__main__":
    main()
