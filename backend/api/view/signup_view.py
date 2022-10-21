from django.http import JsonResponse
from rest_framework.views import APIView

# from backend.api.auth.main import create_user
from backend.api.cqrs_c.users import create_user
from backend.api.view.comm import get_auth_ok_response_template


class SignUpView(APIView):

    def post(self, request, username):
        # input: username, password
        # output: create user in db

        # password = request.headers['password']
        # password = request.password

        response = get_auth_ok_response_template(request)
        response["payload"]["status"] = True
        response["payload"]["payload"] = {
            'username': request.username,
            'settings1': 'r 1',
            'settings2': 'r 2',
        }
        # response["payload"]["payload"] = 'if you can pass middleware you are authenticated'

        # response["payload"]["status"] = create_user(username, password)

        return JsonResponse(response)
