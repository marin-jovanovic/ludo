import base64
import hashlib

import bcrypt

from backend.api.model.users import get_user_model


def is_username_in_db(username):
    return get_user_model().objects.filter(username=username).exists()


def is_access_token_correct(username, access_token):
    if not is_username_in_db(username):
        return False

    r = get_user_model().objects.get(username=username).access_token == access_token

    return {'status': True, 'payload': r}


def is_authenticated(username, password):
    if not is_username_in_db(username):
        return False

    pass_long = password.encode() * 10
    pass_transformed = base64.b64encode(
        hashlib.sha256(pass_long).digest())

    pwd_from_db = get_user_model().objects.get(username=username).password_hash.encode(
        'utf-8')
    return bcrypt.checkpw(pass_transformed, pwd_from_db)


def get_logged_users():

    # logged_users = Users.objects.filter(access_token__isnull=False)
    # for i in logged_users:
    #     print(i.username)

    return list(
        get_user_model().objects.filter(access_token__isnull=False).values("username"))

    # return [i.username for i in logged_users]


def get_user(username):
    try:
        return {
            "status": True,
            "payload": get_user_model().objects.get(username=username)
        }
    except get_user_model().DoesNotExist as e:
        return {
            "status": False
        }