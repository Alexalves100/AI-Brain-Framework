"""
Standardize all agents by adding Interfaces section.
Version: 1.0.0
"""

from pathlib import Path

ROOT = Path("d:/PROJETOS/WEB/AI-Brain-Framework/.ai/agents")

INTERFACES = {
    "01-Solution-Architect.md": [
        "- Chief Architect (decisões globais)",
        "- Core Architect (implementação)",
        "- Engine Architects (especificações)",
    ],
    "02-Core-Architect.md": [
        "- Solution Architect (solução)",
        "- Engine Architects (engines)",
        "- Reviewer (validação)",
    ],
    "03-Brain-Architect.md": [
        "- Context Architect (contexto)",
        "- Knowledge Architect (conhecimento)",
        "- Todas as skills (orquestração)",
    ],
    "04-Knowledge-Architect.md": [
        "- Brain Architect (orquestração)",
        "- Memory Architect (persistência)",
        "- Discovery Architect (descoberta)",
    ],
    "05-Memory-Architect.md": [
        "- Knowledge Architect (conhecimento)",
        "- Context Architect (contexto)",
        "- Brain Architect (orquestração)",
    ],
    "06-Reasoning-Architect.md": [
        "- Brain Architect (orquestração)",
        "- Knowledge Architect (conhecimento)",
        "- Quality Architect (validação)",
    ],
    "07-Discovery-Architect.md": [
        "- Index Architect (indexação)",
        "- Graph Architect (grafos)",
        "- Knowledge Architect (conhecimento)",
    ],
    "08-Index-Architect.md": [
        "- Discovery Architect (descoberta)",
        "- Graph Architect (grafos)",
        "- Knowledge Architect (conhecimento)",
    ],
    "09-Graph-Architect.md": [
        "- Index Architect (indexação)",
        "- Knowledge Architect (conhecimento)",
        "- Database Architect (schemas)",
    ],
    "10-Context-Architect.md": [
        "- Brain Architect (orquestração)",
        "- Memory Architect (persistência)",
        "- Token Economy (economia)",
    ],
    "11-Security-Architect.md": [
        "- Privacy Architect (LGPD)",
        "- Performance Architect (segurança)",
        "- Quality Architect (auditoria)",
    ],
    "12-Privacy-Architect.md": [
        "- Security Architect (segurança)",
        "- Legal Architect (compliance)",
        "- Governance Architect (políticas)",
    ],
    "13-Performance-Architect.md": [
        "- Architecture Architect (decisões)",
        "- Database Architect (queries)",
        "- SRE Architect (operações)",
    ],
    "14-Database-Architect.md": [
        "- Architecture Architect (decisões)",
        "- API Architect (contratos)",
        "- Performance Architect (queries)",
    ],
    "15-API-Architect.md": [
        "- Architecture Architect (decisões)",
        "- Database Architect (schemas)",
        "- Security Architect (auth)",
    ],
    "18-Testing-Architect.md": [
        "- Quality Architect (métricas)",
        "- Implementation Architect (código)",
        "- Reviewer (validação)",
    ],
}


def add_interfaces(agent_path: Path, interfaces: list):
    content = agent_path.read_text(encoding="utf-8")

    if "## Interfaces" in content:
        return False

    section = "\n## Interfaces\n\n"
    for iface in interfaces:
        section += f"{iface}\n"

    content += section
    agent_path.write_text(content, encoding="utf-8")
    return True


def main():
    count = 0
    for filename, interfaces in INTERFACES.items():
        agent_path = ROOT / filename
        if agent_path.exists():
            if add_interfaces(agent_path, interfaces):
                count += 1
    print(f"Updated {count} agents with Interfaces section.")


if __name__ == "__main__":
    main()
