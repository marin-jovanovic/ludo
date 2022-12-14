from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.users import delete_profile
from backend.api.view.comm import get_auth_ok_response_template


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
        del response["auth"]["username"]
        del response["auth"]["accessToken"]
        response["payload"] = delete_profile(username, request.access_token)
        return JsonResponse(response)
