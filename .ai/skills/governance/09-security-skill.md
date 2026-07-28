# Security Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Governance

## Capacidade
Aplicação de segurança

## Inputs
- Código
- Arquitetura
- Configurações

## Outputs
- Análise
- Mitigações
- Gates

## Invariantes
- Security by design
- Auditoria contínua

## Interfaces
Security Engine, Privacy Engine

## Quando Usar
- Quando precisar de aplicação de segurança
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
result = orch.run("09_security", ctx)
```

### Exemplo 2: Caso Avançado
```python
# Pipeline com múltiplas skills
ctx = Context()
ctx.set("input", "complex_value")
results = orch.run_pipeline(["09_security", "security"], ctx)
for r in results:
    print(r.status, r.output)
```

## Métricas de Sucesso
- Latência < 100ms para inputs típicos
- Taxa de erro < 1%
- Cobertura de testes > 80%


## Ver Também

- `11-privacy-skill.md`
- `24-security-auditor.md`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
## Referências
- Ver `framework/Governance/09_security.py` para implementação
- Ver `tests/test_Governance.py` para exemplos de uso
