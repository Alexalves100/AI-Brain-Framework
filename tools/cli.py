"""
AI-Brain-Framework CLI
Version: 1.0.0
Interactive command-line interface for the framework.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework import Context, create_default_orchestrator


def cmd_analyze(args):
    orch = create_default_orchestrator()
    ctx = Context()
    ctx.set("query", args.query)
    ctx.set("code", args.code or args.query)
    ctx.set("text", args.query)

    results = orch.run_pipeline(["brain", "security", "token_economy"], ctx)
    output = {
        "query": args.query,
        "results": [
            {
                "engine": r.metadata.get("engine", r.status.value),
                "status": r.status.value,
                "output": r.output,
            }
            for r in results
        ],
        "tokens_used": ctx.tokens_used,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


def cmd_security(args):
    orch = create_default_orchestrator()
    ctx = Context()
    code = args.code or Path(args.file).read_text(encoding="utf-8") if args.file else ""
    ctx.set("code", code)
    result = orch.run("security", ctx)
    print(json.dumps(result.output, indent=2, ensure_ascii=False))


def cmd_brain(args):
    orch = create_default_orchestrator()
    ctx = Context()
    ctx.set("query", args.query)
    result = orch.run("brain", ctx)
    print(json.dumps(result.output, indent=2, ensure_ascii=False))


def cmd_compress(args):
    orch = create_default_orchestrator()
    ctx = Context()
    text = args.text or Path(args.file).read_text(encoding="utf-8") if args.file else ""
    ctx.set("text", text)
    result = orch.run("token_economy", ctx)
    print(json.dumps(result.output, indent=2, ensure_ascii=False))


def cmd_knowledge(args):
    orch = create_default_orchestrator()
    ctx = Context()
    ctx.set("action", args.action)
    ctx.set("key", args.key)
    ctx.set("content", args.content)
    ctx.set("query", args.query)
    result = orch.run("knowledge", ctx)
    print(json.dumps(result.output, indent=2, ensure_ascii=False))


def cmd_discover(args):
    orch = create_default_orchestrator()
    ctx = Context()
    ctx.set("path", args.path)
    ctx.set("pattern", args.pattern)
    result = orch.run("discovery", ctx)
    print(json.dumps(result.output, indent=2, ensure_ascii=False))


def cmd_reason(args):
    orch = create_default_orchestrator()
    ctx = Context()
    ctx.set("premises", args.premises)
    ctx.set("conclusion", args.conclusion)
    result = orch.run("reasoning", ctx)
    print(json.dumps(result.output, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        prog="ai-brain",
        description="AI-Brain-Framework CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_analyze = sub.add_parser("analyze", help="Full pipeline analysis")
    p_analyze.add_argument("query")
    p_analyze.add_argument("--code", help="Optional code to audit")
    p_analyze.set_defaults(func=cmd_analyze)

    p_brain = sub.add_parser("brain", help="Brain routing")
    p_brain.add_argument("query")
    p_brain.set_defaults(func=cmd_brain)

    p_sec = sub.add_parser("security", help="Security audit")
    p_sec.add_argument("--code", help="Code string")
    p_sec.add_argument("--file", help="File path")
    p_sec.set_defaults(func=cmd_security)

    p_comp = sub.add_parser("compress", help="Compress text")
    p_comp.add_argument("--text", help="Text string")
    p_comp.add_argument("--file", help="File path")
    p_comp.set_defaults(func=cmd_compress)

    p_know = sub.add_parser("knowledge", help="Knowledge base")
    p_know.add_argument("action", choices=["add", "get", "search"])
    p_know.add_argument("--key", help="Entry key")
    p_know.add_argument("--content", help="Content to add")
    p_know.add_argument("--query", help="Search query")
    p_know.set_defaults(func=cmd_knowledge)

    p_disc = sub.add_parser("discover", help="Discover codebase")
    p_disc.add_argument("--path", default=".", help="Root path")
    p_disc.add_argument("--pattern", default="all",
                       choices=["all", "python", "markdown", "config", "docs"])
    p_disc.set_defaults(func=cmd_discover)

    p_reason = sub.add_parser("reason", help="Structured reasoning")
    p_reason.add_argument("--premise", action="append", dest="premises", required=True)
    p_reason.add_argument("--conclusion", required=True)
    p_reason.set_defaults(func=cmd_reason)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
