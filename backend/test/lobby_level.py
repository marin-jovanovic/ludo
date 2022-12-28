import random
import string

from backend.config import get_config
from backend.test.auth import create_profile, login, delete_profile


def leave_game(url, username, access_token, level_id):

    t = requests.put(
        f"{url}/{level_id}",
        headers={
            "Authorization": encode_username_access_token(
                type_="Custom",
                username=username,
                access_token=access_token
            )        },
        data={
            "leave": True,
        },
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

from backend.test.comm import encode_username_access_token


def get_games(url, username, access_token):
    t = requests.get(
        f"{url}/",
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


def create_game(url, username, access_token, level_name, capacity):
    t = requests.post(
        f"{url}/{level_name}",
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


class TestMain(unittest.TestCase):

    def load_config(self):

        config = get_config()

        self.base = config["apiURL"]

        self.level_url = self.base + "/" + config["levelPath"]

        self.non_existing_username = config["nonExistingUsername"]
        self.non_existing_password = config["nonExistingPassword"]

        self.wrong_username = config["incorrectUsername"]
        self.wrong_password = config["incorrectPassword"]

        self.level_id_prefix = config["levelIdPrefix"]

        self.players_username_prefix = config["levelPlayers"]["usernamePrefix"]
        self.players_password_prefix = config["levelPlayers"]["passwordPrefix"]

        self.number_of_players = config["levelUsersGenerated"]

        self.players = {}

        self.max_level_capacity = config["levelMaxCapacity"]

        self.levels = {i: self.level_id_prefix + str(i) for i in range(self.max_level_capacity + 1)}

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

    def log(self, content):
        print(content)

    def test_setup_teardown(self):
        for k, v in self.players.items():
            print(k, v)

        self.assertEqual(True, True)

    def test_get_all_levels(self):

        username = self.players[0]["username"]
        access_token = self.players[0]["access token"]

        r = get_games(
            url=self.level_url,
            username=username,
            access_token=access_token,
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(True, r["auth"]["status"])
        self.assertEqual(username, r["auth"]["username"])
        self.assertEqual(access_token, r["auth"]["accessToken"])

        self.assertEqual(3, len(r["payload"]))
        self.assertEqual(True, r["payload"]["status"])
        self.assertEqual(True, all(
            [
                [i in ["capacity", "name", "players"] for i in level_meta]
                for level_id, level_meta in r["payload"]["levels"].items()
            ]
        ))

        for level_id, level_meta in r["payload"]["levels"].items():

            self.assertEqual(True, isinstance(level_meta["capacity"], int))
            self.assertEqual(True, isinstance(level_meta["name"], str))
            self.assertEqual(True, isinstance(level_meta["players"], list))

            capacity = level_meta["capacity"]
            players = level_meta["players"]

            if len(players) > capacity:
                self.assertEqual(True, False)

        in_level = r["payload"]["inLevel"]

        if not in_level:
            return

        is_found = False

        for level_id, level_meta in r["payload"]["levels"].items():

            players = level_meta["players"]

            if username in players:
                if is_found:
                    """can not be in multiple levels at the same time"""
                    self.assertEqual(True, False)

                is_found = True

        self.assertEqual(True, is_found)

    def test_create_level(self):

        username = self.players[0]["username"]
        access_token = self.players[0]["access token"]

        for capacity, level_name in self.levels.items():

            r = create_game(
                url=self.level_url,
                username=username,
                access_token=access_token,
                level_name=level_name,
                capacity=capacity
            )

    def test_delete_level(self):


        pass


    def test_leave_level(self):

        username = self.players[0]["username"]
        access_token = self.players[0]["access token"]

        for capacity, level_name in self.levels.items():

            r = create_game(
                url=self.level_url,
                username=username,
                access_token=access_token,
                level_name=level_name,
                capacity=capacity
            )

        r = leave_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_id=level_name,

        )



    def test_delete_other_users_level(self):

        raise NotImplementedError


if __name__ == "__main__":
    unittest.main()
