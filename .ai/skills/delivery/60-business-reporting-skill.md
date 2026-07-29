# Business & Financial Reporting Skill

**Versão:** 1.1.0 | **Status:** Oficial | **Categoria:** Delivery

## Capacidade
Geração de relatórios financeiros, comerciais, DRE Gerencial, dashboards de KPIs e exportações visuais para aplicações Web, ERPs, CRMs e E-commerce.

## Incorporação de Padrões das Skills Globais
- **`kpi-dashboard-design`**: Estrutura hierárquica de KPIs (Executivo, Tático, Operacional) e SMART KPIs.
- **`billing-automation`**: Métricas de faturamento recorrente (MRR/ARR), ciclo de billing e taxa de inadimplência (`dunning_rate`).
- **`startup-financial-modeling`**: Demonstração do Resultado do Exercício (DRE Gerencial) e Fluxo de Caixa Projetado.
- **`sales-automator`**: Análise de Ticket Médio (AOV) e comissões por vendedor.

## Inputs
- `report_type`: Tipo de relatório (`accounts_payable_receivable`, `sales_commission`, `revenue`, `invoices`, `dre`, `kpi_metrics`, `html_dashboard`, `summary`)
- `period`: Período de agregação (`day`, `week`, `month`, `custom`)
- `data`: Dataset estruturado com transações, assinaturas, notas fiscais, contas e vendas.

## Outputs
- Sumarização financeira e comercial (totais, saldos, comissões, AOV, MRR).
- DRE Gerencial de Receita Bruta até Lucro Operacional Líquido.
- Renderizador de Dashboard HTML/CSS responsivo integrado aos `CSSTokens`.
- Formatos de exportação: JSON, CSV e HTML/CSS pronto para impressão/PDF.

## Invariantes
- Precisão monetária de 2 casas decimais.
- Cálculos transparentes de margem de lucro e deduções.
- Conformidade visual acessível (WCAG) no dashboard HTML.

## Ver Também
- `business_reporting.py` (Engine executável Python)
- `14-database-skill.md`
- `25-security-report.md`
