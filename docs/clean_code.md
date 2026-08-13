# Clean Code Engine & Guardrails de Engenharia Sênior

O **AI-Brain-Framework** inclui uma suíte nativa de **Clean Code, Guardrails Arquiteturais e Self-Healing Loop** inspirada nas melhores práticas dos 5 maiores projetos open-source do ecossistema de IA (Aider, Awesome-Cursorrules, Sourcery, OpenHands e Ruff), com **zero dependências externas (Python 3.8+ puro)**.

---

## 🎯 Objetivo

Garantir que a IA gere código legível, modular e de fácil entendimento, sem "código sujo", sem escadinhas de `if/else`, com 100% de tipagem estrita e arquitetura defensiva.

---

## 🛡️ As 8 Regras de Ouro (Senior Guardrails)

| Regra | Código | Descrição |
| :--- | :---: | :--- |
| **Single Responsibility (SRP)** | `SRP-001` | Funções com no máximo 30 linhas focadas em apenas uma tarefa. |
| **Guard Clauses / Early Return** | `GUARD-002` | Proíbe aninhamento profundo (`depth > 2`). Erros e edge cases retornam primeiro. |
| **Strict Type Annotations** | `TYPE-003` | 100% dos parâmetros e retornos devem possuir Type Hints. |
| **Defensive Error Handling** | `ERR-004` | Proíbe `except:` genérico e `pass` silencioso. Exige exceções tipadas. |
| **Parameter Limit (Value Objects)** | `PARAM-005` | Máximo de 4 parâmetros por função (acima disso, usar Dataclasses). |
| **Anti-Lazy Code** | `LAZY-006` | Proíbe placeholders como `# TODO implementar depois` ou funções vazias. |
| **No Redundant Else** | `ELSE-007` | Elimina blocos `else` desnecessários após `return` ou `raise`. |
| **Self-Documenting Naming** | `NAME-008` | Nomes autoexplicativos sem abreviações obscuras. |

---

## 🔄 Self-Healing Loop (Auto-Refatoração)

Se a IA gerar um código com nota menor que **90/100** ou com anti-patterns críticos, a `CleanCodeEngine` gera automaticamente uma instrução de refatoração cirúrgica:

```
┌─────────────────────────────────────────────────────────────┐
│                    SELF-HEALING LOOP                        │
├─────────────────────────────────────────────────────────────┤
│ 1. IA gera ou analisa código                                │
│ 2. CodeSmellDetector (AST) avalia a pontuação (0-100)       │
│ 3. Se Score < 90:                                           │
│    ➜ Gera diagnóstico cirúrgico com linha e regra violada   │
│    ➜ Força a IA a refatorar para o padrão Sênior            │
│ 4. Código final é entregue 100% limpo e testado             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Como Utilizar

### 1. Auditoria de Código & Detecção de Code Smells
```python
from framework.engines import CleanCodeEngine
from framework.core import Context

engine = CleanCodeEngine()
ctx = Context()
ctx.set("code", """
def process(a, b, c, d, e):
    if a:
        if b:
            return 1
    return 0
""")

result = engine.run(ctx)
print("Score:", result.output["score"]) # Ex: 68/100
print("Smells detectados:", result.output["smells"])
print("Instrução de Refatoração:", result.output["refactor_instruction"])
```

### 2. Injetando Guardrails Sênior no `PromptBuilder`
```python
from framework.prompts import PromptBuilder

prompt = (
    PromptBuilder()
    .add_role("Senior Staff Backend Engineer")
    .add_senior_guardrails()  # Injeta as 8 regras automaticamente
    .add_task("Criar serviço de conciliação financeira")
    .build()
)
```

---

## 🧪 Validação
- **Testes Unitários:** [`tests/test_code_smells.py`](../tests/test_code_smells.py), [`tests/test_senior_guidelines.py`](../tests/test_senior_guidelines.py) e [`tests/test_clean_code_engine.py`](../tests/test_clean_code_engine.py).
- **128 testes passando com 100% de sucesso.**
