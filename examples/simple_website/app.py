"""
Simple Website Example
Version: 1.0.0
A minimal HTTP server using only Python stdlib that demonstrates
the AI-Brain-Framework in action.
"""

import json
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from framework import (
    create_default_orchestrator,
    Context,
    SecurityHeaders,
    InputValidator,
)


INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI-Brain-Framework Demo</title>
  <style>
    body { font-family: -apple-system, sans-serif; max-width: 720px; margin: 40px auto; padding: 0 16px; }
    h1 { color: #1a1a1a; }
    form { margin: 20px 0; }
    input, button { padding: 8px 12px; font-size: 14px; }
    input { width: 60%; border: 1px solid #ccc; border-radius: 4px; }
    button { background: #0066cc; color: white; border: 0; border-radius: 4px; cursor: pointer; }
    pre { background: #f4f4f4; padding: 12px; border-radius: 4px; overflow-x: auto; }
    .meta { color: #666; font-size: 12px; }
 </style>
</head>
<body>
  <h1>AI-Brain-Framework Demo</h1>
  <p class="meta">Powered by framework/core + framework/engines + framework/standards</p>
  <form method="GET" action="/analyze">
    <input name="q" placeholder="Ask the brain engine..." autofocus>
    <button type="submit">Analyze</button>
 </form>
  <p>Try: <code>sql injection</code>, <code>xss attack</code>, <code>performance issue</code</p>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    orchestrator = None

    def log_message(self, format, *args):
        pass

    def _send(self, body, status=200, ctype="text/html; charset=utf-8"):
        self.send_response(status)
        for k, v in SecurityHeaders.get().items():
            self.send_header(k, v)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/" or url.path == "/index.html":
            self._send(INDEX_HTML.encode("utf-8"))
            return

        if url.path == "/analyze":
            params = parse_qs(url.query)
            query = (params.get("q", [""])[0] or "").strip()

            if not InputValidator.length(query, min_len=1, max_len=500):
                self._send(b"<h1>Invalid input</h1>", status=400)
                return

            if not InputValidator.no_html(query):
                self._send(b"<h1>HTML not allowed</h1>", status=400)
                return

            ctx = Context()
            ctx.set("query", query)
            ctx.set("code", query)
            ctx.set("text", query)

            results = Handler.orchestrator.run_pipeline(
                ["brain", "security", "token_economy"], ctx
            )

            output = {
                "query": query,
                "pipeline": [r.metadata.get("engine", r.status.value) for r in results],
                "brain": results[0].output if len(results) > 0 else None,
                "security": results[1].output if len(results) > 1 else None,
                "tokens_used": ctx.tokens_used,
            }
            body = json.dumps(output, indent=2, ensure_ascii=False).encode("utf-8")
            self._send(body, ctype="application/json; charset=utf-8")
            return

        if url.path == "/health":
            self._send(b'{"status":"ok"}', ctype="application/json")
            return

        self._send(b"<h1>404</h1>", status=404)


def main():
    Handler.orchestrator = create_default_orchestrator()
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    print("AI-Brain-Framework demo running on http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping.")


if __name__ == "__main__":
    main()
