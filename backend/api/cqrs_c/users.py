from backend.api.model.users import Users
from backend.api.auth.user_menagment import get_hashed_password, is_pass_ok
from backend.api.cqrs_q.users import is_username_in_db, is_authenticated

# todo change username
# todo access token


def create_user(username, password):

    # if isinstance(key, bytes):
    #     encoding = 'utf-8'
    #     key = key.decode(encoding)

    if is_username_in_db(username):
        return {'status': False, 'debug': 'user already in db'}

    k, _ = Users.objects.update_or_create(
        username=username, defaults={"password_hash": get_hashed_password(password)}
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
        username=username, defaults={"password_hash": get_hashed_password(new_password_1)}
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
