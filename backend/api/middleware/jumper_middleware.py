import urllib

from decouple import config
from django.http import JsonResponse

from backend.api.comm.comm import get_empty_response_template
from backend.api.cqrs_c.users import create_user, auth_user
from backend.api.cqrs_q.users import is_access_token_correct

import base64

class JumperMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        self.debug = config("DEBUG") != "0"

    def get_authorization_header(self, request):

        if 'HTTP_AUTHORIZATION' not in request.META:
            print("no authorization header")

            return None

        # try:
        authorization_header = request.META['HTTP_AUTHORIZATION']

        # except KeyError:
        #     print("no authorization header")
        #
        #     return None

        # print(f"{authorization_header=}")

        parsed_authorization_header = urllib.parse.unquote(
            authorization_header)

        # print(f"{parsed_authorization_header=}")
        sample_string_bytes = parsed_authorization_header.encode("ascii")
        # print(f"{sample_string_bytes=}")
        base64_bytes = base64.b64decode(sample_string_bytes)
        # print(f"{base64_bytes=}")
        base64_string = base64_bytes.decode("ascii")
        # print(f"{base64_string=}")
        return base64_string

    def __call__(self, request):
        print()

        authorization_header = self.get_authorization_header(request)

        if not authorization_header:
            rejection = get_empty_response_template()
            rejection["payload"] = {"status": False}
            rejection["debug"] = "no authorization header"
            return JsonResponse(rejection)

        # print(f"{request.headers=}")
        # try:
        #     print(f"{request.data=}")
        # except:
        #     pass
        # print(f"{request.body=}")

        auth_type, payload = authorization_header.split(" ")

        username = None
        access_token = None
        rejection = get_empty_response_template()



        if auth_type == "Digest":
            print("digest; not implemented")

            rejection["debug"] = "not implemented"
            return JsonResponse(rejection)

        elif auth_type == 'Create':
            username, password = payload.split(":")

            r = create_user(username, password)

            if not r["status"]:
                print('basic auth')
                print(f"{username=}")
                print(f"{password=}")

                rejection["payload"] = r
                return JsonResponse(rejection)

            r = auth_user(username, password)

            if not r["status"]:
                print("mw: can not create user")
                print("mw: auth err user")

                rejection["payload"] = r
                return JsonResponse(rejection)

            access_token = r["payload"]["access_token"]

        elif auth_type == 'Basic':

            # print(f"{base64_string=}")

            username, password = payload.split(":")

            r = auth_user(username, password)

            if not r["status"]:
                print('basic auth')
                print(f"{username=}")
                print(f"{password=}")
                print("mw: auth err user 2")

                rejection["payload"] = r
                return JsonResponse(rejection)

            access_token = r["payload"]["access_token"]

        elif auth_type == "Custom":
            username, access_token = payload.split(":")

            r = is_access_token_correct(username, access_token)

            if not r:
                print("custom auth")
                print(f"{username=}")
                print(f"{access_token[:5]=}")
                print("err is_access_token_correct")

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
