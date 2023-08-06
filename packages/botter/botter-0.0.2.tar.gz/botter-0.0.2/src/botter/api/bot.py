from typing import *

from .bot_impl import BotImpl
from .handlers import EventAggregator

T = TypeVar('T', bound=BotImpl)
class Bot(EventAggregator, Generic[T]):
    implementation: Type[T] = None
    client: T = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if (self.client is None):
            if (self.implementation is None):
                raise ValueError("Cannot initialize bot without messenger implementation")
            self.client = self.implementation()
        self.client.register_event_processor(self._safe_handle_event)
    
    def start(self) -> NoReturn:
        self.client.start()
    
    @classmethod
    def run(cls, *args, **kwargs) -> NoReturn:
        instance = cls(*args, **kwargs)
        instance.start()

__all__ = \
[
    'Bot',
]
