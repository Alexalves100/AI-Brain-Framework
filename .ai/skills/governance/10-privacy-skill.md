# Privacy Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Governance

## Capacidade
Privacidade e LGPD

## Inputs
- Fluxos de dados
- Bases legais
- Retenção

## Outputs
- DPIA
- Mecanismos
- Compliance

## Invariantes
- Privacy by design
- Minimização

## Interfaces
Security Engine, Compliance Checker

## Quando Usar
- Quando precisar de privacidade e lgpd
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
result = orch.run("10_privacy", ctx)
```

### Exemplo 2: Caso Avançado
```python
# Pipeline com múltiplas skills
ctx = Context()
ctx.set("input", "complex_value")
results = orch.run_pipeline(["10_privacy", "security"], ctx)
for r in results:
    print(r.status, r.output)
```

## Métricas de Sucesso
- Latência < 100ms para inputs típicos
- Taxa de erro < 1%
- Cobertura de testes > 80%


## Ver Também

- `09-security-skill.md`
- `12-privacy-architect`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
## Referências
- Ver `framework/Governance/10_privacy.py` para implementação
- Ver `tests/test_Governance.py` para exemplos de uso
