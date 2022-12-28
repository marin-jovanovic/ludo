import json
import time

from bcrypt import gensalt


def sleep_random():
    salt = gensalt()
    for i in reversed(salt.decode("utf-8")):
        t = int(str(ord(i))[-1])
        if t in [1, 2, 3]:
            time.sleep(t)
            break


def pretty_print_json(payload):
    print(json.dumps(payload, indent=4, sort_keys=True))


def bytes_to_json(content):
    return json.loads(content.decode("utf-8"))


def get_empty_response_template():
    response = {
        "auth": {
            "status": False,
            # "access-token": "",
            # "refresh-token": ""
        },
        "payload": {
            "status": False,
        },
        # "debug": {
        # }
    }
    return response


class Notifier:
    """
    mainly used to send something over ws when db is updated
    """

    def __init__(self):
        self._observers = []

    def notify(self, msg):
        for observer in self._observers:
            observer.update(msg)

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
