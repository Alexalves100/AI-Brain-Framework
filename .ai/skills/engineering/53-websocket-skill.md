# WebSocket Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Comunicação bidirecional em tempo real via WebSocket.

## Princípios
- Conexões persistentes
- Heartbeat/ping-pong
- Reconexão automática no cliente
- Backpressure handling

## Inputs
- Cliente conecta
- Mensagens bidirecionais
- Eventos do servidor

## Outputs
- Mensagens entregues
- Status de conexão
- Métricas de latência

## Protocolo

```
Client                          Server
  |                               |
  |--- Upgrade: websocket ------->|
  |<-- 101 Switching Protocols ---|
  |                               |
  |--- Ping -------------------->|
  |<-- Pong ----------------------|
  |                               |
  |--- Message ------------------>|
  |<-- Message -------------------|
  |                               |
  |--- Close ------------------->|
  |<-- Close --------------------|
```

## Ferramentas

| Ferramenta | Uso |
|---|---|
| Socket.io | Node.js, fallback |
| ws | Node.js, minimal |
| websockets | Python |
| gorilla/websocket | Go |
| Spring WebSocket | Java |

## Invariantes
- Heartbeat a cada 30s
- Timeout de conexão definido
- Mensagens com tamanho máximo
- Autenticação na conexão (não após)
- Rate limit por conexão

## Padrões

```python
# Autenticação no handshake
1. Cliente envia token na query string
2. Server valida antes de aceitar upgrade
3. Conexão autenticada

# Pub/Sub
1. Cliente subscribe a channel
2. Server publica mensagens
3. Cliente recebe em tempo real

# Rooms
1. Cliente join room
2. Server broadcast para room
3. Cliente leave room
```

## Interfaces
- API Skill
- Performance Skill
- Security Architect
- Observability Skill

## Ver Também

- `15-api-skill.md`
- `16-performance-skill.md`
- `31-observability-skill.md`
