import base64
import urllib

from decouple import config
from django.http import JsonResponse

from backend.api.comm.comm import get_empty_response_template
from backend.api.cqrs_c.users import create_user, auth_user
from backend.api.cqrs_q.user import is_access_token_correct


class JumperMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        self.debug = config("DEBUG") != "0"

    def get_authorization_header(self, request):

        if 'HTTP_AUTHORIZATION' not in request.META:
            print("no authorization header")

            return None

        authorization_header = request.META['HTTP_AUTHORIZATION']

        parsed_authorization_header = urllib.parse.unquote(
            authorization_header
        )

        sample_string_bytes = parsed_authorization_header.encode("ascii")
        base64_bytes = base64.b64decode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return base64_string

    def __call__(self, request):
        print()
        rejection = get_empty_response_template()

        authorization_header = self.get_authorization_header(request)

        if not authorization_header:
            rejection["debug"] = "no authorization header"
            print("ret aut header")
            return JsonResponse(rejection)

        # print(f"{request.headers=}")
        # try:
        #     print(f"{request.data=}")
        # except:
        #     pass
        # print(f"{request.body=}")

        auth_type, payload = authorization_header.split(" ", 1)

        username = None
        access_token = None

        if auth_type == "Digest":
            print("digest; not implemented")

            rejection["debug"] = "not implemented"
            print("ret digest")
            return JsonResponse(rejection)

        elif auth_type == 'Create':
            username, password = payload.split(":")

            r = create_user(username, password)

            if not r["status"]:
                rejection["payload"] = r
                print("ret create user")
                return JsonResponse(rejection)

            r = auth_user(username, password)

            if not r["status"]:
                rejection["payload"] = r
                print("ret auth user")
                return JsonResponse(rejection)

            access_token = r["payload"]["access_token"]

        elif auth_type == 'Basic':

            username, password = payload.split(":")
            print(f"{username=} {password=}")
            r = auth_user(username, password)

            if not r["status"]:
                rejection["payload"] = r
                print("ret auth user")
                return JsonResponse(rejection)

            access_token = r["payload"]["access_token"]

        elif auth_type == "Custom":
            username, access_token = payload.split(":")

            r = is_access_token_correct(username, access_token)

            if not r["status"]:
                rejection["payload"] = r
                print("ret access token")
                return JsonResponse(rejection)

        request.username = username
        request.access_token = access_token

        from backend.api.cqrs_q.user import username_to_id
        request.user_id = username_to_id(request.username)

        # fixme only for testing
        #
        # request.ip = "todo"
        # request.synchronizer_token_match = True
        # request.role = "role 1"

        print("mw passed")
        return self.get_response(request)
