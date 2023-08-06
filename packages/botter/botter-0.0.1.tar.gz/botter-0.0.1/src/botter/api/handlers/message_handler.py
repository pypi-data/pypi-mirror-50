from abc import ABC
from dataclasses import dataclass
from typing import *

from .event_handler import *
from ..bot_api import *

@dataclass(frozen=True)
class MessageEvent(Event):
    message: InboundMessage

class MessageHandler(EventHandler, ABC):
    async def can_handle(self, event: Event) -> bool:
        if (isinstance(event, MessageEvent)):
            if (event.message.author != event.bot_user):
                return True
        return False
    
    async def handle_event(self, event: MessageEvent):
        return await self.handle_message(event.message)
    
    async def handle_message(self, message: InboundMessage):
        pass

class ReplyHandler(MessageHandler, ABC):
    async def handle_event(self, event: MessageEvent):
        answer: Optional[Message] = await super().handle_event(event)
        if (answer is not None):
            await event.message.reply(answer)
    
    async def handle_message(self, message: InboundMessage) -> Optional[Message]:
        pass

__all__ = \
[
    'MessageEvent',
    'MessageHandler',
    'ReplyHandler',
]
