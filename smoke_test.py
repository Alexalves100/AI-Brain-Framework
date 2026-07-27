"""Smoke test for AI-Brain-Framework."""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from framework import create_default_orchestrator, Context


def main():
    orch = create_default_orchestrator()

    print("=== Pipeline: brain + security + token_economy ===")
    ctx = Context()
    ctx.set("query", "how to fix sql injection vulnerability")
    ctx.set("code", "execute('SELECT * FROM users WHERE id=' + uid)")
    ctx.set("text", "Claro, vou ajudar. Espero que seja util.")

    for r in orch.run_pipeline(["brain", "security", "token_economy"], ctx):
        engine = r.metadata.get("engine", r.status.value)
        print(f"  {engine:>16} -> {r.status.value}")
        if r.output:
            out = json.dumps(r.output, ensure_ascii=False)
            print("    " + (out[:150] + "..." if len(out) > 150 else out))

    print("\n=== Knowledge Engine ===")
    ctx = Context()
    ctx.set("action", "add")
    ctx.set("key", "csrf")
    ctx.set("content", "Cross-Site Request Forgery mitigation requires tokens")
    r = orch.run("knowledge", ctx)
    print(f"  add csrf -> {r.status.value}")

    ctx = Context()
    ctx.set("action", "search")
    ctx.set("query", "tokens")
    r = orch.run("knowledge", ctx)
    print(f"  search 'tokens' -> {r.output['count']} results")

    print("\n=== Reasoning Engine ===")
    ctx = Context()
    ctx.set("premises", ["All users have email", "Alice is a user"])
    ctx.set("conclusion", "Alice has email")
    r = orch.run("reasoning", ctx)
    print(f"  reasoning -> valid={r.output['valid']} confidence={r.output['confidence']}")

    print("\n=== Discovery Engine ===")
    ctx = Context()
    ctx.set("path", str(Path(__file__).parent / "framework"))
    ctx.set("pattern", "python")
    r = orch.run("discovery", ctx)
    print(f"  discovery framework/ -> {r.output['total_files']} files")

    print(f"\nTotal skills registered: {len(orch.registry)}")
    print(f"Available: {[s.name for s in orch.registry.list()]}")


if __name__ == "__main__":
    main()
