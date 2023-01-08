import pathlib

from django.http import JsonResponse, FileResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template


# todo add all settings that are hardcoded (game settings, number of players, ...)

class MusicView(APIView):
    """
    todo on settings view
    """

    def get(self, request, resource_id=None):
        """


        """
        response = get_auth_ok_response_template(request)


        base_dir = pathlib.Path(__file__).parent.parent.parent.parent.resolve()

        song_path = base_dir / "resources" / "mp3" / "Corruption.mp3"

        with open(song_path, 'rb') as f:
            song_data = f.read()



        # response["payload"] = {
        #     "status": True,
        #     "username": request.username,
        #     # "song": 1,
        #     # "songPayload": song_data
        #
        # }

        return FileResponse(song_path.open("rb"))

        # return JsonResponse(response)



