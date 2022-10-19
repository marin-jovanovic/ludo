import json
import time

import requests

def get_games(username, access_token):
    url = "http://localhost:8000/game"

    t = requests.get(
        f"{url}/",
        headers={
            "Authorization": f"Custom {username}:{access_token}"
        },
        data={
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

def join_game(username, access_token, game_name):
    url = "http://localhost:8000/game"

    t = requests.put(
        f"{url}/{game_name}",
        headers={
            "Authorization": f"Custom {username}:{access_token}"
        },
        data={
            "join": True,
        },
        verify=False
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))
    return json.loads(t.text)


def create_1():
    username = "test"
    access_token = "test"
    game_id = "gn1"
    capacity = 2
    create_game(username, access_token, game_id, capacity)


def leave_1():
    username = "test"
    access_token = "test"
    game_id = "gn1"
    capacity = 2
    leave_game(username, access_token, game_id)


def join_2():
    username = "a"
    access_token = "a"
    game_id = "gn1"
    join_game(username, access_token, game_id)


def leave_2():
    username = "a"
    access_token = "a"
    game_id = "gn1"
    leave_game(username, access_token, game_id)


def join_3():
    username = "b"
    access_token = "b"
    game_id = "gn1"
    join_game(username, access_token, game_id)


def leave_3():
    username = "b"
    access_token = "b"
    game_id = "gn1"
    leave_game(username, access_token, game_id)


def main():
    # username = "b"
    # access_token = "b"
    # game_id = "gn1,"
    # capacity = 2
    # create_game(username, access_token, game_id, capacity)


    # create_1()
    # join_2()
    # join_3()
    # leave_2()
    # leave_1()
    # leave_3()

    username = "test"
    access_token = "test"
    get_games(username, access_token)

    # todo capacity = ful, adding new player?


if __name__ == '__main__':
    main()