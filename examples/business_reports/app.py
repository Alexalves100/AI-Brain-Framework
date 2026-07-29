"""
Exemplo de Painel de Relatórios Financeiros e Comerciais com Suporte a PDF.
Demonstra a geração de relatórios de Contas a Pagar/Receber, Vendas, Comissões,
Faturamento, DRE Gerencial, Dashboard HTML e Exportação direta em PDF.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from framework import Context
from framework.engines import BusinessReportingEngine
from framework.standards import SecurityHeaders

# Dados mockados de sistema comercial / ERP / SaaS
MOCK_DATA = {
    "payables": [
        {"id": 1, "description": "Fornecedor de Software", "amount": 1500.00, "status": "pending"},
        {"id": 2, "description": "Aluguel do Escritório", "amount": 3200.00, "status": "pending"},
        {"id": 3, "description": "Servidor Cloud AWS", "amount": 850.00, "status": "overdue"},
    ],
    "receivables": [
        {"id": 101, "description": "Cliente Acme Corp", "amount": 12500.00, "status": "pending"},
        {"id": 102, "description": "Cliente Globex Inc", "amount": 4800.00, "status": "pending"},
        {"id": 103, "description": "Cliente Initech", "amount": 2100.00, "status": "overdue"},
    ],
    "sales": [
        {"id": 501, "seller_name": "Carlos Silva", "amount": 15000.00, "commission_rate": 0.05},
        {"id": 502, "seller_name": "Mariana Souza", "amount": 22000.00, "commission_rate": 0.05},
        {"id": 503, "seller_name": "Carlos Silva", "amount": 8000.00, "commission_rate": 0.05},
    ],
    "subscriptions": [
        {"id": "sub_1", "plan": "pro", "mrr": 4900.00, "status": "active"},
        {"id": "sub_2", "plan": "enterprise", "mrr": 12000.00, "status": "active"},
    ],
    "transactions": [
        {"id": 901, "type": "income", "amount": 45000.00, "date": "2026-07-01"},
        {"id": 902, "type": "deduction", "amount": 3200.00, "date": "2026-07-05"},
    ],
    "invoices": [
        {"number": "NFE-001", "amount": 15000.00, "status": "issued"},
        {"number": "NFE-002", "amount": 22000.00, "status": "issued"},
        {"number": "NFE-003", "amount": 8000.00, "status": "issued"},
        {"number": "NFE-004", "amount": 4500.00, "status": "cancelled"},
    ]
}

engine = BusinessReportingEngine()

class ReportHandler(BaseHTTPRequestHandler):

    def _send_json(self, data: dict):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        for k, v in SecurityHeaders.get_default_headers().items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

    def _send_html(self, html_content: str):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        for k, v in SecurityHeaders.get_default_headers().items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def do_GET(self):
        ctx = Context()
        ctx.set("data", MOCK_DATA)

        if self.path == "/" or self.path == "/dashboard":
            ctx.set("report_type", "html_dashboard")
            res = engine.run(ctx)
            self._send_html(res.output["html"])

        elif self.path == "/api/reports/pdf":
            ctx.set("report_type", "pdf_printable")
            res = engine.run(ctx)
            self._send_html(res.output["html"])

        elif self.path == "/api/reports/dre":
            ctx.set("report_type", "dre")
            res = engine.run(ctx)
            self._send_json(res.output)

        elif self.path == "/api/reports/kpis":
            ctx.set("report_type", "kpi_metrics")
            res = engine.run(ctx)
            self._send_json(res.output)

        elif self.path == "/api/reports/accounts":
            ctx.set("report_type", "accounts_payable_receivable")
            res = engine.run(ctx)
            self._send_json(res.output)

        elif self.path == "/api/reports/sales":
            ctx.set("report_type", "sales_commission")
            res = engine.run(ctx)
            self._send_json(res.output)

        elif self.path == "/api/reports/revenue":
            ctx.set("report_type", "revenue")
            ctx.set("period", "month")
            res = engine.run(ctx)
            self._send_json(res.output)

        elif self.path == "/api/reports/invoices":
            ctx.set("report_type", "invoices")
            res = engine.run(ctx)
            self._send_json(res.output)

        else:
            self._send_json({"error": "Endpoint não encontrado", "dashboard_url": "http://localhost:8005/"})

def run_server(port: int = 8005):
    server_address = ("", port)
    httpd = HTTPServer(server_address, ReportHandler)
    print(f"Servidor de Relatórios Financeiros rodando em http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
