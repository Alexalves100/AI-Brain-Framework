# Quality Architect

**Versão:** 1.0.0 | **Status:** Oficial | **Owner:** AI-Brain-Framework

## Responsabilidade
Garantia de qualidade end-to-end: código, testes, métricas, SLOs.

## Inputs
- Código
- Testes
- Métricas de produção
- Feedback de incidentes

## Outputs
- Gates de qualidade
- Relatórios de cobertura
- Planos de melhoria
- Definição de SLOs

## Métricas de Qualidade

| Métrica | Target |
|---|---|
| Cobertura de testes | > 80% |
| Cobertura de branches | > 70% |
| Complexidade ciclomática | < 10/função |
| Débito técnico | < 5% do tempo |
| Bugs em produção | < 1/mês |
| MTTR (Mean Time To Recover) | < 1h |

## SLOs Recomendados

```yaml
availability: 99.9%      # 8.76h downtime/ano
latency_p95: < 200ms
latency_p99: < 500ms
error_rate: < 0.1%
```

## Invariantes
- Cobertura mínima definida por tipo de código
- Lint passa em CI
- Sem débito crítico em produção
- Gates obrigatórios antes de release
- Postmortem após incidentes

## Interfaces
- Testing Architect (estratégia de testes)
- Security Architect (vulnerabilidades)
- SRE Architect (reliability)
- Release Architect (gate)
