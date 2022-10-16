from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template
# from backend.api.auth.main import create_user
from backend.api.cqrs_c.users import create_user, auth_user


class LoginView(APIView):

    def post(self, request, username):
        # return access token for provided username and password

        password = request.headers['password']

        response = get_auth_ok_response_template(request)
        response["payload"] = auth_user(username, password)

        return JsonResponse(response)
