import random
import string

from backend.config import get_config
from backend.test.auth import create_profile, login, delete_profile



def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", result_str)

    return result_str


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

def leave_game(url, username, access_token, level_id):

    t = requests.put(
        f"{url}/{level_id}",
        headers={
            "Authorization": encode_username_access_token(
                type_="Custom",
                username=username,
                access_token=access_token
            )
        },
        data={
            "leave": True,
        },
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))
    return json.loads(t.text)

def join_game(url, username, access_token, game_name):

    t = requests.put(
        f"{url}/{game_name}",
        headers={
            "Authorization": encode_username_access_token(
                type_="Custom",
                username=username,
                access_token=access_token
            )        },
        data={
            "join": True,
        },
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
        return
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

    def test_create_one_level(self):

        username = self.players[0]["username"]
        access_token = self.players[0]["access token"]


        # # return ok
        r = create_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_name="level_name",
            capacity=2
        )

        # user role not empty
        r = create_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_name="level_name",
            capacity=2
        )

        # user role not empty
        r = create_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_name="level_name 2",
            capacity=2
        )

        username = self.players[1]["username"]
        access_token = self.players[1]["access token"]

        # duplicate name
        r = create_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_name="level_name",
            capacity=2
        )

        # all good
        r = create_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_name="level_name 2",
            capacity=2
        )

    def test_create_and_leave(self):
        username = self.players[0]["username"]
        access_token = self.players[0]["access token"]

        level_name = "x"
        capacity = 2

        r = create_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_name=level_name,
            capacity=capacity
        )

        r =  leave_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_id=level_name
        )

    def test_join_level(self):
        username = self.players[0]["username"]
        access_token = self.players[0]["access token"]

        level_name = "x"
        capacity = 2

        r = create_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_name=level_name,
            capacity=capacity
        )

        return

        username = self.players[1]["username"]
        access_token = self.players[1]["access token"]

        r = join_game(
            url = self.level_url,
            username = username,
            access_token = access_token,
            game_name = level_name,
        )

        # try adding third player, this needs to fail
        username = self.players[2]["username"]
        access_token = self.players[2]["access token"]

        r = join_game(
            url = self.level_url,
            username = username,
            access_token = access_token,
            game_name = level_name,
        )

        # return

        # remove 2nd
        username = self.players[1]["username"]
        access_token = self.players[1]["access token"]
        r =  leave_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_id=level_name
        )

        # try remove 3rd
        username = self.players[2]["username"]
        access_token = self.players[2]["access token"]
        r =  leave_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_id=level_name
        )

        username = self.players[0]["username"]
        access_token = self.players[0]["access token"]

        r =  leave_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_id=level_name
        )


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
