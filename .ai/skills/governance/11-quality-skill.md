# Quality Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Governance

## Capacidade
Garantia de qualidade

## Inputs
- Código
- Testes
- Métricas

## Outputs
- Gates
- Relatórios
- Planos

## Invariantes
- Cobertura mínima
- Lint passa

## Interfaces
Quality Analyzer, Testing Engine

## Quando Usar
- Quando precisar de garantia de qualidade
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
result = orch.run("11_quality", ctx)
```

### Exemplo 2: Caso Avançado
```python
# Pipeline com múltiplas skills
ctx = Context()
ctx.set("input", "complex_value")
results = orch.run_pipeline(["11_quality", "security"], ctx)
for r in results:
    print(r.status, r.output)
```

## Métricas de Sucesso
- Latência < 100ms para inputs típicos
- Taxa de erro < 1%
- Cobertura de testes > 80%

## Referências
- Ver `framework/Governance/11_quality.py` para implementação
- Ver `tests/test_Governance.py` para exemplos de uso
