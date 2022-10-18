"""
utils for address translations
"""
import asyncio
import time

from hat.aio import run_asyncio
from hat.drivers import iec104

from protocols.util.client import Client





ADDRESSES = []

async def load_addresses(connection=None):
    global ADDRESSES

    if not connection:
        address = iec104.Address('127.0.0.1', 19999)

        connection = await iec104.connect(address)

    raw_data = await connection.interrogate(asdu_address=65535)

    for result in raw_data:
        asdu_address = result.asdu_address
        io_address = result.io_address

        # ADDRESSES.append(Address(asdu_address, io_address))

    [print(i.formatted_name()) for i in ADDRESSES]


class IEC104Client(Client):
    #     class Client(object):
    #     __metaclass__ = ABCMeta
    #
    #     def __init__(self, domain_name="127.0.0.1", port=5000):
    #         print("Client init")
    #         self.domain_name = domain_name
    #         self.port = port
    #
    #     @abstractmethod
    #     async def send(self, payload):
    #         raise NotImplementedError
    #
    #     @abstractmethod
    #     async def receive(self):
    #         raise NotImplementedError
    #
    #     @abstractmethod
    #     async def connect(self):
    #         raise NotImplementedError
    #
    #     @abstractmethod
    #     async def close(self):
    #         raise NotImplementedError

    def __init__(self, domain_name="127.0.0.1", port=5000):
        super(IEC104Client, self).__init__(domain_name, port)

        self.known_states = {}

    async def receive_single(self):
        """"""

    async def receive_all(self, asdu_address):
        """"""

        return await self.connection.interrogate(asdu_address)

        # self.update_states(states)
        # return states

    async def diff(self):
        """"""

    async def connect(self):
        """"""

        address = iec104.Address('127.0.0.1', 19999)

        while True:

            try:
                connection = await iec104.connect(address)
                return connection

            except ConnectionRefusedError:
                n = 3
                for i in range(n):
                    print("trying to reconnect in", n - i)
                    await asyncio.sleep(1)
                print("reconnecting\n")

    async def send(self, payload):
        """"""

    async def receive(self):
        """"""

    # todo implement async enter and exit
    async def close(self):
        """"""


async def iec_104_init_wrapper(domain_name="127.0.0.1", port=19999):
    client = IEC104Client(domain_name, port)

    client.address = iec104.Address(domain_name, port)
    client.connection = await iec104.connect(client.address)

    return client


# async def connect():
#     address = iec104.Address('127.0.0.1', 19999)
#
#     while True:
#
#         try:
#             connection = await iec104.connect(address)
#             return connection
#
#         except ConnectionRefusedError:
#             n = 3
#             for i in range(n):
#                 print("trying to reconnect in", n - i)
#                 await asyncio.sleep(1)
#             print("reconnecting\n")
#

async def async_main():

    client = await iec_104_init_wrapper("127.0.0.1", 19999)

    raw_data = await client.receive_all(asdu_address=65535)
    [print(i) for i in raw_data]

    return

    # address = iec104.Address('127.0.0.1', 19999)
    # while True:
    #     try:
    #         connection = await iec104.connect(address)
    #         break
    #     except:
    #         continue
    #
    # try:
    #     raw_data = await connection.interrogate(asdu_address=65535)
    # except:
    #     address = iec104.Address('127.0.0.1', 19999)
    #     connection = await iec104.connect(address)
    #     raw_data = await connection.interrogate(asdu_address=65535)
    #
    # [print(i) for i in raw_data]
    #
    # return

    # connection = await connect()
    # breakpoint()

    raw_data = await connection.interrogate(asdu_address=65535)
    print(len(raw_data))
    print("r", raw_data)

    while True:

        try:
            print("fetch")
            raw_data = await connection.receive()
            print("r", raw_data)

        except ConnectionError:
            print("connection lost")

            connection = await connect()


def main():
    run_asyncio(async_main())


if __name__ == '__main__':
    main()


# address = iec104.Address('127.0.0.1', 19999)
# while True:
#     try:
#         connection = await iec104.connect(address)
#         break
#     except:
#         continue
#
# try:
#     raw_data = await connection.interrogate(asdu_address=65535)
# except:
#     address = iec104.Address('127.0.0.1', 19999)
#     connection = await iec104.connect(address)
#     raw_data = await connection.interrogate(asdu_address=65535)
#
# [print(i) for i in raw_data]
#
# return

# async def async_main():
#
#     await asyncio.sleep(5)
#     print("start")
#     address = iec104.Address('127.0.0.1', 19999)
#     connection = await iec104.connect(address)
#     raw_data = await connection.interrogate(asdu_address=65535)
#     [print(i) for i in raw_data]
#     return
#
#
#
#     connection = await connect()
#     breakpoint()
#
#     raw_data = await connection.interrogate(asdu_address=65535)
#     print(len(raw_data))
#     print("r", raw_data)
#
#     while True:
#
#         try:
#             print("fetch")
#             raw_data = await connection.receive()
#             print("r", raw_data)
#
#         except ConnectionError:
#             print("connection lost")
#
#             connection = await connect()
#
#
# def main():
#     address = Address('127.0.0.1', 19999)
#
#
# if __name__ == '__main__':
#     main()