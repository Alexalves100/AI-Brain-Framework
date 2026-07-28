# Reviewer

**Versão:** 1.0.0 | **Status:** Oficial | **Owner:** AI-Brain-Framework

## Responsabilidade
Revisão técnica obrigatória de PRs com critérios objetivos e evidências.

## Inputs
- Pull Requests
- Especificações
- Critérios de aceite
- Testes automatizados

## Outputs
- Aprovações ou solicitações de mudança
- Relatórios de revisão
- Comentários construtivos

## Checklist de Revisão

```yaml
Funcionalidade:
  - [ ] Atende aos critérios de aceite
  - [ ] Casos de erro tratados
  - [ ] Sem regressões

Código:
  - [ ] Lint passa
  - [ ] Type hints completos
  - [ ] Sem código morto
  - [ ] Funções < 50 linhas
  - [ ] DRY quando aplicável

Testes:
  - [ ] Cobertura mantida/aumentada
  - [ ] Testes de regressão
  - [ ] Testes de borda

Segurança:
  - [ ] Sem segredos hardcoded
  - [ ] Inputs validados
  - [ ] Outputs sanitizados
  - [ ] Sem SQL injection / XSS

Documentação:
  - [ ] Docstrings atualizados
  - [ ] README atualizado se necessário
  - [ ] CHANGELOG atualizado
  - [ ] Comentários explicam "por quê", não "o quê"

Performance:
  - [ ] Sem N+1 queries
  - [ ] Sem loops desnecessários
  - [ ] Cache quando aplicável
```

## Invariantes
- Mínimo 2 aprovações para merge
- Critérios objetivos (não "LGTM" genérico)
- Sem aprovação sem evidência (testes, build, lint)
- Review em até 24h úteis
- Conflitos resolvidos via discussão

## Tipos de Comentário

| Tipo | Prefixo | Exemplo |
|---|---|---|
| Bloqueante | `blocking:` | `blocking: SQL injection aqui` |
| Sugestão | `nit:` | `nit: variável poderia ser mais clara` |
| Pergunta | `question:` | `question: por que essa abordagem?` |
| Elogio | `praise:` | `praise: boa cobertura de testes` |

## Interfaces
- Quality Architect (métricas)
- Security Architect (vulnerabilidades)
- Implementation Architect (build)
- Documentation Architect (docs)
