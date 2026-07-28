# Memory Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Core

## Capacidade
Memória persistente entre sessões

## Inputs
- Estado atual
- Histórico
- Contexto

## Outputs
- Snapshot
- Recuperação
- Histórico

## Invariantes
- Imutável após commit
- Recuperação determinística

## Interfaces
Knowledge Engine, Context Engine

## Quando Usar
- Quando precisar de memória persistente entre sessões
- Em pipelines que combinam múltiplas skills

## Quando NÃO Usar
- Para tarefas fora do escopo desta skill
- Quando uma skill mais específica já cobre o caso

## Anti-Patterns
- Ignorar invariantes
- Usar sem validar inputs

## Exemplos

### Exemplo 1: Caso Simples
```python
from framework import create_default_orchestrator, Context
orch = create_default_orchestrator()
ctx = Context()
ctx.set("input", "value")
result = orch.run("02_memory", ctx)
```

### Exemplo 2: Caso Avançado
```python
# Pipeline com múltiplas skills
ctx = Context()
ctx.set("input", "complex_value")
results = orch.run_pipeline(["02_memory", "security"], ctx)
for r in results:
    print(r.status, r.output)
```

## Métricas de Sucesso
- Latência < 100ms para inputs típicos
- Taxa de erro < 1%
- Cobertura de testes > 80%


## Ver Também

- `01-knowledge-skill.md`
- `07-context-skill.md`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
## Referências
- Ver `framework/Core/02_memory.py` para implementação
- Ver `tests/test_Core.py` para exemplos de uso
