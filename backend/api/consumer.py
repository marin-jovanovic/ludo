import asyncio
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from backend.api.cqrs_c.users import active_users_notifier
from backend.api.model.game import games_notifier, game_created_notifier,game_left_notifier,game_join_notifier



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


class GameConsumer(Consumer):

    async def connect(self):
        games_notifier.attach(self)
        await self.accept()

    async def disconnect(self, code):
        games_notifier.detach(self)


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
