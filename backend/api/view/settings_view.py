from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template

# todo add all settings that are hardcoded (game settings, number of players, ...)

class SettingsView(APIView):
    """

    """

    def get(self, request):

        response = get_auth_ok_response_template(request)

        response["payload"] = {
            "status": True,
            "username": request.username
        }

        return JsonResponse(response)
