import json


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
