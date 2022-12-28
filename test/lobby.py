import json
import time

import requests
import random
import string
import urllib.parse
import base64
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


class Auth:

    def __init__(self):
        self.base = "http://localhost:8000"

    def encode_username_password(self, type_, username, password):

        unencoded = f"{type_} {username}:{password}"
        as_bytes = unencoded.encode("ascii")
        base64_bytes = base64.b64encode(as_bytes)
        base64_string = base64_bytes.decode("ascii")
        return base64_string


    def encode_username_access_token(self, type_, username, access_token):

        unencoded = f"{type_} {username}:{access_token}"
        as_bytes = unencoded.encode("ascii")
        base64_bytes = base64.b64encode(as_bytes)
        base64_string = base64_bytes.decode("ascii")
        return base64_string

    def create_profile(self, username, password):
        print()
        print("create user")

        url = f"{self.base}/signup/{username}"

        t = requests.post(
            url,
            headers={
                "Authorization": self.encode_username_password(
                    type_="Create",
                    username=username,
                    password=password
                )
            },
            data={
            },
        )

        print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))
        return json.loads(t.text)

    def logout(self, username, access_token):
        print()
        print("logout")
        url = f"{self.base}/logout/{username}"

        t = requests.post(
            url,
            headers={
                "Authorization": self.encode_username_access_token(
                    type_="Custom",
                    username=username,
                    access_token=access_token
                )
            },
            data={
            },
        )

        print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))
        return json.loads(t.text)

    def login(self, username, password):
        print()
        print("login")
        url = f"{self.base}/login/{username}"

        t = requests.post(
            url,
            headers={
                "Authorization": self.encode_username_password(
                    type_="Basic",
                    username=username,
                    password=password
                )
            },
            data={
            },
        )

        print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))
        return json.loads(t.text)

    def delete_profile(self, username, access_token):
        print()
        print("delete profile")
        url = f"{self.base}/deleteProfile/{username}"
        auth = urllib.parse.quote(f"{username}:{access_token}")

        t = requests.post(
            url,
            headers={
                "Authorization": self.encode_username_access_token(
                    type_="Custom",
                    username=username,
                    access_token=access_token
                )
            },
            data={
            },
        )

        print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))
        return json.loads(t.text)

def log_error(pl):
    print(f"[err] {pl}")

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", result_str)

    return result_str

def main():

    auth = Auth()

    username = get_random_string(10)
    username = "jqszpenmhz"
    password = "@,<>12#*mdAmf-"
    # password = "aA1@aaaa"

    r = auth.create_profile(username=username, password=password)
    if not r["auth"]["status"]:
        log_error("signup")
        return
    access_token = r["auth"]["accessToken"]

    r = auth.logout(username=username, access_token=access_token)
    if not r["auth"]["status"]:
        log_error("logout")
        return

    r = auth.login(username=username, password=password)
    if not r["auth"]["status"]:
        log_error("login")
        return
    access_token = r["auth"]["accessToken"]

    r = auth.delete_profile(username=username, access_token=access_token)
    if not r["auth"]["status"]:
        log_error("delete profile")
        return

    # print(f"{r=}")

    # print(auth.create_user())

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

    # username = "test"
    # access_token = "test"
    # get_games(username, access_token)
    #
    # # todo capacity = ful, adding new player?


if __name__ == '__main__':
    main()