# AI-Brain-Framework

**Version:** 1.0.0 | **Status:** Production | **License:** MIT

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org)
[![Tests](https://img.shields.io/badge/tests-62%20passing-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-success.svg)](pyproject.toml)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-blue.svg)](https://github.com/astral-sh/ruff)

Framework profissional com **cérebro digital** para construção de **websites e sistemas web profissionais**.

Zero dependências externas. Apenas Python 3.8+.

---

## Instalação

### Via pip (quando publicado)

```bash
pip install ai-brain-framework
```

### Local (desenvolvimento)

```bash
git clone <repo>
cd AI-Brain-Framework
pip install -e ".[dev]"
```

---

## Uso Rápido (Python)

```python
from framework import create_default_orchestrator, Context

orch = create_default_orchestrator()

ctx = Context()
ctx.set("query", "sql injection vulnerability")
ctx.set("code", "execute('SELECT * FROM users WHERE id=' + uid)")
ctx.set("text", "Claro, vou ajudar. Espero que seja util.")

results = orch.run_pipeline(
    ["brain", "security", "token_economy"],
    ctx,
)

for r in results:
    print(r.metadata.get("engine"), "->", r.status.value)
    print(r.output)
```

---

## Uso via CLI

```bash
# Análise completa (brain + security + token_economy)
ai-brain analyze "sql injection vulnerability"

# Roteamento por categoria
ai-brain brain "performance issue"

# Auditoria de segurança
ai-brain security --code "execute('SELECT * FROM ' + table)"

# Compressão de texto
ai-brain compress --text "Claro, vou ajudar. Espero que seja util."

# Knowledge base
ai-brain knowledge add --key csrf --content "Mitigation requires tokens"
ai-brain knowledge search --query "tokens"

# Reasoning estruturado
ai-brain reason --premise "All users have email" --premise "Alice is a user" \
              --conclusion "Alice has email"

# Discovery de codebase
ai-brain discover --path ./framework --pattern python
```

---

## Uso como Web Server

Quatro exemplos prontos, todos em Python puro (sem Flask/FastAPI):

```bash
python examples/simple_website/app.py   # http://localhost:8000
python examples/rest_api/app.py         # http://localhost:8001
python examples/websocket/app.py        # ws://localhost:8002
python examples/graphql/app.py          # http://localhost:8003
```

---

## Engines Disponíveis (8)

| Engine | Função |
|---|---|
| `brain` | Roteamento por categoria (security, performance, architecture, docs, testing) |
| `security` | Auditoria regex (SQLi, XSS, eval, hardcoded secrets, weak hash, insecure HTTP) |
| `token_economy` | Compressão de texto (remove filler, normaliza whitespace) |
| `memory` | KV persistente em JSON |
| `knowledge` | Knowledge base com search/indexing |
| `reasoning` | Raciocínio estruturado com premissas e confidence |
| `discovery` | Scan de codebase por tipo de arquivo |
| `ui_design` | Validação de UI/UX (acessibilidade, semântica, responsividade) |

## Módulos Adicionais

| Módulo | Função |
|---|---|
| `scanners` | CodeScanner, DependencyScanner, StructureScanner |
| `analyzers` | ComplexityAnalyzer, QualityAnalyzer, MetricsAnalyzer |
| `builders` | ProjectBuilder, ModuleBuilder, ConfigBuilder |
| `governance` | PolicyEngine, AuditLog, ComplianceChecker |
| `prompts` | PromptRegistry, PromptBuilder |
| `schemas` | SchemaValidator, SchemaRegistry |

---

## Testes

```bash
python -m unittest discover tests
```

76 testes passando.

---

## Segurança por Padrão

Todos os exemplos aplicam automaticamente:

- **OWASP Headers** (CSP, HSTS, X-Frame-Options, etc.)
- **Input Validation** (whitelist: email, slug, UUID, length, no-HTML)
- **Security Audit** em todo input de código

---

## Arquitetura

```
AI-Brain-Framework/
├── framework/
│   ├── core/           # Skill, Registry, Context, Orchestrator
│   ├── engines/        # 7 engines funcionais
│   └── standards/      # SecurityHeaders, InputValidator
├── examples/           # 4 exemplos web
├── tests/              # 29 testes
├── tools/cli.py        # CLI interativa
├── pyproject.toml      # Pacote Python
└── .github/workflows/  # CI/CD
```

---

## Skills Oficiais (63)

Definidas em `.ai/skills/`, organizadas por categoria:
- **core** (4): brain, knowledge, memory, reasoning
- **discovery** (3): discovery, index, graph
- **context** (2): context, token-economy
- **governance** (9): security, privacy, quality, review, rate-limiting, secrets-management, authentication, authorization
- **engineering** (24): architecture, database, api, performance, documentation, secure-dev-framework, token-efficient-coder, security-auditor, security-report, ui-design, multi-tenancy, api-versioning, prompt-engineering, model-evaluation, webhook-design, search, graphql, websocket, docker, kubernetes, infrastructure-as-code
- **delivery** (21): implementation, testing, release, governance, error-handling, logging, caching, observability, cost-optimization, incident-response, capacity-planning, chaos-engineering, feature-flags, background-jobs, database-migration, data-pipeline, refactoring, notifications, file-upload, api-testing, ci-cd, disaster-recovery

Veja `.ai/HIERARCHY.md` para diagramas e `.ai/EXECUTION_FLOW.md` para fluxos.

---

## Licença

MIT — Veja `LICENSE`.
