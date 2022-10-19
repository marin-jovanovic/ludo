import json
import time

import requests

def get_last(portfolio):
    t = requests.get(
        f"{url}/{portfolio}",
        data={
            "options": "last"
        },
        verify=False
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))


def patch():

    t = requests.patch(
        url + "d",
        data={
            "name": "d",
            "colour": "p"

        },
        verify=False
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))

def delete(portfolio):
    print(f"{portfolio=}")
    t = requests.delete(
        f"{url}/{portfolio}",
        data={
            # "portfolio": portfolio
        },
        verify=False
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))

def create_game(username, access_token, game_name, capacity):
    url = "http://localhost:8000/game"

    t = requests.post(
        f"{url}/{game_name}",
        headers={
            "Authorization": f"Custom {username}:{access_token}"
            # "Authorization": f"Basic {username}:{access_token}"
        },
        data={
            "capacity": capacity,
            "tmp": 2
        },
        verify=False
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))
    return json.loads(t.text)

def leave_game(username, access_token, game_name):
    url = "http://localhost:8000/game"

    t = requests.put(
        f"{url}/{game_name}",
        headers={
            "Authorization": f"Custom {username}:{access_token}"
        },
        data={
            "leave": True,
        },
        verify=False
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))
    return json.loads(t.text)


def main():
    username = "test"
    access_token = "test"
    game_id = "gn1"
    capacity = 2

    leave_game(username, access_token, game_id)
    # create_game(username, access_token, game_id, capacity)



if __name__ == '__main__':
    main()