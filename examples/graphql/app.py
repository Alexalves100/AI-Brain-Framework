"""
GraphQL Example
Version: 1.0.0
Minimal GraphQL server using only Python stdlib with AI-Brain-Framework.
Implements: query parsing, type validation, resolver dispatch, JSON response.
"""

import json
import re
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from framework import create_default_orchestrator, Context, SecurityHeaders, InputValidator


SCHEMA = {
    "types": {
        "User": {
            "fields": {"id": "ID!", "name": "String!", "email": "String!"},
        },
        "Query": {
            "fields": {
                "user": {"type": "User", "args": {"id": "ID!"}},
                "users": {"type": "[User!]!", "args": {}},
                "analyze": {"type": "String", "args": {"query": "String!"}},
            },
        },
    },
    "data": {
        "users": {
            "1": {"id": "1", "name": "Alice", "email": "alice@example.com"},
            "2": {"id": "2", "name": "Bob", "email": "bob@example.com"},
        }
    },
}


def parse_query(query: str):
    """Extract operation name and field selections."""
    query = query.strip()
    m = re.search(r"\{\s*(\w+)", query)
    if not m:
        return None, None
    field = m.group(1)
    args_m = re.search(r"\(([^)]*)\)", query)
    args = {}
    if args_m:
        for arg in args_m.group(1).split(","):
            if ":" in arg:
                k, v = arg.split(":", 1)
                args[k.strip()] = parse_value(v.strip())
    return field, args


def parse_value(v):
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    if v.isdigit():
        return int(v)
    return v


def resolve(field: str, args: dict, schema: dict, orchestrator):
    if field == "user":
        uid = args.get("id")
        if not InputValidator.uuid(uid) and not isinstance(uid, int):
            return None
        return schema["data"]["users"].get(str(uid))
    if field == "users":
        return list(schema["data"]["users"].values())
    if field == "analyze":
        q = args.get("query", "")
        if not InputValidator.length(q, 1, 500):
            return "invalid"
        ctx = Context()
        ctx.set("query", q)
        ctx.set("code", q)
        ctx.set("text", q)
        results = orchestrator.run_pipeline(
            ["brain", "security", "token_economy"], ctx
        )
        return "|".join(
            f"{r.metadata.get('engine', r.status.value)}:{r.status.value}"
            for r in results
        )
    return None


class Handler(BaseHTTPRequestHandler):
    orchestrator = None

    def log_message(self, fmt, *args):
        pass

    def _send(self, body, status=200):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        for k, v in SecurityHeaders.csp_for_api() and SecurityHeaders.get().items():
            self.send_header(k, v)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if urlparse(self.path).path == "/health":
            return self._send({"status": "ok"})
        if urlparse(self.path).path == "/schema":
            return self._send(SCHEMA["types"])
        self._send({"error": "POST queries to /"}, status=404)

    def do_POST(self):
        if urlparse(self.path).path != "/":
            return self._send({"error": "not found"}, status=404)

        length = int(self.headers.get("Content-Length", 0))
        if not length:
            return self._send({"errors": [{"message": "empty body"}]}, status=400)

        try:
            body = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            return self._send({"errors": [{"message": "invalid JSON"}]}, status=400)

        query = body.get("query", "")
        if not InputValidator.length(query, 1, 5000):
            return self._send({"errors": [{"message": "invalid query"}]}, status=400)
        if not InputValidator.no_html(query):
            return self._send({"errors": [{"message": "HTML not allowed"}]}, status=400)

        field, args = parse_query(query)
        if not field:
            return self._send({"errors": [{"message": "parse error"}]}, status=400)

        result = resolve(field, args, SCHEMA, Handler.orchestrator)
        return self._send({"data": {field: result}})


def main():
    Handler.orchestrator = create_default_orchestrator()
    server = HTTPServer(("127.0.0.1", 8003), Handler)
    print("GraphQL demo running on http://127.0.0.1:8003")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping.")


if __name__ == "__main__":
    main()
