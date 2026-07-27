# Contributing to AI-Brain-Framework

**Version:** 1.0.0

Obrigado por considerar contribuir. Este documento define o processo.

---

## Princípios

1. **Architecture First** — Toda mudança nasce da arquitetura.
2. **Documentation First** — Nada existe sem documentação.
3. **Tests Required** — Toda feature vem com testes.
4. **Backward Compatible** — Não quebre a API pública.

---

## Setup

```bash
git clone <repo>
cd AI-Brain-Framework
pip install -e ".[dev]"
pre-commit install
```

---

## Workflow

1. **Fork** o repositório
2. **Branch** descritivo: `feat/nova-engine`, `fix/bug-x`, `docs/melhoria-y`
3. **Commit** mensagens claras (Conventional Commits)
4. **Testes** — `python -m unittest discover tests` deve passar
5. **Lint** — `ruff check framework tests tools`
6. **PR** com descrição do que mudou e por quê

---

## Estrutura de Commit

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Exemplos:**
- `feat(engines): add CacheEngine`
- `fix(security): correct SQL injection regex`
- `docs(readme): update usage examples`

---

## Adicionando uma Engine

1. Criar arquivo em `framework/engines/<name>.py`
2. Herdar de `Skill`
3. Implementar `run(self, context: Context) -> SkillResult`
4. Exportar em `framework/engines/__init__.py`
5. Adicionar testes em `tests/test_engines.py`
6. Documentar em `.ai/skills/engineering/`

---

## Adicionando um Exemplo

1. Criar pasta em `examples/<name>/`
2. Criar `app.py` com servidor HTTP
3. Usar `SecurityHeaders` + `InputValidator`
4. Documentar no `examples/README.md`

---

## Code Review

- Mínimo 1 aprovação
- Lint passa
- Testes passam
- Documentação atualizada

---

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob MIT.
