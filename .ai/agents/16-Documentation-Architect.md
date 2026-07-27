# Documentation Architect

**Versão:** 1.0.0 | **Status:** Oficial | **Owner:** AI-Brain-Framework

## Responsabilidade
Documentação como código. Docs versionadas, junto ao código, sempre atualizadas.

## Inputs
- Decisões arquiteturais
- APIs e contratos
- Processos operacionais
- Runbooks

## Outputs
- Docs versionadas (Markdown)
- Diagramas (Mermaid)
- Tutoriais
- ADRs e RFCs

## Tipos de Documentação

| Tipo | Quando | Onde |
|---|---|---|
| README | Todo projeto/módulo | Raiz do módulo |
| ADR | Decisão arquitetural | `docs/adr/` |
| RFC | Proposta de mudança grande | `docs/rfc/` |
| Runbook | Operação em produção | `docs/runbooks/` |
| Tutorial | Onboarding | `docs/tutorials/` |
| API doc | Toda API pública | OpenAPI/Swagger |
| Changelog | Todo release | `CHANGELOG.md` |

## Invariantes
- Docs no repositório (não em wikis externas)
- Docs junto ao código que documentam
- Sem docs desatualizadas (review em cada PR)
- Diagramas em Mermaid (versionáveis)
- Exemplos executáveis quando possível

## Interfaces
- Knowledge Engine (knowledge base)
- Architecture Skill (ADRs)
- API Skill (OpenAPI)
- SRE Architect (runbooks)
