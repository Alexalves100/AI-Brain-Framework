# Logging Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Logging estruturado, contextual e auditável.

## Princípios
- JSON estruturado
- Contexto rico
- Níveis apropriados
- Sem PII em logs

## Inputs
- Evento
- Contexto (user_id, request_id, etc.)
- Nível

## Outputs
- Log estruturado (JSON)
- Correlation ID
- Métricas derivadas

## Invariantes
- Nunca logar senhas/tokens
- PII sempre mascarado
- Timestamps em UTC
- Correlation ID em toda request

## Níveis

```python
import logging
logging.DEBUG    # Dev only
logging.INFO     # Eventos normais
logging.WARNING  # Anormal mas recuperável
logging.ERROR    # Falha mas sistema ok
logging.CRITICAL # Sistema comprometido
```

## Interfaces
- Observability Skill
- Error Handling Skill
- SRE Architect

## Ver Também

- `27-error-handling-skill.md`
- `31-observability-skill.md`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
