from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template


class SignUpView(APIView):

    def post(self, request, username):

        print("signup post", username)

        password = request.headers['password']
        print(f"{password=}")

        # todo add to db
        # todo hash

        # return tokens

        response = get_auth_ok_response_template(request)
        response["payload"]["status"] = True

        return JsonResponse(response)
