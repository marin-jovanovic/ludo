from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template


class LoginView(APIView):

    def post(self, request, username):
        """
        return access token for provided username and password
        """

        # todo perform check if username is same as one in middleware used

        response = get_auth_ok_response_template(request)
        response["payload"]["status"] = True
        return JsonResponse(response)
