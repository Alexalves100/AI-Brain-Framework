# Kubernetes Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Orquestração de containers com Kubernetes: deployments, services, ingress.

## Princípios
- Declarativo (YAML)
- Auto-scaling
- Self-healing
- Rolling updates

## Inputs
- Imagem Docker
- Requisitos de recursos
- Networking

## Outputs
- Manifests YAML
- Deployments
- Services
- Ingress

## Recursos Principais

```yaml
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:1.0.0
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
```

## Invariantes
- Resource limits definidos
- Health checks obrigatórios
- Secrets via Secret/External Secrets
- Network Policies restritivas
- Pod Disruption Budget

## Interfaces
- Docker Skill
- CI/CD Skill
- SRE Architect
- Security Architect

## Ver Também

- `55-docker-skill.md`
- `57-cicd-skill.md`
- `58-iac-skill.md`
