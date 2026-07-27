"""
AI-Brain-Framework — Preenchimento Oficial de Conteúdo
Version: 1.0.0
Purpose: Preencher todos os arquivos oficiais com conteúdo denso e objetivo
"""

from pathlib import Path

ROOT = Path("d:/PROJETOS/WEB/AI-Brain-Framework")

# ============================================================
# CONTEÚDO OFICIAL — Economy Edition
# ============================================================

AGENTS = {
    "00-Chief-Architect.md": """# Chief Architect

**Versão:** 1.0.0 | **Status:** Oficial | **Owner:** AI-Brain-Framework

## Responsabilidade
Autoridade máxima. Aprova toda alteração arquitetural.

## Inputs
- Decisões dos Solution/Core Architects
- RFCs e ADRs
- Solicitações de mudança

## Outputs
- Aprovações formais
- Decisões arquiteturais vinculantes
- Versionamento de arquitetura

## Invariantes
- Nenhuma alteração sem aprovação
- Toda decisão registrada em ADR
- Hierarquia respeitada

## Interfaces
- Todos os agentes (via governança)
- Release Architect (gate final)
""",

    "01-Solution-Architect.md": """# Solution Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Arquitetura da solução. Traduz visão em sistemas concretos.

## Inputs
- Requisitos de negócio
- Restrições técnicas
- Decisões do Chief Architect

## Outputs
- Diagramas de solução
- Especificações de componentes
- Trade-offs documentados

## Invariantes
- Alinhamento com arquitetura global
- Documentação obrigatória
- Rastreabilidade de decisões
""",

    "02-Core-Architect.md": """# Core Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Define e mantém o Core do framework.

## Inputs
- Especificações de engines
- Restrições de performance
- Decisões do Solution Architect

## Outputs
- Especificação do Core
- Contratos de API internos
- Padrões de implementação

## Invariantes
- Core imutável sem aprovação
- Contratos versionados
- Compatibilidade retroativa
""",

    "03-Brain-Architect.md": """# Brain Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Responsável pelo Brain Engine — orquestração cognitiva central.

## Inputs
- Skills oficiais
- Prompts oficiais
- Estado de contexto

## Outputs
- Decisões de orquestração
- Roteamento de skills
- Estado cognitivo

## Invariantes
- Single Source of Truth
- Skills versionadas
- Contexto auditável
""",

    "04-Knowledge-Architect.md": """# Knowledge Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Knowledge Engine — gestão de conhecimento versionado.

## Inputs
- Documentos oficiais
- Decisões registradas
- Glossário

## Outputs
- Base de conhecimento
- Índices de busca
- Grafos de conhecimento

## Invariantes
- Conhecimento versionado
- Fontes citadas
- Sem duplicação
""",

    "05-Memory-Architect.md": """# Memory Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Memory Engine — memória persistente entre sessões.

## Inputs
- Decisões arquiteturais
- Estado de projetos
- Contexto de longo prazo

## Outputs
- Snapshots de estado
- Recuperação de contexto
- Histórico versionado

## Invariantes
- Memória imutável após commit
- Recuperação determinística
- Privacidade por padrão
""",

    "06-Reasoning-Architect.md": """# Reasoning Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Reasoning Engine — raciocínio estruturado e auditável.

## Inputs
- Problema definido
- Premissas
- Restrições

## Outputs
- Cadeia de raciocínio
- Conclusão justificada
- Alternativas avaliadas

## Invariantes
- Lógica explícita
- Premissas declaradas
- Conclusão verificável
""",

    "07-Discovery-Architect.md": """# Discovery Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Discovery Engine — descoberta estruturada de informações.

## Inputs
- Escopo de busca
- Critérios de relevância
- Fontes autorizadas

## Outputs
- Inventário de fontes
- Mapa de descoberta
- Recomendações

## Invariantes
- Fontes oficiais primeiro
- Descoberta reproduzível
- Sem inferência sem fonte
""",

    "08-Index-Architect.md": """# Index Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Index Engine — indexação estruturada de conhecimento.

## Inputs
- Documentos
- Metadados
- Esquemas de classificação

## Outputs
- Índices navegáveis
- Tabelas de referência
- Mapas de conteúdo

## Invariantes
- Índices atualizados
- Esquemas estáveis
- Busca determinística
""",

    "09-Graph-Architect.md": """# Graph Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Graph Engine — grafos de conhecimento e relações.

## Inputs
- Entidades
- Relacionamentos
- Ontologias

## Outputs
- Grafos navegáveis
- Queries otimizadas
- Visualizações

## Invariantes
- Ontologias versionadas
- Relacionamentos tipados
- Sem ciclos órfãos
""",

    "10-Context-Architect.md": """# Context Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Context Engine — gestão de contexto entre agentes.

## Inputs
- Estado de sessão
- Tokens disponíveis
- Prioridades

## Outputs
- Contexto empacotado
- Resumos executivos
- Decisões de priorização

## Invariantes
- Contexto mínimo viável
- Tokens auditáveis
- Sem duplicação
""",

    "11-Security-Architect.md": """# Security Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Segurança desde a concepção. Aplica skill `security-auditor`.

## Inputs
- Arquitetura proposta
- Código
- Configurações

## Outputs
- Análise de ameaças
- Recomendações de mitigação
- Gates de segurança

## Invariantes
- Security by design
- Zero trust por padrão
- Auditoria contínua
""",

    "12-Privacy-Architect.md": """# Privacy Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
LGPD e privacidade por padrão.

## Inputs
- Fluxos de dados pessoais
- Bases legais
- Retenção

## Outputs
- DPIA
- Política de privacidade
- Mecanismos de consentimento

## Invariantes
- Privacy by design
- Minimização de dados
- Direito do titular respeitado
""",

    "13-Performance-Architect.md": """# Performance Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Performance como requisito, não otimização tardia.

## Inputs
- SLAs
- Métricas de uso
- Gargalos identificados

## Outputs
- Budgets de performance
- Planos de otimização
- Dashboards

## Invariantes
- Medir antes de otimizar
- Core Web Vitals respeitados
- Cache quando possível
""",

    "14-Database-Architect.md": """# Database Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Modelagem e arquitetura de bancos de dados.

## Inputs
- Requisitos de dados
- Volume estimado
- Padrões de acesso

## Outputs
- Esquemas
- Índices
- Estratégias de migração

## Invariantes
- Normalização adequada
- Integridade referencial
- Backups versionados
""",

    "15-API-Architect.md": """# API Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Design e governança de APIs.

## Inputs
- Casos de uso
- Consumidores
- Restrições

## Outputs
- Especificações OpenAPI
- Contratos
- Versionamento

## Invariantes
- RESTful por padrão
- Versionamento semântico
- Documentação obrigatória
""",

    "16-Documentation-Architect.md": """# Documentation Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Documentação como código.

## Inputs
- Decisões
- APIs
- Processos

## Outputs
- Docs versionadas
- Diagramas
- Tutoriais

## Invariantes
- Docs no repositório
- Docs junto ao código
- Sem docs desatualizadas
""",

    "17-Quality-Architect.md": """# Quality Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Qualidade end-to-end.

## Inputs
- Código
- Testes
- Métricas

## Outputs
- Gates de qualidade
- Relatórios
- Planos de melhoria

## Invariantes
- Cobertura mínima definida
- Lint obrigatório
- Sem débito crítico
""",

    "18-Testing-Architect.md": """# Testing Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Estratégia e cobertura de testes.

## Inputs
- Requisitos
- Código
- Riscos

## Outputs
- Plano de testes
- Suítes automatizadas
- Relatórios de cobertura

## Invariantes
- Pirâmide de testes respeitada
- Testes determinísticos
- CI obrigatório
""",

    "19-Governance-Architect.md": """# Governance Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Governança técnica e compliance.

## Inputs
- Políticas
- Processos
- Auditorias

## Outputs
- Políticas formalizadas
- Relatórios de compliance
- Gates de governança

## Invariantes
- Compliance contínuo
- Políticas versionadas
- Auditoria rastreável
""",

    "20-Implementation-Architect.md": """# Implementation Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Implementação controlada e auditável.

## Inputs
- Especificações
- Contratos
- Padrões

## Outputs
- Código
- PRs
- Builds

## Invariantes
- TDD quando aplicável
- Commits semânticos
- Builds reproduzíveis
""",

    "21-Release-Architect.md": """# Release Architect

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Gestão de releases.

## Inputs
- Builds
- Aprovações
- Riscos

## Outputs
- Versões publicadas
- Notas de release
- Rollbacks

## Invariantes
- Semver obrigatório
- Changelog atualizado
- Rollback testado
""",

    "22-Reviewer.md": """# Reviewer

**Versão:** 1.0.0 | **Status:** Oficial

## Responsabilidade
Revisão técnica obrigatória.

## Inputs
- PRs
- Especificações
- Critérios de aceite

## Outputs
- Aprovações
- Solicitações de mudança
- Relatórios de revisão

## Invariantes
- Mínimo 2 aprovações
- Critérios objetivos
- Sem aprovação sem evidência
""",
}

PROMPTS = {
    "architecture.prompt.md": """# Architecture Prompt

**Versão:** 1.0.0 | **Status:** Oficial

## Uso
Decisões arquiteturais.

## Estrutura
1. Contexto
2. Restrições
3. Alternativas
4. Decisão
5. Consequências
6. Trade-offs

## Regra
Toda decisão gera ADR.
""",

    "specification.prompt.md": """# Specification Prompt

**Versão:** 1.0.0 | **Status:** Oficial

## Uso
Especificações técnicas.

## Estrutura
1. Objetivo
2. Escopo
3. Fora de escopo
4. Requisitos funcionais
5. Requisitos não-funcionais
6. Critérios de aceite

## Regra
Spec antes de código.
""",

    "implementation.prompt.md": """# Implementation Prompt

**Versão:** 1.0.0 | **Status:** Oficial

## Uso
Implementação controlada.

## Estrutura
1. Spec aprovada
2. Padrões aplicados
3. Testes definidos
4. Commits semânticos
5. PR com critérios

## Regra
Sem spec, sem código.
""",

    "documentation.prompt.md": """# Documentation Prompt

**Versão:** 1.0.0 | **Status:** Oficial

## Uso
Documentação técnica.

## Estrutura
1. Propósito
2. Como usar
3. Exemplos
4. Limitações
5. Referências

## Regra
Doc junto ao código.
""",

    "security.prompt.md": """# Security Prompt

**Versão:** 1.0.0 | **Status:** Oficial

## Uso
Análise de segurança.

## Estrutura
1. Ameaças (STRIDE)
2. Vetores de ataque
3. Mitigações
4. Validação
5. Monitoramento

## Regra
Security by design.
""",

    "review.prompt.md": """# Review Prompt

**Versão:** 1.0.0 | **Status:** Oficial

## Uso
Revisão técnica.

## Estrutura
1. Critérios objetivos
2. Evidências
3. Riscos
4. Aprovação ou mudança

## Regra
Sem evidência, sem aprovação.
""",

    "testing.prompt.md": """# Testing Prompt

**Versão:** 1.0.0 | **Status:** Oficial

## Uso
Estratégia de testes.

## Estrutura
1. Unit
2. Integration
3. E2E
4. Performance
5. Security

## Regra
Pirâmide de testes.
""",

    "release.prompt.md": """# Release Prompt

**Versão:** 1.0.0 | **Status:** Oficial

## Uso
Gestão de releases.

## Estrutura
1. Versão (Semver)
2. Changelog
3. Aprovações
4. Rollback plan
5. Comunicação

## Regra
Release reversível.
""",
}

RULES = {
    "architecture.rules.md": """# Architecture Rules

**Versão:** 1.0.0 | **Status:** Oficial

## Obrigatório
- Toda decisão gera ADR
- Diagramas versionados
- Contratos antes de código

## Proibido
- Acoplamento cíclico
- Decisões sem registro
- Arquitetura implícita
""",

    "naming.rules.md": """# Naming Rules

**Versão:** 1.0.0 | **Status:** Oficial

## Convenção
- kebab-case para arquivos
- PascalCase para classes
- camelCase para funções/variáveis
- UPPER_SNAKE_CASE para constantes

## Proibido
- Abreviações obscuras
- Nomes genéricos (data, info, util)
""",

    "markdown.rules.md": """# Markdown Rules

**Versão:** 1.0.0 | **Status:** Oficial

## Obrigatório
- Headers hierárquicos (H1 único)
- Listas ordenadas quando sequenciais
- Code blocks com linguagem

## Proibido
- Markdown sem header
- Links quebrados
- Imagens sem alt
""",

    "documentation.rules.md": """# Documentation Rules

**Versão:** 1.0.0 | **Status:** Oficial

## Obrigatório
- README em todo módulo
- Doc junto ao código
- Changelog atualizado

## Proibido
- Docs desatualizadas
- Docs fora do repositório
""",

    "security.rules.md": """# Security Rules

**Versão:** 1.0.0 | **Status:** Oficial

## Obrigatório
- Validação de entrada
- Sanitização de saída
- Princípio do menor privilégio

## Proibido
- Segredos em código
- Dependências sem auditoria
- Endpoints sem auth
""",

    "coding.rules.md": """# Coding Rules

**Versão:** 1.0.0 | **Status:** Oficial

## Obrigatório
- Funções pequenas (<50 linhas)
- DRY quando aplicável
- Tratamento explícito de erros

## Proibido
- Código morto
- Comentários óbvios
- Magic numbers
""",

    "versioning.rules.md": """# Versioning Rules

**Versão:** 1.0.0 | **Status:** Oficial

## Convenção
Semver: MAJOR.MINOR.PATCH

## Regras
- MAJOR: breaking changes
- MINOR: features
- PATCH: fixes
""",

    "quality.rules.md": """# Quality Rules

**Versão:** 1.0.0 | **Status:** Oficial

## Obrigatório
- Lint passa
- Cobertura mínima
- Sem warnings

## Proibido
- TODO sem issue
- Código sem testes
""",

    "dependency.rules.md": """# Dependency Rules

**Versão:** 1.0.0 | **Status:** Oficial

## Obrigatório
- Lockfile versionado
- Auditoria regular
- Licenças compatíveis

## Proibido
- Dependências não utilizadas
- Versões com vulnerabilidades
""",

    "token.rules.md": """# Token Rules

**Versão:** 1.0.0 | **Status:** Oficial

## Obrigatório
- Respostas objetivas
- Sem contextualização desnecessária
- Reutilizar docs existentes

## Proibido
- Repetição de informação
- Explicações redundantes
- Exemplos não essenciais
""",

    "review.rules.md": """# Review Rules

**Versão:** 1.0.0 | **Status:** Oficial

## Obrigatório
- Mínimo 2 aprovações
- Critérios objetivos
- Evidências anexadas

## Proibido
- Aprovação sem teste
- LGTM genérico
""",
}

WORKFLOWS = {
    "build-framework.md": """# Build Framework Workflow

**Versão:** 1.0.0 | **Status:** Oficial

## Passos
1. Chief Architect aprova escopo
2. Solution Architect define solução
3. Core Architect define Core
4. Engine Architects implementam
5. Reviewer valida
6. Quality Architect audita
7. Release Architect publica
""",

    "create-engine.md": """# Create Engine Workflow

**Versão:** 1.0.0 | **Status:** Oficial

## Passos
1. Especificação aprovada
2. Contratos definidos
3. Implementação isolada
4. Testes obrigatórios
5. Documentação
6. Review
7. Integração
""",

    "create-module.md": """# Create Module Workflow

**Versão:** 1.0.0 | **Status:** Oficial

## Passos
1. Spec do módulo
2. Padrões aplicados
3. Implementação
4. Testes
5. Docs
6. Review
7. Merge
""",

    "update-architecture.md": """# Update Architecture Workflow

**Versão:** 1.0.0 | **Status:** Oficial

## Passos
1. Necessidade identificada
2. RFC redigida
3. ADR proposto
4. Review
5. Aprovação Chief
6. Atualização de docs
7. Comunicação
""",

    "review-module.md": """# Review Module Workflow

**Versão:** 1.0.0 | **Status:** Oficial

## Passos
1. PR aberto
2. CI passa
3. Reviewer técnico
4. Quality Architect
5. Security Architect (se aplicável)
6. Aprovação final
7. Merge
""",

    "release-version.md": """# Release Version Workflow

**Versão:** 1.0.0 | **Status:** Oficial

## Passos
1. Versão definida (Semver)
2. Changelog atualizado
3. Build validado
4. Testes de regressão
5. Aprovação Release
6. Tag criada
7. Publicação
""",

    "audit-framework.md": """# Audit Framework Workflow

**Versão:** 1.0.0 | **Status:** Oficial

## Passos
1. Escopo definido
2. Checklist aplicado
3. Evidências coletadas
4. Relatório gerado
5. Ações corretivas
6. Validação
7. Fechamento
""",
}

MEMORY = {
    "framework-memory.md": """# Framework Memory

**Versão:** 1.0.0 | **Status:** Oficial

## Estado Atual
- Versão: 1.0.0
- 23 agentes oficiais
- 22 skills oficiais
- 11 regras oficiais

## Histórico
- 2026-07-27: Estrutura inicial
""",

    "architecture-memory.md": """# Architecture Memory

**Versão:** 1.0.0 | **Status:** Oficial

## Decisões Ativas
- ADR-001: Estrutura modular
- ADR-002: Skills versionadas
""",

    "decisions.md": """# Decisions Log

**Versão:** 1.0.0 | **Status:** Oficial

## Formato
- ID
- Data
- Decisão
- Contexto
- Consequências

## Entradas
- ADR-001: Estrutura modular
""",

    "glossary.md": """# Glossary

**Versão:** 1.0.0 | **Status:** Oficial

## Termos
- **Skill**: Capacidade reutilizável
- **Agent**: Entidade com responsabilidade
- **Engine**: Módulo técnico
- **Core**: Núcleo imutável
""",

    "roadmap.md": """# Roadmap

**Versão:** 1.0.0 | **Status:** Oficial

## v1.0.0 (Atual)
- Estrutura base
- 23 agentes
- 22 skills

## v1.1.0 (Próximo)
- Skills avançadas
- Integração CI
""",

    "conventions.md": """# Conventions

**Versão:** 1.0.0 | **Status:** Oficial

## Código
- Indentação: 2 espaços
- Encoding: UTF-8
- Line ending: LF

## Docs
- Markdown
- Hierarquia H1-H6
""",
}

POLICIES = {
    "architecture-policy.md": """# Architecture Policy

**Versão:** 1.0.0 | **Status:** Oficial

## Princípios
- Architecture First
- Documentação obrigatória
- Decisões registradas

## Aplicação
Toda alteração arquitetural requer ADR.
""",

    "security-policy.md": """# Security Policy

**Versão:** 1.0.0 | **Status:** Oficial

## Princípios
- Security by design
- Zero trust
- Auditoria contínua

## Aplicação
Skill `security-auditor` obrigatória em releases.
""",

    "privacy-policy.md": """# Privacy Policy

**Versão:** 1.0.0 | **Status:** Oficial

## Princípios
- LGPD
- Privacy by design
- Minimização

## Aplicação
DPIA obrigatório em features com dados pessoais.
""",

    "token-policy.md": """# Token Policy

**Versão:** 1.0.0 | **Status:** Oficial

## Princípios
- Economia máxima
- Respostas objetivas
- Reuso de docs

## Aplicação
Skill `token-efficient-coder` como padrão.
""",

    "documentation-policy.md": """# Documentation Policy

**Versão:** 1.0.0 | **Status:** Oficial

## Princípios
- Doc junto ao código
- Versionamento
- Atualização contínua

## Aplicação
README obrigatório em todo módulo.
""",

    "review-policy.md": """# Review Policy

**Versão:** 1.0.0 | **Status:** Oficial

## Princípios
- Mínimo 2 aprovações
- Critérios objetivos
- Evidências obrigatórias

## Aplicação
Skill `review` em todo PR.
""",

    "release-policy.md": """# Release Policy

**Versão:** 1.0.0 | **Status:** Oficial

## Princípios
- Semver
- Changelog
- Rollback testado

## Aplicação
Skill `release` em toda publicação.
""",
}

TEMPLATES = {
    "architecture.template.md": """# Architecture Template

**Versão:** 1.0.0 | **Status:** Oficial

## Estrutura
1. Contexto
2. Restrições
3. Decisão
4. Alternativas
5. Consequências
""",

    "specification.template.md": """# Specification Template

**Versão:** 1.0.0 | **Status:** Oficial

## Estrutura
1. Objetivo
2. Escopo
3. Fora de escopo
4. Requisitos
5. Critérios de aceite
""",

    "engine.template.md": """# Engine Template

**Versão:** 1.0.0 | **Status:** Oficial

## Estrutura
1. Propósito
2. Interfaces
3. Dependências
4. Limitações
""",

    "protocol.template.md": """# Protocol Template

**Versão:** 1.0.0 | **Status:** Oficial

## Estrutura
1. Mensagens
2. Estados
3. Erros
""",

    "api.template.md": """# API Template

**Versão:** 1.0.0 | **Status:** Oficial

## Estrutura
1. Endpoints
2. Schemas
3. Erros
4. Autenticação
""",

    "database.template.md": """# Database Template

**Versão:** 1.0.0 | **Status:** Oficial

## Estrutura
1. Tabelas
2. Relacionamentos
3. Índices
4. Migrações
""",

    "workflow.template.md": """# Workflow Template

**Versão:** 1.0.0 | **Status:** Oficial

## Estrutura
1. Trigger
2. Passos
3. Outputs
4. Validação
""",

    "adr.template.md": """# ADR Template

**Versão:** 1.0.0 | **Status:** Oficial

## Estrutura
1. ID
2. Status
3. Contexto
4. Decisão
5. Consequências
""",

    "rfc.template.md": """# RFC Template

**Versão:** 1.0.0 | **Status:** Oficial

## Estrutura
1. Resumo
2. Motivação
3. Design
4. Alternativas
5. Impacto
""",

    "test.template.md": """# Test Template

**Versão:** 1.0.0 | **Status:** Oficial

## Estrutura
1. Cenário
2. Setup
3. Execução
4. Asserts
""",
}

SKILLS = {
    "core": {
        "00-brain-skill.md": """# Brain Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Core

## Capacidade
Orquestração cognitiva central. Ativa skills conforme contexto.

## Inputs
- Estado de contexto
- Skills disponíveis
- Prioridades

## Outputs
- Skill selecionada
- Roteamento
- Estado atualizado

## Invariantes
- Single skill ativa por vez
- Contexto mínimo
- Rastreabilidade

## Interfaces
- Todas as skills
- Context Engine
""",

        "01-knowledge-skill.md": """# Knowledge Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Core

## Capacidade
Gestão de conhecimento versionado.

## Inputs
- Documentos
- Queries
- Índices

## Outputs
- Conhecimento recuperado
- Fontes citadas
- Recomendações

## Invariantes
- Fontes oficiais
- Sem inferência
- Versionamento
""",

        "02-memory-skill.md": """# Memory Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Core

## Capacidade
Memória persistente entre sessões.

## Inputs
- Estado atual
- Histórico
- Contexto

## Outputs
- Snapshot
- Recuperação
- Histórico

## Invariantes
- Imutável após commit
- Recuperação determinística
""",

        "03-reasoning-skill.md": """# Reasoning Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Core

## Capacidade
Raciocínio estruturado e auditável.

## Inputs
- Problema
- Premissas
- Restrições

## Outputs
- Cadeia lógica
- Conclusão
- Alternativas

## Invariantes
- Lógica explícita
- Premissas declaradas
""",
    },
    "discovery": {
        "04-discovery-skill.md": """# Discovery Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Discovery

## Capacidade
Descoberta estruturada de informações.

## Inputs
- Escopo
- Critérios
- Fontes

## Outputs
- Inventário
- Mapa
- Recomendações

## Invariantes
- Fontes oficiais
- Reproduzibilidade
""",

        "05-index-skill.md": """# Index Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Discovery

## Capacidade
Indexação estruturada.

## Inputs
- Documentos
- Metadados
- Esquemas

## Outputs
- Índices
- Referências
- Mapas

## Invariantes
- Atualização contínua
- Busca determinística
""",

        "06-graph-skill.md": """# Graph Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Discovery

## Capacidade
Grafos de conhecimento.

## Inputs
- Entidades
- Relacionamentos
- Ontologias

## Outputs
- Grafos
- Queries
- Visualizações

## Invariantes
- Ontologias versionadas
- Tipagem explícita
""",
    },
    "context": {
        "07-context-skill.md": """# Context Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Context

## Capacidade
Gestão de contexto entre agentes.

## Inputs
- Estado
- Tokens
- Prioridades

## Outputs
- Contexto empacotado
- Resumos
- Decisões

## Invariantes
- Mínimo viável
- Auditável
""",

        "08-token-economy-skill.md": """# Token Economy Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Context

## Capacidade
Economia máxima de tokens.

## Inputs
- Conteúdo
- Contexto
- Prioridades

## Outputs
- Versão compacta
- Resumo executivo
- Referências

## Invariantes
- Sem perda de informação essencial
- Reuso de docs
- Respostas objetivas
""",
    },
    "governance": {
        "09-security-skill.md": """# Security Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Governance

## Capacidade
Aplicação de segurança.

## Inputs
- Código
- Arquitetura
- Configurações

## Outputs
- Análise
- Mitigações
- Gates

## Invariantes
- Security by design
- Auditoria contínua
""",

        "10-privacy-skill.md": """# Privacy Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Governance

## Capacidade
Privacidade e LGPD.

## Inputs
- Fluxos de dados
- Bases legais
- Retenção

## Outputs
- DPIA
- Mecanismos
- Compliance

## Invariantes
- Privacy by design
- Minimização
""",

        "11-quality-skill.md": """# Quality Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Governance

## Capacidade
Garantia de qualidade.

## Inputs
- Código
- Testes
- Métricas

## Outputs
- Gates
- Relatórios
- Planos

## Invariantes
- Cobertura mínima
- Lint passa
""",

        "12-review-skill.md": """# Review Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Governance

## Capacidade
Revisão técnica.

## Inputs
- PR
- Spec
- Critérios

## Outputs
- Aprovação
- Mudanças
- Relatório

## Invariantes
- Mínimo 2 aprovações
- Evidências
""",
    },
    "engineering": {
        "13-architecture-skill.md": """# Architecture Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Decisões arquiteturais.

## Inputs
- Requisitos
- Restrições
- Contexto

## Outputs
- Decisão
- ADR
- Trade-offs

## Invariantes
- Documentação
- Aprovação Chief
""",

        "14-database-skill.md": """# Database Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Modelagem de dados.

## Inputs
- Requisitos
- Volume
- Acesso

## Outputs
- Esquemas
- Índices
- Migrações

## Invariantes
- Integridade
- Backups
""",

        "15-api-skill.md": """# API Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Design de APIs.

## Inputs
- Casos de uso
- Consumidores
- Restrições

## Outputs
- Especificação
- Contratos
- Versão

## Invariantes
- RESTful
- OpenAPI
- Versionamento
""",

        "16-performance-skill.md": """# Performance Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Otimização de performance.

## Inputs
- SLAs
- Métricas
- Gargalos

## Outputs
- Budgets
- Planos
- Dashboards

## Invariantes
- Medir antes
- Core Web Vitals
""",

        "17-documentation-skill.md": """# Documentation Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Documentação técnica.

## Inputs
- Código
- Decisões
- APIs

## Outputs
- Docs
- Diagramas
- Tutoriais

## Invariantes
- Junto ao código
- Versionada
""",

        "22-secure-dev-framework.md": """# Secure Dev Framework

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Framework principal — ativa todas as skills de segurança em conjunto.

## Skills Ativadas
- `security-auditor`
- `security-report`
- `token-efficient-coder`
- `09-security-skill`
- `10-privacy-skill`

## Inputs
- Código completo
- Configurações
- Arquitetura

## Outputs
- Análise integrada
- Relatórios consolidados
- Gates de segurança

## Invariantes
- Ativação simultânea
- Sem conflito entre skills
- Rastreabilidade total
- Zero trust aplicado

## Interfaces
- Todas as skills de segurança
- Security Architect
- Release Architect
""",

        "23-token-efficient-coder.md": """# Token Efficient Coder

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Economia máxima de tokens + respostas 100% objetivas (sem contextualização).

## Princípios
- Resposta direta
- Sem introdução
- Sem despedida
- Sem repetição
- Reuso de docs existentes
- Bullet points quando possível
- Código sem comentários óbvios

## Inputs
- Tarefa
- Contexto mínimo
- Restrições

## Outputs
- Código compacto
- Resposta objetiva
- Sem verbosidade

## Invariantes
- Zero contextualização desnecessária
- Respostas em formato mínimo viável
- Cada token é auditado
- Sem explicações redundantes

## Formato de Resposta
```
[STATUS]
- Ação executada

[RESULTADO]
- Output direto

[VALIDAÇÃO]
- Evidência objetiva
```

## Interfaces
- Todas as skills
- Context Engine
""",

        "24-security-auditor.md": """# Security Auditor

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Análise de segurança de alto nível (CSRF, cookies, headers, XSS, SQLi, vazamento de dados, mobile, etc.).

## Vetores Analisados
- CSRF (Cross-Site Request Forgery)
- Cookies (Secure, HttpOnly, SameSite)
- Headers (CSP, HSTS, X-Frame-Options, etc.)
- XSS (Reflected, Stored, DOM-based)
- SQLi (Union, Boolean, Time-based)
- Vazamento de dados (Logs, Errors, Stack traces)
- Mobile (Deep links, Insecure storage, Certificate pinning)
- Autenticação (JWT, Session, OAuth)
- Autorização (IDOR, BOLA, Privilege escalation)
- Criptografia (TLS, Hash, Salt)

## Inputs
- Código fonte
- Endpoints
- Configurações
- Dependências

## Outputs
- Findings categorizados (Critical/High/Medium/Low)
- CVSS scores
- Recomendações de mitigação
- Evidências (PoC)

## Invariantes
- Sem falso negativo crítico
- Evidência obrigatória
- Reproduzibilidade
- OWASP Top 10 coberto

## Checklist
```
[ ] CSRF tokens validados
[ ] Cookies com flags corretos
[ ] Headers de segurança presentes
[ ] Input sanitizado
[ ] Output encoded
[ ] Queries parametrizadas
[ ] Logs sem dados sensíveis
[ ] Mobile storage seguro
[ ] Auth robusta
[ ] Authz granular
[ ] TLS 1.2+ obrigatório
[ ] Hash com salt
```

## Interfaces
- `security-report` (gera relatório)
- `secure-dev-framework` (orquestra)
- Security Architect
""",

        "25-security-report.md": """# Security Report

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Geração de relatórios profissionais de segurança.

## Inputs
- Findings do `security-auditor`
- Contexto do projeto
- Audiência (executiva/técnica)

## Outputs
- Relatório executivo
- Relatório técnico
- Plano de remediação
- Métricas de risco

## Estrutura do Relatório
```
1. Resumo Executivo
   - Score de risco
   - Findings críticos
   - Status geral

2. Escopo
   - Sistemas analisados
   - Período
   - Metodologia

3. Findings
   - ID
   - Severidade
   - Descrição
   - Evidência
   - Impacto
   - Recomendação
   - CVSS

4. Plano de Remediação
   - Prioridade
   - Esforço
   - Responsável
   - Prazo

5. Anexos
   - PoCs
   - Logs
   - Referências
```

## Invariantes
- Linguagem objetiva
- Evidências anexadas
- Reproduzibilidade
- Sem omissão de findings críticos

## Formatos Suportados
- Markdown
- HTML
- PDF
- JSON

## Interfaces
- `security-auditor` (recebe findings)
- `secure-dev-framework` (orquestra)
- Security Architect
- Release Architect
""",
    },
    "delivery": {
        "18-implementation-skill.md": """# Implementation Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Implementação controlada.

## Inputs
- Spec
- Padrões
- Contratos

## Outputs
- Código
- PRs
- Builds

## Invariantes
- TDD
- Commits semânticos
""",

        "19-testing-skill.md": """# Testing Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Estratégia de testes.

## Inputs
- Requisitos
- Código
- Riscos

## Outputs
- Plano
- Suítes
- Relatórios

## Invariantes
- Pirâmide
- CI
""",

        "20-release-skill.md": """# Release Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Gestão de releases.

## Inputs
- Builds
- Aprovações
- Riscos

## Outputs
- Versões
- Notas
- Rollbacks

## Invariantes
- Semver
- Changelog
""",

        "21-governance-skill.md": """# Governance Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Governança técnica.

## Inputs
- Políticas
- Processos
- Auditorias

## Outputs
- Compliance
- Relatórios
- Gates

## Invariantes
- Contínuo
- Versionado
""",
    },
}

SKILLS_README = """# Skills — Índice Oficial

**Versão:** 1.0.0 | **Status:** Oficial

## Categorias

### Core (4)
- `00-brain-skill.md` — Orquestração cognitiva
- `01-knowledge-skill.md` — Gestão de conhecimento
- `02-memory-skill.md` — Memória persistente
- `03-reasoning-skill.md` — Raciocínio estruturado

### Discovery (3)
- `04-discovery-skill.md` — Descoberta
- `05-index-skill.md` — Indexação
- `06-graph-skill.md` — Grafos

### Context (2)
- `07-context-skill.md` — Contexto
- `08-token-economy-skill.md` — Economia de tokens

### Governance (4)
- `09-security-skill.md` — Segurança
- `10-privacy-skill.md` — Privacidade
- `11-quality-skill.md` — Qualidade
- `12-review-skill.md` — Revisão

### Engineering (10)
- `13-architecture-skill.md` — Arquitetura
- `14-database-skill.md` — Banco de dados
- `15-api-skill.md` — APIs
- `16-performance-skill.md` — Performance
- `17-documentation-skill.md` — Documentação
- `22-secure-dev-framework.md` — Framework de segurança integrado
- `23-token-efficient-coder.md` — Codificação econômica
- `24-security-auditor.md` — Auditoria de segurança
- `25-security-report.md` — Relatórios de segurança

### Delivery (4)
- `18-implementation-skill.md` — Implementação
- `19-testing-skill.md` — Testes
- `20-release-skill.md` — Releases
- `21-governance-skill.md` — Governança

## Total: 27 skills oficiais

## Convenção
- `XX-nome-skill.md`
- XX = número sequencial
- nome-skill = kebab-case
"""

SKILL_TEMPLATE = """# [Nome da Skill]

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** [Core/Discovery/Context/Governance/Engineering/Delivery]

## Capacidade
[Descrição objetiva da capacidade]

## Inputs
- [Input 1]
- [Input 2]

## Outputs
- [Output 1]
- [Output 2]

## Invariantes
- [Regra 1]
- [Regra 2]

## Interfaces
- [Skill/Engine relacionada]
"""

# ============================================================
# EXECUÇÃO
# ============================================================

def write(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def fill_agents():
    base = ROOT / ".ai" / "agents"
    for name, content in AGENTS.items():
        write(base / name, content)

def fill_prompts():
    base = ROOT / ".ai" / "prompts"
    for name, content in PROMPTS.items():
        write(base / name, content)

def fill_rules():
    base = ROOT / ".ai" / "rules"
    for name, content in RULES.items():
        write(base / name, content)

def fill_workflows():
    base = ROOT / ".ai" / "workflows"
    for name, content in WORKFLOWS.items():
        write(base / name, content)

def fill_memory():
    base = ROOT / ".ai" / "memory"
    for name, content in MEMORY.items():
        write(base / name, content)

def fill_policies():
    base = ROOT / ".ai" / "policies"
    for name, content in POLICIES.items():
        write(base / name, content)

def fill_templates():
    base = ROOT / ".ai" / "templates"
    for name, content in TEMPLATES.items():
        write(base / name, content)

def fill_skills():
    base = ROOT / ".ai" / "skills"
    write(base / "README.md", SKILLS_README)
    write(base / "SKILL.template.md", SKILL_TEMPLATE)
    for category, files in SKILLS.items():
        for name, content in files.items():
            write(base / category / name, content)

if __name__ == "__main__":
    fill_agents()
    fill_prompts()
    fill_rules()
    fill_workflows()
    fill_memory()
    fill_policies()
    fill_templates()
    fill_skills()
    print("All official content filled.")
