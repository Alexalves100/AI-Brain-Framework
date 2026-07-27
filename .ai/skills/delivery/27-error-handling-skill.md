# Error Handling Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Tratamento estruturado de erros com classificação, logging e recovery.

## Princípios
- Fail fast
- Erros explícitos
- Logging contextual
- Recovery automático quando possível

## Inputs
- Exceções
- Contexto de execução
- Criticidade

## Outputs
- Erro classificado
- Log estruturado
- Ação de recovery (se aplicável)

## Invariantes
- Nunca swallow exceptions
- Stack trace apenas em logs
- Mensagens genéricas para usuário
- Métricas de erro expostas

## Classificação

```python
class ErrorSeverity:
    CRITICAL = "critical"   # Sistema down
    HIGH = "high"           # Feature quebrada
    MEDIUM = "medium"       # Degradação
    LOW = "low"             # Cosmético
```

## Interfaces
- Logging Skill
- Observability Skill
- SRE Architect
