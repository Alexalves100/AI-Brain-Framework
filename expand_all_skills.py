"""
Expand all basic skills with the expanded template structure.
Version: 1.0.0
"""

from pathlib import Path

ROOT = Path("d:/PROJETOS/WEB/AI-Brain-Framework/.ai/skills")

EXPANDED_TEMPLATE = """# {title}

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** {category}

## Capacidade
{capability}

## Inputs
{inputs}

## Outputs
{outputs}

## Invariantes
{invariants}

## Interfaces
{interfaces}

## Quando Usar
- {usage_1}
- {usage_2}

## Quando NÃO Usar
- {anti_usage_1}
- {anti_usage_2}

## Anti-Patterns
- {anti_pattern_1}
- {anti_pattern_2}

## Exemplos

### Exemplo 1: Caso Simples
```python
from framework import create_default_orchestrator, Context
orch = create_default_orchestrator()
ctx = Context()
ctx.set("input", "value")
result = orch.run("{name_lower}", ctx)
```

### Exemplo 2: Caso Avançado
```python
# Pipeline com múltiplas skills
ctx = Context()
ctx.set("input", "complex_value")
results = orch.run_pipeline(["{name_lower}", "security"], ctx)
for r in results:
    print(r.status, r.output)
```

## Métricas de Sucesso
- Latência < 100ms para inputs típicos
- Taxa de erro < 1%
- Cobertura de testes > 80%

## Referências
- Ver `framework/{category}/{name_lower}.py` para implementação
- Ver `tests/test_{category}.py` para exemplos de uso
"""


SKILLS_DATA = {
    "core": [
        ("00-brain-skill", "Brain Skill", "Orquestração cognitiva central", [
            "Estado de contexto", "Skills disponíveis", "Prioridades"
        ], [
            "Skill selecionada", "Roteamento", "Estado atualizado"
        ], [
            "Single skill ativa por vez", "Contexto mínimo", "Rastreabilidade"
        ], [
            "Todas as skills", "Context Engine"
        ]),
        ("01-knowledge-skill", "Knowledge Skill", "Gestão de conhecimento versionado", [
            "Documentos", "Queries", "Índices"
        ], [
            "Conhecimento recuperado", "Fontes citadas", "Recomendações"
        ], [
            "Fontes oficiais", "Sem inferência", "Versionamento"
        ], [
            "Discovery Engine", "Index Engine"
        ]),
        ("02-memory-skill", "Memory Skill", "Memória persistente entre sessões", [
            "Estado atual", "Histórico", "Contexto"
        ], [
            "Snapshot", "Recuperação", "Histórico"
        ], [
            "Imutável após commit", "Recuperação determinística"
        ], [
            "Knowledge Engine", "Context Engine"
        ]),
        ("03-reasoning-skill", "Reasoning Skill", "Raciocínio estruturado e auditável", [
            "Problema", "Premissas", "Restrições"
        ], [
            "Cadeia lógica", "Conclusão", "Alternativas"
        ], [
            "Lógica explícita", "Premissas declaradas"
        ], [
            "Brain Engine", "Knowledge Engine"
        ]),
    ],
    "discovery": [
        ("04-discovery-skill", "Discovery Skill", "Descoberta estruturada de informações", [
            "Escopo", "Critérios", "Fontes"
        ], [
            "Inventário", "Mapa", "Recomendações"
        ], [
            "Fontes oficiais", "Reproduzibilidade"
        ], [
            "Index Engine", "Graph Engine"
        ]),
        ("05-index-skill", "Index Skill", "Indexação estruturada", [
            "Documentos", "Metadados", "Esquemas"
        ], [
            "Índices", "Referências", "Mapas"
        ], [
            "Atualização contínua", "Busca determinística"
        ], [
            "Discovery Engine", "Graph Engine"
        ]),
        ("06-graph-skill", "Graph Skill", "Grafos de conhecimento", [
            "Entidades", "Relacionamentos", "Ontologias"
        ], [
            "Grafos", "Queries", "Visualizações"
        ], [
            "Ontologias versionadas", "Tipagem explícita"
        ], [
            "Index Engine", "Knowledge Engine"
        ]),
    ],
    "context": [
        ("07-context-skill", "Context Skill", "Gestão de contexto entre agentes", [
            "Estado", "Tokens", "Prioridades"
        ], [
            "Contexto empacotado", "Resumos", "Decisões"
        ], [
            "Mínimo viável", "Auditável"
        ], [
            "Brain Engine", "Token Economy Engine"
        ]),
        ("08-token-economy-skill", "Token Economy Skill", "Economia máxima de tokens", [
            "Conteúdo", "Contexto", "Prioridades"
        ], [
            "Versão compacta", "Resumo executivo", "Referências"
        ], [
            "Sem perda de informação essencial", "Reuso de docs"
        ], [
            "Context Engine", "Todas as skills"
        ]),
    ],
    "governance": [
        ("09-security-skill", "Security Skill", "Aplicação de segurança", [
            "Código", "Arquitetura", "Configurações"
        ], [
            "Análise", "Mitigações", "Gates"
        ], [
            "Security by design", "Auditoria contínua"
        ], [
            "Security Engine", "Privacy Engine"
        ]),
        ("10-privacy-skill", "Privacy Skill", "Privacidade e LGPD", [
            "Fluxos de dados", "Bases legais", "Retenção"
        ], [
            "DPIA", "Mecanismos", "Compliance"
        ], [
            "Privacy by design", "Minimização"
        ], [
            "Security Engine", "Compliance Checker"
        ]),
        ("11-quality-skill", "Quality Skill", "Garantia de qualidade", [
            "Código", "Testes", "Métricas"
        ], [
            "Gates", "Relatórios", "Planos"
        ], [
            "Cobertura mínima", "Lint passa"
        ], [
            "Quality Analyzer", "Testing Engine"
        ]),
        ("12-review-skill", "Review Skill", "Revisão técnica", [
            "PR", "Spec", "Critérios"
        ], [
            "Aprovação", "Mudanças", "Relatório"
        ], [
            "Mínimo 2 aprovações", "Evidências"
        ], [
            "Quality Skill", "Security Skill"
        ]),
    ],
    "engineering": [
        ("13-architecture-skill", "Architecture Skill", "Decisões arquiteturais", [
            "Requisitos", "Restrições", "Contexto"
        ], [
            "Decisão", "ADR", "Trade-offs"
        ], [
            "Documentação", "Aprovação Chief"
        ], [
            "Solution Architect", "Core Architect"
        ]),
        ("14-database-skill", "Database Skill", "Modelagem de dados", [
            "Requisitos", "Volume", "Acesso"
        ], [
            "Esquemas", "Índices", "Migrações"
        ], [
            "Integridade", "Backups"
        ], [
            "Architecture Skill", "Performance Skill"
        ]),
        ("15-api-skill", "API Skill", "Design de APIs", [
            "Casos de uso", "Consumidores", "Restrições"
        ], [
            "Especificação", "Contratos", "Versão"
        ], [
            "RESTful", "OpenAPI", "Versionamento"
        ], [
            "Architecture Skill", "Documentation Skill"
        ]),
        ("16-performance-skill", "Performance Skill", "Otimização de performance", [
            "SLAs", "Métricas", "Gargalos"
        ], [
            "Budgets", "Planos", "Dashboards"
        ], [
            "Medir antes", "Core Web Vitals"
        ], [
            "Architecture Skill", "Observability"
        ]),
        ("17-documentation-skill", "Documentation Skill", "Documentação técnica", [
            "Código", "Decisões", "APIs"
        ], [
            "Docs", "Diagramas", "Tutoriais"
        ], [
            "Junto ao código", "Versionada"
        ], [
            "Documentation Architect", "Knowledge Engine"
        ]),
    ],
    "delivery": [
        ("18-implementation-skill", "Implementation Skill", "Implementação controlada", [
            "Spec", "Padrões", "Contratos"
        ], [
            "Código", "PRs", "Builds"
        ], [
            "TDD", "Commits semânticos"
        ], [
            "Architecture Skill", "Testing Skill"
        ]),
        ("19-testing-skill", "Testing Skill", "Estratégia de testes", [
            "Requisitos", "Código", "Riscos"
        ], [
            "Plano", "Suítes", "Relatórios"
        ], [
            "Pirâmide", "CI"
        ], [
            "Quality Skill", "Implementation Skill"
        ]),
        ("20-release-skill", "Release Skill", "Gestão de releases", [
            "Builds", "Aprovações", "Riscos"
        ], [
            "Versões", "Notas", "Rollbacks"
        ], [
            "Semver", "Changelog"
        ], [
            "Release Architect", "Quality Skill"
        ]),
        ("21-governance-skill", "Governance Skill", "Governança técnica", [
            "Políticas", "Processos", "Auditorias"
        ], [
            "Compliance", "Relatórios", "Gates"
        ], [
            "Contínuo", "Versionado"
        ], [
            "Policy Engine", "Audit Log"
        ]),
    ],
}


def expand_skill(category: str, filename: str, title: str, capability: str,
                 inputs: list, outputs: list, invariants: list, interfaces: list):
    content = EXPANDED_TEMPLATE.format(
        title=title,
        category=category.capitalize(),
        capability=capability,
        inputs="\n".join(f"- {i}" for i in inputs),
        outputs="\n".join(f"- {o}" for o in outputs),
        invariants="\n".join(f"- {inv}" for inv in invariants),
        interfaces=", ".join(interfaces),
        usage_1=f"Quando precisar de {capability.lower()}",
        usage_2="Em pipelines que combinam múltiplas skills",
        anti_usage_1="Para tarefas fora do escopo desta skill",
        anti_usage_2="Quando uma skill mais específica já cobre o caso",
        anti_pattern_1="Ignorar invariantes",
        anti_pattern_2="Usar sem validar inputs",
        name_lower=filename.replace("-skill", "").replace("-", "_"),
    )
    path = ROOT / category / f"{filename}.md"
    path.write_text(content, encoding="utf-8")
    return path


def main():
    count = 0
    for category, skills in SKILLS_DATA.items():
        for skill_data in skills:
            filename, title, capability, inputs, outputs, invariants, interfaces = skill_data
            expand_skill(category, filename, title, capability, inputs, outputs, invariants, interfaces)
            count += 1
    print(f"Expanded {count} skills.")


if __name__ == "__main__":
    main()
