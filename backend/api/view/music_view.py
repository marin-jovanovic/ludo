import pathlib

from django.http import FileResponse
from rest_framework.views import APIView


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
