# Discovery Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Discovery

## Capacidade
Descoberta estruturada de informações

## Inputs
- Escopo
- Critérios
- Fontes

## Outputs
- Inventário
- Mapa
- Recomendações

## Invariantes
- Fontes oficiais
- Reproduzibilidade

## Interfaces
Index Engine, Graph Engine

## Quando Usar
- Quando precisar de descoberta estruturada de informações
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
result = orch.run("04_discovery", ctx)
```

### Exemplo 2: Caso Avançado
```python
# Pipeline com múltiplas skills
ctx = Context()
ctx.set("input", "complex_value")
results = orch.run_pipeline(["04_discovery", "security"], ctx)
for r in results:
    print(r.status, r.output)
```

## Métricas de Sucesso
- Latência < 100ms para inputs típicos
- Taxa de erro < 1%
- Cobertura de testes > 80%

## Referências
- Ver `framework/Discovery/04_discovery.py` para implementação
- Ver `tests/test_Discovery.py` para exemplos de uso
