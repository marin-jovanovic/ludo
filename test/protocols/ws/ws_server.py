import os
import sys

import asyncio
import signal

import nest_asyncio
import websockets
from hat.aio import run_asyncio

from protocols.util.server import Server
from protocols.util.message import Message


class WSServer(Server):

    def __init__(self, domain_name="127.0.0.1", port=8765):
        super().__init__(domain_name, port)

        self.debug_counter = 0

    async def driver(self, websocket, _):

        async for raw_data in websocket:
            print("received:", raw_data)
            print()

            message = Message(raw_data)

            await websocket.send(
                str("echo: " + str(self.debug_counter) + " "
                    + str(message))
            )

            self.debug_counter += 1

            print("msg", message)


async def init_server():

    server = WSServer("localhost", 8765)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    print("connect on ws://" + server.host_name + ":" + str(server.port))

    asyncio.get_event_loop().run_until_complete(
        websockets.serve(server.driver, server.host_name, server.port))
    asyncio.get_event_loop().run_forever()

    return server


async def async_main():
    await init_server()


def main():
    nest_asyncio.apply()
    run_asyncio(async_main())


if __name__ == '__main__':
    main()
