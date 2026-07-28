# Security Report

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

## Ver Também

- `24-security-auditor.md`
- `22-secure-dev-framework.md`

## Histórico

- 1.0.0 (2026-07-27): Criação inicial
