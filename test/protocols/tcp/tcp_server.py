import asyncio

from protocols.util.message import Message, MessageCodes


class EchoConnection(asyncio.Protocol):

    def __init__(self):
        print("echo connection init")
        self.raw_data_buffer = ""

    def connection_made(self, transport):
        peer_name = transport.get_extra_info('peername')
        print('Connection from {}'.format(peer_name))
        self.transport = transport

    def data_received(self, data):

        self.raw_data_buffer += data.decode()

        while self.raw_data_buffer.endswith(";"):
            to_process, self.raw_data_buffer = self.raw_data_buffer.split(";", 1)

            m = Message(to_process)

            if m.payload == MessageCodes.FIN.value:
                print("fin message code detected; closing connection")
                self.transport.close()
            else:
                payload = Message({"server_add_len": len(m.payload)},
                                  str(m.payload) + " tmp")

                self.transport.write(payload.byte_representation())


async def async_main():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoConnection(),
        '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    main()
