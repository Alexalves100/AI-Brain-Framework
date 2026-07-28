# Capacity Planning Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Previsão e planejamento de capacidade de recursos.

## Princípios
- Baseado em dados históricos
- Projeções conservadoras
- Buffer de 30%
- Review trimestral

## Inputs
- Métricas históricas (90+ dias)
- Projeções de crescimento
- SLOs
- Restrições de budget

## Outputs
- Capacity plans
- Recomendações de provisionamento
- Projeções de custo

## Invariantes
- Dados de pelo menos 90 dias
- Buffer mínimo de 30%
- SLOs respeitados
- Auto-scaling configurado
- Review trimestral

## Fórmula

```
Capacity Needed = (Peak Usage × Growth Factor) + Safety Buffer

Onde:
- Peak Usage = P95 dos últimos 90 dias
- Growth Factor = 1 + (projeção de crescimento %)
- Safety Buffer = 30%
```

## Interfaces
- Capacity Architect
- FinOps Architect
- Performance Skill
- Observability Skill

## Ver Também

- `32-cost-optimization-skill.md`
- `29-capacity-architect`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
