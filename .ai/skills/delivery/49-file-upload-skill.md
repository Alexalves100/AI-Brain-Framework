# File Upload Skill

**Versão:** 1.0.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Upload seguro de arquivos: validação, storage, CDN.

## Princípios
- Validação rigorosa (tipo, tamanho)
- Storage isolado
- URLs assinadas (não permanentes)
- Scan de malware

## Inputs
- Arquivo do usuário
- Tipo esperado
- Tamanho máximo
- Visibilidade

## Outputs
- Arquivo armazenado
- URL de acesso (temporária ou permanente)
- Metadados (mime, size, hash)

## Validação

```python
# Tipo MIME (não confiar em extensão)
- Whitelist: image/jpeg, image/png, application/pdf
- Magic bytes check (primeiros bytes do arquivo)

# Tamanho
- Max: 10MB para imagens
- Max: 100MB para vídeos

# Nome do arquivo
- Sanitizar (remover ../, caracteres especiais)
- Gerar UUID para storage
```

## Storage

| Storage | Uso |
|---|---|
| S3 | AWS-native |
| GCS | GCP-native |
| Azure Blob | Azure-native |
| MinIO | Self-hosted S3-compatible |
| Cloudflare R2 | S3-compatible, sem egress |

## Padrões

```python
# Upload direto (cliente → storage)
1. Cliente pede URL assinada
2. Cliente faz PUT direto no storage
3. Cliente notifica backend
4. Backend valida e persiste metadata

# Upload via backend
1. Cliente envia arquivo
2. Backend valida
3. Backend salva no storage
4. Backend retorna URL
```

## Invariantes
- Validação dupla (MIME + magic bytes)
- URLs assinadas com expiração
- Scan de malware (ClamAV)
- Limite de tamanho aplicado
- Logs de upload

## Ver Também

- `15-api-skill.md`
- `09-security-skill.md`
- `10-privacy-skill.md`
- Limite de tamanho aplicado
- Logs de upload

## Interfaces
- Security Architect
- API Skill
- Privacy Architect (LGPD)
- Storage (S3/GCS)
