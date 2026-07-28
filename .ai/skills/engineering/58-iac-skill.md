# Infrastructure as Code Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Engineering

## Capacidade
Gestão de infraestrutura via código: Terraform, Pulumi, CloudFormation.

## Princípios
- Infra como código versionado
- State management
- Plan antes de apply
- Módulos reutilizáveis

## Inputs
- Recursos a provisionar
- Provider (AWS, GCP, Azure)
- Variáveis

## Outputs
- Código IaC
- Plan de mudanças
- Recursos provisionados

## Ferramentas

| Ferramenta | Provider |
|---|---|
| Terraform | Multi-cloud |
| Pulumi | Multi-cloud |
| CloudFormation | AWS |
| CDK | AWS |
| Deployment Manager | GCP |
| ARM Templates | Azure |

## Exemplo Terraform

```hcl
resource "aws_s3_bucket" "data" {
  bucket = "my-data-bucket"
  
  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration {
    status = "Enabled"
  }
}
```

## Invariantes
- State em backend remoto (S3, GCS)
- Plan revisado antes de apply
- Módulos reutilizáveis
- Variáveis em arquivos separados
- Outputs documentados

## Interfaces
- Docker Skill
- Kubernetes Skill
- Security Architect
- FinOps Architect

## Ver Também

- `55-docker-skill.md`
- `56-kubernetes-skill.md`
- `57-cicd-skill.md`
