from abc import ABC
from dataclasses import dataclass

from .event_handler import Event, EventHandler

@dataclass(frozen=True)
class StartEvent(Event):
    pass

class StartHandler(EventHandler, ABC):
    async def can_handle(self, event: Event) -> bool:
        return isinstance(event, StartEvent)

__all__ = \
[
    'StartEvent',
    'StartHandler',
]
