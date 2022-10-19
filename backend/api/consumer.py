import asyncio
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from backend.api.cqrs_c.users import active_users_notifier


class PracticeConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        active_users_notifier.attach(self)

        await self.accept()

    def update(self, msg):

        r = msg
        msg = json.dumps({
            "message": "getUserActive",
            "args": {i["username"]: {"isActive": True} for i in r}
        })

        async def test(a):

            await self.send(a)

        asyncio.run(test(msg))

    async def receive(self, text_data=None, bytes_data=None, **kwargs):

        t = {"rec ans": "f"}

        t = json.dumps(t)
        await self.send(t)

    async def disconnect(self, code):
        active_users_notifier.detach(self)

