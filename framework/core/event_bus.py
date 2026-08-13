"""
EventBus Module.
Barramento de eventos desacoplado (Publish/Subscribe) em Python puro para
comunicação entre serviços, auditoria e execução de rotinas assíncronas/callbacks.
"""
import threading
from typing import Any, Callable, Dict, List


class EventBus:
    """Barramento de eventos desacoplado (Publish/Subscribe) thread-safe."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = {}
        self._lock = threading.RLock()
        self.published_events_count = 0

    def subscribe(self, event_name: str, handler: Callable[[Any], None]) -> None:
        """Inscreve um handler para ser executado quando o evento especificado for publicado."""
        with self._lock:
            if event_name not in self._subscribers:
                self._subscribers[event_name] = []
            if handler not in self._subscribers[event_name]:
                self._subscribers[event_name].append(handler)

    def unsubscribe(self, event_name: str, handler: Callable[[Any], None]) -> bool:
        """Remove um handler previamente inscrito."""
        with self._lock:
            if event_name in self._subscribers and handler in self._subscribers[event_name]:
                self._subscribers[event_name].remove(handler)
                return True
            return False

    def publish(self, event_name: str, data: Any = None) -> int:
        """Publica um evento para todos os inscritos. Retorna o número de handlers executados."""
        handlers_to_call = []
        with self._lock:
            self.published_events_count += 1
            if event_name in self._subscribers:
                handlers_to_call = list(self._subscribers[event_name])

        for handler in handlers_to_call:
            try:
                handler(data)
            except Exception:
                # Trata erros em handlers para não interromper outros inscritos
                pass

        return len(handlers_to_call)

    def clear(self) -> None:
        """Remove todas as inscrições do barramento."""
        with self._lock:
            self._subscribers.clear()

