# CI/CD Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Pipelines de CI/CD: build, test, deploy automatizados.

## Princípios
- Pipelines como código
- Gates de qualidade obrigatórios
- Deploy incremental
- Rollback automatizado

## Inputs
- Código fonte
- Testes
- Ambientes (dev, staging, prod)

## Outputs
- Pipeline executado
- Artefatos publicados
- Deploy realizado

## Ferramentas

| Ferramenta | Uso |
|---|---|
| GitHub Actions | GitHub-native |
| GitLab CI | GitLab-native |
| Jenkins | Self-hosted, flexível |
| CircleCI | SaaS |
| GitLab CI/CD | Integrado |

## Pipeline Típico

```yaml
stages:
  - lint
  - test
  - build
  - deploy-staging
  - deploy-prod

lint:
  stage: lint
  script: ruff check .

test:
  stage: test
  script: pytest --cov

build:
  stage: build
  script: docker build -t app:$CI_COMMIT_SHA .

deploy-staging:
  stage: deploy-staging
  script: kubectl apply -f k8s/staging/

deploy-prod:
  stage: deploy-prod
  script: kubectl apply -f k8s/prod/
  when: manual
```

## Invariantes
- Testes bloqueiam merge
- Build reproduzível
- Deploy idempotente
- Rollback testado
- Secrets via vault

## Interfaces
- Docker Skill
- Kubernetes Skill
- Testing Architect
- Release Architect

## Ver Também

- `55-docker-skill.md`
- `56-kubernetes-skill.md`
- `20-release-skill.md`
