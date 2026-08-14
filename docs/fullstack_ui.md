# 🎨 Fullstack UI Engine & Design System Premium

O **Fullstack UI Engine** é o subsistema de aceleração de desenvolvimento frontend de alto padrão (*Level Premium*) do **AI-Brain-Framework**.

Projetado com base nas referências globais do mercado (*shadcn/ui, Radix UI, Open Props, React Aria e axe-core*), ele opera em **Python 3.8+ puro (zero dependências externas)** e garante interfaces elegantes, táteis, fluidas e acessíveis, **eliminando qualquer estética de "site genérico feito por IA"**.

---

## 🏛️ Os 3 Pilares do Motor Frontend

```
                       FULLSTACK & FRONTEND UI ENGINE
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
  ┌──────────────┐             ┌──────────────┐             ┌──────────────┐
  │ 1. COMPONENT │             │  2. FRONTEND │             │  3. API-TO-UI│
  │   BUILDER    │             │   AUDITOR    │             │   GENERATOR  │
  └──────┬───────┘             └──────┬───────┘             └──────┬───────┘
         │                            │                            │
   • HTML5/CSS3                 • WCAG 2.1 AA                • Backend Schema
     Moderno                      (Acessibilidade)             -> TypeScript SDK
   • React / Next.js            • CSS Smells &               • Auto-Formulários
     (TSX + Tailwind)             Z-Index Hell                 com Validação
   • Micro-Interações           • Detector de Clichês        • Fetch & Error
     e Estados                    de IA                        Handling Tipado
```

---

## 🚀 Como Usar no Python

### 1. Geração de Tokens de Design e Tipografia Fluida (`DesignTokens`)

Gera variáveis CSS com paletas HSL profissionais, tipografia fluida com `clamp()` e sombras multicamadas:

```python
from framework import DesignTokens

tokens = DesignTokens()

# Gera folha de estilos CSS completa para o tema Warm Slate
css_code = tokens.generate_css_variables(theme_name="warm_slate")

print(css_code)
# Contém:
# --text-2xl: clamp(1.500rem, 1.333rem + 0.833vw, 2.000rem);
# --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
# --shadow-sm, --radius-md, etc.
```

---

### 2. Geração de Componentes de Alta Fidelidade (`ComponentBuilder`)

Gera componentes completos com todos os estados (`default`, `hover`, `active`, `focus-visible`, `loading`, `disabled`) em **React Next.js (TSX + Tailwind)** ou **Vanilla HTML5/CSS**:

```python
from framework import ComponentBuilder

builder = ComponentBuilder()

# 1. Botão acessível em React TSX + Tailwind
react_btn = builder.build_button(
    label="Salvar Alterações",
    variant="primary",
    size="md",
    stack="react_tailwind"
)

# 2. Card de Métricas em HTML5 Semântico + CSS
vanilla_card = builder.build_card(
    title="Faturamento Mensal",
    subtitle="Consolidado de vendas Q3",
    stack="vanilla"
)
```

---

### 3. Auditoria de Acessibilidade WCAG 2.1 AA & Anti-Clichês (`A11yAuditor`)

Audita código HTML/JSX e aponta violações de acessibilidade, z-index excessivo e clichês visuais de IA:

```python
from framework import A11yAuditor

auditor = A11yAuditor()

codigo_jsx = """
<div>
  <h1>Painel Principal</h1>
  <h3>Subseção</h3> <!-- Salto inválido de h1 para h3 -->
  <button><svg></svg></button> <!-- Botão de ícone sem aria-label -->
  <img src="banner.jpg" /> <!-- Imagem sem alt -->
</div>
"""

resultado = auditor.audit(codigo_jsx, filename="Dashboard.tsx")

print(resultado.score)            # Ex: 50 / 100
print(resultado.passed)           # False (reprovado por erros críticos)
for violacao in resultado.violations:
    print(f"[{violacao.severity.upper()}] {violacao.message} -> {violacao.fix_recommendation}")
```

---

### 4. Gerador de SDK TypeScript e Formulários (`APIClientGenerator`)

Gera interfaces TypeScript tipadas e clientes `fetch()` com tratamento de erro a partir de schemas:

```python
from framework import APIClientGenerator

generator = APIClientGenerator()

schema_usuario = {
    "id": "integer",
    "nome": "string",
    "email": "string",
    "ativo": "boolean"
}

# 1. Gera interface TypeScript
ts_types = generator.generate_typescript_interface("Usuario", schema_usuario, required_fields=["id", "nome", "email"])

# 2. Gera client fetch tipado
ts_client = generator.generate_fetch_client("criarUsuario", "POST", "/api/usuarios", "Usuario", "Usuario")

# 3. Gera formulário React completo com estado e validação
react_form = generator.generate_react_form("Usuario", schema_usuario, required_fields=["nome", "email"])
```

---

## 🧰 Uso via Servidor MCP (Cursor & Claude Desktop)

O **FullstackUIEngine** expõe 3 ferramentas nativas no Servidor MCP:

1. **`frontend_component_scaffold`**:
   > *"Crie um componente de Input com validação de e-mail e helper text em React TSX usando Tailwind."*
2. **`frontend_a11y_audit`**:
   > *"Audite o arquivo `components/Navbar.tsx` para garantir conformidade com WCAG 2.1 AA."*
3. **`generate_typed_api_client`**:
   > *"Gere a interface TypeScript e o formulário de cadastro para o modelo Produto com campos nome, preco e categoria."*
