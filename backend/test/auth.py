import json
import unittest

import requests

from backend.config import get_config
from backend.test.comm import encode_username_password, \
    encode_username_access_token


def create_profile(username, password, base):
    print()
    print("create user")

    url = f"{base}/signup/{username}"

    t = requests.post(
        url,
        headers={
            "Authorization": encode_username_password(
                type_="Create",
                username=username,
                password=password
            )
        }
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))
    return json.loads(t.text)


def login(username, password, base):
    print()
    print("login")
    url = f"{base}/login/{username}"

    t = requests.post(
        url,
        headers={
            "Authorization": encode_username_password(
                type_="Basic",
                username=username,
                password=password
            )
        }
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))
    return json.loads(t.text)


def delete_profile(username, access_token, base):
    print()
    print("delete profile")
    url = f"{base}/deleteProfile/{username}"

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


def logout(username, access_token, base):
    print()
    print("logout")
    url = f"{base}/logout/{username}"

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


class TestAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = get_config()

        cls.base = config["apiURL"]

        cls.non_existing_username = config["nonExistingUsername"]
        cls.non_existing_password = config["nonExistingPassword"]

        cls.wrong_username = config["incorrectUsername"]
        cls.wrong_password = config["incorrectPassword"]

        """
        login
        we need to obtain new access token
        """
        r = login(
            username=cls.non_existing_username,
            password=cls.non_existing_password,
            base=cls.base
        )
        try:
            access_token = r["auth"]["accessToken"]

            delete_profile(
                username=cls.non_existing_username,
                access_token=access_token,
                base=cls.base

            )

        except KeyError:
            pass

        print("setup done")

    @classmethod
    def tearDownClass(cls):
        pass

    def cleanup_delete_profile(self, username, access_token):
        r = delete_profile(
            username=username,
            access_token=access_token,
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        self.assertEqual(True, r["payload"]["status"])

    def test_create_profile(self):

        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password,
            base=self.base
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        self.cleanup_delete_profile(self.non_existing_username, access_token)

    def test_create_profile_that_already_exists(self):

        """setup"""
        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password
            , base=self.base
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        """confirmed: profile exists"""
        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password
            , base=self.base
        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(2, len(r["payload"]))
        self.assertEqual(False, r["auth"]["status"])
        self.assertEqual(False, r["payload"]["status"])
        self.assertEqual("username is taken", r["payload"]["description"])

        self.cleanup_delete_profile(self.non_existing_username, access_token)

    def test_login(self):
        """create"""
        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password
            , base=self.base
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        """logout"""
        r = logout(
            username=self.non_existing_username,
            access_token=access_token
            ,
            base=self.base
        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        self.assertEqual(True, r["payload"]["status"])

        """login"""
        r = login(
            username=self.non_existing_username,
            password=self.non_existing_password,
            base=self.base

        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        self.cleanup_delete_profile(self.non_existing_username, access_token)

    def test_login_non_existing_user(self):

        """login"""
        r = login(
            username=self.wrong_username,
            password=self.non_existing_password,
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(2, len(r["payload"]))
        self.assertEqual(False, r["auth"]["status"])
        self.assertEqual(False, r["payload"]["status"])
        self.assertEqual(
            "username password combination mismatch. Please check your credentials and try again",
            r["payload"]["description"]
        )

    def test_login_wrong_password(self):
        """create"""
        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password
            , base=self.base
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        """logout"""
        r = logout(
            username=self.non_existing_username,
            access_token=access_token,
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        self.assertEqual(True, r["payload"]["status"])

        """false login"""
        r = login(
            username=self.non_existing_username,
            password=self.wrong_password,
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(2, len(r["payload"]))
        self.assertEqual(False, r["auth"]["status"])
        self.assertEqual(False, r["payload"]["status"])
        self.assertEqual(
            "username password combination mismatch. Please check your credentials and try again",
            r["payload"]["description"]
        )

        """login"""
        r = login(
            username=self.non_existing_username,
            password=self.non_existing_password,
            base=self.base

        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        self.cleanup_delete_profile(self.non_existing_username, access_token)

    def test_login_wrong_username(self):
        """create"""
        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password
            , base=self.base
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        """logout"""
        r = logout(
            username=self.non_existing_username,
            access_token=access_token,
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        self.assertEqual(True, r["payload"]["status"])

        """false login"""
        r = login(
            username=self.wrong_username,
            password=self.non_existing_password,
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(2, len(r["payload"]))
        self.assertEqual(False, r["auth"]["status"])
        self.assertEqual(False, r["payload"]["status"])
        self.assertEqual(
            "username password combination mismatch. Please check your credentials and try again",
            r["payload"]["description"]
        )

        """login"""
        r = login(
            username=self.non_existing_username,
            password=self.non_existing_password,
            base=self.base

        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        self.cleanup_delete_profile(self.non_existing_username, access_token)

    def test_logout(self):
        """create"""
        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password
            , base=self.base
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        """logout"""
        r = logout(
            username=self.non_existing_username,
            access_token=access_token,
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        self.assertEqual(True, r["payload"]["status"])

        """
        login
        we need to obtain new access token
        """
        r = login(
            username=self.non_existing_username,
            password=self.non_existing_password,
            base=self.base

        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        self.cleanup_delete_profile(self.non_existing_username, access_token)

    def test_logout_wrong_access_token(self):
        """create"""
        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password
            , base=self.base
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])
        access_token = r["auth"]["accessToken"]

        """logout"""
        r = logout(
            username=self.wrong_username,
            access_token=access_token + " ",
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(False, r["auth"]["status"])
        self.assertEqual(False, r["payload"]["status"])

        """
        login
        we need to obtain new access token
        """
        r = login(
            username=self.non_existing_username,
            password=self.non_existing_password,
            base=self.base

        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        self.cleanup_delete_profile(self.non_existing_username, access_token)

    def test_logout_wrong_username(self):
        """create"""
        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password
            , base=self.base
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])
        access_token = r["auth"]["accessToken"]

        """logout"""
        r = logout(
            username=self.wrong_username,
            access_token=access_token,
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(False, r["auth"]["status"])
        self.assertEqual(False, r["payload"]["status"])

        """
        login
        we need to obtain new access token
        """
        r = login(
            username=self.non_existing_username,
            password=self.non_existing_password,
            base=self.base

        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        self.cleanup_delete_profile(self.non_existing_username, access_token)

    def test_delete(self):
        """create"""
        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password
            , base=self.base
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        self.cleanup_delete_profile(self.non_existing_username, access_token)

    def test_delete_wrong_username(self):
        """create"""
        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password
            , base=self.base
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        r = delete_profile(
            username=self.wrong_username,
            access_token=access_token,
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(False, r["auth"]["status"])
        self.assertEqual(False, r["payload"]["status"])

        self.cleanup_delete_profile(self.non_existing_username, access_token)

    def test_delete_wrong_access_token(self):
        """create"""
        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password
            , base=self.base
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        r = delete_profile(
            username=self.non_existing_username,
            access_token=access_token + " ",
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(False, r["auth"]["status"])
        self.assertEqual(False, r["payload"]["status"])

        self.cleanup_delete_profile(self.non_existing_username, access_token)

    def test_actions_after_profile_deletion(self):
        """create"""
        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password,
            base=self.base

        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        """delete"""
        self.cleanup_delete_profile(self.non_existing_username, access_token)

        """try delete again"""
        r = delete_profile(
            username=self.non_existing_username,
            access_token=access_token,
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(False, r["auth"]["status"])
        self.assertEqual(False, r["payload"]["status"])

        """try logout"""
        r = logout(
            username=self.non_existing_username,
            access_token=access_token
            ,
            base=self.base
        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(False, r["auth"]["status"])
        self.assertEqual(False, r["payload"]["status"])

        """try login"""
        r = login(
            username=self.non_existing_username,
            password=self.non_existing_password,
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(2, len(r["payload"]))
        self.assertEqual(False, r["auth"]["status"])
        self.assertEqual(False, r["payload"]["status"])
        self.assertEqual(
            "username password combination mismatch. Please check your credentials and try again",
            r["payload"]["description"]
        )

    def test_actions_after_logout(self):
        """create"""
        r = create_profile(
            username=self.non_existing_username,
            password=self.non_existing_password,
            base=self.base
        )
        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        """logout"""
        r = logout(
            username=self.non_existing_username,
            access_token=access_token
            ,
            base=self.base

        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        self.assertEqual(True, r["payload"]["status"])

        """try logout again -> must fail"""
        r = logout(
            username=self.non_existing_username,
            access_token=access_token
            ,
            base=self.base
        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(False, r["auth"]["status"])
        self.assertEqual(False, r["payload"]["status"])

        """try delete -> must fail"""
        r = delete_profile(
            username=self.non_existing_username,
            access_token=access_token,
            base=self.base
        )
        self.assertEqual(1, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(False, r["auth"]["status"])
        self.assertEqual(False, r["payload"]["status"])

        """login"""
        r = login(
            username=self.non_existing_username,
            password=self.non_existing_password,
            base=self.base
        )

        self.assertEqual(3, len(r["auth"]))
        self.assertEqual(1, len(r["payload"]))
        self.assertEqual(True, r["auth"]["status"])
        access_token = r["auth"]["accessToken"]
        self.assertEqual(self.non_existing_username, r["auth"]["username"])
        self.assertEqual(True, r["payload"]["status"])

        self.cleanup_delete_profile(self.non_existing_username, access_token)

    def test_change_username(self):
        raise NotImplementedError


if __name__ == "__main__":
    unittest.main()
