from django.http import JsonResponse
from rest_framework.views import APIView
from backend.api.view.comm import get_auth_ok_response_template


class LoginView(APIView):

    def post(self, request, username):
        # return access token for provided username and password

        response = get_auth_ok_response_template(request)
        return JsonResponse(response)
