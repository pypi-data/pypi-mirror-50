from dataclasses import replace
from typing import *

import discord

from ..api.bot_api import *
from ..util.os_operations import safe_remove

class DiscordUser(User):
    discord_user: discord.user.BaseUser
    client: discord.Client
    
    def __init__(self, client: discord.Client, member: discord.user.BaseUser):
        self.discord_user = member
        self.client = client
        
        super().__init__ \
        (
            id = self.discord_user.id,
            display_name = self.discord_user.display_name,
        )

class DiscordAttachment(Attachment):
    discord_attachment: discord.Attachment
    client: discord.Client
    
    def __init__(self, client: discord.Client, attachment: discord.Attachment):
        self.discord_attachment = attachment
        self.client = client
        
        super().__init__ \
        (
            id = self.discord_attachment.id,
            filename = self.discord_attachment.filename,
            type = AttachmentType.Image if (self.is_image) else AttachmentType.Document,
        )
    
    @property
    def is_image(self) -> bool:
        return self.discord_attachment.height is not None
    
    @property
    def weight(self) -> int:
        return self.discord_attachment.size
    
    @property
    async def content(self) -> bytes:
        return await self.discord_attachment.read(use_cached=True)


class DiscordMessage(InboundMessage):
    discord_message: discord.Message
    client: discord.Client
    
    def __init__(self, client: discord.Client, message: discord.Message):
        self.discord_message = message
        self.client = client
        
        attachments: Optional[List[discord.Attachment]] = self.discord_message.attachments
        if (attachments):
            attachments = [ DiscordAttachment(client, att) for att in attachments ]
        else:
            attachments = list()
        super().__init__ \
        (
            id = self.discord_message.id,
            text = self.discord_message.content,
            attachments = attachments,
            author = DiscordUser(client, self.discord_message.author),
        )
    
    async def reply(self, message: Message):
        await send_message(self.discord_message.channel, replace(message, text=f"{self.discord_message.author.mention}\n{message.text}"))

async def send_message(channel: discord.TextChannel, message: Message):
    text = message.text.strip()
    files = [ (await at.temp_file, at.filename) for at in message.attachments]
    await channel.send(text or None, files = [ discord.File(*f) for f in files ])
    for loc, _ in files:
        safe_remove(loc)

__all__ = \
[
    'DiscordAttachment',
    'DiscordMessage',
    'DiscordUser',
    
    'send_message',
]
