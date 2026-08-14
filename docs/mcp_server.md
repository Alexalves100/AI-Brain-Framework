# 🔌 Servidor MCP Nativo (Model Context Protocol)

O **AI-Brain-Framework** inclui um servidor oficial **Model Context Protocol (MCP)** embutido e desenvolvido em **Python 3.8+ puro (zero dependências externas)**.

Ele permite conectar o framework diretamente a assistentes de IA e IDEs modernas como **Cursor, Claude Desktop, Windsurf, VS Code (Roo Code / Claude Dev / Continue)**, dando acesso a ferramentas avançadas de análise AST, redução de tokens, auditoria de Clean Code e segurança em tempo real.

---

## 🚀 Como Iniciar o Servidor MCP

### Via Linha de Comando (Terminal)

```bash
# Opção 1: Via módulo Python
python -m framework.mcp

# Opção 2: Via script de ferramentas
python tools/mcp_server.py

# Opção 3: Via CLI do framework (quando instalado via pip)
ai-brain-mcp
```

O servidor se comunica através de **Standard I/O (`stdio`)** utilizando o protocolo JSON-RPC 2.0.

---

## 🛠️ Configuração Prática nas IDEs e Assistentes

### 1. Cursor IDE

No seu projeto ou globalmente, adicione ou edite o arquivo `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "ai-brain": {
      "command": "python",
      "args": ["-m", "framework.mcp"],
      "cwd": "/caminho/absoluto/para/AI-Brain-Framework"
    }
  }
}
```

> **Dica no Windows:** Utilize barras duplas ou normais no caminho, por exemplo: `"C:/projects/AI-Brain-Framework"`.

---

### 2. Claude Desktop (Anthropic)

Abra o arquivo de configuração do Claude Desktop:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

Adicione a seção `mcpServers`:

```json
{
  "mcpServers": {
    "ai-brain": {
      "command": "python",
      "args": ["-m", "framework.mcp"],
      "cwd": "D:/projects/AI-Brain-Framework"
    }
  }
}
```

Reinicie o **Claude Desktop**. O ícone de martelo (🛠️) aparecerá no chat com todas as ferramentas disponíveis.

---

### 3. Windsurf IDE (Codeium)

No arquivo de configuração de MCP do Windsurf (`~/.codeium/windsurf/mcp_config.json`):

```json
{
  "mcpServers": {
    "ai-brain": {
      "command": "python",
      "args": ["-m", "framework.mcp"],
      "cwd": "D:/projects/AI-Brain-Framework"
    }
  }
}
```

---

### 4. VS Code (Extensões Roo Code / Continue)

Nas configurações da extensão (aba MCP Servers), adicione:

* **Name:** `ai-brain`
* **Transport Type:** `stdio`
* **Command:** `python`
* **Arguments:** `["-m", "framework.mcp"]`
* **Working Directory:** `/caminho/do/AI-Brain-Framework`

---

## 🧰 Ferramentas Expostas pelo Servidor MCP

| Ferramenta | Descrição | Parâmetros |
| :--- | :--- | :--- |
| **`clean_code_audit`** | Audita o código em relação a princípios SOLID, nesting profundo, funções longas e retorna a nota (0-100) com instruções de self-healing. | `code` (string), `file_path` (string opcional) |
| **`get_symbols_overview`** | Retorna o esqueleto estrutural AST (.pyi style) com classes, métodos e assinaturas de tipos, economizando 75%+ de tokens de contexto. | `code` (string), `file_path` (string opcional) |
| **`get_symbol_body`** | Extrai cirurgicamente o código-fonte integral de uma classe ou função específica (ex: `AuthService.login`). | `code` (string), `symbol_name` (string) |
| **`security_scan`** | Varre vulnerabilidades estáticas de segurança (SQL Injection, XSS, eval, segredos hardcoded). | `code` (string) |
| **`compress_tokens`** | Reduz o consumo de tokens através de compressão AST ou conversacional. | `text` (string), `mode` (string opcional) |
| **`analyze_complexity`** | Calcula métricas de complexidade ciclomática e cognitiva. | `code` (string) |
| **`list_symbols`** | Lista todas as classes e funções com suas respectivas linhas. | `code` (string) |

---

## 💡 Exemplos de Uso no Chat da IA (Cursor / Claude)

Depois de configurar o MCP, você pode interagir naturalmente com o modelo:

### Exemplo 1: Pedir visão geral de um módulo sem gastar tokens
> **Você:** *"IA, use o MCP get_symbols_overview no arquivo `auth.py` e me explique a estrutura dele."*
> **IA:** Executa a ferramenta e recebe o esqueleto em segundos, sem consumir a janela de contexto com o corpo das funções.

### Exemplo 2: Auditoria de Clean Code
> **Você:** *"Analise esta função de checkout usando clean_code_audit do AI-Brain."*
> **IA:** O MCP retorna a pontuação de 0 a 100, lista se há acoplamento ou falta de type hints e já retorna o plano de correção exato.

### Exemplo 3: Extração Cirúrgica de Função
> **Você:** *"Extraia apenas a função `validate_token` da classe `JWTAuth` com o get_symbol_body."*
> **IA:** Recebe exatamente o bloco de código solicitado sem alucinações.

---

## 🧪 Testando o Servidor Localmente via Terminal

Você pode enviar comandos JSON-RPC manualmente para validar a resposta do servidor:

```bash
# Teste de Inicialização MCP
python -c "
import subprocess, json
p = subprocess.Popen(['python', '-m', 'framework.mcp'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
req = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05'}}) + '\n'
out, _ = p.communicate(req)
print(out)
"
```
