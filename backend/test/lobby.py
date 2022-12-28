import random
import string

from backend.config import get_config
from backend.test.auth import create_profile, login, delete_profile


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


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", result_str)

    return result_str


def main():
    username = "b"
    access_token = "b"
    game_id = "gn1,"
    capacity = 2
    create_game(username, access_token, game_id, capacity)

    create_1()
    join_2()
    join_3()
    leave_2()
    leave_1()
    leave_3()

    username = "test"
    access_token = "test"
    get_games(username, access_token)
    #
    # # todo capacity = ful, adding new player?


import json
import unittest

import requests

from backend.test.comm import encode_username_password, \
    encode_username_access_token


class TestMain(unittest.TestCase):

    # def load_config(cls):
    #
    #     config = get_config()
    #
    #     cls.base = config["apiURL"]
    #
    #     cls.game_url = cls.base + "/lobby"
    #
    #     cls.non_existing_username = config["nonExistingUsername"]
    #     cls.non_existing_password = config["nonExistingPassword"]
    #
    #     cls.wrong_username = config["incorrectUsername"]
    #     cls.wrong_password = config["incorrectPassword"]
    #
    #     cls.game_id = config["gameId"]
    #
    #     cls.players_username_prefix = config["gamePlayers"]["usernamePrefix"]
    #     cls.players_password_prefix = config["gamePlayers"]["passwordPrefix"]
    #
    #     cls.number_of_player = config["gameUsersGenerated"]
    #
    #     cls.players = {}

    def load_config(self):

        config = get_config()

        self.base = config["apiURL"]

        self.game_url = self.base + "/lobby"

        self.non_existing_username = config["nonExistingUsername"]
        self.non_existing_password = config["nonExistingPassword"]

        self.wrong_username = config["incorrectUsername"]
        self.wrong_password = config["incorrectPassword"]

        self.game_id = config["gameId"]

        self.players_username_prefix = config["gamePlayers"]["usernamePrefix"]
        self.players_password_prefix = config["gamePlayers"]["passwordPrefix"]

        self.number_of_players = config["gameUsersGenerated"]

        self.players = {}

    @classmethod
    def setUpClass(cls):

        cls.load_config(cls)

        """create users"""

        for i in range(cls.number_of_players):

            try:

                r = create_profile(
                    username=f"{cls.players_username_prefix} {i}",
                    password=f"{cls.players_password_prefix} {i}",
                    base=cls.base
                )
                access_token = r["auth"]["accessToken"]

            except KeyError:
                """login"""
                r = login(
                    username=f"{cls.players_username_prefix} {i}",
                    password=f"{cls.players_password_prefix} {i}",
                    base=cls.base

                )

                access_token = r["auth"]["accessToken"]

            cls.players[i] = {
                "username": f"{cls.players_username_prefix} {i}",
                "access token": access_token
            }

        print("setup done")

    @classmethod
    def tearDownClass(cls):

        cls.load_config(cls)

        for i in range(cls.number_of_players):
            """login"""
            r = login(
                username=f"{cls.players_username_prefix} {i}",
                password=f"{cls.players_password_prefix} {i}",
                base=cls.base
            )
            access_token = r["auth"]["accessToken"]

            delete_profile(
                username=f"{cls.players_username_prefix} {i}",
                access_token=access_token,
                base=cls.base
            )

    def create_profile(self, username, password):
        print()
        print("create user")

        url = f"{self.base}/signup/{username}"

        t = requests.post(
            url,
            headers={
                "Authorization": encode_username_password(
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
                "Authorization": encode_username_access_token(
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

    def log(self, content):
        print(content)

    def create_game(self, username, access_token, game_name, capacity):
        url = "http://localhost:8000/game"

        t = requests.post(
            f"{url}/{game_name}",
            headers={
                "Authorization": encode_username_access_token(
                    type_="Custom",
                    username=username,
                    access_token=access_token
                )
            },
            data={
                "capacity": capacity,
            }
        )

        print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))
        return json.loads(t.text)

    def test_setup_teardown(self):
        for k, v in self.players.items():
            print(k, v)

        self.assertEqual(True, True)

    def test_create_game(self):

        r = self.create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        r = self.create_game(
            self.non_existing_username,
            access_token,
            self.game_id,
            capacity=2
        )

        print(f"{r=}")

        self.cleanup_delete_profile(self.non_existing_username, access_token)


if __name__ == "__main__":
    unittest.main()
