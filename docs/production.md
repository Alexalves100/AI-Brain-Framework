# Guia de Uso em Produção

**Versão:** 1.0.0 | **Status:** Oficial

Este guia cobre como usar o AI-Brain-Framework em ambiente de produção.

---

## 1. Instalação

### Como Pacote Python

```bash
pip install ai-brain-framework
```

### Como Container Docker

```bash
docker pull ai-brain-framework:1.0.0
docker run -p 8000:8000 ai-brain-framework:1.0.0
```

### Via Docker Compose (todos os 4 exemplos)

```bash
docker-compose up
```

---

## 2. Cenários de Uso

### Cenário A: Web Service com Segurança OWASP

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
from framework import create_default_orchestrator, Context
from framework.standards import SecurityHeaders, InputValidator, RateLimiter

orch = create_default_orchestrator()
limiter = RateLimiter(max_requests=60, window_seconds=60)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        allowed, _ = limiter.is_allowed(client_ip)
        if not allowed:
            self.send_response(429)
            self.end_headers()
            return

        for k, v in SecurityHeaders.get().items():
            self.send_header(k, v)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        # ... lógica de negócio ...
```

### Cenário B: API REST com Auditoria

```python
from framework import create_default_orchestrator, Context

orch = create_default_orchestrator()

def audit_request(payload: str) -> dict:
    ctx = Context()
    ctx.set("code", payload)
    ctx.set("query", payload)
    result = orch.run("security", ctx)
    return result.output
```

### Cenário C: WebSocket com Pipeline

```python
from framework import create_default_orchestrator, Context

orch = create_default_orchestrator()

def handle_message(msg: str) -> list:
    ctx = Context()
    ctx.set("query", msg)
    ctx.set("code", msg)
    ctx.set("text", msg)
    return orch.run_pipeline(
        ["brain", "security", "token_economy"], ctx
    )
```

### Cenário D: Validação de UI

```python
from framework import create_default_orchestrator, Context

orch = create_default_orchestrator()

def validate_ui(html: str, css: str) -> dict:
    ctx = Context()
    ctx.set("html", html)
    ctx.set("css", css)
    result = orch.run("ui_design", ctx)
    return {
        "score": result.output["score"],
        "issues": result.output["findings"],
    }
```

---

## 3. Configuração para Produção

### Variáveis de Ambiente

```bash
# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/ai-brain/app.log

# Rate limiting
RATE_LIMIT_REQUESTS=60
RATE_LIMIT_WINDOW=60

# Server
HOST=0.0.0.0
PORT=8000

# i18n
LOCALE=en  # ou pt-BR

# Debug (NUNCA true em produção)
DEBUG=false
```

### Configuração via Código

```python
# config.py
import os
from pathlib import Path

class Config:
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "8000"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "/var/log/ai-brain/app.log")
    LOCALE = os.getenv("LOCALE", "en")
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
```

---

## 4. Observabilidade

### Logging Estruturado

```python
from framework import get_logger

logger = get_logger("my_app", log_file="/var/log/app.log")
logger.info("request_received", extra={
    "method": "POST",
    "path": "/api/users",
    "client_ip": "1.2.3.4",
})
```

### Métricas de Performance

```python
from framework import MetricsCollector

metrics = MetricsCollector()

with metrics.measure("brain_skill"):
    orch.run("brain", ctx)

# Expor via endpoint /metrics
print(metrics.all())
```

### Auditoria

```python
from framework.governance import AuditLog

audit = AuditLog(path="/var/log/ai-brain/audit.jsonl")
audit.log("user_created", actor="admin", user_id="123")
```

---

## 5. Segurança em Produção

### Checklist

- [x] Headers OWASP aplicados (CSP, HSTS, X-Frame-Options)
- [x] Validação de entrada em todos os endpoints
- [x] Rate limiting por IP/usuário
- [x] HTTPS obrigatório (TLS 1.2+)
- [x] Logs estruturados sem dados sensíveis
- [x] Auditoria de ações críticas
- [x] Dependências atualizadas
- [x] Container executando como usuário não-root

### Scan Automático

```python
# Em CI/CD, rodar antes do deploy
from framework import create_default_orchestrator, Context

orch = create_default_orchestrator()
ctx = Context()
ctx.set("code", open("src/main.py").read())
result = orch.run("security", ctx)
if result.output["total"] > 0:
    print("FAIL: security issues found")
    for f in result.output["findings"]:
        print(f"  [{f['severity']}] {f['type']}")
    exit(1)
```

---

## 6. Deploy

### Opção 1: Docker

```bash
docker build -t my-app:1.0.0 .
docker run -d -p 8000:8000 --name my-app my-app:1.0.0
```

### Opção 2: Docker Compose

```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=INFO
      - RATE_LIMIT_REQUESTS=100
    restart: unless-stopped
```

### Opção 3: Systemd

```ini
# /etc/systemd/system/ai-brain.service
[Unit]
Description=AI-Brain-Framework
After=network.target

[Service]
Type=simple
User=ai-brain
WorkingDirectory=/opt/ai-brain
ExecStart=/usr/bin/python3 -m my_app
Restart=always
Environment=LOG_LEVEL=INFO

[Install]
WantedBy=multi-user.target
```

---

## 7. Monitoramento

### Health Check

```python
def health_check() -> dict:
    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime": get_uptime(),
        "engines": 8,
    }
```

### Endpoint `/metrics`

```python
from framework import MetricsCollector

metrics = MetricsCollector()

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            import json
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(metrics.all()).encode())
```

---

## 8. Escalabilidade

### Stateless

O framework é **stateless** por padrão. Cada request cria seu próprio `Context`.

### Horizontal Scaling

```bash
# Múltiplas instâncias atrás de load balancer
docker run -d --name app-1 my-app:1.0.0
docker run -d --name app-2 my-app:1.0.0
docker run -d --name app-3 my-app:1.0.0
```

### Cache

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_brain_route(query_hash: str) -> str:
    # Cache de rotas do brain engine
    ...
```

---

## 9. Troubleshooting

### Logs não aparecem

```bash
# Verificar LOG_LEVEL
echo $LOG_LEVEL

# Verificar permissões do arquivo
ls -la /var/log/ai-brain/
```

### Performance degradada

```python
# Verificar métricas
from framework import MetricsCollector
mc = MetricsCollector()
print(mc.all())
# Identificar skills lentas
```

### Memory leak

```python
# O framework não mantém estado global
# Cada Context é descartado após uso
# Verificar se há referências circulares no código
```

---

## 10. Referência Rápida

| Necessidade | Comando/Módulo |
|---|---|
| Criar web service | `examples/simple_website/app.py` |
| Criar API REST | `examples/rest_api/app.py` |
| Criar WebSocket | `examples/websocket/app.py` |
| Criar GraphQL | `examples/graphql/app.py` |
| Auditar código | `orch.run("security", ctx)` |
| Validar UI | `orch.run("ui_design", ctx)` |
| Comprimir texto | `orch.run("token_economy", ctx)` |
| Persistir dados | `orch.run("memory", ctx)` |
| Knowledge base | `orch.run("knowledge", ctx)` |
| Reasoning | `orch.run("reasoning", ctx)` |
| Scan codebase | `orch.run("discovery", ctx)` |

---

## Próximos Passos

1. **Customize** os agentes/skills em `.ai/` para seu domínio
2. **Adicione** engines específicas em `framework/engines/`
3. **Configure** CI/CD com os workflows em `.github/workflows/`
4. **Monitore** com `/metrics` endpoint
5. **Itere** baseado em métricas reais de produção

---

**Suporte:** Consulte `README.md`, `CONTRIBUTING.md`, e os 76 testes em `tests/`.
