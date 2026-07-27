# Security Auditor

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Análise de segurança de alto nível (CSRF, cookies, headers, XSS, SQLi, vazamento de dados, mobile, etc.).

## Vetores Analisados

### Web
- CSRF (Cross-Site Request Forgery)
- Cookies (Secure, HttpOnly, SameSite)
- Headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- XSS (Reflected, Stored, DOM-based)
- SSRF (Server-Side Request Forgery)
- Open Redirect
- CORS misconfiguration

### Backend
- SQLi (Union, Boolean, Time-based, Error-based)
- NoSQLi
- Command Injection
- Path Traversal
- XXE (XML External Entity)
- Deserialization

### Mobile
- Insecure storage
- Certificate pinning ausente
- Deep links maliciosos
- Backup inseguro
- Root/Jailbreak detection

### Dados
- Vazamento em logs
- Stack traces expostos
- Mensagens de erro verbosas
- PII em URLs
- Tokens em código

### Auth/Authz
- JWT mal configurado
- Session fixation
- IDOR (Insecure Direct Object Reference)
- BOLA (Broken Object Level Authorization)
- Privilege escalation
- Weak passwords

### Criptografia
- TLS < 1.2
- Hash sem salt
- MD5/SHA1
- Chaves hardcoded

## Inputs
- Código fonte
- Endpoints
- Configurações
- Dependências

## Outputs
- Findings categorizados (Critical/High/Medium/Low)
- CVSS scores
- Recomendações de mitigação
- Evidências (PoC)

## Checklist Completo
```
WEB
[ ] CSRF tokens validados
[ ] Cookies: Secure + HttpOnly + SameSite
[ ] CSP definido
[ ] HSTS habilitado
[ ] X-Frame-Options: DENY
[ ] X-Content-Type-Options: nosniff
[ ] Input sanitizado (whitelist)
[ ] Output encoded (context-aware)
[ ] CORS restritivo
[ ] Redirect validado

BACKEND
[ ] Queries parametrizadas
[ ] ORM seguro
[ ] Sem eval/exec
[ ] Path validado
[ ] XML parser seguro
[ ] Deserialization controlada

MOBILE
[ ] Keystore seguro
[ ] Certificate pinning
[ ] Deep links validados
[ ] Backup criptografado
[ ] Root detection

DADOS
[ ] Logs sem PII
[ ] Errors genéricos
[ ] PII criptografado
[ ] Tokens em vault
[ ] Retenção definida

AUTH
[ ] JWT com expiração
[ ] Refresh token rotation
[ ] MFA disponível
[ ] Session timeout
[ ] Password policy

AUTHZ
[ ] RBAC granular
[ ] IDOR prevenido
[ ] BOLA prevenido
[ ] Princípio do menor privilégio

CRIPTO
[ ] TLS 1.2+
[ ] Hash: bcrypt/argon2
[ ] Salt único por usuário
[ ] Chaves rotacionadas
```

## Invariantes
- Sem falso negativo crítico
- Evidência obrigatória
- Reproduzibilidade
- OWASP Top 10 coberto
- CVSS calculado

## Severidade
- **Critical**: exploração trivial, impacto total
- **High**: exploração média, impacto alto
- **Medium**: exploração difícil, impacto médio
- **Low**: exploração complexa, impacto baixo

## Interfaces
- `security-report` (gera relatório)
- `secure-dev-framework` (orquestra)
- Security Architect
