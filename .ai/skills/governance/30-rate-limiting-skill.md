# Rate Limiting Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Governance

## Capacidade
Proteção contra abuso via limites de taxa por IP/usuário/endpoint.

## Princípios
- Limites por criticidade do endpoint
- Sliding window
- Fail open em caso de erro
- Métricas de throttling

## Inputs
- Identificador (IP, user_id, api_key)
- Endpoint
- Limite configurado

## Outputs
- Permitido/Bloqueado
- Headers de rate limit
- Métricas

## Invariantes
- Limites mais estritos em login/pagamentos
- Headers `X-RateLimit-*` sempre presentes
- 429 com Retry-After
- Whitelist para serviços internos

## Estratégias

```python
# Token bucket
allowed, remaining = limiter.is_allowed(client_id)

# Sliding window
hits = [t for t in hits if t > now - window]
if len(hits) >= limit:
    return 429

# Headers
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1234567890
Retry-After: 60
```

## Interfaces
- Security Skill
- API Skill
- SRE Architect

## Ver Também

- `09-security-skill.md`
- `15-api-skill.md`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
