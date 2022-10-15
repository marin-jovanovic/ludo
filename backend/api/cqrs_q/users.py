from backend.api.model.users import Users
import argparse
import base64
import getpass
import hashlib
import json
import sys
import argparse
import base64
import getpass
import hashlib
import json
import sys
import time
from os import path

import bcrypt
from bcrypt import hashpw, gensalt
from bcrypt import hashpw, gensalt

import bcrypt
from bcrypt import hashpw, gensalt


def is_username_in_db(username):
    return Users.objects.filter(username=username).exists()


def is_authenticated(username, password):

    if not is_username_in_db(username):
        return False

    pass_long = password.encode() * 10
    pass_transformed = base64.b64encode(
        hashlib.sha256(pass_long).digest())

    pwd_from_db = Users.objects.filter(username=username).encode('utf-8')

    return bcrypt.checkpw(pass_transformed, pwd_from_db)
    #
    #
    # return Users.objects.filter(username=username, password=password).exists()
    #
    #
    #
    # return