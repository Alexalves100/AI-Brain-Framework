import unittest

from framework import Context
from framework.engines import BusinessReportingEngine


class TestBusinessReportingEngine(unittest.TestCase):

    def setUp(self):
        self.engine = BusinessReportingEngine()
        self.mock_data = {
            "payables": [
                {"amount": 1000.0, "status": "pending"},
                {"amount": 500.0, "status": "overdue"},
            ],
            "receivables": [
                {"amount": 3000.0, "status": "pending"},
                {"amount": 1000.0, "status": "overdue"},
            ],
            "sales": [
                {"seller_name": "Alice", "amount": 10000.0, "commission_rate": 0.10},
                {"seller_name": "Bob", "amount": 5000.0, "commission_rate": 0.05},
            ],
            "subscriptions": [
                {"plan": "pro", "mrr": 2000.0, "status": "active"},
            ],
            "transactions": [
                {"type": "income", "amount": 20000.0},
                {"type": "deduction", "amount": 2000.0},
            ],
            "invoices": [
                {"number": "NF-1", "amount": 10000.0, "status": "issued"},
                {"number": "NF-2", "amount": 5000.0, "status": "cancelled"},
            ]
        }

    def test_accounts_payable_receivable_report(self):
        ctx = Context()
        ctx.set("report_type", "accounts_payable_receivable")
        ctx.set("data", self.mock_data)

        res = self.engine.run(ctx)
        self.assertEqual(res.output["summary"]["total_payable"], 1500.0)
        self.assertEqual(res.output["summary"]["total_receivable"], 4000.0)
        self.assertEqual(res.output["summary"]["overdue_payable"], 500.0)
        self.assertEqual(res.output["summary"]["dunning_rate_pct"], 25.0)

    def test_sales_commission_and_aov(self):
        ctx = Context()
        ctx.set("report_type", "sales_commission")
        ctx.set("data", self.mock_data)

        res = self.engine.run(ctx)
        summary = res.output["summary"]

        self.assertEqual(summary["total_sales_volume"], 15000.0)
        self.assertEqual(summary["total_commissions"], 1250.0)
        self.assertEqual(summary["average_order_value"], 7500.0)

    def test_dre_report(self):
        ctx = Context()
        ctx.set("report_type", "dre")
        ctx.set("data", self.mock_data)

        res = self.engine.run(ctx)
        dre = res.output["dre"]

        self.assertEqual(dre["1_receita_bruta"], 20000.0)
        self.assertEqual(dre["2_deducoes_e_impostos"], 2000.0)
        self.assertEqual(dre["3_receita_liquida"], 18000.0)
        self.assertEqual(dre["4_comissoes_de_vendas"], 1250.0)
        self.assertEqual(dre["5_despesas_operacionais"], 1500.0)
        self.assertEqual(dre["7_lucro_operacional_liquido"], 15250.0)

    def test_kpi_metrics_and_html_rendering(self):
        ctx = Context()
        ctx.set("data", self.mock_data)

        # Test KPI metrics
        ctx.set("report_type", "kpi_metrics")
        res_kpi = self.engine.run(ctx)
        self.assertEqual(res_kpi.output["kpis"]["mrr"], 2000.0)
        self.assertEqual(res_kpi.output["kpis"]["arr"], 24000.0)

        # Test HTML Dashboard rendering
        ctx.set("report_type", "html_dashboard")
        res_html = self.engine.run(ctx)
        self.assertIn("<!DOCTYPE html>", res_html.output["html"])
        self.assertIn("Painel de Relatórios & KPIs Gerenciais", res_html.output["html"])

    def test_pdf_printable_report(self):
        ctx = Context()
        ctx.set("data", self.mock_data)
        ctx.set("report_type", "pdf_printable")

        res_pdf = self.engine.run(ctx)
        self.assertIn("window.print()", res_pdf.output["html"])
        self.assertIn("@media print", res_pdf.output["html"])

if __name__ == "__main__":
    unittest.main()
