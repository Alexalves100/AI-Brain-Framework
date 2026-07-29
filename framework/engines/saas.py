"""
Engine SaaS Multi-Tenant.
Gerencia resolução de tenants, isolamento de dados, controle de planos/quotas
e Feature Flags por tenant em aplicações SaaS.
"""
from typing import Dict, Any, Optional, Set
import threading

class TenantContext:
    """Representa o contexto isolado de um tenant."""

    def __init__(self, tenant_id: str, plan: str = "free", name: Optional[str] = None):
        self.tenant_id = tenant_id
        self.plan = plan
        self.name = name or tenant_id
        self.settings: Dict[str, Any] = {}
        self.feature_flags: Set[str] = set()
        self.usage_counters: Dict[str, int] = {}

class SaaSManager:
    """Motor central de gestão Multi-Tenant e SaaS."""

    PLAN_LIMITS = {
        "free": {"api_calls_per_day": 1_000, "storage_mb": 500, "max_users": 3},
        "pro": {"api_calls_per_day": 100_000, "storage_mb": 50_000, "max_users": 25},
        "enterprise": {"api_calls_per_day": 10_000_000, "storage_mb": 1_000_000, "max_users": 1_000},
    }

    def __init__(self):
        self._tenants: Dict[str, TenantContext] = {}
        self._local = threading.local()

    def register_tenant(self, tenant_id: str, plan: str = "free", name: Optional[str] = None) -> TenantContext:
        """Cadastra um novo tenant com seu plano inicial."""
        tenant = TenantContext(tenant_id, plan=plan, name=name)
        self._tenants[tenant_id] = tenant
        return tenant

    def get_tenant(self, tenant_id: str) -> Optional[TenantContext]:
        """Obtém os dados do tenant pelo ID."""
        return self._tenants.get(tenant_id)

    def set_current_tenant(self, tenant_id: str) -> bool:
        """Define o tenant ativo na thread atual."""
        if tenant_id in self._tenants:
            self._local.tenant_id = tenant_id
            return True
        return False

    def get_current_tenant(self) -> Optional[TenantContext]:
        """Retorna o tenant ativo na thread atual."""
        tenant_id = getattr(self._local, "tenant_id", None)
        if tenant_id:
            return self._tenants.get(tenant_id)
        return None

    def resolve_tenant_from_headers(self, headers: Dict[str, str]) -> Optional[str]:
        """Resolve o ID do tenant a partir do header X-Tenant-ID ou Host."""
        # 1. Checa header explícito
        for k, v in headers.items():
            if k.lower() == "x-tenant-id":
                return v

        # 2. Checa subdomínio no Host (ex: acme.meusaas.com)
        host = headers.get("Host") or headers.get("host")
        if host and "." in host:
            parts = host.split(".")
            if len(parts) >= 3 and parts[0] != "www":
                return parts[0]

        return None

    def is_feature_enabled(self, tenant_id: str, feature_name: str) -> bool:
        """Verifica se uma feature flag está habilitada para o tenant."""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return False
        return feature_name in tenant.feature_flags

    def enable_feature(self, tenant_id: str, feature_name: str) -> None:
        """Habilita uma feature flag para um tenant."""
        tenant = self.get_tenant(tenant_id)
        if tenant:
            tenant.feature_flags.add(feature_name)

    def check_quota(self, tenant_id: str, metric: str, current_usage: int) -> bool:
        """Verifica se o uso atual do tenant está dentro dos limites do seu plano."""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return False

        plan_limits = self.PLAN_LIMITS.get(tenant.plan, self.PLAN_LIMITS["free"])
        max_allowed = plan_limits.get(metric)
        if max_allowed is None:
            return True

        return current_usage <= max_allowed
