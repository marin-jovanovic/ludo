from abc import ABC

from hat.aio import run_asyncio
from websocket import create_connection

from protocols.util.client import Client
from time import sleep

from protocols.util.message import Message


class WSClient(Client, ABC):

    def __init__(self, domain_name="127.0.0.1", port=8765):
        super().__init__(domain_name, port)

        # open socket
        while True:
            try:
                self.connection = create_connection(self._get_uri())
                break
            except ConnectionRefusedError:
                print("connection refused")

            sleep(1)
            print("reconnecting")

        print("connected")

    def _get_uri(self):
        return "ws://" + str(self.domain_name) + ":" + str(self.port)

    async def send(self, payload):
        self.connection.send(payload)

    async def receive(self):
        # receive from socket
        return self.connection.recv()


async def async_main():
    client = WSClient()

    message = Message("header", "msg")

    await client.send(message.byte_representation())
    value = await client.receive()
    print(value, type(value))
    # print(await client.receive())

    await client.send("1")
    print(await client.receive())

    await client.send("2")
    print(await client.receive())
    # print(await client.receive())

    await client.send("3")
    await client.send("4")
    print(await client.receive())
    print(await client.receive())

    await client.send("5")
    await client.send("6")
    print(await client.receive())
    print(await client.receive())

    client.connection.close()


def main():
    run_asyncio(async_main())


if __name__ == '__main__':
    main()
