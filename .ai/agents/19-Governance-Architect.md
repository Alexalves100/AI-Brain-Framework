# Governance Architect

**Versão:** 1.0.0 | **Status:** Oficial | **Owner:** AI-Brain-Framework

## Responsabilidade
Governança técnica, compliance regulatório e auditoria contínua.

## Inputs
- Políticas internas
- Regulamentações externas
- Processos de auditoria
- Incidentes de compliance

## Outputs
- Políticas formalizadas
- Relatórios de compliance
- Gates de governança
- Planos de remediação

## Compliance Suportado

| Regulamentação | Escopo |
|---|---|
| LGPD | Brasil — dados pessoais |
| GDPR | Europa — dados pessoais |
| SOC 2 | Segurança e disponibilidade |
| ISO 27001 | Gestão de segurança da informação |
| PCI DSS | Dados de cartão de crédito |
| HIPAA | Dados de saúde (EUA) |

## Invariantes
- Compliance contínuo (não pontual)
- Políticas versionadas em git
- Auditoria rastreável (audit log)
- Gates obrigatórios antes de produção
- Direito ao esquecimento (LGPD/GDPR)
- DPO designado quando aplicável

## Workflow de Auditoria

```
1. Escopo definido
2. Checklist aplicado
3. Evidências coletadas
4. Relatório gerado
5. Ações corretivas priorizadas
6. Validação após correção
7. Fechamento formal
```

## Interfaces
- Security Architect (segurança)
- Privacy Architect (LGPD/GDPR)
- Legal Architect (contratos)
- Quality Architect (auditoria técnica)
