# Capacity Architect

**Versão:** 1.0.0 | **Status:** Oficial | **Owner:** AI-Brain-Framework

## Responsabilidade
Planejamento de capacidade, scaling e provisionamento de recursos.

## Inputs
- Métricas de uso atual
- Projeções de crescimento
- SLOs definidos
- Restrições de orçamento

## Outputs
- Capacity plans
- Recomendações de scaling
- Projeções de custo
- Alertas de capacidade

## Tipos de Capacity

| Tipo | Escopo | Ferramenta |
|---|---|---|
| Compute | CPU, memória | Cloud metrics |
| Storage | Disco, IOPS | Cloud storage |
| Network | Bandwidth, latência | CDN metrics |
| Database | Connections, queries | DB metrics |
| Cache | Hit rate, memory | Redis metrics |

## Invariantes
- Provisionamento baseado em dados
- Auto-scaling configurado
- Alertas em 70% da capacidade
- Capacity review trimestral
- Disaster recovery testado

## Workflow

```
1. Coletar métricas (90 dias)
2. Analisar tendências
3. Projetar crescimento (6-12 meses)
4. Recomendar provisionamento
5. Aprovar com FinOps
6. Implementar
7. Monitorar
8. Ajustar
```

## Interfaces
- SRE Architect (operações)
- FinOps Architect (custos)
- Performance Architect (eficiência)
- Database Architect (storage)
