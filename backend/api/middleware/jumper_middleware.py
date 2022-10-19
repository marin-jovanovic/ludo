from decouple import config
import urllib

from django.http import JsonResponse

from backend.api.comm.comm import get_empty_response_template
from backend.api.cqrs_q.users import is_access_token_correct


class JumperMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        self.debug = config("DEBUG") != "0"

    def __call__(self, request):
        print()

        authorization_header = request.META['HTTP_AUTHORIZATION']
        parsed_authorization_header = urllib.parse.unquote(authorization_header)
        auth_type, payload = parsed_authorization_header.split(" ")

        username = None
        access_token = None

        if auth_type == "Digest":
            rejection = get_empty_response_template()
            rejection["debug"] = "not implemented"
            return JsonResponse(rejection)

        elif auth_type== "Custom":
            username, access_token = payload.split(":")
            print(f"{username=}")
            print(f"{access_token=}")

            r = is_access_token_correct(username, access_token)

            if not r:

                rejection = get_empty_response_template()
                rejection["debug"] = "not is_validated"
                return JsonResponse(rejection)

        request.username = username
        request.refresh_token = None

        # fixme only for testing
        request.access_token = "tmp"

        request.ip = "127.0.0.1"
        request.synchronizer_token_match = True
        request.role = "role 1"

        return self.get_response(request)
