import asyncio
import datetime
import json
import signal
import time
from collections import defaultdict
from threading import Thread

import websockets

from backend.api.ws.util.message import Message
from backend.api.ws.util.server import Server

from backend.api.cqrs_q.users import get_logged_users
from channels.db import database_sync_to_async

class WSServer(Server):

    def __init__(self, domain_name="127.0.0.1", port=8765):
        super().__init__(domain_name, port)

        self.debug_counter = 0

        self.rooms = defaultdict(set)
        self.rooms_meta = {}

        self.m_command_action = {
            "deleteRoom": self.delete_room,
            "createRoom": self.create_room,
        }

        self.active_users = {}

        self.user_make_active("1")

    def user_get_active(self, user_id):
        print(80 * "-")

        # a custom function that blocks for a moment
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

        # print("result", r)


        # users = get_logged_users()
        # rest of the code

        t = json.dumps({
            "message": "getUserActive",
            "args": {i["username"]: {"isActive": True} for i in r}
        })

        # print("a",80 * "-")
        # print(t)
        return t
        # return json.dumps({
        #     "message": "getUserActive",
        #     "args": json.dumps({i: json.dumps({"isActive": True}) for i in r})
        # })

    def user_make_active(self, user_id):

        ct = datetime.datetime.now()
        print("current time:-", ct)

        ts = ct.timestamp()

        self.active_users[user_id] = {
            "logged in": ts
        }

        return str(True)

    def delete_room(self, room_id, user_id):
        print(f"{room_id=} deleted by {user_id=}")
        pass

    def create_room(self, room_id, user_id, capacity):
        print(f"{room_id=} created by {user_id=}")
        self.rooms_meta[room_id] = {"capacity": capacity}
        print(f"{self.rooms_meta=}")

        self.lobby_join_room(room_id, user_id)

        return "room created"

    def lobby_join_room(self, room_id, user_id):
        print(f"{user_id=} joined {room_id=}")
        self.rooms[room_id].add(user_id)

        pass

    def lobby_leave_room(self, room_id, user_id):
        print(f"{user_id=} left {room_id=}")
        self.rooms[room_id].remove(user_id)
        pass

    def is_room_full(self, room_id):
        return False
        pass

    # async def driver(self, websocket, _):
    #
    #     async for raw_data in websocket:
    #         print()
    #         print(f"received: {raw_data=}")
    #
    #         message = Message(raw_data)
    #         print(f"{message.header=}")
    #         print(f"{message.payload=}")
    #
    #         command = message.payload["command"]
    #         print(f"{command=}")
    #         args = message.payload["args"]
    #         print(f"{args=}")
    #
    #         response = {}
    #
    #         if command == "createRoom":
    #             response["message"] = self.create_room(
    #                 args["roomId"],
    #                 message.header["username"],
    #                 args["capacity"]
    #             )
    #
    #         elif command == "logIn":
    #             response["message"] = self.user_make_active(
    #                 message.header["username"],
    #             )
    #
    #         elif command == "getActive":
    #
    #             while True:
    #                 response = self.user_get_active(
    #                     message.header["username"],
    #                 )
    #
    #                 await websocket.send(
    #                     json.dumps(response)
    #                 )
    #
    #         else:
    #             response["message"] = "unsupported command"
    #
    #         print(f"{response=}")
    #
    #         time.sleep(0.4)
    #
    #         await websocket.send(
    #             json.dumps(response)
    #         )
    #
    #         self.debug_counter += 1

#
# def init_server():
#     server = WSServer("localhost", 8765)
#
#     # signal.signal(signal.SIGINT, signal.SIG_DFL)
#
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#
#     print("connect on ws://" + server.host_name + ":" + str(server.port))
#
#     loop.run_until_complete(
#         websockets.serve(server.driver, server.host_name, server.port))
#     loop.run_forever()
#
#
# def main():
#     init_server()
#
#
# if __name__ == '__main__':
#     main()
