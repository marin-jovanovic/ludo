import urllib

from decouple import config
from django.http import JsonResponse

from backend.api.comm.comm import get_empty_response_template
from backend.api.cqrs_c.users import create_user, auth_user
from backend.api.cqrs_q.users import is_access_token_correct


class JumperMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        self.debug = config("DEBUG") != "0"

    def __call__(self, request):
        print()

        # print(f"{request.META=}")

        try:
            authorization_header = request.META['HTTP_AUTHORIZATION']
        except KeyError:
            rejection = get_empty_response_template()
            rejection["payload"] = {"status": False}
            rejection["debug"] = "no authorization header"
            return JsonResponse(rejection)

        parsed_authorization_header = urllib.parse.unquote(authorization_header)
        auth_type, payload = parsed_authorization_header.split(" ")

        username = None
        access_token = None

        if auth_type == "Digest":
            rejection = get_empty_response_template()
            rejection["debug"] = "not implemented"
            return JsonResponse(rejection)

        elif auth_type == 'Create':
            print('basic auth')
            username, password = payload.split(":")
            print(f"{username=}")
            print(f"{password=}")

            r = create_user(username, password)

            if not r["status"]:
                rejection = get_empty_response_template()
                rejection["payload"] = r
                return JsonResponse(rejection)

            r = auth_user(username, password)

            if not r["status"]:
                rejection = get_empty_response_template()
                rejection["payload"] = r
                return JsonResponse(rejection)

            access_token = r["payload"]["access_token"]

        elif auth_type == 'Basic':
            print('basic auth')
            username, password = payload.split(":")
            print(f"{username=}")
            print(f"{password=}")

            # r = create_user(username, password)
            r = auth_user(username, password)

            if not r["status"]:
                rejection = get_empty_response_template()
                rejection["payload"] = r
                return JsonResponse(rejection)

            access_token = r["payload"]["access_token"]

        elif auth_type == "Custom":
            username, access_token = payload.split(":")
            print(f"{username=}")
            print(f"{access_token[:5]=}")

            r = is_access_token_correct(username, access_token)

            if not r:
                rejection = get_empty_response_template()
                rejection["debug"] = "not is_validated"
                return JsonResponse(rejection)

        request.username = username
        request.access_token = access_token

        # fixme only for testing
        #
        # request.ip = "127.0.0.1"
        # request.synchronizer_token_match = True
        # request.role = "role 1"

        return self.get_response(request)
