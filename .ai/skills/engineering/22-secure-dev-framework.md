# Secure Dev Framework

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
