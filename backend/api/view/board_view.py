from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_q.level_config import get_config
from backend.api.cqrs_q.player_order import get_players
from backend.api.game.resources import get_moves, \
    getMap, get_start_pool
from backend.api.view.comm import get_auth_ok_response_template


class BoardView(APIView):

    def get(self, request, level_id):
        response = get_auth_ok_response_template(request)

        response['payload'] = {
            "status": True,
            "players": get_players(level_id=level_id),
            "config": get_config(level_id=level_id),
            'startPool': get_start_pool(),
            'moves': get_moves(),
            'map': getMap(),
        }

        return JsonResponse(response)
