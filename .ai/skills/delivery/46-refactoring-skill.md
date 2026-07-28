# Refactoring Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Refatoração segura e incremental de código existente.

## Princípios
- Comportamento preservado (refactor ≠ rewrite)
- Testes antes de refatorar
- Pequenas mudanças frequentes
- Commits atômicos

## Inputs
- Código a refatorar
- Code smells identificados
- Testes existentes

## Outputs
- Código melhorado
- Testes ainda passando
- Métricas melhoradas

## Code Smells Comuns

| Smell | Refatoração |
|---|---|
| Long Method | Extract Method |
| Long Class | Extract Class |
| Duplicated Code | Extract Method/Class |
| Large Parameter List | Parameter Object |
| Feature Envy | Move Method |
| Data Clumps | Extract Class |
| Primitive Obsession | Value Object |
| Switch Statements | Polymorphism |
| Refused Bequest | Replace Inheritance |
| Comments | Better Naming |

## Workflow (Fowler)

```
1. Identificar code smell
2. Escrever teste que falha (se necessário)
3. Aplicar refatoração pequena
4. Rodar testes
5. Commit
6. Repetir
```

## Invariantes
- Comportamento externo preservado
- Testes passam antes e depois
- Commits atômicos
- Sem mudança de funcionalidade
- Code review obrigatório

## Interfaces
- Implementation Architect
- Testing Architect
- Reviewer
- Quality Architect

## Ver Também

- `18-implementation-skill.md`
- `11-quality-skill.md`
- `12-review-skill.md`
