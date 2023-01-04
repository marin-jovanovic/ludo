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

    :param password: password which needs to be checked
    :return: is_password_strong_enough: bool
    """

    flag = True
    reasons = []

    # length
    l = 8
    if len(password) < l:
        t = f"password must be at least {l} characters long"
        reasons.append(t)
        flag = False

    # special chars
    test_list = ["?", "!", "%", "&", "@", "$",
                 "+", "-", ".", "_", ",", "\"", "\'"]
    if not any(item in list(password) for item in test_list):
        t = "password must contain special character"
        print(t)
        reasons.append(t)
        flag = False

    # digit
    if not any(char.isdigit() for char in password):
        t = "password must contain number"
        print(t)
        reasons.append(t)
        flag = False

    # upper case
    if not any(char.isupper() for char in password):
        t = "password must contain uppercase letter"
        print(t)
        reasons.append(t)
        flag = False

    # lower case
    if not any(char.islower() for char in password):
        t = "password must contain lowercase letter"
        print(t)
        reasons.append(t)
        flag = False

    return {"status": flag, "reasons": reasons, "message": ", ".join(reasons)}
