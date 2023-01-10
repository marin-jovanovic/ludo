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

        base_dir = pathlib.Path(__file__).parent.parent.parent.parent.resolve()

        song_path = base_dir / "resources" / "mp3" / "Corruption.mp3"

        return FileResponse(song_path.open("rb"))




