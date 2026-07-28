# Notifications Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Envio de notificações multi-canal: email, push, SMS, in-app.

## Princípios
- User preference respeitada
- Não spam (rate limiting)
- Templates versionados
- Delivery tracking

## Inputs
- Tipo de notificação
- Destinatário
- Conteúdo (template + variáveis)
- Canal preferido

## Outputs
- Notificação enviada
- Status de entrega
- Métricas de engagement

## Canais

| Canal | Uso | Latência |
|---|---|---|
| Email | Transacional, marketing | Minutos |
| Push (FCM/APNS) | Mobile, real-time | Segundos |
| SMS | Crítico, 2FA | Segundos |
| In-app | Web, mobile | Imediato |
| Webhook | Integração B2B | Imediato |

## Ferramentas

| Ferramenta | Canais |
|---|---|
| SendGrid | Email |
| Twilio | SMS, Voice |
| Firebase Cloud Messaging | Push |
| OneSignal | Push multi-plataforma |
| Novu | Multi-canal unificado |

## Invariantes
- Opt-in/opt-out respeitado
- Rate limiting por usuário
- Templates com variáveis validadas
- Retry com backoff
- Logs de entrega

## Workflow

```
1. Trigger (evento, schedule, manual)
2. Buscar preferências do usuário
3. Renderizar template
4. Enviar via canal preferido
5. Tracking de entrega
6. Retry se falhar
```

## Ver Também

- `38-background-jobs-skill.md`
- `27-error-handling-skill.md`
- `10-privacy-skill.md`
```

## Interfaces
- Background Jobs Skill
- Error Handling Skill
- Privacy Architect (consentimento)
- Product Manager (regras de negócio)
