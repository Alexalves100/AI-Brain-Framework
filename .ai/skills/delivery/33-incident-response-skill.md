# Incident Response Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Resposta estruturada a incidentes em produção.

## Princípios
- Acknowledge em < 15min
- Mitigate antes de root cause
- Communicate sempre
- Postmortem sem blame

## Inputs
- Alerta ou reporte
- Severidade
- Impacto

## Outputs
- Incident response
- Status updates
- Postmortem
- Action items

## Sev Levels

| Sev | Impacto | Response Time |
|---|---|---|
| Sev1 | Sistema down | < 15min |
| Sev2 | Feature quebrada | < 1h |
| Sev3 | Degradação | < 4h |
| Sev4 | Cosmético | < 1 semana |

## Workflow

```
1. DETECT (alerta ou reporte)
2. ACK (acknowledge em < 15min)
3. ASSESS (severidade e impacto)
4. MITIGATE (parar o sangramento)
5. COMMUNICATE (status page, stakeholders)
6. RESOLVE (root cause)
7. POSTMORTEM (sem blame, com action items)
```

## Invariantes
- Sempre comunicar (mesmo que "ainda investigando")
- Postmortem em até 5 dias úteis
- Action items com owner e deadline
- Sem blame (foco em sistemas, não pessoas)

## Interfaces
- SRE Architect
- Logging Skill
- Observability Skill
- Communication channels
