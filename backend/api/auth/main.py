"""
implementation without refresh tokens

access token has unlimited lifetime

password is stored as hash
"""

import base64
import hashlib
from secrets import token_hex

from bcrypt import gensalt, hashpw


def generate_access_token():
    return token_hex(256)


def get_hashed_password(password: str) -> (str, str):
    """
    returns all decoded to utf-8

    from https://pypi.org/project/bcrypt/

    The bcrypt algorithm only handles passwords up to 72 characters, any
    characters beyond that are ignored. To work around this, a common approach
    is to hash a password with a cryptographic hash (such as sha256) and then
    base64 encode it to prevent NULL byte problems before hashing the result
    with bcrypt:
    """

    pass_long = password.encode() * 10

    salt = gensalt()

    hashed = hashpw(base64.b64encode(hashlib.sha256(pass_long).digest()),
                    salt).decode("utf-8")

    return hashed


def is_pass_ok(password: str):
    """

        checks if {password} is strong enough
        new parameters can be easily added by appending to the current list of
        parameters

        Parameters:
        password (str): password which needs to be checked

        Returns:
        dict: A dictionary with keys "status", "reasons", and "message". The
              "status" key has a value of True if the password is strong enough and
              False if it is not. The "reasons" key has a value of a list of
              strings, each representing a reason why the password is not strong
              enough. The "message" key has a value of a string, which is a
              comma-separated list of the items in the "reasons" list.

        """

    reasons = []
    flag = True

    if len(password) < 8:
        reasons.append("password must be at least 8 characters long")
        flag = False
    if not any(char.isdigit() for char in password):
        reasons.append("password must contain a number")
        flag = False
    if not any(char.isupper() for char in password):
        reasons.append("password must contain an uppercase letter")
        flag = False
    if not any(char.islower() for char in password):
        reasons.append("password must contain a lowercase letter")
        flag = False
    if not any(char in "? !%&@$+-._,\"\'" for char in password):
        reasons.append("password must contain a special character")
        flag = False

    return {"status": flag, "reasons": reasons, "message": ", ".join(reasons)}

    # flag = True
    # reasons = []
    #
    # # length
    # l = 8
    # if len(password) < l:
    #     t = f"password must be at least {l} characters long"
    #     reasons.append(t)
    #     flag = False
    #
    # # special chars
    # test_list = ["?", "!", "%", "&", "@", "$",
    #              "+", "-", ".", "_", ",", "\"", "\'"]
    # if not any(item in list(password) for item in test_list):
    #     t = "password must contain special character"
    #     print(t)
    #     reasons.append(t)
    #     flag = False
    #
    # # digit
    # if not any(char.isdigit() for char in password):
    #     t = "password must contain number"
    #     print(t)
    #     reasons.append(t)
    #     flag = False
    #
    # # upper case
    # if not any(char.isupper() for char in password):
    #     t = "password must contain uppercase letter"
    #     print(t)
    #     reasons.append(t)
    #     flag = False
    #
    # # lower case
    # if not any(char.islower() for char in password):
    #     t = "password must contain lowercase letter"
    #     print(t)
    #     reasons.append(t)
    #     flag = False
    #
    # return {"status": flag, "reasons": reasons, "message": ", ".join(reasons)}


def t_is_pass_ok():
    # Test password that is too short
    result = is_pass_ok("abc123!")
    assert result["status"] == False
    assert "password must be at least 8 characters long" in result["reasons"]
    # assert result["message"] == "password must be at least 8 characters long"

    # Test password that doesn't contain a number
    result = is_pass_ok("abcdefghijklm")
    assert result["status"] == False
    assert "password must contain a number" in result["reasons"]
    # assert result["message"] == "password must contain a number"

    # Test password that doesn't contain an uppercase letter
    result = is_pass_ok("abcdefgh1ijklm")
    assert result["status"] == False
    assert "password must contain an uppercase letter" in result["reasons"]
    # assert result["message"] == "password must contain an uppercase letter"

    # Test password that doesn't contain a lowercase letter
    result = is_pass_ok("ABCDEFGH1IJKLM")
    assert result["status"] == False
    assert "password must contain a lowercase letter" in result["reasons"]
    # assert result["message"] == "password must contain a lowercase letter"

    # Test password that doesn't contain a special character
    result = is_pass_ok("AbCdEfGh1IjKlM")
    assert result["status"] == False
    assert "password must contain a special character" in result["reasons"]
    # assert result["message"] == "password must contain a special character"

    # Test valid password
    result = is_pass_ok("AbCdEfG1hIjKlM!")
    assert result["status"] == True
    assert len(result["reasons"]) == 0
    assert result["message"] == ""

    print("all ok")


if __name__ == '__main__':
    t_is_pass_ok()
