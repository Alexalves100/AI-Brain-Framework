# API Versioning Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Versionamento de APIs com compatibilidade retroativa.

## Princípios
- Versionamento explícito na URL ou header
- Compatibilidade retroativa por 12 meses
- Deprecation policy clara
- Changelog de API

## Inputs
- Tipo de mudança (breaking, feature, fix)
- Audiência afetada
- Timeline de deprecation

## Outputs
- Versão de API
- Changelog
- Sunset date
- Migration guide

## Estratégias de Versionamento

| Estratégia | Exemplo | Uso |
|---|---|---|
| URL Path | `/api/v1/users` | Mais comum, fácil de cache |
| Header | `Accept: application/vnd.api+json;version=2` | Mais flexível |
| Query Param | `/api/users?version=2` | Menos recomendado |

## Tipos de Mudança

| Tipo | Compatibilidade | Ação |
|---|---|---|
| Adicionar campo | Compatível | Minor version |
| Remover campo | Breaking | Major + deprecation |
| Mudar tipo | Breaking | Major + migration guide |
| Renomear endpoint | Breaking | Major + redirect |
| Bug fix | Compatível | Patch |

## Invariantes
- Major version suportada por 12 meses
- Sunset date anunciado 6 meses antes
- Changelog público
- Migration guide para breaking changes
- Versionamento no OpenAPI spec

## Workflow

```
1. Decidir tipo de mudança
2. Criar nova versão (se breaking)
3. Manter versão antiga por 12 meses
4. Anunciar deprecation (6 meses antes)
5. Sunset date
6. Remover versão antiga
```

## Interfaces
- API Architect
- Documentation Architect
- Product Manager (comunicação)
- Security Architect (deprecation segura)

## Ver Também

- `15-api-skill.md`
- `17-documentation-skill.md`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
