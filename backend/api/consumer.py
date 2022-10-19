import asyncio
import json
import time
from threading import Thread

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from channels.generic.websocket import AsyncWebsocketConsumer
from backend.api.cqrs_q.users import get_logged_users

from backend.api.cqrs_q.users import get_logged_users

# u = get_logged_users()
# print(u)

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from backend.api.cqrs_c.users import auth_notifier


class PracticeConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        class DecimalViewer:
            """updates the Decimal viewer"""

            # def __init__(self):
                # self.parent = parent
            #     self.active_users = {}

            def update(self, msg):
                print(80 * "-")
                # print(f"update {msg=} ")
                # for i in msg:
                #     print(i)

                # await self.parent(msg)

        view1 = DecimalViewer()
        # view1 = DecimalViewer(self.send_)
        auth_notifier.attach(view1)

        auth_notifier.attach(self)
        # print(self)
        # print(self.update)

        await self.accept()

    def update(self, msg):

        print(f"update {msg=} ")

        async def test(a):
            # print("task")
            # init_server()
            await self.send("a")
            # auth_notifier.notify("bbbbbb")
            # print('This is from another thread')

        asyncio.run(test("d"))
        # asyncio.ensure_future(test(2))
        # await asyncio.gather(test(2), test(2), test(2))
        # thread = Thread(target=task)
        # thread.start()
        # thread.join()

        # for i in msg:
        #     print(i)

    # async def observer(self):

    async def send_(self, data):
        print("send___________________")
        # await self.send(data)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):

        def task(result):
            # print(fo)
            # block for a moment
            # time.sleep(1)
            # sleep(1)
            # display a message
            # print('This is from another thread')
            users = get_logged_users()
            # users = await database_sync_to_async(get_logged_users())()

            # print(f"{users=}")
            # result = users
            for i in users:
                result.append(i)

        r = []
        # t = []
        thread = Thread(target=task, args=(r,))
        thread.start()

        thread.join()

        # r = await get_logged_users()

        t = json.dumps({
            "message": "getUserActive",
            "args": {i["username"]: {"isActive": True} for i in r}
        })
        print(t)
        # print("a",80 * "-")
        # print(t)
        # return t
        await self.send(t)


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

        r = await get_logged_users()

        t = json.dumps({
            "message": "getUserActive",
            "args": {i["username"]: {"isActive": True} for i in r}
        })

        # print("a",80 * "-")
        # print(t)
        # return t
        await self.send(text_data=t)

        # await self.send(text_data="Hello world!")
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
