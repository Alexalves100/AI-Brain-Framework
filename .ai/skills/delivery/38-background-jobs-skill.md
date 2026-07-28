# Background Jobs Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Processamento assíncrono via filas e workers.

## Princípios
- Idempotência
- Retry com backoff
- Dead letter queue
- Monitoring de jobs

## Inputs
- Tarefa a executar
- Prioridade
- Retry policy

## Outputs
- Job enfileirado
- Resultado processado
- Status (pending/running/completed/failed)

## Ferramentas Recomendadas

| Ferramenta | Uso |
|---|---|
| Celery | Python, Redis/RabbitMQ |
| BullMQ | Node.js, Redis |
| Sidekiq | Ruby, Redis |
| Resque | Ruby, Redis |
| AWS SQS | AWS-native |
| Google Cloud Tasks | GCP-native |

## Invariantes
- Jobs idempotentes (retry-safe)
- Timeout definido
- Dead letter queue para falhas
- Monitoring de duração
- Cleanup de jobs antigos

## Workflow

```
1. Producer enfileira job
2. Worker pega job
3. Worker processa (com timeout)
4. Sucesso → marca completed
5. Falha → retry com backoff
6. Após N retries → dead letter queue
7. Alerta se DLQ não vazia
```

## Interfaces
- Architecture Skill
- Error Handling Skill
- Observability Skill
- SRE Architect

## Ver Também

- `27-error-handling-skill.md`
- `31-observability-skill.md`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
