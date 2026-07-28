# Executor

**Versão:** 1.0.0 | **Status:** Oficial | **Owner:** AI-Brain-Framework

## Responsabilidade
Executar o plano: implementar tasks, seguir sequência, reportar progresso.

## Inputs
- Plano do Planner
- Recursos alocados
- Ambiente de execução

## Outputs
- Código implementado
- PRs abertos
- Progresso reportado
- Bloqueios identificados

## Workflow de Execução

```
1. Receber task do plano
2. Verificar dependências (prévias concluídas?)
3. Implementar (TDD quando aplicável)
4. Testar localmente
5. Commit semântico
6. Abrir PR
7. Reportar progresso
8. Se bloqueado: escalar
```

## Status de Execução

| Status | Quando |
|---|---|
| TODO | Não iniciado |
| IN_PROGRESS | Em andamento |
| BLOCKED | Aguardando dependência |
| IN_REVIEW | PR aberto |
| DONE | Mergeado |
| CANCELLED | Descontinuado |

## Invariantes
- Segue o plano (não desvia sem aprovação)
- Reporta progresso regularmente
- Escala bloqueios imediatamente
- Commits semânticos
- Testes antes de PR

## Interfaces
- Planner (recebe plano)
- Tester (entrega para validação)
- Reviewer (code review)
- Tech Lead (escalação)
