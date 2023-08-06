from typing import *

import discord

from botter.api import BotEventProcessorImpl
from botter.api.handlers import *
from .discord_api import *

class DiscordBot(BotEventProcessorImpl):
    token: str
    client: discord.Client
    logger_name = 'botter.discord.bot-impl'
    bot_user: DiscordUser
    
    def __init__(self, token: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = discord.Client()
        
        if (token is not None):
            self.token = token
        if (getattr(self, 'token', None) is None):
            self.token = None
        
        self.register_discord_events()
    
    def register_discord_events(self):
        self.client.event(self.on_message)
        self.client.event(self.on_ready)
    
    def create_event(self, event_type: Type[Event], **kwargs):
        # noinspection PyArgumentList
        return event_type(bot_user=self.bot_user, **kwargs)
    
    async def on_message(self, message: discord.Message):
        event = self.create_event(MessageEvent, message=DiscordMessage(self.client, message))
        await self.process_event(event)
    
    async def on_ready(self):
        self.bot_user = DiscordUser(self.client, self.client.user)
        event = self.create_event(StartEvent)
        await self.process_event(event)
    
    def start(self):
        if (self.token is None):
            raise ValueError("Cannot start Discord bot without token!")
        self.client.run(self.token)

__all__ = \
[
    'DiscordBot',
]
