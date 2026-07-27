# Context Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Context

## Capacidade
Gestão de contexto entre agentes

## Inputs
- Estado
- Tokens
- Prioridades

## Outputs
- Contexto empacotado
- Resumos
- Decisões

## Invariantes
- Mínimo viável
- Auditável

## Interfaces
Brain Engine, Token Economy Engine

## Quando Usar
- Quando precisar de gestão de contexto entre agentes
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
result = orch.run("07_context", ctx)
```

### Exemplo 2: Caso Avançado
```python
# Pipeline com múltiplas skills
ctx = Context()
ctx.set("input", "complex_value")
results = orch.run_pipeline(["07_context", "security"], ctx)
for r in results:
    print(r.status, r.output)
```

## Métricas de Sucesso
- Latência < 100ms para inputs típicos
- Taxa de erro < 1%
- Cobertura de testes > 80%

## Referências
- Ver `framework/Context/07_context.py` para implementação
- Ver `tests/test_Context.py` para exemplos de uso
