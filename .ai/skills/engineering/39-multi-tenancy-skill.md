# Multi-Tenancy Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Arquitetura SaaS multi-tenant com isolamento de dados.

## Princípios
- Isolamento por tenant (company_id)
- Row Level Security no banco
- UUIDs não-sequenciais
- Testes de cross-tenant

## Inputs
- Modelo de tenancy (silo, pool, hybrid)
- Requisitos de compliance
- Volume de tenants

## Outputs
- Schema com company_id
- Políticas RLS
- Middleware de tenant context
- Testes de isolamento

## Modelos de Tenancy

| Modelo | Isolamento | Custo | Uso |
|---|---|---|---|
| Silo | DB por tenant | Alto | Enterprise, compliance |
| Pool | Schema por tenant | Médio | Mid-market |
| Hybrid | Row-level | Baixo | SMB, startups |

## Invariantes
- Toda entidade tem tenant_id
- RLS habilitado em produção
- Testes de isolamento obrigatórios
- Super admin bypass explícito
- Auditoria de acessos cross-tenant

## Workflow

```
1. Identificar tenant (JWT, subdomain, header)
2. Setar contexto (SET app.current_tenant_id)
3. RLS filtra automaticamente
4. Validar em testes
5. Auditar tentativas de cross-tenant
```

## Interfaces
- Database Architect
- Security Architect
- API Architect
- Privacy Architect (LGPD)

## Ver Também

- `14-database-skill.md`
- `09-security-skill.md`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
