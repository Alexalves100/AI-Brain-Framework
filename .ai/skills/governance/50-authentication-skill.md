# Authentication Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Governance

## Capacidade
Autenticação segura de usuários: senhas, tokens, MFA, SSO.

## Princípios
- Senhas com hash forte (bcrypt, argon2)
- Tokens opacos (não JWT puro)
- MFA para perfis críticos
- Session management seguro

## Inputs
- Credenciais (senha, token, biometric)
- MFA code (se aplicável)
- Contexto (IP, device)

## Outputs
- Session/token
- User info
- MFA challenge (se necessário)

## Métodos

| Método | Segurança | UX |
|---|---|---|
| Senha + bcrypt | Média | Boa |
| Senha + MFA | Alta | Média |
| Magic link | Média | Boa |
| OAuth/SSO | Alta | Boa |
| WebAuthn/FIDO2 | Muito alta | Excelente |
| Biometria | Alta | Excelente |

## Invariantes
- Senhas NUNCA em plain text
- Hash com salt único
- Rate limit em tentativas (5/15min)
- MFA para perfis críticos
- Session timeout definido
- Logout invalida tokens

## Workflow

```
1. Credenciais recebidas
2. Validação (hash compare)
3. Se MFA habilitado:
   → Challenge MFA
   → Validação código
4. Se OK:
   → Gerar session/token
   → Persistir (se stateful)
   → Retornar
```

## Interfaces
- Security Architect
- Privacy Architect
- API Skill
- Rate Limiting Skill

## Ver Também

- `09-security-skill.md`
- `51-authorization-skill.md`
- `30-rate-limiting-skill.md`
