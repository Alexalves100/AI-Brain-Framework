# 🩹 Motor de Aplicação Cirúrgica de Patches (SurgicalCodePatcher)

O **SurgicalCodePatcher** é o subsistema de edição cirúrgica e aplicação de alterações em código-fonte do **AI-Brain-Framework**.

Desenvolvido com base nos melhores padrões da indústria (*Aider, ast-grep, Cline/Roo Code e LibCST*), ele opera em **Python 3.8+ puro (zero dependências externas)** e elimina erros de *"Context mismatch"* com **Fuzzy Matching**, **Substituição Estrutural de Nós AST** e **Rollback Sintático Automático**.

---

## 🏛️ Modos e Estratégias de Patch

```
                      INSTRUÇÃO DE PATCH (IA / Desenvolvedor)
                                        │
                                        ▼
       ┌─────────────────────────────────────────────────────────────────┐
       │                   SURGICAL CODE PATCHER                         │
       ├─────────────────────────────────────────────────────────────────┤
       │ 1. Backup em Memória (Snapshot Transacional)                    │
       │ 2. Seleção de Estratégia:                                       │
       │    ├── [ast_node]        -> Substitui nó por símbolo exato      │
       │    ├── [search_replace]  -> Fuzzy Matcher com tolerância        │
       │    └── [unified_diff]    -> Aplica Hunks com ajuste de offset   │
       └────────────────────────────────┬────────────────────────────────┘
                                        │
                                        ▼
       ┌─────────────────────────────────────────────────────────────────┐
       │             3. VALIDADOR SINTÁTICO AUTOMÁTICO                   │
       ├─────────────────────────────────────────────────────────────────┤
       │ • Testa ast.parse(novo_codigo)                                  │
       │ • Código Válido? -> Salva no disco e retorna diff aplicado      │
       │ • SyntaxError?   -> Auto-Rollback imediato e retorna erro claro │
       └─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Como Usar no Python

### 1. Substituição Estrutural de Nó AST (Classe ou Método Específico)

Substitui um método inteiro informando apenas o caminho do símbolo (`AuthService.login`), sem risco de alterar ou corromper o restante do arquivo:

```python
from framework import SurgicalCodePatcher

patcher = SurgicalCodePatcher()

codigo_original = """class AuthService:
    def login(self, username, password):
        # Versao antiga simples
        return username == "admin" and password == "123"

    def logout(self, user_id):
        print("Logged out")
"""

novo_metodo = """    def login(self, username, password):
        # Nova versao segura
        import hmac
        return hmac.compare_digest(username, "admin") and hmac.compare_digest(password, "secret")"""

res = patcher.patch_string(
    source_code=codigo_original,
    patch_data=novo_metodo,
    strategy="ast_node",
    symbol_name="AuthService.login"
)

print(res.success)          # True
print(res.diff_summary)     # Mostra o diff unificado exato gerado
```

---

### 2. Blocos Search/Replace com Fuzzy Matching (Tolerância a Espaços)

Substitui trechos de código mesmo se houver pequenas divergências de indentação ou quebra de linha geradas pelo LLM:

```python
patch_aider = """<<<<<<< SEARCH
        return username == "admin" and password == "123"
=======
        import secrets
        return secrets.compare_digest(username, "admin")
>>>>>>> REPLACE"""

res = patcher.patch_string(
    source_code=codigo_original,
    patch_data=patch_aider,
    strategy="search_replace"
)

print(res.success)          # True
print(res.blocks_applied)   # 1
```

---

### 3. Validação Sintática Automática & Auto-Rollback

Se o LLM gerar um patch que quebra a sintaxe do Python (ex: dois pontos faltando ou indentação quebrada), o patcher rejeita a alteração e mantém o código 100% íntegro:

```python
patch_com_erro = """<<<<<<< SEARCH
        return username == "admin" and password == "123"
=======
        def invalid_syntax(:
            broken_indent
>>>>>>> REPLACE"""

res = patcher.patch_string(
    source_code=codigo_original,
    patch_data=patch_com_erro,
    strategy="search_replace"
)

print(res.success)       # False
print(res.syntax_valid)  # False
print(res.error)         # "SyntaxError in code after patch: ..."
# O arquivo original permanece intacto!
```

---

### 4. Aplicação Direta em Arquivos no Disco (`patch_file`)

```python
res = patcher.patch_file(
    file_path="services/auth.py",
    patch_data=patch_aider,
    dry_run=False # Defina dry_run=True para simular sem gravar no disco
)

if res.success:
    print("Arquivo atualizado com sucesso!")
```

---

## 🧰 Uso via Servidor MCP (Cursor & Claude Desktop)

O **SurgicalCodePatcher** está disponível como ferramenta nativa do Servidor MCP: **`apply_surgical_patch`**.

### Exemplo no Cursor ou Claude:
> **Você:** *"IA, use a ferramenta `apply_surgical_patch` para refatorar o método `AuthService.login` no arquivo `services/auth.py` utilizando comparação criptográfica segura."*
> **IA:** Dispara a ferramenta passando `file_path="services/auth.py"`, `symbol_name="AuthService.login"`, e o novo código. O patcher valida a sintaxe com `ast.parse()` e aplica a alteração no disco.
