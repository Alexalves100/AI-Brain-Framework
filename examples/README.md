# Examples

**Version:** 1.0.0 | **Status:** Official

## Available Examples

| Example | Port | Description |
|---|---|---|
| `simple_website` | 8000 | Minimal HTTP server with security headers, validation, brain routing |
| `rest_api` | 8001 | REST API with CRUD, security audit on writes |
| `websocket` | 8002 | WebSocket server with frame parsing, brain pipeline per message |
| `graphql` | 8003 | GraphQL server with query parsing, resolver dispatch |

## Run

```bash
python examples/simple_website/app.py
python examples/rest_api/app.py
python examples/websocket/app.py
python examples/graphql/app.py
```

All examples use only Python stdlib (no external dependencies).
