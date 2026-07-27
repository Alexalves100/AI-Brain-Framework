# Knowledge Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Core

## Capacidade
Gestão de conhecimento versionado

## Inputs
- Documentos
- Queries
- Índices

## Outputs
- Conhecimento recuperado
- Fontes citadas
- Recomendações

## Invariantes
- Fontes oficiais
- Sem inferência
- Versionamento

## Interfaces
Discovery Engine, Index Engine

## Quando Usar
- Quando precisar de gestão de conhecimento versionado
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
result = orch.run("01_knowledge", ctx)
```

### Exemplo 2: Caso Avançado
```python
# Pipeline com múltiplas skills
ctx = Context()
ctx.set("input", "complex_value")
results = orch.run_pipeline(["01_knowledge", "security"], ctx)
for r in results:
    print(r.status, r.output)
```

## Métricas de Sucesso
- Latência < 100ms para inputs típicos
- Taxa de erro < 1%
- Cobertura de testes > 80%

## Referências
- Ver `framework/Core/01_knowledge.py` para implementação
- Ver `tests/test_Core.py` para exemplos de uso
