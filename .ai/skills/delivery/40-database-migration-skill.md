# Database Migration Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Migrações de banco de dados com zero downtime.

## Princípios
- Forward-only (sem rollback destrutivo)
- Backward-compatible
- Pequenas e frequentes
- Testadas em staging primeiro

## Inputs
- Mudança de schema
- Dados a migrar
- Janela de manutenção

## Outputs
- Migration script
- Rollback plan (se possível)
- Validação pré e pós

## Estratégias

| Mudança | Estratégia |
|---|---|
| Adicionar coluna | Direct (sem downtime) |
| Remover coluna | 2 fases: ignorar → remover |
| Renomear coluna | 2 fases: nova + sync → remover antiga |
| Mudar tipo | Nova coluna + backfill + switch |
| Adicionar índice | CONCURRENTLY (sem lock) |
| Particionar tabela | Shadow table + switch atômico |

## Invariantes
- Sem DROP COLUMN direto em produção
- Sem ALTER TABLE em tabelas grandes sem teste
- Backfill em batches
- Feature flag para mudanças destrutivas
- Backup antes de qualquer migração destrutiva

## Workflow

```
1. Spec da mudança
2. Migration script (forward-only)
3. Testes em staging
4. Backup em produção
5. Deploy em produção (pequenas janelas)
6. Validação pós-deploy
7. Cleanup após estabilização
```

## Interfaces
- Database Architect
- SRE Architect
- Quality Architect
- Release Architect

## Ver Também

- `14-database-skill.md`
- `20-release-skill.md`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
