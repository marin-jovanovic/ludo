import base64


def encode_username_password(type_, username, password):
    unencoded = f"{type_} {username}:{password}"
    as_bytes = unencoded.encode("ascii")
    base64_bytes = base64.b64encode(as_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


def encode_username_access_token(type_, username, access_token):
    unencoded = f"{type_} {username}:{access_token}"
    as_bytes = unencoded.encode("ascii")
    base64_bytes = base64.b64encode(as_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string
