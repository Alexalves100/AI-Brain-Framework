# Search Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Implementação de busca eficiente: full-text, fuzzy, faceted.

## Princípios
- Indexação otimizada
- Busca rápida (< 100ms p95)
- Ranking relevante
- Suporte a múltiplos idiomas

## Inputs
- Query do usuário
- Filtros
- Ordenação

## Outputs
- Resultados rankeados
- Total de matches
- Facets para filtros

## Ferramentas

| Ferramenta | Tipo | Uso |
|---|---|---|
| Elasticsearch | Full-text + analytics | Apps complexos |
| Algolia | SaaS, fast | Frontend |
| Meilisearch | Self-hosted, fast | Alternativa ao ES |
| Typesense | Self-hosted, typo-tolerant | Alternativa ao Algolia |
| PostgreSQL FTS | Full-text simples | Apps simples |
| SQLite FTS5 | Full-text local | Apps pequenos |

## Invariantes
- Latência p95 < 200ms
- Suporte a typos (fuzzy match)
- Highlighting de matches
- Paginação eficiente
- Monitoring de queries lentas

## Workflow

```
1. User input → normalização
2. Query → search engine
3. Ranking (BM25, TF-IDF, ML)
4. Filtros aplicados
5. Paginação
6. Retorno com highlighting
```

## Ver Também

- `15-api-skill.md`
- `16-performance-skill.md`
- `14-database-skill.md`

## Interfaces
- API Skill
- Performance Skill
- Database Skill
- UX Researcher
