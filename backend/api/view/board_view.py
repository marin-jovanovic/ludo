from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.game.resources import get_moves, \
    getMap, get_start_pool
from backend.api.cqrs_q.player_order import get_players
from backend.api.cqrs_q.level_config import get_config
from backend.api.view.comm import get_auth_ok_response_template


class BoardView(APIView):

    def get(self, request, level_id, resource):
        print("get board,", level_id, resource)
        response = get_auth_ok_response_template(request)

        if resource == "players":

            # response["payload"] = {


            response['payload'] = {
                "status": True,
                "payload": get_players(level_id=level_id)
            }

            # print(f"{response=}")

            return JsonResponse(response)




        configuration = {
            'startPool': get_start_pool,
            'moves': get_moves,
            'config': get_config,
            'map': getMap,
            # todo fetch from FE
            # 'players': get_players
        }

        response['payload'] = {
            "status": True,
            "payload": configuration[resource]()
        }

        return JsonResponse(response)
