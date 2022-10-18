import enum
from ast import literal_eval
import json
import re


class MessageCodes(enum.Enum):
    FIN = "FIN"


# todo check if literal eval is safe
class Message:
    """
    used for communication between server and client

    when server or client is sending message it is sending this object

    assumption is that we can only send strings with used protocol

    header is stored as dictionary

    payload is stored as any

    ----------------------------------------------------------------------------

    recommended use

            message = Message(
                {"param 1": "val 1", "param 2": "val 2"},
                "payload content"
            )

        server sending

            server.send(
                message.encode()
            )

        server receiving
            message = server.receive().decode()

    supported use

            message = Message(arg[0], arg[1])
            arg[0] = None, any
            arg[1] = None, any, left out


    """



    def __init__(self, *args):
        if len(args) == 1:

            message = args[0]

            # if isinstance(args[0], str):
            #
            #     message = str(message)

            self.header, self.payload = Message.decode(message)

        elif len(args) == 2:

            h, p = args[0], args[1]

            if not p:
                p = h if h else p

                h = {}

            if h:

                try:
                    self.header = literal_eval(h)

                    # todo check cast to json

                except ValueError:
                    self.header = h

            else:
                self.header = {}

            payload_buffer = None

            if not isinstance(self.header, dict):

                payload_buffer = self.header
                self.header = {}

            if p:

                try:
                    self.payload = literal_eval(p)
                except (ValueError, SyntaxError):
                    self.payload = p

            else:
                self.payload = None

            if payload_buffer:
                self.payload = str(payload_buffer) + str(self.payload)

        else:
            raise NotImplementedError


        if not hasattr(self.header, "len"):
            self.header["len"] = len(self.payload)
        # print(f"Message; instantiated with {self.header=} {self.payload=}")

    def byte_representation(self):
        return (str({"header": self.header, "payload": self.payload}) + ";").encode("utf-8")

    def __str__(self):
        return str(["header:", self.header, "payload", self.payload])

    @staticmethod
    def decode(message: str):
        """
        decodes message and tries to evaluate its content

        expected
            message = {
                "header": any,
                "payload": any
            }


        :param message: input as string
        :return: decoded message as (header, payload)
        """

        # print(f"to decode {message=} {type(message)=}")

        if not isinstance(message, str):

            if not message:
                return {}, None

            message = str(message)

        try:

            p = re.compile('(?<!\\\\)\'')
            string_cleaned_message = p.sub('\"', message)
            message_as_json = json.loads(string_cleaned_message)
            # print(f"{message_as_json=} {type(message_as_json)=}")

            # message_as_json = json.loads(message)

            if "header" in message_as_json:
                header = message_as_json["header"]

            else:
                header = {}
                payload = message_as_json

            if "header" in message_as_json and "payload" in message_as_json:
                payload = message_as_json["payload"]

        except json.decoder.JSONDecodeError:

            header = {}

            try:
                payload = literal_eval(message)

            except (ValueError, SyntaxError):
                header = {}
                payload = message

        return header, payload

    @staticmethod
    def encode(message):
        return json.dumps(message)


def main():

    try:
        Message()
        assert False
    except NotImplementedError:
        pass

    for m, expected_header, expected_payload in [
        ("{'header': {}, 'payload': '1 aaa'}", {}, "1 aaa"),
        (None, {}, None),
        ("a", {}, "a"),
        ({"a": "b"}, {}, {"a": "b"}),
        ({"a": "b", "c": {"d": "e"}}, {}, {"a": "b", "c": {"d": "e"}}),
        (["a", "b"], {}, ["a", "b"]),
        ({"c", "ab"}, {}, {"c", "ab"}),

    ]:
        print(f"test {m=}, {expected_header=} {expected_payload=}")

        # todo test with one arg
        message = Message(m)
        print(f"{message.header=}")
        print(f"{message.payload=}")

        assert message.header == expected_header
        assert message.payload == expected_payload

        print()

    for header, payload, expected_header, expected_payload in [
        (None, None, {}, None),
        (None, "a", {}, "a"),
        ("a", None, {}, "a"),
        ({"a": "b"}, None, {}, {"a": "b"}),
        (None, {"a": "b"}, {}, {"a": "b"}),
        ({"a": "b"}, {"c": "d"}, {"a": "b"}, {"c": "d"}),
        ({"a": "b", "c": {"d": "e"}}, None, {}, {"a": "b", "c": {"d": "e"}}),
        ({"a": "b", "c": {"d": "e"}}, {"f": "g", "h": {"i": "j"}},
         {"a": "b", "c": {"d": "e"}}, {"f": "g", "h": {"i": "j"}}),

        (None, ["a", "b"], {}, ["a", "b"]),
        (["a", "b"], None, {}, ["a", "b"]),

        ("c", ["a", "b"], {}, "c" + str(["a", "b"])),
        (["d", "e"], ["a", "b"], {}, str(["d", "e"]) + str(["a", "b"])),
        ({"c"}, ["a", "b"], {}, str({"c"}) + str(["a", "b"])),
        ({"c"}, None, {}, {"c"}),
        ({"c"}, "ab", {}, str({"c"}) + "ab"),
    ]:
        print(f"test {header=} {payload=}")

        # todo test with one arg
        message = Message(header, payload)
        print(f"{message.header=}")
        print(f"{message.payload=}")

        assert message.header == expected_header
        assert message.payload == expected_payload

        print()

    m = Message("1 aaa")


if __name__ == '__main__':
    main()
