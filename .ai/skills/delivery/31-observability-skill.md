# Observability Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Pilares de observabilidade: métricas, logs e traces.

## Princípios
- Três pilares: metrics, logs, traces
- Correlation ID贯穿 tudo
- SLI/SLO definidos
- Dashboards por serviço

## Inputs
- Eventos do sistema
- Métricas de runtime
- Traces de requests

## Outputs
- Métricas (RED: Rate, Errors, Duration)
- Logs estruturados
- Distributed traces
- Alertas

## Invariantes
- Toda request tem correlation ID
- Métricas RED expostas
- Traces amostrados (1% em prod)
- Alertas em SLO violations

## Três Pilares

```yaml
Metrics:
  - Request rate (req/s)
  - Error rate (%)
  - Duration (p50, p95, p99)
  - Saturation (CPU, memory)

Logs:
  - Structured (JSON)
  - Correlation ID
  - Level (DEBUG/INFO/WARN/ERROR)
  - Context (user_id, request_id)

Traces:
  - Span por operação
  - Parent-child relationships
  - Sampling (1% prod, 100% debug)
  - Export para Jaeger/Tempo
```

## Interfaces
- Logging Skill
- Error Handling Skill
- Performance Skill
- SRE Architect
