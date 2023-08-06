# Botter - Simple interface for creating cross-messenger bots

**Botter** is a framework which allows your bots run in any available messenger.
Currently, there are only one implementation for [Discord](https://discord.app),
but it is easy to implement other platforms.

Okay, let's get started!

## Getting Started

### Creating an Application
At first, you should register a bot in the desired platform.
As all messengers provide different ways to do so, we will not describe this process here.

### Create Handler
Botter uses event-based architecture, with a most-common event - `MessageEvent`.
Events are handled by `EventHandler`'s.

So, let's create out own:
```python
from botter.api import *
from botter.api.handlers import *

class SimpleEchoHandler(ReplyHandler):
    async def handle_message(self, message: InboundMessage) -> Message:
        return Message(f"You've said:\n" + message.text)
```

Here we use the `ReplyHandler`, which:
 - Nests `MessageHandler`
 - Checks the event is `MessageEvent`
 - Calls method `handle_message()` with the message from event.
 - If this method returns `Message` rather than None,
`ReplyHandler` would send it to server with a mention to the original message's author.

### Crate a Bot
Then we need to create a `Bot` - object that aggregates handlers and mappings to the implementation.
Here we use discord driver as an example.
```python
from botter.discord import DiscordBot

class EchoBot(Bot[DiscordBot]):
    token = 'INSERT_YOUR_TOKEN_HERE'
    event_handlers = [ SimpleEchoHandler ]
    client = DiscordBot(token=token)
```

Okay, let's try it out!

![Simple EchoBot - Discord](docs/echo-1-discord.png)

Wow! It works!

### Extending Events
Now, let's try to have some fun with the events.
