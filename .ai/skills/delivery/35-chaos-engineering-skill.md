# Chaos Engineering Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Testes de resiliência via injeção controlada de falhas.

## Princípios
- Start small
- Automatize experimentos
- Minimize blast radius
- Aprenda com cada experimento

## Inputs
- Hipótese de resiliência
- Sistema alvo
- Tipo de falha

## Outputs
- Experimentos executados
- Resultados observados
- Melhorias identificadas

## Tipos de Falhas

```python
# Latência
- Adicionar delay em chamadas
- Timeout forçado

# Erros
- Exceções aleatórias
- Status codes específicos (500, 503)

# Recursos
- CPU exhaustion
- Memory exhaustion
- Disk full

# Network
- Packet loss
- DNS failures
- Connection drops

# Dependências
- Service down
- Database unreachable
- Cache miss
```

## Workflow

```
1. HYPOTHESIS: "Sistema X tolera falha Y"
2. BASELINE: Medir comportamento normal
3. EXPERIMENT: Injetar falha Y
4. OBSERVE: Medir comportamento
5. ANALYZE: Comparar com baseline
6. IMPROVE: Aplicar fixes
7. REPEAT
```

## Invariantes
- Ambiente de staging primeiro
- Blast radius limitado
- Rollback automático disponível
- Monitoramento durante experimento
- Comunicação com stakeholders

## Interfaces
- SRE Architect
- Reliability testing
- Observability Skill
