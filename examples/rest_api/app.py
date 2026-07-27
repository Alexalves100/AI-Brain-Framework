"""
REST API Example
Version: 1.0.0
Minimal REST API using only Python stdlib with AI-Brain-Framework.
"""

import json
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from framework import create_default_orchestrator, Context, SecurityHeaders, InputValidator


KB = {
    "users": {
        "1": {"id": "1", "name": "Alice", "email": "alice@example.com"},
        "2": {"id": "2", "name": "Bob", "email": "bob@example.com"},
    }
}


class Handler(BaseHTTPRequestHandler):
    orchestrator = None

    def log_message(self, fmt, *args):
        pass

    def _send(self, body, status=200, ctype="application/json"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        for k, v in SecurityHeaders.csp_for_api() and SecurityHeaders.get().items():
            self.send_header(k, v)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            return {}

    def do_GET(self):
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]

        if parts == ["users"]:
            return self._send({"users": list(KB["users"].values())})
        if len(parts) == 2 and parts[0] == "users":
            user = KB["users"].get(parts[1])
            if not user:
                return self._send({"error": "not found"}, status=404)
            return self._send(user)
        if parts == ["health"]:
            return self._send({"status": "ok"})

        return self._send({"error": "not found"}, status=404)

    def do_POST(self):
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        if parts != ["users"]:
            return self._send({"error": "not found"}, status=404)

        body = self._read_body()
        name = body.get("name", "")
        email = body.get("email", "")

        if not InputValidator.length(name, 1, 100):
            return self._send({"error": "invalid name"}, status=400)
        if not InputValidator.email(email):
            return self._send({"error": "invalid email"}, status=400)

        ctx = Context()
        ctx.set("code", json.dumps(body))
        sec = Handler.orchestrator.run("security", ctx)

        new_id = str(len(KB["users"]) + 1)
        KB["users"][new_id] = {"id": new_id, "name": name, "email": email}

        return self._send({
            "created": KB["users"][new_id],
            "security_findings": sec.output.get("findings", []),
        }, status=201)


def main():
    Handler.orchestrator = create_default_orchestrator()
    server = HTTPServer(("127.0.0.1", 8001), Handler)
    print("REST API demo running on http://127.0.0.1:8001")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping.")


if __name__ == "__main__":
    main()
