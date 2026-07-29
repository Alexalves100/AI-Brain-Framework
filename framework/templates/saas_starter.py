"""
Template Starter para Aplicações SaaS Profissionais.
Demonstra a integração entre HTTP Server nativo, JWT Auth, Multi-Tenancy,
Security Headers e Design System Tokens.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
from pathlib import Path

# Adiciona diretório raiz ao PYTHONPATH se necessário
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from framework.standards import SecurityHeaders, CSSTokens, JWTAuth, PasswordHasher, RBACManager
from framework.engines import SaaSManager

saas_engine = SaaSManager()

# Pre-registra tenants de exemplo
saas_engine.register_tenant("acme", plan="pro", name="Acme Corporation")
saas_engine.register_tenant("globex", plan="free", name="Globex Inc")

jwt_service = JWTAuth(secret_key="super_secret_saas_key_production_ready")
rbac = RBACManager()
rbac.add_role("admin", ["read:all", "write:all", "delete:all"])
rbac.add_role("user", ["read:own", "write:own"])

class SaaSHandler(BaseHTTPRequestHandler):

    def _set_security_headers(self, content_type: str = "application/json"):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        headers = SecurityHeaders.get_default_headers()
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()

    def do_GET(self):
        # Resolve Tenant
        headers_dict = {k: v for k, v in self.headers.items()}
        tenant_id = saas_engine.resolve_tenant_from_headers(headers_dict) or "default"

        if self.path == "/health":
            self._set_security_headers("application/json")
            resp = {
                "status": "healthy",
                "tenant_resolved": tenant_id,
                "framework": "AI-Brain-Framework",
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))

        elif self.path == "/css/base.css":
            self._set_security_headers("text/css")
            css_content = CSSTokens.get_google_fonts_import() + "\n" + CSSTokens.generate_css_variables("dark")
            self.wfile.write(css_content.encode("utf-8"))

        else:
            self._set_security_headers("application/json")
            resp = {
                "message": "Bem-vindo ao AI-Brain SaaS Starter",
                "tenant": tenant_id,
                "endpoints": ["/health", "/css/base.css"],
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))

def run_server(port: int = 8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, SaaSHandler)
    print(f"Servidor SaaS Starter rodando em http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
