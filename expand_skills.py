"""
AI-Brain-Framework — Expansão das 4 Skills Prioritárias
Version: 1.0.0
"""

from pathlib import Path

ROOT = Path("d:/PROJETOS/WEB/AI-Brain-Framework")

SECURE_DEV = """# Secure Dev Framework

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Framework principal — ativa todas as skills de segurança em conjunto.

## Skills Ativadas
- `security-auditor` (análise)
- `security-report` (relatório)
- `token-efficient-coder` (resposta)
- `09-security-skill` (segurança)
- `10-privacy-skill` (privacidade)
- `11-quality-skill` (qualidade)
- `12-review-skill` (revisão)

## Inputs
- Código fonte completo
- Configurações (env, nginx, docker)
- Arquitetura (diagramas, ADRs)
- Dependências (package.json, requirements.txt)

## Outputs
- Análise integrada
- Relatórios consolidados
- Gates de segurança
- Plano de remediação

## Fluxo de Execução
```
1. Receber código/config
2. security-auditor → findings
3. privacy-skill → DPIA
4. quality-skill → métricas
5. review-skill → aprovação
6. security-report → documento final
7. token-efficient-coder → resposta objetiva
```

## Invariantes
- Ativação simultânea
- Sem conflito entre skills
- Rastreabilidade total
- Zero trust aplicado
- Findings ordenados por severidade

## Checklist Integrado
```
[ ] CSRF tokens
[ ] Cookies seguros
[ ] Headers de segurança
[ ] XSS prevenido
[ ] SQLi prevenido
[ ] Vazamento de dados
[ ] Mobile security
[ ] LGPD compliance
[ ] Cobertura de testes
[ ] Lint passa
[ ] Review aprovado
```

## Interfaces
- Todas as skills de segurança
- Security Architect
- Release Architect
- Quality Architect
"""

TOKEN_CODER = """# Token Efficient Coder

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Economia máxima de tokens + respostas 100% objetivas (sem contextualização).

## Princípios
- Resposta direta
- Sem introdução
- Sem despedida
- Sem repetição
- Reuso de docs existentes
- Bullet points quando possível
- Código sem comentários óbvios

## Inputs
- Tarefa
- Contexto mínimo
- Restrições

## Outputs
- Código compacto
- Resposta objetiva
- Sem verbosidade

## Formato de Resposta
```
[STATUS]
- Ação executada

[RESULTADO]
- Output direto

[VALIDAÇÃO]
- Evidência objetiva
```

## Invariantes
- Zero contextualização desnecessária
- Respostas em formato mínimo viável
- Cada token é auditado
- Sem explicações redundantes
- Sem exemplos não essenciais
- Sem recapitulação do pedido

## Padrões de Compressão

### Código
- Remover comentários óbvios
- Nomes curtos quando escopo claro
- Inline quando possível
- Sem linhas em branco desnecessárias

### Texto
- Bullet points > parágrafos
- Tabelas > listas longas
- Sem introduções ("Vou explicar...")
- Sem conclusões ("Espero ter ajudado...")

## Anti-Patterns
- ❌ "Claro, vou ajudar com isso!"
- ❌ "Primeiro, vamos entender..."
- ❌ "Espero que isso seja útil"
- ❌ "Se precisar de mais ajuda..."
- ❌ Explicar o que vai fazer antes de fazer

## Interfaces
- Todas as skills
- Context Engine
"""

SECURITY_AUDITOR = """# Security Auditor

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
"""

SECURITY_REPORT = """# Security Report

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Geração de relatórios profissionais de segurança.

## Inputs
- Findings do `security-auditor`
- Contexto do projeto
- Audiência (executiva/técnica)

## Outputs
- Relatório executivo
- Relatório técnico
- Plano de remediação
- Métricas de risco

## Estrutura do Relatório

### 1. Resumo Executivo
```
- Score de risco: [0-100]
- Findings críticos: [N]
- Findings altos: [N]
- Findings médios: [N]
- Findings baixos: [N]
- Status geral: [Crítico/Alto/Médio/Baixo]
- Recomendação: [Bloquear/Aprovar com ressalvas/Aprovar]
```

### 2. Escopo
```
- Sistemas analisados: [...]
- Período: [data início - data fim]
- Metodologia: [OWASP/NIST/Interna]
- Ferramentas: [...]
- Limitações: [...]
```

### 3. Findings
```
### [ID-001] [Título]
- **Severidade**: Critical/High/Medium/Low
- **CVSS**: [score]
- **CWE**: [ID]
- **OWASP**: [categoria]
- **Descrição**: [técnica]
- **Evidência**: [PoC/print/log]
- **Impacto**: [negócio + técnico]
- **Recomendação**: [mitigação]
- **Referências**: [links]
```

### 4. Plano de Remediação
```
| ID | Severidade | Ação | Esforço | Responsável | Prazo |
|----|------------|------|---------|-------------|-------|
| 001 | Critical | [ação] | [h/d] | [nome] | [data] |
| 002 | High | [ação] | [h/d] | [nome] | [data] |
```

### 5. Anexos
- PoCs completos
- Logs de exploração
- Screenshots
- Referências externas

## Invariantes
- Linguagem objetiva
- Evidências anexadas
- Reproduzibilidade
- Sem omissão de findings críticos
- Sem minimização de riscos

## Formatos Suportados
- Markdown (default)
- HTML
- PDF
- JSON (machine-readable)

## Template Executivo (1 página)
```
# Relatório de Segurança — [Projeto]

**Data**: [YYYY-MM-DD]
**Versão**: [X.Y.Z]
**Auditor**: [nome/skill]

## Score: [X/100]

## Findings
- 🔴 Critical: [N]
- 🟠 High: [N]
- 🟡 Medium: [N]
- 🟢 Low: [N]

## Top 3 Riscos
1. [título + impacto]
2. [título + impacto]
3. [título + impacto]

## Recomendação
[Aprovar/Bloquear/Aprovar com ressalvas]

## Próximos Passos
1. [ação 1]
2. [ação 2]
3. [ação 3]
```

## Interfaces
- `security-auditor` (recebe findings)
- `secure-dev-framework` (orquestra)
- Security Architect
- Release Architect
- Stakeholders
"""

def write(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

if __name__ == "__main__":
    base = ROOT / ".ai" / "skills" / "engineering"
    write(base / "22-secure-dev-framework.md", SECURE_DEV)
    write(base / "23-token-efficient-coder.md", TOKEN_CODER)
    write(base / "24-security-auditor.md", SECURITY_AUDITOR)
    write(base / "25-security-report.md", SECURITY_REPORT)
    print("4 skills prioritárias expandidas.")
