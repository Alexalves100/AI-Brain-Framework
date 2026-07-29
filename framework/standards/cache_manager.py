"""
Cache Manager Module.
Gerencia cache em memória com suporte a expiração TTL (Time To Live),
métricas de Hit/Miss e política de invalidação sem dependências externas.
"""
import time
import threading
from typing import Any, Dict, Optional, Tuple, Callable

class CacheManager:
    """Gerenciador de cache em memória thread-safe com suporte a TTL."""

    def __init__(self, default_ttl_seconds: int = 300):
        self.default_ttl = default_ttl_seconds
        self._store: Dict[str, Tuple[Any, float]] = {}  # key -> (value, expire_at)
        self._lock = threading.RLock()
        self.hits = 0
        self.misses = 0

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Armazena um item no cache com um TTL opcional em segundos."""
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        expire_at = time.time() + ttl if ttl > 0 else float("inf")
        with self._lock:
            self._store[key] = (value, expire_at)

    def get(self, key: str, default: Any = None) -> Any:
        """Obtém um item do cache se ele for válido e não expirado."""
        with self._lock:
            if key not in self._store:
                self.misses += 1
                return default

            val, expire_at = self._store[key]
            if time.time() > expire_at:
                del self._store[key]
                self.misses += 1
                return default

            self.hits += 1
            return val

    def delete(self, key: str) -> bool:
        """Remove um item do cache."""
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    def clear(self) -> None:
        """Limpa todos os itens armazenados no cache."""
        with self._lock:
            self._store.clear()
            self.hits = 0
            self.misses = 0

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso do cache (hits, misses, total de chaves)."""
        with self._lock:
            # Limpa expirados na contagem
            now = time.time()
            valid_keys = sum(1 for _, expire_at in self._store.values() if now <= expire_at)
            total = self.hits + self.misses
            hit_rate = (self.hits / total * 100) if total > 0 else 0.0

            return {
                "hits": self.hits,
                "misses": self.misses,
                "active_items": valid_keys,
                "hit_rate_pct": round(hit_rate, 2),
            }

    def cached(self, ttl_seconds: Optional[int] = None):
        """Decorator para aplicar cache em funções."""
        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                # Gera chave baseada no nome da função e argumentos
                key = f"{func.__module__}.{func.__qualname__}:{args}:{kwargs}"
                cached_val = self.get(key)
                if cached_val is not None:
                    return cached_val
                val = func(*args, **kwargs)
                self.set(key, val, ttl_seconds=ttl_seconds)
                return val
            return wrapper
        return decorator
