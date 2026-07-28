# Secrets Management Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Governance

## Capacidade
Gestão segura de segredos: API keys, tokens, senhas, certificados.

## Princípios
- Segredos NUNCA em código
- Cifragem em repouso e em trânsito
- Rotação periódica
- Auditoria de acessos

## Inputs
- Tipo de segredo (API key, DB password, cert)
- Escopo (qual serviço usa)
- TTL desejado

## Outputs
- Segredo armazenado em vault
- Política de acesso
- Logs de auditoria

## Ferramentas Recomendadas

| Ferramenta | Uso |
|---|---|
| HashiCorp Vault | Multi-cloud, dynamic secrets |
| AWS Secrets Manager | AWS-native |
| GCP Secret Manager | GCP-native |
| Azure Key Vault | Azure-native |
| Doppler | Developer-friendly |

## Invariantes
- Segredos NUNCA em git
- Acesso auditado e logado
- Rotação automática
- Princípio do menor privilégio
- Cifragem em repouso (AES-256)

## Workflow

```
1. Criar segredo no vault
2. Definir política de acesso (quem pode ler)
3. Aplicação busca via SDK/CLI
4. Cache em memória (não disco)
5. Rotação automática (90 dias)
6. Auditoria contínua
```

## Interfaces
- Security Architect
- DevOps/Platform Engineer
- Compliance/LGPD

## Ver Também

- `09-security-skill.md`
- `11-security-architect`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
