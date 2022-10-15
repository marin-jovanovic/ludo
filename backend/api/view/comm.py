from api.comm.constants import INTERNAL_SERVER_ERROR_MESSAGE


def get_auth_ok_response_template(request):
    for i in ["access_token", "refresh_token"]:
        if not hasattr(request, i):
            print(f"missing {i} in request")
            raise Exception(INTERNAL_SERVER_ERROR_MESSAGE)

    response = {
        "auth": {
            "status": True,
            "access-token": request.access_token,
            "refresh-token": request.refresh_token
        },
        "payload": {
            "status": False,

        }
    }
    return response


def get_auth_err_response_template(request):
    response = {
        "auth": {
            "status": False,
        }
    }
    return response


def check_request_contains(
        request, attribute, raise_exception=True, default_attribute=None):
    # todo check if request.attribute == None, think its checked in line 32

    # if raise_exception

    if not hasattr(request, attribute):
        print(f"missing {attribute} in request")

    if raise_exception:
        if not hasattr(request, attribute):
            raise Exception(INTERNAL_SERVER_ERROR_MESSAGE)

    if hasattr(request, attribute):
        if getattr(request, attribute):
            return getattr(request, attribute)

    if raise_exception:
        raise Exception(INTERNAL_SERVER_ERROR_MESSAGE)

    return default_attribute
