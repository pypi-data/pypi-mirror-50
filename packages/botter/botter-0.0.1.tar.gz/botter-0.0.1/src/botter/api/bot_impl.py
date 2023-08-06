from abc import ABC
from typing import *

from .handlers import Event
from ..util import Logging

EventProcessorType = Callable[[Event], Awaitable[None]]

class BotImpl(ABC):
    def __init__(self, *args, **kwargs):
        assert not (args or kwargs), f"Positional not keyword arguments are not allowed here, got: args={args}, kwargs={kwargs}"
    def start(self) -> NoReturn:
        raise NotImplementedError
    def register_event_processor(self, processor: EventProcessorType):
        raise NotImplementedError

class BotEventProcessorImpl(BotImpl, Logging, ABC):
    event_processors: List[EventProcessorType]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (getattr(self, 'event_processors', None) is None):
            self.event_processors = list()
    
    def register_event_processor(self, processor: EventProcessorType):
        self.event_processors.append(processor)
    async def process_event(self, event: Event):
        self.logger.info(f"Handling event {event}...")
        for processor in self.event_processors:
            self.logger.debug(f"Calling processor {processor}...")
            await processor(event)

__all__ = \
[
    'EventProcessorType',
    'BotImpl',
    'BotEventProcessorImpl',
]
