import base64
import hashlib

import bcrypt

from backend.api.model.user import get_user_model

def username_to_id(username):
    return get_user_model().objects.get(username=username).id


def get_user_object(username):
    return get_user_model().objects.get(username=username)


def is_username_in_db(username):
    return get_user_model().objects.filter(username=username).exists()


def get_access_token(username):
    return get_user_model().objects.get(username=username).access_token


def is_access_token_correct(username, access_token):
    if not is_username_in_db(username):
        return {"status": False}

    r = get_access_token(username) == access_token

    return {'status': r}


def is_authenticated(username, password):
    if not is_username_in_db(username):
        return False

    pass_long = password.encode() * 10
    pass_transformed = base64.b64encode(
        hashlib.sha256(pass_long).digest())

    pwd_from_db = get_user_model().objects.get(
        username=username).password_hash.encode(
        'utf-8')
    return bcrypt.checkpw(pass_transformed, pwd_from_db)


def get_logged_users():
    return list(
        get_user_model().objects.filter(access_token__isnull=False).values(
            "username"))


def get_users_in_level(level_id):
    return {
        "status": True,
        "payload": list(get_user_model().objects.filter(
            currently_playing__id=level_id,
            currently_playing__is_active=True
        ))
    }


def get_user(username):
    try:
        return {
            "status": True,
            "payload": get_user_object(username)
        }
    except get_user_model().DoesNotExist as e:
        print("get user err")
        return {
            "status": False,
            "debug": "user with this username does not exist"
        }
