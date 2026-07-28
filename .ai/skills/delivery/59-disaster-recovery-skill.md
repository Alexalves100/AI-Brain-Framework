# Disaster Recovery Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Recuperação de desastres: backup, RTO, RPO, testes de failover.

## Princípios
- Backup 3-2-1 (3 cópias, 2 mídias, 1 offsite)
- RTO < 1h para sistemas críticos
- RPO < 15min para dados críticos
- Testes trimestrais

## Inputs
- Sistemas críticos
- SLA definido
- Dados a proteger

## Outputs
- Plano de DR
- Backups automatizados
- Testes de failover

## Métricas

| Métrica | Definição | Target |
|---|---|---|
| RTO | Recovery Time Objective | < 1h |
| RPO | Recovery Point Objective | < 15min |
| MTTR | Mean Time To Recover | < 30min |
| Backup Success Rate | % de backups OK | > 99.9% |

## Estratégias

```yaml
# Backup
- Diário: incremental
- Semanal: full
- Mensal: archive (offsite)
- Retenção: 30d / 90d / 1y

# Failover
- Ativo-Ativo: sempre disponível
- Ativo-Passivo: standby
- Multi-Region: DR geográfico
- Backup-Restore: mais simples

# Testes
- Mensal: backup restore
- Trimestral: failover completo
- Anual: DR completo (simulado)
```

## Invariantes
- Backup automatizado (sem manual)
- Backup testado regularmente
- Runbook de DR atualizado
- Comunicação clara durante incidente
- Postmortem após cada DR

## Interfaces
- SRE Architect
- Database Architect
- Security Architect
- Incident Response Skill

## Ver Também

- `33-incident-response-skill.md`
- `56-kubernetes-skill.md`
- `40-database-migration-skill.md`
