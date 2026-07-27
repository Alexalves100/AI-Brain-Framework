# Reasoning Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Core

## Capacidade
Raciocínio estruturado e auditável

## Inputs
- Problema
- Premissas
- Restrições

## Outputs
- Cadeia lógica
- Conclusão
- Alternativas

## Invariantes
- Lógica explícita
- Premissas declaradas

## Interfaces
Brain Engine, Knowledge Engine

## Quando Usar
- Quando precisar de raciocínio estruturado e auditável
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
result = orch.run("03_reasoning", ctx)
```

### Exemplo 2: Caso Avançado
```python
# Pipeline com múltiplas skills
ctx = Context()
ctx.set("input", "complex_value")
results = orch.run_pipeline(["03_reasoning", "security"], ctx)
for r in results:
    print(r.status, r.output)
```

## Métricas de Sucesso
- Latência < 100ms para inputs típicos
- Taxa de erro < 1%
- Cobertura de testes > 80%

## Referências
- Ver `framework/Core/03_reasoning.py` para implementação
- Ver `tests/test_Core.py` para exemplos de uso
