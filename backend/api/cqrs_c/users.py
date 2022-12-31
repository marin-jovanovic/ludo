import json

from backend.api.auth.main import generate_access_token
from backend.api.auth.main import get_hashed_password, is_pass_ok
from backend.api.comm.comm import Notifier
from backend.api.cqrs_q.users import get_logged_users
from backend.api.cqrs_q.users import is_username_in_db, is_authenticated, \
    is_access_token_correct, get_user
from backend.api.model.player import get_user_model

# todo change username
# todo access token

active_users_notifier = Notifier()

def delete_profile(username, access_token):
    if not is_access_token_correct(username, access_token)["status"]:
        return {
            'status': False,
            "description": 'username access token combination mismatch. Please check your credentials and try again'
        }

    t = get_user_model().objects.get(username=username, access_token= access_token).delete()

    return {'status': True}


def logout(username, access_token):
    """
    we trust access token because it is checked in mw
    """

    print("acces token", is_access_token_correct(username, access_token))

    if not is_access_token_correct(username, access_token)["status"]:
        return {
            'status': False,
            # "description": 'username access token combination mismatch. Please check your credentials and try again'
        }

    k, _ = get_user_model().objects.update_or_create(
        username=username, defaults={"access_token": None}
    )

    print(f"{k=} {_=}")
    r = k.save()
    print(f"{r=}")
    # k.save()

    return {'status': True}


def auth_user(username, password):
    """
    authenticate existing user

    generate access token for this user
    write access token to db

    """

    if not is_authenticated(username, password):
        return {
            'status': False,
            "description": 'username password combination mismatch. Please check your credentials and try again'
        }

    access_token = generate_access_token()

    k, _ = get_user_model().objects.update_or_create(
        username=username, defaults={"access_token": access_token}
    )
    k.save()

    logged_users = get_logged_users()

    msg = json.dumps({
        "message": "getUserActive",
        "args": {i["username"]: {"isActive": True} for i in logged_users}
    })

    active_users_notifier.notify(msg)

    return {'status': True, 'payload': {'access_token': access_token}}


def create_user(username, password):
    if is_username_in_db(username):
        return {'status': False, "description": 'username is taken'}

    rej = is_pass_ok(password)

    if not rej["status"]:

        return  rej
        # return {'status': False, 'debug': 'pw not matching criteria complexiti'}


    k, _ = get_user_model().objects.update_or_create(
        username=username,
        defaults={"password_hash": get_hashed_password(password)}
    )
    k.save()

    return {'status': True}


def change_password(username, old_password, new_password_1, new_password_2):
    if not is_username_in_db(username):
        return {'status': False, 'debug': 'user not already in db'}

    if not is_authenticated(username, old_password):
        return {'status': False, 'debug': 'username + pass combo err'}

    if not is_pass_ok(new_password_2)["status"]:
        return  is_pass_ok(new_password_2)

    if not new_password_1 == new_password_2:
        return {'status': False, 'debug': 'pw1 != pw2'}

    k, _ = get_user_model().objects.update_or_create(
        username=username,
        defaults={"password_hash": get_hashed_password(new_password_1)}
    )
    k.save()
    return {'status': True}


def delete_user(username, password):
    if not is_username_in_db(username):
        return {'status': False, 'debug': 'user not in db'}

    if not is_authenticated(username, password):
        return {'status': False, 'debug': 'username + pass combo err'}

    get_user_model().objects.get(username=username, password=password).delete()

    return {'status': True}


def __make_user_join(username):
    r = get_user(username)
    if r["status"]:
        creator_o = r["payload"]
    else:
        return r

    is_playing_game = __is_playing_game(player_o=creator_o)

    if is_playing_game["payload"]:
        return {"status": False, "payload": "user role not empty (playing another game)"}

    _assign_role_to_user(creator_o, "joined")

    return {"status": True}


def __is_playing_game(player_o):
    return {"status": True, "payload": bool(player_o.game_role)}


def make_user_available_to_play(username):
    r = get_user(username)
    if r["status"]:
        creator_o = r["payload"]
    else:
        return r

    _assign_role_to_user(creator_o, None)

    return {"status": True}


def make_user_game_creator(username):
    """
    user_o.game_role = role
    user_o.save()
    """

    # fixme what if he is currently in another game?

    r = get_user(username)
    if r["status"]:
        creator_o = r["payload"]
    else:
        return r

    is_playing_game = __is_playing_game(player_o=creator_o)

    if is_playing_game["payload"]:
        return {"status": False, "payload": "user role not empty"}

    _assign_role_to_user(creator_o, "creator")

    return {"status": True}


def _assign_role_to_user(user_o, role):
    user_o.game_role = role
    user_o.save()

    return {"statue": True}
