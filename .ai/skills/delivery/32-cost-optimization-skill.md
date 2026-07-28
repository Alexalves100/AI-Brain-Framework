# Cost Optimization Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Otimização de custos cloud e recursos de TI.

## Princípios
- Medir antes de otimizar
- Tags obrigatórias
- Right-sizing contínuo
- Reserved capacity quando previsível

## Inputs
- Bills de cloud
- Métricas de uso
- Padrões de tráfego

## Outputs
- Recomendações de economia
- Scripts de right-sizing
- Relatórios de FinOps

## Invariantes
- Não comprometer SLOs
- Tags em 100% dos recursos
- Alertas em 80% do budget
- Review mensal

## Técnicas

```python
# Compute
- Rightsizing (CPU/memory)
- Spot/Preemptible instances
- Auto-scaling
- Schedule-based scaling (dev/staging)

# Storage
- Lifecycle policies (S3 → Glacier)
- Compression
- Deduplication
- Tiered storage

# Database
- Read replicas (read-heavy)
- Archiving (old data)
- Index optimization
- Connection pooling

# Network
- CDN (CloudFront, Cloudflare)
- Caching (Redis, Memcached)
- Compression (gzip, brotli)
- HTTP/2 or HTTP/3
```

## Interfaces
- FinOps Architect
- Capacity Architect
- Performance Skill

## Ver Também

- `34-capacity-planning-skill.md`
- `27-finops-architect`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
