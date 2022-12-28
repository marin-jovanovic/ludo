from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template
from backend.api.cqrs_c.users import delete_profile

class DeleteProfileView(APIView):
    """
    middleware handles business logic
    """

    def post(self, request, username):
        """
        return empty payload
        logic handled in middleware
        """

        response = get_auth_ok_response_template(request)
        response["payload"] = delete_profile(username, request.access_token)
        return JsonResponse(response)
