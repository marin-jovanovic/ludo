import json
import time

import requests
import random
import string
import urllib.parse
import base64
import pytest
import unittest


class TestMain(unittest.TestCase):

    def setup(self):
        self.base = "http://localhost:8000"
        self.username = "ffff"
        self.password = "@,<>12#*mdAmf-"

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

    def test_create_profile(self):
        self.setup()

        r = self.create_profile(username=self.username, password=self.password)

        if r["payload"]["status"]:
            self.assertEqual(True, True)

        if r["payload"]["message"] == "username is taken":
            self.assertEqual(True, True)
            return

        self.assertEqual(True, r["payload"]["status"])

    def test_login(self):
        self.setup()

        r = self.create_profile(username=self.username, password=self.password)

        r = self.login(username=self.username, password=self.password)

        self.assertEqual(True, r["payload"]["status"])

    def test_logout(self):
        self.setup()

        r = self.login(username=self.username, password=self.password)

        self.assertEqual(True, r["auth"]["status"])

        access_token = r["auth"]["accessToken"]

        r = self.logout(username=self.username, access_token=access_token)
        self.assertEqual(True, r["payload"]["status"])

    def test_delete(self):
        self.setup()

        r = self.login(username=self.username, password=self.password)

        self.assertEqual(True, r["auth"]["status"])

        access_token = r["auth"]["accessToken"]

        r = self.delete_profile(username=self.username, access_token=access_token)
        self.assertEqual(True, r["payload"]["status"])


if __name__ == "__main__":
    unittest.main()