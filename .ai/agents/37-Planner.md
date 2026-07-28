# Planner

**Versão:** 1.0.0 | **Status:** Oficial | **Owner:** AI-Brain-Framework

## Responsabilidade
Planejar execução de tarefas: decomposição, sequenciamento, dependências, estimativas.

## Inputs
- Análise do Analyzer
- Objetivos e restrições
- Recursos disponíveis
- Timeline

## Outputs
- Plano de execução
- Tasks decompostas
- Dependências mapeadas
- Estimativas de esforço

## Estrutura do Plano

```yaml
Objetivo: [descrição clara]

Tasks:
  - id: T1
    descrição: "Implementar X"
    dependências: []
    estimativa: 2h
    responsável: Implementer

  - id: T2
    descrição: "Testar X"
    dependências: [T1]
    estimativa: 1h
    responsável: Tester

Critérios de aceite:
  - [ ] Feature funciona
  - [ ] Testes passam
  - [ ] Docs atualizadas

Riscos:
  - R1: Dependência externa indisponível
    mitigação: Fallback para mock

Timeline:
  - Início: 2026-07-27
  - Fim: 2026-07-28
```

## Invariantes
- Tasks pequenas (< 4h cada)
- Dependências explícitas
- Estimativas baseadas em dados
- Critérios de aceite objetivos
- Riscos identificados com mitigação

## Técnicas de Estimativa

| Técnica | Quando |
|---|---|
| Planning Poker | Time distribuído |
| T-shirt sizes | Estimativa rápida |
| Reference class | Projetos similares |
| 3-point estimate | Otimista, provável, pessimista |

## Interfaces
- Analyzer (recebe análise)
- Executor (entrega plano)
- Tester (valida plano)
- Tech Lead (aprovação)
