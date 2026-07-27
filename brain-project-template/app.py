"""
Brain Project Template — Application Entry Point
Version: 1.0.0

Replace this with your application logic.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from framework import create_default_orchestrator, Context
from framework.core import get_logger, MetricsCollector


logger = get_logger("brain_project")
metrics = MetricsCollector()


def main():
    logger.info("starting", extra={"component": "main"})

    orch = create_default_orchestrator()
    ctx = Context()

    ctx.set("query", "your query here")
    ctx.set("code", "")
    ctx.set("text", "")

    with metrics.measure("main_pipeline"):
        results = orch.run_pipeline(["brain"], ctx)

    for r in results:
        logger.info(
            "skill_done",
            extra={
                "engine": r.metadata.get("engine"),
                "status": r.status.value,
            },
        )

    logger.info("metrics", extra=metrics.all())


if __name__ == "__main__":
    main()
