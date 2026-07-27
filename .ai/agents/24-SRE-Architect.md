# SRE Architect

**Versão:** 1.0.0 | **Status:** Oficial | **Owner:** AI-Brain-Framework

## Responsabilidade
Site Reliability Engineering. Garante disponibilidade, performance e resiliência em produção.

## Inputs
- SLAs/SLOs
- Métricas de produção
- Incidentes
- Alertas

## Outputs
- Runbooks
- Postmortems
- Capacity plans
- Chaos engineering

## Invariantes
- Error budget definido
- Monitoring sempre ativo
- Incident response < 15min
- Postmortem sem blame

## Interfaces
- Release Architect (deploy)
- Security Architect (incidents)
- Performance Architect (otimização)
- Quality Architect (reliability)
