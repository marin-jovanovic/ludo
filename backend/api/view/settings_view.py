import pathlib

from django.http import JsonResponse, FileResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template


# todo add all settings that are hardcoded (game settings, number of players, ...)

class SettingsView(APIView):
    """
    todo on settings view
    """

    def get(self, request, resource_id=None):
        """


        """
        response = get_auth_ok_response_template(request)







        response["payload"] = {
            "status": True,
            "username": request.username,
            # "song": 1,
            # "songPayload": song_data

        }

        # return FileResponse(song_path.open("rb"))

        return JsonResponse(response)



