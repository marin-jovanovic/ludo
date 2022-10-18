import time

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


from channels.generic.websocket import AsyncWebsocketConsumer

from backend.api.cqrs_q.users import get_logged_users

# u = get_logged_users()
# print(u)

from channels.generic.websocket import AsyncJsonWebsocketConsumer

class PracticeConsumer(AsyncJsonWebsocketConsumer):

      async def connect(self):
           await self.accept()

      async def receive(self, text_data=None, bytes_data=None, **kwargs):
            if text_data == 'PING':
                 await self.send('PONG')

class PingConsumer(AsyncWebsocketConsumer):
    # groups = ["broadcast"]

    async def connect(self):
        print("conn")
        # Called on connection.
        # To accept the connection call:
        await self.accept()
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        # await self.accept("subprotocol")
        # To reject the connection, call:
        # await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        print("rec")
        print(text_data, bytes_data)

        time.sleep(2.4)
        # users = get_logged_users()
        # print(users)
        await self.send(text_data="Hello world!")
        # res = await database_sync_to_async(get_logged_users())()
        # Called with either text_data or bytes_data for each frame
        # You can call:
        # Or, to send a binary frame:
        # await self.send(bytes_data="Hello world!")

        print("sent")
        # Want to force-close the connection? Call:
        # await self.close()
        # Or add a custom WebSocket error code!
        # await self.close(code=4123)

    async def disconnect(self, close_code):
        print("disc")
        # Called when the socket closes
