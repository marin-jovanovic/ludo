import asyncio

from protocols.util.client import Client
from protocols.util.message import Message, MessageCodes


class EchoConnection(asyncio.Protocol):

    def __init__(self, on_con_lost):
        self.on_con_lost = on_con_lost
        self.rec_q = asyncio.Queue()
        self.raw_data_buffer = ""

    def connection_made(self, transport):
        peer_name = transport.get_extra_info('peername')
        print('Connection from {}'.format(peer_name))
        self.transport = transport

    def data_received(self, data):

        self.raw_data_buffer += data.decode()

        while self.raw_data_buffer.endswith(";"):
            to_process, self.raw_data_buffer = self.raw_data_buffer.split(";", 1)

            message = Message(to_process)

            self.rec_q.put_nowait(message)

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


class TCPClient(Client):
    # todo add option to connect to multiple servers

    def __init__(self, domain_name="127.0.0.1", port=8888):
        super(TCPClient, self).__init__(domain_name, port)

        self.loop = asyncio.get_running_loop()
        self.on_con_lost = self.loop.create_future()
        self.protocol = EchoConnection(self.on_con_lost)

    async def send(self, payload):

        self.transport.write(payload.byte_representation())

    async def receive(self):

        ret = await self.protocol.rec_q.get()

        # no processing

        self.protocol.rec_q.task_done()

        return ret

    async def close(self):

        # todo

        if self.protocol.rec_q.empty():
            await self.protocol.rec_q.join()


        try:
            await self.on_con_lost
        finally:
            self.transport.close()

        # self.transport.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


async def tcp_client_wrapper(domain_name="127.0.0.1", port=8888):
    client = TCPClient(domain_name, port)

    client.transport, _ = await client.loop.create_connection(
        lambda: client.protocol,
        domain_name,
        port
    )

    return client


async def async_main():
    async with await tcp_client_wrapper() as p:

        await p.send(t := Message("1 aaa"))
        print("sending", t)
        print("Data received:", await p.receive(),  "\n")

        await p.send(t := Message({"a": 1, "b": 2}))
        print("sending", t)
        print("Data received:", await p.receive(),  "\n")

        await p.send(t := Message("2 bbb"))
        print("sending", t)
        await p.send(t := Message("3 ccc"))
        print("sending", t)
        print("Data received:", await p.receive())
        print("Data received:", await p.receive(),  "\n")

        await p.send(t := Message(9999 * "xxxxxxxxx"))
        print("sending", t)
        print("Data received:", await p.receive(),  "\n")

        await p.send(t := Message("4 ddd"))
        print("sending", t)
        await p.send(t := Message("5 eee"))
        print("sending", t)
        # await p.send(t := Message("FIN"))
        print("sending", t)
        print("Data received:", await p.receive())
        print("Data received:", await p.receive(),  "\n")

    print("done")

def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    main()
