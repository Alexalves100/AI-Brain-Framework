# Model Evaluation Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Avaliação sistemática de modelos de ML/IA: accuracy, bias, robustness.

## Princípios
- Métricas alinhadas ao negócio
- Testes em dados diversos
- Avaliação contínua
- Comparação com baseline

## Inputs
- Modelo treinado
- Dataset de teste
- Métricas definidas

## Outputs
- Relatório de avaliação
- Confusion matrix
- Métricas por segmento
- Recomendações

## Métricas Comuns

| Tipo | Métricas |
|---|---|
| Classificação | Accuracy, Precision, Recall, F1, AUC |
| Regressão | MAE, RMSE, R² |
| Ranking | NDCG, MAP, MRR |
| Geração | BLEU, ROUGE, perplexity |
| LLM | Human eval, GPT-4 as judge |

## Invariantes
- Dataset de teste separado
- Métricas por subgrupo (fairness)
- Baseline definido
- Avaliação antes de deploy
- Monitoring em produção

## Workflow

```
1. Separar dataset (train/val/test)
2. Definir métricas de sucesso
3. Avaliar modelo no test set
4. Analisar por subgrupo
5. Comparar com baseline
6. Documentar resultados
7. Aprovar ou iterar
```

## Interfaces
- ML Engineer
- AI Safety Architect
- Data Engineer
- Quality Architect

## Ver Também

- `42-prompt-engineering-skill.md`
- `33-ai-safety-architect`
- `44-data-pipeline-skill.md`
