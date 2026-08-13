# Otimização de Tokens & Inteligência de Símbolos AST (Estilo Serena MCP)

O **AI-Brain-Framework** inclui uma camada avançada de economia de contexto e tokens inspirada na arquitetura de ferramentas simbólicas do **Serena MCP**, operando com **zero dependências externas (Python 3.8+ puro)**.

---

## 🎯 Objetivo

Reduzir o consumo de contexto em até **90%** ao inspecionar código ou interagir com LLMs, eliminando a necessidade de ler arquivos inteiros sem perder tipos, assinaturas e contratos de interface.

---

## 📊 Tabela Comparativa de Benchmark: Antes vs. Depois

Testes realizados em arquivos reais do próprio repositório:

| Arquivo Testado | Tokens Originais (Arquivo Bruto) | Modo Antigo (Apenas Regex) | Modo Serena (AST Skeleton) | Tokens Economizados | Taxa de Economia (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`orchestrator.py`** | 710 tokens | 557 tokens | **175 tokens** | **535 tokens** | **75.4%** |
| **`code_scanner.py`** | 632 tokens | 487 tokens | **256 tokens** | **376 tokens** | **59.5%** |
| **`discovery.py`** | 1.122 tokens | 867 tokens | **245 tokens** | **877 tokens** | **78.2%** |
| **TOTAL ACUMULADO** | **2.464 tokens** | **1.911 tokens** | **676 tokens** | **1.788 tokens** | **72.6%** |

---

## 🧠 Como Funciona (Arquitetura em Camadas)

```
┌─────────────────────────────────────────────────────────────┐
│                 PROGRESSIVE CONTEXT DISCLOSURE              │
├──────────────────────────────┬──────────────────────────────┤
│ Nível 1: Skeletons (.pyi)    │ Nível 2: Símbolo Alvo        │
│ (Arquivos de Referência)     │ (Onde a IA vai editar)       │
│                              │                              │
│ ➜ 70% a 90% de economia      │ ➜ 100% Completo              │
│ ➜ Mantém classes, métodos,   │ ➜ Entrega cada linha interna │
│   types hints e docstrings   │   e comentários sem cortes   │
│ ➜ Substitui corpo por '...'  │ ➜ Zero risco de quebra       │
└──────────────────────────────┴──────────────────────────────┘
```

---

## 🚀 Como Utilizar

### 1. Geração de Skeleton AST (Modo `ast_skeleton`)
```python
from framework.engines import TokenEconomyEngine
from framework.core import Context

engine = TokenEconomyEngine()
ctx = Context()
ctx.set("code", open("framework/core/orchestrator.py").read())
ctx.set("mode", "ast_skeleton")

result = engine.run(ctx)
print(result.output["text"])
# Retorna apenas o esqueleto com assinaturas e types (economia de 75.4%)
```

### 2. Extração Cirúrgica de Símbolo Alvo (Modo `symbol_focus`)
```python
ctx = Context()
ctx.set("code", open("framework/core/orchestrator.py").read())
ctx.set("symbol", "Orchestrator.run_pipeline")

result = engine.run(ctx)
# Retorna o código-fonte integral apenas do método 'run_pipeline'
print(result.output["text"])
```

### 3. Listagem de Símbolos do Arquivo (Modo `symbols`)
```python
ctx = Context()
ctx.set("code", open("framework/core/orchestrator.py").read())
ctx.set("mode", "symbols")

result = engine.run(ctx)
# Retorna lista estruturada de classes, métodos, linhas de início e fim
print(result.output["symbols"])
```

### 4. Minificação de Código (Modo `minify`)
```python
ctx = Context()
ctx.set("code", "# Comentário\nx = 1\n\n\ny = 2")
ctx.set("mode", "minify")

result = engine.run(ctx)
# Remove comentários e linhas vazias redundantes preservando sintaxe
print(result.output["text"])
```

---

## 🛡️ Salvaguardas Anti-Alucinação

1. **Sintaxe Validada:** Todo esqueleto gerado é compilado via `ast.parse()` antes de ser entregue.
2. **Preservação de Tipagem:** Type hints (`Optional[Dict[str, Any]]`, `-> List[str]`, etc.) e decorators (`@property`, `@staticmethod`) são mantidos integralmente.
3. **Preservação de Docstrings:** A explicação funcional de métodos e classes é mantida.
4. **Isolamento de Alvo:** O código que a IA precisa editar nunca é truncado.
