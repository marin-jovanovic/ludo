from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.users import logout
from backend.api.view.comm import get_auth_ok_response_template


class LogoutView(APIView):

    def post(self, request, username):
        # todo delete access token

        print(f"{username=}")
        print(f"{request.headers=}")

        access_token = request.access_token

        response = get_auth_ok_response_template(request)
        response["payload"] = logout(username, access_token)

        return JsonResponse(response)
