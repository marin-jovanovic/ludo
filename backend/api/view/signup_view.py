from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template


class SignUpView(APIView):
    """
    middleware handles business logic
    """

    def post(self, request, username):
        response = get_auth_ok_response_template(request)
        return JsonResponse(response)
