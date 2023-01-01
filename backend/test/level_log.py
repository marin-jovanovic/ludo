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


# todo automate using statistics    view

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

def log_driver(url, username, access_token):
    t = requests.put(
        # url,
        f"{url}",
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

def get_log(url, username, access_token):
    t = requests.get(
        f"{url}",
        headers={
            "Authorization": encode_username_access_token(
                type_="Custom",
                username=username,
                access_token=access_token
            )
        },
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))
    return json.loads(t.text)

def add_to_log(url, username, access_token, token_id):
    t = requests.put(
        f"{url}",
        headers={
            "Authorization": encode_username_access_token(
                type_="Custom",
                username=username,
                access_token=access_token
            )
        },
        data={
            "tokenId": token_id
        }
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))
    return json.loads(t.text)



class TestMain(unittest.TestCase):

    def construct_log_path(self, level_id):
        level_id = str(level_id)

        config = get_config()
        return self.base + "/" + config["levelPath"] + "/" + level_id + "/" + config["levelLogPath"]


    def load_config(self):

        config = get_config()

        self.base = config["apiURL"]

        self.level_url = self.base + "/" + config["levelPath"]
        # self.level_log_url = self.base + "/" + config["levelLogPath"]
        # self.log_url =

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

    def test_get_log(self):
        username = self.players[0]["username"]
        access_token = self.players[0]["access token"]

        level_name = "y"
        capacity = 2

        r = create_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_name=level_name,
            capacity=capacity
        )

        level_id = r["payload"]["levelId"]


        r = get_log(
            url=self.construct_log_path(level_id),
            username=username,
            access_token=access_token,
        )

        # log = r["payload"]["payload"]
        # max_rule = max(log.keys())
        # print(f"{max_rule=}")

        # entry = log[max_rule]
        # if entry.action == "roll" and


        # r = add_to_log(
        #     url=self.construct_log_path(level_id),
        #     username=username,
        #     access_token=access_token,
        #     token_id=0
        # )

        # r = get_log(
        #     url=self.construct_log_path(level_id),
        #     username=username,
        #     access_token=access_token,
        # )


        r =  leave_game(
            url=self.level_url,
            username=username,
            access_token=access_token,
            level_id=level_name
        )


if __name__ == "__main__":
    unittest.main()
