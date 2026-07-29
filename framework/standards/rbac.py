"""
Role-Based Access Control (RBAC) Module.
Gerencia papéis, permissões granulares e controle de acesso hierárquico.
"""
from typing import Dict, Set, List, Optional

class RBACManager:
    """Gerenciador de controle de acesso baseado em papéis (RBAC)."""

    def __init__(self):
        self.roles: Dict[str, Set[str]] = {}
        self.role_hierarchy: Dict[str, Set[str]] = {}

    def add_role(self, role: str, permissions: Optional[List[str]] = None) -> None:
        """Registra um novo papel com um conjunto de permissões."""
        if role not in self.roles:
            self.roles[role] = set()
        if permissions:
            self.roles[role].update(permissions)

    def add_permission(self, role: str, permission: str) -> None:
        """Adiciona uma permissão a um papel existente."""
        if role not in self.roles:
            self.roles[role] = set()
        self.roles[role].add(permission)

    def add_child_role(self, parent_role: str, child_role: str) -> None:
        """Define hierarquia onde parent_role herda todas as permissões de child_role."""
        if parent_role not in self.role_hierarchy:
            self.role_hierarchy[parent_role] = set()
        self.role_hierarchy[parent_role].add(child_role)

    def get_effective_permissions(self, role: str) -> Set[str]:
        """Obtém todas as permissões de um papel, incluindo as herdadas."""
        if role not in self.roles:
            return set()

        effective = set(self.roles[role])

        # Herança recursiva
        visited = set()
        queue = list(self.role_hierarchy.get(role, set()))

        while queue:
            child = queue.pop(0)
            if child in visited:
                continue
            visited.add(child)
            if child in self.roles:
                effective.update(self.roles[child])
            if child in self.role_hierarchy:
                queue.extend(self.role_hierarchy[child])

        return effective

    def has_permission(self, role: str, permission: str) -> bool:
        """Verifica se um papel possui uma permissão específica."""
        effective_perms = self.get_effective_permissions(role)
        return permission in effective_perms or "*" in effective_perms
