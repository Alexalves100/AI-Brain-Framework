# Docker Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Containerização de aplicações com Docker: imagens, multi-stage builds, otimização.

## Princípios
- Imagens mínimas (alpine, distroless)
- Multi-stage builds
- Layer caching otimizado
- Sem segredos em imagens

## Inputs
- Aplicação a containerizar
- Runtime necessário
- Dependências

## Outputs
- Dockerfile otimizado
- Imagem Docker
- docker-compose.yml (se aplicável)

## Boas Práticas

```dockerfile
# Multi-stage build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user

FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
WORKDIR /app
COPY . .
USER nobody
EXPOSE 8000
CMD ["python", "app.py"]
```

## Invariantes
- Imagem < 500MB quando possível
- USER não-root
- HEALTHCHECK definido
- Sem segredos hardcoded
- .dockerignore presente

## Otimizações

```dockerfile
# Layer caching
COPY requirements.txt .  # Cache de deps separado
RUN pip install
COPY . .                 # Código muda mais

# Multi-arch
FROM --platform=linux/amd64 python:3.11-slim

# Labels
LABEL version="1.0.0"
LABEL maintainer="team@example.com"
```

## Interfaces
- Kubernetes Skill
- CI/CD Skill
- Security Architect
- Performance Architect

## Ver Também

- `56-kubernetes-skill.md`
- `57-cicd-skill.md`
- `58-iac-skill.md`
