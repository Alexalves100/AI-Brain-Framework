# Testing Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Estratégia de testes

## Inputs
- Requisitos
- Código
- Riscos

## Outputs
- Plano
- Suítes
- Relatórios

## Invariantes
- Pirâmide
- CI

## Interfaces
Quality Skill, Implementation Skill

## Quando Usar
- Quando precisar de estratégia de testes
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
result = orch.run("19_testing", ctx)
```

### Exemplo 2: Caso Avançado
```python
# Pipeline com múltiplas skills
ctx = Context()
ctx.set("input", "complex_value")
results = orch.run_pipeline(["19_testing", "security"], ctx)
for r in results:
    print(r.status, r.output)
```

## Métricas de Sucesso
- Latência < 100ms para inputs típicos
- Taxa de erro < 1%
- Cobertura de testes > 80%


## Ver Também

- `18-implementation-skill.md`
- `11-quality-skill.md`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
## Referências
- Ver `framework/Delivery/19_testing.py` para implementação
- Ver `tests/test_Delivery.py` para exemplos de uso
