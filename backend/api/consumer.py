import asyncio
import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from backend.api.model.acceptance_log import \
    acceptance_log_entry_created_notifier
from backend.api.model.level import games_notifier
from backend.api.model.level import level_join_left_notifier
from backend.api.model.message import message_notifier


class Consumer(AsyncJsonWebsocketConsumer):

    # def __init__(self, notifier=None):
    #     # super().__init__(*args, **kwargs)
    #     self.notifier = notifier

    async def connect(self):
        # self.notifier.attach(self)

        await self.accept()

    def update(self, msg):
        async def driver(pl):
            await self.send(pl)

        asyncio.run(driver(msg))

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        t = {"rec ans": "todo practice consumer"}

        t = json.dumps(t)
        await self.send(t)

    # async def disconnect(self, code):
    # self.notifier.detach(self)


#


# trigger on new message
class MessageConsumer(Consumer):

    async def connect(self):
        message_notifier.attach(self)
        await self.accept()

    async def disconnect(self, code):
        message_notifier.detach(self)


class GameConsumer(Consumer):

    async def connect(self):
        games_notifier.attach(self)
        await self.accept()

    async def disconnect(self, code):
        games_notifier.detach(self)


class AcceptanceLogEntryCreatedConsumer(Consumer):

    async def connect(self):
        acceptance_log_entry_created_notifier.attach(self)
        await self.accept()

    async def disconnect(self, code):
        acceptance_log_entry_created_notifier.detach(self)


class LevelJoinLeftConsumer(Consumer):

    async def connect(self):
        level_join_left_notifier.attach(self)
        await self.accept()

    async def disconnect(self, code):
        level_join_left_notifier.detach(self)

# class GameCreatedConsumer(Consumer):
#
#     async def connect(self):
#         game_created_notifier.attach(self)
#         await self.accept()
#
#     async def disconnect(self, code):
#         game_created_notifier.detach(self)
#
# class GameJoinConsumer(Consumer):
#     async def connect(self):
#         game_join_notifier.attach(self)
#         await self.accept()
#
#     async def disconnect(self, code):
#         game_join_notifier.detach(self)
#
# class GameLeftConsumer(Consumer):
#     async def connect(self):
#         game_join_notifier.attach(self)
#         await self.accept()
#
#     async def disconnect(self, code):
#         game_join_notifier.detach(self)


# class GameDeletedConsumer(Consumer):
#     async def connect(self):
#         .attach(self)
#         await self.accept()
#
#     async def disconnect(self, code):
#         game_deleted_notifier.detach(self)
