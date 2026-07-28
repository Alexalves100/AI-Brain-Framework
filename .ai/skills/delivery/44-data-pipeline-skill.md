# Data Pipeline Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Pipelines de dados robustos: ETL/ELT, batch e streaming.

## Princípios
- Idempotência
- Schema evolution
- Data quality checks
- Monitoring e alerting

## Inputs
- Fonte de dados
- Destino
- Transformações
- SLA

## Outputs
- Pipeline executado
- Dados transformados
- Métricas de qualidade
- Alertas de falha

## Ferramentas

| Tipo | Ferramentas |
|---|---|
| Batch | Airflow, Prefect, Dagster |
| Streaming | Kafka, Pulsar, Kinesis |
| Transform | dbt, Spark, Beam |
| Orchestration | Airflow, Dagster, Prefect |

## Padrões

```python
# Extract
- CDC (Change Data Capture)
- Batch incremental
- API polling
- Event streaming

# Transform
- SQL (dbt)
- Python (pandas, Spark)
- Data quality checks

# Load
- Upsert (idempotência)
- Partitioning (date, hash)
- Compression
```

## Invariantes
- Idempotência (retry-safe)
- Schema versionado
- Data lineage documentado
- Monitoring de SLA
- Alertas em falhas
- PII mascarado

## Interfaces
- Data Engineer
- Database Architect
- ML Engineer (features)
- SRE Architect (monitoring)

## Ver Também

- `14-database-skill.md`
- `43-model-evaluation-skill.md`
- `40-database-migration-skill.md`
