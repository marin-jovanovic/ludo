from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_q.users import is_access_token_correct
from backend.api.view.comm import get_auth_ok_response_template


class ValidationView(APIView):

    def post(self, request, username):

        print(request.headers)
        # access_token = request.headers['accessToken']

        response = get_auth_ok_response_template(request)
        # response["payload"] = is_access_token_correct(username, access_token)

        return JsonResponse(response)
