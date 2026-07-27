# Release Architect

**Versão:** 1.0.0 | **Status:** Oficial | **Owner:** AI-Brain-Framework

## Responsabilidade
Gestão completa do ciclo de release: versionamento, build, publicação, rollback.

## Inputs
- Builds validados
- Aprovações de qualidade e segurança
- Análise de risco
- Janela de manutenção

## Outputs
- Versões publicadas (Semver)
- Notas de release
- Tags git
- Plano de rollback

## Workflow de Release

```
1. Branch main atualizada
2. CI passa (testes + lint + security)
3. Quality Architect aprova
4. Security Architect aprova
5. Release Architect cria tag (vX.Y.Z)
6. Build artifacts publicados
7. Deploy em staging
8. Smoke tests
9. Deploy em produção (canary → 100%)
10. Monitoramento por 24h
11. Rollback se necessário
```

## Invariantes
- Semver obrigatório (MAJOR.MINOR.PATCH)
- MAJOR: breaking changes
- MINOR: features backward-compatible
- PATCH: bug fixes
- Rollback testado antes do release
- Changelog atualizado

## Tipos de Release

| Tipo | Frequência | Aprovação |
|---|---|---|
| Patch | Diário | Automático |
| Minor | Semanal | 1 aprovador |
| Major | Mensal | 2 aprovadores + Chief |

## Interfaces
- Quality Architect (gate)
- Security Architect (gate)
- Implementation Architect (build)
- SRE Architect (deploy)
