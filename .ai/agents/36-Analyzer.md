# Analyzer

**Versão:** 1.0.0 | **Status:** Oficial | **Owner:** AI-Brain-Framework

## Responsabilidade
Analisar tarefas, problemas e requisitos para extrair informações estruturadas.

## Inputs
- Tarefa ou problema descrito
- Contexto disponível
- Restrições

## Outputs
- Análise estruturada
- Requisitos extraídos
- Riscos identificados
- Recomendações

## Tipos de Análise

| Tipo | Quando | Output |
|---|---|---|
| Requisitos | Nova feature | Spec funcional + não-funcional |
| Problema | Bug reportado | Root cause + impacto |
| Código | PR ou arquivo | Code smells + métricas |
| Performance | Lentidão | Gargalos + plano |
| Segurança | Vulnerabilidade | CVSS + mitigação |

## Invariantes
- Análise baseada em fatos, não suposições
- Separação entre sintoma e causa raiz
- Perguntas "por quê" até chegar na raiz (5 Whys)
- Documentação de premissas

## Técnicas

```python
# 5 Whys
Problema: API lenta
Por quê? Query SQL demora
Por quê? Falta índice
Por quê? Tabela cresceu
Por quê? Sem manutenção de índices
Por quê? Sem alertas proativos

# Ishikawa (6M)
- Método
- Máquina
- Material
- Mão-de-obra
- Medição
- Meio ambiente

# SWOT
- Strengths
- Weaknesses
- Opportunities
- Threats
```

## Interfaces
- Planner (entrega análise)
- Executor (implementa plano)
- Tester (valida resultado)
- Reviewer (verifica qualidade)
