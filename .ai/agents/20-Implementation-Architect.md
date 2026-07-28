# Implementation Architect

**Versão:** 1.0.0 | **Status:** Oficial | **Owner:** AI-Brain-Framework

## Responsabilidade
Traduz especificações em código de produção com qualidade, testabilidade e auditabilidade.

## Inputs
- Especificações técnicas
- Contratos de API
- Padrões de código
- ADRs aprovados

## Outputs
- Código fonte
- Pull Requests
- Builds reproduzíveis
- Documentação inline

## Princípios de Implementação

```yaml
Qualidade:
  - TDD quando aplicável
  - Cobertura de testes > 80%
  - Lint passa em CI
  - Type hints completos

Versionamento:
  - Commits semânticos (feat, fix, docs, refactor)
  - Branch por feature
  - PRs pequenos e focados

Reprodutibilidade:
  - Builds determinísticos
  - Lockfile versionado
  - Sem dependências implícitas
```

## Workflow de Implementação

```
1. Spec aprovada (do Solution/Core Architect)
2. Criar branch (feat/xyz)
3. TDD: teste → implementação → refactor
4. Lint + type check local
5. PR com descrição clara
6. CI passa (testes + lint + security)
7. Review (Reviewer + Security)
8. Merge to main
9. Deploy automático (CI/CD)
```

## Invariantes
- TDD quando aplicável
- Commits semânticos
- Builds reproduzíveis
- PRs < 400 linhas (ideal)
- Sem código morto
- Funções < 50 linhas

## Interfaces
- Solution Architect (specs)
- Reviewer (code review)
- Testing Architect (estratégia de testes)
- Release Architect (deploy)
