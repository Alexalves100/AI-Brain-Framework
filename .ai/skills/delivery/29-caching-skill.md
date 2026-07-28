# Caching Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Estratégias de cache para performance e redução de carga.

## Princípios
- Cache invalidation é difícil
- TTL adequado
- Cache stampede prevention
- Métricas de hit/miss

## Inputs
- Dados a cachear
- TTL desejado
- Chave de cache

## Outputs
- Valor cacheado
- Hit/miss metrics
- Invalidação controlada

## Invariantes
- Nunca cachear dados sensíveis sem criptografia
- TTL máximo definido
- Invalidação em writes
- Monitoring de hit rate

## Estratégias

```python
# Cache-aside (lazy loading)
value = cache.get(key)
if value is None:
    value = expensive_query()
    cache.set(key, value, ttl=300)

# Write-through
cache.set(key, value)
db.write(value)

# TTL-based
cache.set(key, value, ttl=300)

# Cache stampede prevention
with cache.lock(key):
    value = expensive_query()
    cache.set(key, value, ttl=300)
```

## Interfaces
- Performance Skill
- Architecture Skill
- SRE Architect

## Ver Também

- `16-performance-skill.md`
- `31-observability-skill.md`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
