# Token Economy Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Context

## Capacidade
Economia máxima de tokens

## Inputs
- Conteúdo
- Contexto
- Prioridades

## Outputs
- Versão compacta
- Resumo executivo
- Referências

## Invariantes
- Sem perda de informação essencial
- Reuso de docs

## Interfaces
Context Engine, Todas as skills

## Quando Usar
- Quando precisar de economia máxima de tokens
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
result = orch.run("08_token_economy", ctx)
```

### Exemplo 2: Caso Avançado
```python
# Pipeline com múltiplas skills
ctx = Context()
ctx.set("input", "complex_value")
results = orch.run_pipeline(["08_token_economy", "security"], ctx)
for r in results:
    print(r.status, r.output)
```

## Métricas de Sucesso
- Latência < 100ms para inputs típicos
- Taxa de erro < 1%
- Cobertura de testes > 80%


## Ver Também

- `07-context-skill.md`
- `23-token-efficient-coder.md`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
## Referências
- Ver `framework/Context/08_token_economy.py` para implementação
- Ver `tests/test_Context.py` para exemplos de uso
