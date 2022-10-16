from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template
# from backend.api.auth.main import create_user
from backend.api.cqrs_c.users import create_user
class SignUpView(APIView):

    def post(self, request, username):

        # print("signup post", username)

        password = request.headers['password']
        # print(f"{password=}")

        # todo add to db
        # todo hash

        # return tokens

        response = get_auth_ok_response_template(request)
        response["payload"]["status"] = create_user(username, password)

        return JsonResponse(response)
