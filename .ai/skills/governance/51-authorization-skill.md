# Authorization Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Governance

## Capacidade
Controle de acesso: RBAC, ABAC, policies.

## Princípios
- Princípio do menor privilégio
- Default deny
- Separação de concerns
- Audit trail completo

## Inputs
- User identity
- Resource
- Action
- Context (tenant, time, IP)

## Outputs
- Permitido/Negado
- Razão da decisão
- Audit log

## Modelos

| Modelo | Quando | Complexidade |
|---|---|---|
| RBAC | Roles fixas | Baixa |
| ABAC | Atributos dinâmicos | Média |
| ReBAC | Relacionamentos | Média |
| PBAC | Policies complexas | Alta |

## Implementação

```python
# RBAC simples
if user.role == "admin":
    return ALLOW

# ABAC com contexto
if (user.tenant_id == resource.tenant_id
    and user.has_permission("read")
    and time.now() within resource.access_window):
    return ALLOW

# Policy-based (OPA, Casbin)
policy.evaluate({
    "user": user,
    "resource": resource,
    "action": "read",
    "context": ctx,
})
```

## Invariantes
- Default deny (tudo bloqueado por padrão)
- Audit log de toda decisão
- Separação de authn e authz
- Testes de bypass (negative tests)
- Documentação de policies

## Ver Também

- `50-authentication-skill.md`
- `09-security-skill.md`
- `39-multi-tenancy-skill.md`
- Documentação de policies

## Interfaces
- Security Architect
- Privacy Architect
- Multi-Tenancy Skill
- Audit Log
