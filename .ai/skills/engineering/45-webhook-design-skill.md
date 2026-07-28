# Webhook Design Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Design de webhooks idempotentes, seguros e observáveis.

## Princípios
- Idempotência (não processar 2x)
- Assinatura verificada
- Retry com backoff
- Logging completo

## Inputs
- Evento a notificar
- URL de destino
- Headers de segurança

## Outputs
- Webhook enviado
- Resposta do receiver
- Log da entrega
- Retry se falhar

## Estrutura do Webhook

```json
POST /webhooks/{gateway}
Headers:
  Content-Type: application/json
  X-Signature: sha256={hmac}
  X-Request-ID: {uuid}
  X-Timestamp: {iso8601}
  X-Retry-Count: {n}

Body:
{
  "event": "payment.approved",
  "id": "evt_123",
  "timestamp": "2026-07-27T10:00:00Z",
  "data": { ... }
}
```

## Invariantes
- Assinatura HMAC válida
- Timestamp recente (< 5min)
- Idempotência via event_id
- Retry exponencial (1s, 2s, 4s, 8s, 16s)
- Dead letter queue após N retries
- Logs estruturados

## Workflow do Receiver

```
1. Receber POST
2. Validar assinatura
3. Validar timestamp
4. Verificar idempotência (event_id já processado?)
5. Processar evento
6. Retornar 200 OK
7. Se falhar: retornar 5xx (retry)
```

## Interfaces
- API Skill
- Security Architect
- Payment Skill
- Error Handling Skill

## Ver Também

- `15-api-skill.md`
- `09-security-skill.md`
- `27-error-handling-skill.md`
