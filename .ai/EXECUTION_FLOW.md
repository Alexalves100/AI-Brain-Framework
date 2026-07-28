# AI-Brain-Framework — Fluxo de Execução

**Versão:** 1.0.0 | **Status:** Oficial

---

## Fluxo de Execução de uma Skill

```mermaid
flowchart TD
    A[Request chega] --> B{Autenticação válida?}
    B -->|Não| C[401 Unauthorized]
    B -->|Sim| D{Rate limit OK?}
    D -->|Não| E[429 Too Many Requests]
    D -->|Sim| F[Orchestrator.run]
    F --> G[Skill Registry lookup]
    G --> H{Skill encontrada?}
    H -->|Não| I[ERROR: skill not found]
    H -->|Sim| J[Validate inputs]
    J -->|Inválido| K[ERROR: invalid inputs]
    J -->|Válido| L[Skill.run]
    L --> M[Processa contexto]
    M --> N[Retorna SkillResult]
    N --> O{Status?}
    O -->|SUCCESS| P[Output + metadata]
    O -->|ERROR| Q[Error message]
    O -->|SKIPPED| R[Skip reason]
    P --> S[Metrics.record]
    Q --> S
    R --> S
    S --> T[Audit log]
    T --> U[Response ao cliente]
```

## Fluxo de Pipeline

```mermaid
flowchart LR
    A[Pipeline start] --> B[Skill 1]
    B --> C{Status?}
    C -->|ERROR| D[Stop pipeline]
    C -->|SUCCESS| E[Skill 2]
    E --> F{Status?}
    F -->|ERROR| D
    F -->|SUCCESS| G[Skill N]
    G --> H{Status?}
    H -->|ERROR| D
    H -->|SUCCESS| I[All results]
    D --> J[Partial results + error]
    I --> K[Aggregate output]
    J --> K
    K --> L[Return]
```

## Fluxo de Decisão por Domínio

```mermaid
flowchart TD
    Start[Nova tarefa] --> Q1{Tipo?}
    Q1 -->|UI| UI[UI Design Skill]
    Q1 -->|Segurança| SEC[Security Skill]
    Q1 -->|Performance| PERF[Performance Skill]
    Q1 -->|Dados| DATA[Knowledge/Memory]
    Q1 -->|Deploy| DEP[Release Skill]
    Q1 -->|Bug| BUG[Error Handling + Incident]

    UI --> R[Resultado]
    SEC --> R
    PERF --> R
    DATA --> R
    DEP --> R
    BUG --> R
```

## Fluxo de Release

```mermaid
flowchart LR
    A[Code commit] --> B[CI: tests]
    B --> C[CI: lint]
    C --> D[CI: security]
    D --> E{Quality gate}
    E -->|Fail| F[Block merge]
    E -->|Pass| G[Reviewer 1]
    G --> H[Reviewer 2]
    H --> I{2 approvals?}
    I -->|Não| J[Request changes]
    I -->|Sim| K[Merge to main]
    K --> L[Deploy staging]
    L --> M[Smoke tests]
    M --> N{OK?}
    N -->|Não| O[Rollback]
    N -->|Sim| P[Deploy prod canary]
    P --> Q[Deploy prod 100%]
    Q --> R[Monitor 24h]
```

## Fluxo de Incident Response

```mermaid
flowchart TD
    A[Alert/Report] --> B[Sev classification]
    B --> C{Sev1?}
    C -->|Sim| D[Page on-call]
    C -->|Não| E[Sev2-4: ticket]
    D --> F[ACK < 15min]
    F --> G[Assess impact]
    G --> H[Mitigate]
    H --> I[Communicate]
    I --> J[Resolve root cause]
    J --> K[Postmortem < 5 days]
    K --> L[Action items]
    L --> M[Track to closure]
```

---

## Tabela de Decisão Rápida

| Se você precisa de... | Use a skill... |
|---|---|
| Roteamento inteligente | `brain` |
| Persistir conhecimento | `knowledge` |
| Estado entre sessões | `memory` |
| Raciocínio explícito | `reasoning` |
| Descoberta de código | `discovery` |
| Compressão de texto | `token-economy` |
| Auditoria de segurança | `security-auditor` |
| Relatório de segurança | `security-report` |
| Validação de UI | `ui-design` |
| Tratamento de erro | `error-handling` |
| Logging estruturado | `logging` |
| Cache | `caching` |
| Observabilidade | `observability` |
| Otimização de custos | `cost-optimization` |
| Resposta a incidente | `incident-response` |
| Capacity planning | `capacity-planning` |
| Chaos engineering | `chaos-engineering` |
| Feature flags | `feature-flags` |
| Secrets | `secrets-management` |
| Background jobs | `background-jobs` |
| Multi-tenancy | `multi-tenancy` |
| DB migrations | `database-migration` |
| API versioning | `api-versioning` |
| Rate limiting | `rate-limiting` |
| Implementação | `implementation` |
| Testes | `testing` |
| Release | `release` |
| Governança | `governance` |

---

**Este documento é o guia visual de execução do framework.**
