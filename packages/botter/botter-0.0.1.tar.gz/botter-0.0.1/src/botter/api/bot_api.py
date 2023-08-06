import os
from dataclasses import *
from enum import Enum, auto
from tempfile import mkstemp
from typing import *

@dataclass(frozen=True)
class User:
    id: str
    display_name: str = field(compare=False)

class AttachmentType(Enum):
    Image = auto()
    Audio = auto()
    Document = auto()

@dataclass
class Attachment:
    id: str
    type: AttachmentType
    filename: str
    
    _tmp_file: str = field(repr=False, default=None, init=False)
    @property
    async def temp_file(self) -> str:
        """
        Returns a path to a temporary file with attachment content.
        You should never use this property with the regular files,
        as they can be easily deleted by the program.
        
        :return: str
        """
        
        if (self._tmp_file is not None):
            if (os.path.isfile(self._tmp_file)):
                return self._tmp_file
        
        fd, path = mkstemp(suffix=self.filename)
        with os.fdopen(fd, 'wb') as f:
            f.write(await self.content)
        self._tmp_file = path
        return path
    
    @property
    async def content(self) -> bytes:
        raise NotImplementedError
    
    @property
    def weight(self) -> int:
        """
        Attachment size in bytes.
        
        :return: int
        """
        
        raise NotImplementedError

@dataclass
class FileAttachment(Attachment):
    path: str
    id: str = field(init=False, default=None)
    filename: str = field(init=False, default=None)
    
    def __post_init__(self):
        if (self.id is None):
            self.id = hash(self.path)
        if (self.filename is None):
            self.filename = os.path.basename(self.path)
    
    @property
    def weight(self) -> int:
        return os.path.getsize(self.path)
    
    @property
    async def content(self) -> bytes:
        with open(self.path, 'rb') as f:
            return f.read()

@dataclass(frozen=True)
class Message:
    text: str
    attachments: List[Attachment] = field(default_factory=list)

    @property
    def has_attachments(self) -> bool:
        return len(self.attachments) > 0
    @property
    def has_image(self) -> bool:
        return any(at.type == AttachmentType.Image for at in self.attachments)

@dataclass(frozen=True)
class InboundMessage(Message):
    id: str = None
    author: User = None
    
    def __post_init__(self):
        if (self.id is None):
            raise ValueError("Field 'id' is mandatory!")
        if (self.author is None):
            raise ValueError("Field 'author' is mandatory!")
    
    async def reply(self, message: 'Message'):
        raise NotImplementedError

__all__ = \
[
    'User',
    'AttachmentType',
    'Attachment',
    'FileAttachment',
    'Message',
    'InboundMessage',
]
