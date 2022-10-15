"""
implementation without refresh tokens
only access token with unlimited lifetime

password is stored as hash

todo which one?

"""

from secrets import token_hex




def obtain_tokens(username, password):
    print(f"{username=}")
    print(f"{password=}")

    return {
        'is_valid': False,
        "accessToken":  token_hex(256),

    }

def logout():
    pass
    # remove from db

    # return status

def _is_valid_access_token(username, access_token):
    pass

def _is_valid_password(username, password):
    pass

def is_valid(
        username,
        choice_access_token_or_password,
        flag_access_token_or_password):

    if flag_access_token_or_password:
        return _is_valid_access_token(username, choice_access_token_or_password)

    else:
        return _is_valid_password(username, choice_access_token_or_password)