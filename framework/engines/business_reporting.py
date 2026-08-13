"""
Business Reporting Engine.
Processa datasets comerciais e financeiros para geração de relatórios gerenciais,
DRE Gerencial, KPIs comerciais (Ticket Médio/AOV), MRR/ARR, Dashboard HTML responsivo
e suporte nativo a impressão/geração de PDF (A4 Print-Friendly).
"""
from datetime import datetime, timezone
from typing import Any, Dict

from ..core import Context, Skill, SkillResult, SkillStatus
from ..standards import CSSTokens


class BusinessReportingEngine(Skill):
    name = "business_reporting"
    version = "1.2.0"
    category = "delivery"
    description = "Gera relatórios comerciais, DRE gerencial, KPIs de vendas, Dashboard HTML e relatórios para PDF"

    def run(self, context: Context) -> SkillResult:
        report_type = context.get("report_type", "summary")
        period = context.get("period", "month")  # day, week, month, custom
        data = context.get("data", {})
        auto_print = context.get("auto_print", False)

        if report_type == "accounts_payable_receivable":
            report = self.generate_accounts_report(data)
        elif report_type == "sales_commission":
            report = self.generate_sales_commission_report(data)
        elif report_type == "revenue":
            report = self.generate_revenue_report(data, period)
        elif report_type == "invoices":
            report = self.generate_invoices_report(data)
        elif report_type == "dre":
            report = self.generate_dre_report(data)
        elif report_type == "kpi_metrics":
            report = self.generate_kpi_dashboard_metrics(data)
        elif report_type == "html_dashboard":
            report = {"html": self.render_html_dashboard(data, auto_print=auto_print)}
        elif report_type == "pdf_printable":
            report = {"html": self.render_html_dashboard(data, auto_print=True)}
        else:
            report = self.generate_summary_dashboard(data)

        context.set("report_result", report)

        return SkillResult(
            status=SkillStatus.SUCCESS,
            output=report,
            metadata={"engine": "business_reporting", "type": report_type, "period": period}
        )

    def generate_accounts_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera relatório de Contas a Pagar vs Contas a Receber."""
        payables = data.get("payables", [])
        receivables = data.get("receivables", [])

        total_payable = sum(item.get("amount", 0.0) for item in payables)
        total_receivable = sum(item.get("amount", 0.0) for item in receivables)

        overdue_payable = sum(item.get("amount", 0.0) for item in payables if item.get("status") == "overdue")
        overdue_receivable = sum(item.get("amount", 0.0) for item in receivables if item.get("status") == "overdue")

        net_cashflow_projected = total_receivable - total_payable
        dunning_rate = (overdue_receivable / total_receivable * 100) if total_receivable > 0 else 0.0

        return {
            "report_name": "Relatório de Contas a Pagar e Receber",
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_payable": round(total_payable, 2),
                "total_receivable": round(total_receivable, 2),
                "overdue_payable": round(overdue_payable, 2),
                "overdue_receivable": round(overdue_receivable, 2),
                "dunning_rate_pct": round(dunning_rate, 2),
                "net_cashflow_projected": round(net_cashflow_projected, 2),
            },
            "payables_count": len(payables),
            "receivables_count": len(receivables),
        }

    def generate_sales_commission_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera relatório de Vendas, Ticket Médio (AOV) e Comissões."""
        sales = data.get("sales", [])
        commissions_by_seller: Dict[str, Dict[str, float]] = {}

        total_sales_volume = 0.0
        total_commissions = 0.0

        for sale in sales:
            seller = sale.get("seller_name", "Desconhecido")
            amount = sale.get("amount", 0.0)
            rate = sale.get("commission_rate", 0.05)
            commission = amount * rate

            total_sales_volume += amount
            total_commissions += commission

            if seller not in commissions_by_seller:
                commissions_by_seller[seller] = {"total_sales": 0.0, "total_commission": 0.0, "sales_count": 0}

            commissions_by_seller[seller]["total_sales"] += amount
            commissions_by_seller[seller]["total_commission"] += commission
            commissions_by_seller[seller]["sales_count"] += 1

        total_sales_count = len(sales)
        average_order_value = (total_sales_volume / total_sales_count) if total_sales_count > 0 else 0.0

        for metrics in commissions_by_seller.values():
            metrics["total_sales"] = round(metrics["total_sales"], 2)

            metrics["total_commission"] = round(metrics["total_commission"], 2)
            count = metrics["sales_count"]
            metrics["average_order_value"] = round(metrics["total_sales"] / count, 2) if count > 0 else 0.0

        return {
            "report_name": "Relatório de Vendas e Comissões",
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_sales_volume": round(total_sales_volume, 2),
                "total_commissions": round(total_commissions, 2),
                "sales_count": total_sales_count,
                "average_order_value": round(average_order_value, 2),
                "sellers_count": len(commissions_by_seller),
            },
            "sellers_breakdown": commissions_by_seller,
        }

    def generate_revenue_report(self, data: Dict[str, Any], period: str = "month") -> Dict[str, Any]:
        """Gera relatório de Faturamento e estimativas MRR/ARR."""
        transactions = data.get("transactions", [])
        subscriptions = data.get("subscriptions", [])

        total_gross_revenue = sum(t.get("amount", 0.0) for t in transactions if t.get("type") == "income")
        total_deductions = sum(t.get("amount", 0.0) for t in transactions if t.get("type") == "deduction")
        net_revenue = total_gross_revenue - total_deductions

        mrr = sum(sub.get("mrr", 0.0) for sub in subscriptions if sub.get("status") == "active")
        arr = mrr * 12.0

        return {
            "report_name": f"Relatório de Faturamento ({period.capitalize()})",
            "period": period,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "gross_revenue": round(total_gross_revenue, 2),
                "deductions": round(total_deductions, 2),
                "net_revenue": round(net_revenue, 2),
                "mrr": round(mrr, 2),
                "arr": round(arr, 2),
                "transactions_count": len(transactions),
            }
        }

    def generate_invoices_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera relatório de Notas Fiscais Emitidas."""
        invoices = data.get("invoices", [])
        status_counts = {"issued": 0, "cancelled": 0, "pending": 0}
        total_invoice_amount = 0.0

        for inv in invoices:
            status = inv.get("status", "pending")
            status_counts[status] = status_counts.get(status, 0) + 1
            if status == "issued":
                total_invoice_amount += inv.get("amount", 0.0)

        return {
            "report_name": "Relatório de Notas Fiscais Emitidas",
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_issued_amount": round(total_invoice_amount, 2),
                "total_invoices": len(invoices),
                "status_breakdown": status_counts,
            }
        }

    def generate_dre_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera DRE Gerencial (Demonstração do Resultado do Exercício)."""
        rev_summary = self.generate_revenue_report(data)["summary"]
        sales_summary = self.generate_sales_commission_report(data)["summary"]
        acc_summary = self.generate_accounts_report(data)["summary"]

        gross_revenue = rev_summary["gross_revenue"]
        deductions = rev_summary["deductions"]
        net_revenue = gross_revenue - deductions

        commissions = sales_summary["total_commissions"]
        operating_expenses = acc_summary["total_payable"]
        total_costs = commissions + operating_expenses

        net_operating_profit = net_revenue - total_costs
        margin_pct = (net_operating_profit / gross_revenue * 100) if gross_revenue > 0 else 0.0

        return {
            "report_name": "Demonstração do Resultado do Exercício (DRE Gerencial)",
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "dre": {
                "1_receita_bruta": round(gross_revenue, 2),
                "2_deducoes_e_impostos": round(deductions, 2),
                "3_receita_liquida": round(net_revenue, 2),
                "4_comissoes_de_vendas": round(commissions, 2),
                "5_despesas_operacionais": round(operating_expenses, 2),
                "6_custos_totais": round(total_costs, 2),
                "7_lucro_operacional_liquido": round(net_operating_profit, 2),
                "8_margem_operacional_pct": round(margin_pct, 2),
            }
        }

    def generate_kpi_dashboard_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna conjunto consolidado de métricas de KPI para dashboards executivos."""
        dre = self.generate_dre_report(data)["dre"]
        sales = self.generate_sales_commission_report(data)["summary"]
        accounts = self.generate_accounts_report(data)["summary"]
        revenue = self.generate_revenue_report(data)["summary"]

        return {
            "report_name": "Resumo de KPIs Executivos",
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "kpis": {
                "gross_revenue": dre["1_receita_bruta"],
                "net_profit": dre["7_lucro_operacional_liquido"],
                "margin_pct": dre["8_margem_operacional_pct"],
                "average_order_value": sales["average_order_value"],
                "total_sales_volume": sales["total_sales_volume"],
                "mrr": revenue["mrr"],
                "arr": revenue["arr"],
                "overdue_receivables": accounts["overdue_receivable"],
                "dunning_rate_pct": accounts["dunning_rate_pct"],
            }
        }

    def generate_summary_dashboard(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera painel consolidado com todos os indicadores gerenciais."""
        return {
            "report_name": "Painel Consolidado de Negócios",
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "kpis": self.generate_kpi_dashboard_metrics(data)["kpis"],
            "dre": self.generate_dre_report(data)["dre"],
            "accounts": self.generate_accounts_report(data)["summary"],
            "sales": self.generate_sales_commission_report(data)["summary"],
            "invoices": self.generate_invoices_report(data)["summary"],
        }

    def render_html_dashboard(self, data: Dict[str, Any], auto_print: bool = False) -> str:
        """Renderiza uma página HTML/CSS responsiva com suporte a impressão e exportação em PDF (A4 Print-Friendly)."""
        summary = self.generate_summary_dashboard(data)
        kpis = summary["kpis"]
        dre = summary["dre"]
        css_vars = CSSTokens.generate_css_variables("dark")
        font_import = CSSTokens.get_google_fonts_import()

        auto_print_script = "<script>window.onload = function() { window.print(); }</script>" if auto_print else ""

        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel de Relatórios & KPIs - AI-Brain-Framework</title>
    <style>
        {font_import}
        {css_vars}

        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: var(--font-sans);
            background-color: var(--color-bg-primary);
            color: var(--color-text-primary);
            padding: var(--space-xl);
            line-height: 1.5;
        }}
        header {{
            margin-bottom: var(--space-2xl);
            border-bottom: 1px solid var(--color-border);
            padding-bottom: var(--space-md);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        h1 {{ font-family: var(--font-heading); font-size: 1.8rem; color: var(--color-text-primary); }}
        .badge {{ background: var(--color-accent); color: #fff; padding: 0.25rem 0.75rem; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 600; }}
        .btn-print {{
            background-color: var(--color-accent);
            color: #ffffff;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: var(--radius-md);
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .btn-print:hover {{ background-color: var(--color-accent-hover); }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: var(--space-lg);
            margin-bottom: var(--space-2xl);
        }}
        .kpi-card {{
            background: var(--color-bg-surface);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            transition: transform 0.2s, border-color 0.2s;
        }}
        .kpi-card:hover {{ border-color: var(--color-accent); transform: translateY(-2px); }}
        .kpi-title {{ font-size: 0.85rem; color: var(--color-text-secondary); text-transform: uppercase; letter-spacing: 0.05em; }}
        .kpi-value {{ font-family: var(--font-heading); font-size: 1.6rem; font-weight: 700; color: var(--color-text-primary); margin-top: var(--space-xs); }}
        .kpi-subtitle {{ font-size: 0.75rem; color: var(--color-success); margin-top: var(--space-xs); }}

        .table-container {{
            background: var(--color-bg-surface);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            margin-bottom: var(--space-xl);
        }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; }}
        th, td {{ padding: var(--space-sm) var(--space-md); border-bottom: 1px solid var(--color-border); }}
        th {{ color: var(--color-text-secondary); text-transform: uppercase; font-size: 0.75rem; }}
        .text-right {{ text-align: right; }}

        /* Regras de Impressão e PDF (A4 Print-Friendly) */
        @media print {{
            @page {{ size: A4; margin: 1.5cm; }}
            body {{
                background-color: #ffffff !important;
                color: #000000 !important;
                padding: 0 !important;
            }}
            .btn-print, .badge {{ display: none !important; }}
            .kpi-card, .table-container {{
                background: #ffffff !important;
                border: 1px solid #cccccc !important;
                color: #000000 !important;
                box-shadow: none !important;
            }}
            .kpi-value, h1, h2, td, th {{ color: #000000 !important; }}
            table th {{ border-bottom: 2px solid #000000 !important; }}
            table td {{ border-bottom: 1px solid #dddddd !important; }}
        }}
    </style>
</head>
<body>
    <header>
        <div>
            <h1>Painel de Relatórios & KPIs Gerenciais</h1>
            <p style="color: var(--color-text-secondary); font-size: 0.85rem;">AI-Brain-Framework • Atualizado em: {summary['generated_at']}</p>
        </div>
        <div>
            <button class="btn-print" onclick="window.print()">🖨️ Salvar em PDF / Imprimir</button>
            <span class="badge">PRODUÇÃO</span>
        </div>
    </header>

    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-title">Receita Bruta</div>
            <div class="kpi-value">R$ {kpis['gross_revenue']:,.2f}</div>
            <div class="kpi-subtitle">▲ Faturamento acumulado</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Lucro Operacional</div>
            <div class="kpi-value">R$ {kpis['net_profit']:,.2f}</div>
            <div class="kpi-subtitle">Margem: {kpis['margin_pct']}%</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Ticket Médio (AOV)</div>
            <div class="kpi-value">R$ {kpis['average_order_value']:,.2f}</div>
            <div class="kpi-subtitle">Por venda realizada</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Receita Recorrente (MRR)</div>
            <div class="kpi-value">R$ {kpis['mrr']:,.2f}</div>
            <div class="kpi-subtitle">ARR Estimado: R$ {kpis['arr']:,.2f}</div>
        </div>
    </div>

    <div class="table-container">
        <h2 style="font-size: 1.2rem; margin-bottom: var(--space-md);">DRE Gerencial Simplificada</h2>
        <table>
            <thead>
                <tr>
                    <th>Linha da DRE</th>
                    <th class="text-right">Valor (R$)</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>1. Receita Bruta</td><td class="text-right">R$ {dre['1_receita_bruta']:,.2f}</td></tr>
                <tr><td>2. Deduções e Impostos</td><td class="text-right" style="color: var(--color-error);">- R$ {dre['2_deducoes_e_impostos']:,.2f}</td></tr>
                <tr style="font-weight: 600;"><td>3. Receita Líquida</td><td class="text-right">R$ {dre['3_receita_liquida']:,.2f}</td></tr>
                <tr><td>4. Comissões de Vendas</td><td class="text-right" style="color: var(--color-error);">- R$ {dre['4_comissoes_de_vendas']:,.2f}</td></tr>
                <tr><td>5. Despesas Operacionais</td><td class="text-right" style="color: var(--color-error);">- R$ {dre['5_despesas_operacionais']:,.2f}</td></tr>
                <tr style="font-weight: 700; color: var(--color-success); font-size: 1rem;">
                    <td>6. Lucro Operacional Líquido</td>
                    <td class="text-right">R$ {dre['7_lucro_operacional_liquido']:,.2f}</td>
                </tr>
            </tbody>
        </table>
    </div>
    {auto_print_script}
</body>
</html>"""
