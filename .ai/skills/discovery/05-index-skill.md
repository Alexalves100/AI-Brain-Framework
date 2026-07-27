# Index Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Discovery

## Capacidade
Indexação estruturada

## Inputs
- Documentos
- Metadados
- Esquemas

## Outputs
- Índices
- Referências
- Mapas

## Invariantes
- Atualização contínua
- Busca determinística

## Interfaces
Discovery Engine, Graph Engine

## Quando Usar
- Quando precisar de indexação estruturada
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
result = orch.run("05_index", ctx)
```

### Exemplo 2: Caso Avançado
```python
# Pipeline com múltiplas skills
ctx = Context()
ctx.set("input", "complex_value")
results = orch.run_pipeline(["05_index", "security"], ctx)
for r in results:
    print(r.status, r.output)
```

## Métricas de Sucesso
- Latência < 100ms para inputs típicos
- Taxa de erro < 1%
- Cobertura de testes > 80%

## Referências
- Ver `framework/Discovery/05_index.py` para implementação
- Ver `tests/test_Discovery.py` para exemplos de uso
