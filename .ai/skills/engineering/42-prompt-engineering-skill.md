# Prompt Engineering Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Otimização de prompts para LLMs: clareza, contexto, few-shot, chain-of-thought.

## Princípios
- Instruções claras e específicas
- Contexto suficiente
- Exemplos (few-shot) quando útil
- Formato de saída definido

## Inputs
- Tarefa do LLM
- Contexto necessário
- Restrições

## Outputs
- Prompt otimizado
- Versões A/B para teste
- Métricas de qualidade

## Técnicas

```python
# Zero-shot
"Classifique o sentimento deste texto: {texto}"

# Few-shot
"Classifique o sentimento:
- 'Adoro este produto' → positivo
- 'Odiei este produto' → negativo
- '{texto}' →"

# Chain-of-thought
"Pense passo a passo:
1. Identifique os atores
2. Liste os conflitos
3. Proponha soluções
Conclusão:"

# Role prompting
"Você é um especialista em segurança. Analise:"

# Output format
"Responda em JSON: {schema}"
```

## Invariantes
- Prompt versionado em git
- A/B testing de variações
- Métricas de qualidade definidas
- Sem alucinações (grounding)
- Custo de tokens monitorado

## Interfaces
- AI Safety Architect
- ML Engineer
- Token Economy Skill

## Ver Também

- `08-token-economy-skill.md`
- `23-token-efficient-coder.md`
- `43-model-evaluation-skill.md`
