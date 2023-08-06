from abc import ABC
from dataclasses import dataclass
from typing import *

from .event_handler import *
from ..bot_api import *

@dataclass(frozen=True)
class MessageEvent(Event):
    message: InboundMessage

class MessageHandler(EventHandler, ABC):
    async def can_handle(self, event: MessageEvent) -> bool:
        return await super().can_handle(event) \
           and await self._can_handle__check_author(event)
    
    async def _can_handle__check_author(self, event: MessageEvent) -> bool:
        return event.message.author != event.bot_user
    
    async def _can_handle__check_event_type(self, event: Event) -> bool:
        return isinstance(event, MessageEvent)
    
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

class OnMentionHandler(MessageHandler, ABC):
    only_on_mention: bool = False
    def __init__(self, only_on_mention: bool = False):
        super().__init__()
        self.only_on_mention = only_on_mention
    
    async def can_handle(self, event: MessageEvent) -> bool:
        return await super().can_handle(event) \
           and await self._can_handle__check_author(event)
    
    async def _can_handle__check_mention(self, event: MessageEvent) -> bool:
        return event.message.author


__all__ = \
[
    'MessageEvent',
    'MessageHandler',
    'ReplyHandler',
]
