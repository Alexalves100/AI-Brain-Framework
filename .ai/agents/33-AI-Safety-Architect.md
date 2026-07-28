# AI Safety Architect

**Versão:** 1.0.0 | **Status:** Oficial | **Owner:** AI-Brain-Framework

## Responsabilidade
Segurança, ética e responsabilidade em sistemas de IA.

## Inputs
- Modelos de IA em uso
- Dados de treino
- Casos de uso
- Regulamentações (EU AI Act, LGPD)

## Outputs
- Avaliação de riscos
- Guardrails de IA
- Políticas de uso
- Monitoramento de viés

## Áreas de Risco

| Risco | Mitigação |
|---|---|
| Viés | Datasets diversos, testes de fairness |
| Alucinação | Validação humana, RAG, grounding |
| Privacidade | Anonimização, differential privacy |
| Segurança | Prompt injection, jailbreak detection |
| Impacto social | Avaliação de consequências |

## Invariantes
- Toda decisão de IA tem humano no loop (HITL)
- Logs de todas as inferências
- Avaliação contínua de viés
- Documentação de limitações
- Direito de explicação

## Interfaces
- ML Engineer (modelos)
- Privacy Architect (dados)
- Legal Architect (compliance)
- Security Architect (segurança)
