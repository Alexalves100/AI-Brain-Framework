# Feature Flags Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Deploy seguro com feature flags para ativação progressiva e rollback instantâneo.

## Princípios
- Decouple deploy de release
- Ativação gradual (canary → 100%)
- Rollback instantâneo sem deploy
- Cleanup após 100% rollout

## Inputs
- Flag name
- Variações (A/B, multivariate)
- Audiência (%, user_id, tenant)
- Métricas de sucesso

## Outputs
- Flag configurada
- Rollout progressivo
- Métricas por variação

## Tipos de Flags

| Tipo | Uso | Exemplo |
|---|---|---|
| Release | Ativar feature gradualmente | `new-checkout-flow` |
| Experiment | A/B test | `checkout-button-color` |
| Operational | Control técnico | `rate-limit-enabled` |
| Permission | Acesso por tier | `premium-features` |

## Invariantes
- Flag tem owner definido
- Cleanup após 100% rollout
- Default OFF para novas features
- Métricas de impacto monitoradas
- Documentação atualizada

## Workflow

```
1. Criar flag (default OFF)
2. Deploy código (flag OFF, sem impacto)
3. Internal testing (5%)
4. Canary (10% → 25% → 50%)
5. Full rollout (100%)
6. Monitorar métricas
7. Cleanup (remover flag)
```

## Interfaces
- Release Architect
- Quality Architect (métricas)
- Security Architect (acesso)
- Documentation Architect

## Ver Também

- `20-release-skill.md`
- `33-incident-response-skill.md`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
