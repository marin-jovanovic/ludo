import json

import argparse
import base64
import getpass
import hashlib
import json
import sys
import time
from os import path
from bcrypt import hashpw, gensalt


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
            "access-token": "",
            "refresh-token": ""
        },
        "payload": {
        },
        "debug": {
        }
    }
    return response
