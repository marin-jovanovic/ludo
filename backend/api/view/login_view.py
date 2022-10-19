from django.http import JsonResponse
from rest_framework.views import APIView

# from backend.api.auth.main import create_user
from backend.api.cqrs_c.users import auth_user
from backend.api.view.comm import get_auth_ok_response_template


class LoginView(APIView):

    def post(self, request, username):
        # return access token for provided username and password
        print(f"post {username=}")

        password = request.headers["Authorization"].split(" ")[1].split(":")[0]
        print(f"{password=}")

        response = get_auth_ok_response_template(request)
        response["payload"] = auth_user(username, password)

        return JsonResponse(response)
