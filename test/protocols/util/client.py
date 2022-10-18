from abc import ABCMeta, abstractmethod


class Address:

    @staticmethod
    def get_as_csv(asdu_address, io_address):
        return str(asdu_address) + ";" + str(io_address)

    def __init__(self, asdu_address, io_address):
        self.asdu_address = asdu_address
        self.io_address = io_address

    def __str__(self):
        return f"{self.asdu_address=} {self.io_address=}"

    def formatted_name(self):
        return Address.get_as_csv(self.asdu_address, self.io_address)


class Data:

    def __init__(self, asdu_address, io_address, value):
        self.asdu_address = asdu_address
        self.io_address = io_address
        self.value = value


class Client(object):
    __metaclass__ = ABCMeta

    def __init__(self, domain_name="127.0.0.1", port=5000):
        print("Client init")
        self.domain_name = domain_name
        self.port = port

        # (asdu, io) -> value
        self.known_states = {}

    @abstractmethod
    async def send(self, payload):
        raise NotImplementedError

    @abstractmethod
    async def receive(self):
        raise NotImplementedError

    # @abstractmethod
    # async def connect(self):
    #     raise NotImplementedError

    @abstractmethod
    async def close(self):
        raise NotImplementedError

    def update_states(self, new_payload):
        """


        :param new_payload: Data
        :return:
        """

        new_states = {}
        diff = {}

        for i in new_payload:

            if (k := (i.asdu_address, i.io_address)) not in self.known_states:
                new_states[k] = i.value
                self.known_states[k] = i.value

            elif self.known_states[k] != i.value:
                diff[k] = i.value
                self.known_states[k] = i.value

        print("diff")
        for k, v in diff.items():
            print(k, v)

        print("new states")
        for k, v in new_states.items():
            print(k, v)

        return new_states, diff
