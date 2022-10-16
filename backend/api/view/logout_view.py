from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template
from backend.api.cqrs_c.users import logout

class LogoutView(APIView):

    def post(self, request, username):
        # delete access token

        access_token = request.headers['accessToken']

        response = get_auth_ok_response_template(request)
        response["payload"] = logout(username, access_token)

        return JsonResponse(response)
