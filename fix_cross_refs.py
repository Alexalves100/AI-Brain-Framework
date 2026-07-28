"""
Fix cross-references in all skills.
Version: 1.0.0
"""

from pathlib import Path

ROOT = Path("d:/PROJETOS/WEB/AI-Brain-Framework/.ai/skills")

CROSS_REFS = {
    "core": {
        "00-brain-skill.md": ["01-knowledge-skill.md", "07-context-skill.md", "03-reasoning-skill.md"],
        "01-knowledge-skill.md": ["00-brain-skill.md", "02-memory-skill.md", "04-discovery-skill.md"],
        "02-memory-skill.md": ["01-knowledge-skill.md", "07-context-skill.md", "38-background-jobs-skill.md"],
        "03-reasoning-skill.md": ["00-brain-skill.md", "01-knowledge-skill.md", "13-architecture-skill.md"],
    },
    "discovery": {
        "04-discovery-skill.md": ["05-index-skill.md", "06-graph-skill.md", "01-knowledge-skill.md"],
        "05-index-skill.md": ["04-discovery-skill.md", "06-graph-skill.md", "01-knowledge-skill.md"],
        "06-graph-skill.md": ["05-index-skill.md", "01-knowledge-skill.md", "39-multi-tenancy-skill.md"],
    },
    "context": {
        "07-context-skill.md": ["00-brain-skill.md", "08-token-economy-skill.md", "02-memory-skill.md"],
        "08-token-economy-skill.md": ["07-context-skill.md", "23-token-efficient-coder.md", "42-prompt-engineering-skill.md"],
    },
    "governance": {
        "09-security-skill.md": ["11-privacy-skill.md", "24-security-auditor.md", "37-secrets-management-skill.md"],
        "10-privacy-skill.md": ["09-security-skill.md", "39-multi-tenancy-skill.md", "19-governance-architect"],
        "11-quality-skill.md": ["12-review-skill.md", "19-testing-skill.md", "17-quality-architect"],
        "12-review-skill.md": ["11-quality-skill.md", "22-reviewer", "46-refactoring-skill.md"],
        "30-rate-limiting-skill.md": ["09-security-skill.md", "15-api-skill.md", "45-webhook-design-skill.md"],
        "37-secrets-management-skill.md": ["09-security-skill.md", "11-security-architect", "30-rate-limiting-skill.md"],
    },
    "engineering": {
        "13-architecture-skill.md": ["14-database-skill.md", "15-api-skill.md", "16-documentation-architect"],
        "14-database-skill.md": ["13-architecture-skill.md", "40-database-migration-skill.md", "39-multi-tenancy-skill.md"],
        "15-api-skill.md": ["13-architecture-skill.md", "41-api-versioning-skill.md", "45-webhook-design-skill.md"],
        "16-performance-skill.md": ["13-architecture-skill.md", "29-caching-skill.md", "31-observability-skill.md"],
        "17-documentation-skill.md": ["13-architecture-skill.md", "16-documentation-architect", "32-tech-writer"],
        "22-secure-dev-framework.md": ["09-security-skill.md", "24-security-auditor.md", "25-security-report.md"],
        "23-token-efficient-coder.md": ["08-token-economy-skill.md", "42-prompt-engineering-skill.md"],
        "24-security-auditor.md": ["09-security-skill.md", "25-security-report.md", "22-secure-dev-framework.md"],
        "25-security-report.md": ["24-security-auditor.md", "22-secure-dev-framework.md", "33-incident-response-skill.md"],
        "26-ui-design-skill.md": ["17-documentation-skill.md", "16-performance-skill.md", "35-ux-researcher"],
        "39-multi-tenancy-skill.md": ["14-database-skill.md", "09-security-skill.md", "10-privacy-skill.md"],
        "41-api-versioning-skill.md": ["15-api-skill.md", "17-documentation-skill.md", "13-architecture-skill.md"],
        "42-prompt-engineering-skill.md": ["08-token-economy-skill.md", "23-token-efficient-coder.md", "43-model-evaluation-skill.md"],
        "43-model-evaluation-skill.md": ["42-prompt-engineering-skill.md", "33-ai-safety-architect", "44-data-pipeline-skill.md"],
        "45-webhook-design-skill.md": ["15-api-skill.md", "09-security-skill.md", "27-error-handling-skill.md"],
    },
    "delivery": {
        "18-implementation-skill.md": ["19-testing-skill.md", "20-release-skill.md", "46-refactoring-skill.md"],
        "19-testing-skill.md": ["18-implementation-skill.md", "11-quality-skill.md", "39-tester"],
        "20-release-skill.md": ["18-implementation-skill.md", "21-release-architect", "36-feature-flags-skill.md"],
        "21-governance-skill.md": ["19-governance-architect", "11-quality-skill.md", "09-security-skill.md"],
        "27-error-handling-skill.md": ["28-logging-skill.md", "31-observability-skill.md", "33-incident-response-skill.md"],
        "28-logging-skill.md": ["27-error-handling-skill.md", "31-observability-skill.md", "34-logging-skill.md"],
        "29-caching-skill.md": ["16-performance-skill.md", "31-observability-skill.md", "38-background-jobs-skill.md"],
        "31-observability-skill.md": ["28-logging-skill.md", "27-error-handling-skill.md", "33-incident-response-skill.md"],
        "32-cost-optimization-skill.md": ["34-capacity-planning-skill.md", "27-finops-architect", "16-performance-skill.md"],
        "33-incident-response-skill.md": ["31-observability-skill.md", "35-chaos-engineering-skill.md", "24-sre-architect"],
        "34-capacity-planning-skill.md": ["32-cost-optimization-skill.md", "29-capacity-architect", "16-performance-skill.md"],
        "35-chaos-engineering-skill.md": ["33-incident-response-skill.md", "31-observability-skill.md", "29-caching-skill.md"],
        "36-feature-flags-skill.md": ["20-release-skill.md", "33-incident-response-skill.md", "38-background-jobs-skill.md"],
        "38-background-jobs-skill.md": ["27-error-handling-skill.md", "31-observability-skill.md", "29-caching-skill.md"],
        "40-database-migration-skill.md": ["14-database-skill.md", "20-release-skill.md", "39-multi-tenancy-skill.md"],
        "44-data-pipeline-skill.md": ["14-database-skill.md", "43-model-evaluation-skill.md", "40-database-migration-skill.md"],
        "46-refactoring-skill.md": ["18-implementation-skill.md", "11-quality-skill.md", "12-review-skill.md"],
    },
}


def add_cross_refs(skill_path: Path, cross_refs: list):
    content = skill_path.read_text(encoding="utf-8")

    if "## Ver Também" in content or "## Ver Tambem" in content:
        return False

    section = "\n## Ver Também\n\n"
    for ref in cross_refs:
        section += f"- `{ref}`\n"

    if "## Histórico" in content:
        content = content.replace("## Histórico", section + "\n## Histórico")
    elif "## Historico" in content:
        content = content.replace("## Historico", section + "\n## Historico")
    else:
        content += section

    skill_path.write_text(content, encoding="utf-8")
    return True


def main():
    count = 0
    for category, refs in CROSS_REFS.items():
        for filename, cross_refs in refs.items():
            skill_path = ROOT / category / filename
            if skill_path.exists():
                if add_cross_refs(skill_path, cross_refs):
                    count += 1
    print(f"Updated {count} skills with cross-references.")


if __name__ == "__main__":
    main()
