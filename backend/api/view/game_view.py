import urllib

from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.game import get_specific_game, receive_instruction
from backend.api.cqrs_c.game_log import add_entry
from backend.api.game.order import determine_order
from backend.api.game.resources import get_config
from backend.api.model.c_q import get_player_order
from backend.api.view.comm import get_auth_ok_response_template


class GameView(APIView):

    def get(self, request, name):

        response = get_auth_ok_response_template(request)
        response['payload'] = get_specific_game(name)

        return JsonResponse(response)

    def put(self, request, name):
        """used for sending info

        set performed in game log when user rolls dice
        so other players can update board

        when user makes choice which token to move
        """

        # todo check if authorized

        print("put game, only for setting received flag")
        response = get_auth_ok_response_template(request)

        unquoted_body = urllib.parse.unquote(request.body)
        body = urllib.parse.parse_qs(unquoted_body)

        print(f"{request.body=}")
        print(f"{request.data=}")

        try:
            instruction_id = body["instructionId"][0]
            # action = body["action"][0]
        except KeyError:
            instruction_id = request.data["instructionId"]
            # action = request.data["action"]

        print(f"{instruction_id=}")

        response['payload'] = receive_instruction(name, instruction_id)

        return JsonResponse(response)

    def post(self, request, name):
        # todo when is this used?

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
