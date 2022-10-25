import json
import urllib

from django.http import JsonResponse
from rest_framework.views import APIView

# from backend.api.auth.main import create_user
from backend.api.cqrs_c.users import auth_user
from backend.api.cqrs_c.game import create_game, leave_game, join_game, \
    get_games, get_specific_game
from backend.api.model.player_order import get_player_order
from backend.api.view.comm import get_auth_ok_response_template
from backend.api.cqrs_c.game_log import add_entry
from backend.api.game.game import determine_order, get_config

class GameView(APIView):

    def get(self, request, name):

        print("get games")
        response = get_auth_ok_response_template(request)
        response['payload'] = get_specific_game(name)

        return JsonResponse(response)

    def post(self, request, name):
        response = get_auth_ok_response_template(request)

        creator_username = request.username

        unquoted_body = urllib.parse.unquote(request.body)
        body = urllib.parse.parse_qs(unquoted_body)

        print(f"{request.body=}")
        print(f"{request.data=}")

        try:
            token = body["token"][0]
            action = body["action"][0]
        except KeyError:
            token = request.data["token"]
            action = request.data["action"]

        if action == "start":
            def driver():

                # todo
                print("determine users")

                # todo this is joining order, not playing order, change this
                order = get_player_order(name)
                print(f"{order=}")
                if not order["status"]:
                    print("get game err")
                    return order
                else:
                    o_o = order["payload"]

                print(80 * "-")
                print(o_o)

                from rest_framework.renderers import JSONRenderer

                json = JSONRenderer().render(o_o)
                print(f"{json=}")
                for i in o_o:
                    print(i, i.index)

                m_join_order_to_username = {i.index: i.player_id.username for i in o_o}
                print(f"{m_join_order_to_username=}")

                game_conf = get_config()

                order = determine_order(
                    game_conf['number of players'],
                    game_conf['choice: highest; order'],
                    game_conf['choice: clockwise; anticlockwise'],
                    game_conf['flag: tie in order'],
                )
                for i in order:
                    print(f"befor {i=}")
                    i["game"] = name
                    i["player"] = m_join_order_to_username[i["player"]]
                    print(f"after {i=}")

                    r = add_entry(**i)
                    if not r["status"]:
                        return r

            r = driver()
            response["payload"] = r
            return JsonResponse(response)


        dice_result = None

        response["payload"] = add_entry(name, creator_username, token, dice_result, action)

        return JsonResponse(response)

