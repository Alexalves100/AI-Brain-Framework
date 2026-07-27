# Architecture Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Decisões arquiteturais

## Inputs
- Requisitos
- Restrições
- Contexto

## Outputs
- Decisão
- ADR
- Trade-offs

## Invariantes
- Documentação
- Aprovação Chief

## Interfaces
Solution Architect, Core Architect

## Quando Usar
- Quando precisar de decisões arquiteturais
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
result = orch.run("13_architecture", ctx)
```

### Exemplo 2: Caso Avançado
```python
# Pipeline com múltiplas skills
ctx = Context()
ctx.set("input", "complex_value")
results = orch.run_pipeline(["13_architecture", "security"], ctx)
for r in results:
    print(r.status, r.output)
```

## Métricas de Sucesso
- Latência < 100ms para inputs típicos
- Taxa de erro < 1%
- Cobertura de testes > 80%

## Referências
- Ver `framework/Engineering/13_architecture.py` para implementação
- Ver `tests/test_Engineering.py` para exemplos de uso
