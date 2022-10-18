from backend.api.auth.main import generate_access_token
from backend.api.auth.main import get_hashed_password, is_pass_ok
from backend.api.cqrs_q.users import is_username_in_db, is_authenticated, \
    is_access_token_correct
from backend.api.model.users import Users


# todo change username
# todo access token

def logout(username, access_token):
    if not is_access_token_correct(username, access_token):
        return {'status': False, 'debug': 'user + access token combination err'}

    k, _ = Users.objects.update_or_create(
        username=username, defaults={"access_token": None}
    )
    k.save()

    return {'status': True, 'payload': {}}


def auth_user(username, password):
    if not is_authenticated(username, password):
        return {'status': False, 'debug': 'user + pass combination err'}

    access_token = generate_access_token()

    k, _ = Users.objects.update_or_create(
        username=username, defaults={"access_token": access_token}
    )
    k.save()

    return {'status': True, 'payload': {'access_token': access_token}}


def create_user(username, password):
    if is_username_in_db(username):
        return {'status': False, 'debug': 'user already in db'}

    k, _ = Users.objects.update_or_create(
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

    if not is_pass_ok(new_password_2):
        # todo
        return {'status': False, 'debug': 'pw not matching criteria complexiti'}

    if not new_password_1 == new_password_2:
        return {'status': False, 'debug': 'pw1 != pw2'}

    k, _ = Users.objects.update_or_create(
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

    Users.objects.filter(username=username, password=password).delete()

    return {'status': True}