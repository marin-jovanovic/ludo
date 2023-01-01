import urllib

from django.http import JsonResponse, HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from backend.api.cqrs_c.level import create_game, leave_level, join_game, \
    get_active_levels, in_which_level_is_user
from backend.api.cqrs_q.users import get_user
from backend.api.game.game import add_entry_to_log
from backend.api.model.game_log import game_log_model
from backend.api.model.level import _get_level_model
from backend.api.model.player_order import get_player_order_model
from backend.api.view.comm import get_auth_ok_response_template


def get_log(level_id):
    log = game_log_model().objects.filter(game_id=level_id, game_id__is_active=True).order_by("instruction_id").values()
    # log = game_log_model().objects.filter(game_id__name=level_id, game_id__is_active=True).order_by("instruction_id").values()
    log = list(log)

    return {
        "status": True,
        "payload": log
    }

class LevelLogView(APIView):
    # todo observers

    def get(self, request, level_id):

        response = get_auth_ok_response_template(request)

        r = get_log(level_id)
        if not r["status"]:
            return r

        log = r["payload"]

        ret_log = {}

        for entry in log:
            # todo del instruction_id from value, and all other non used entries
            ret_log[entry["instruction_id"]] = entry



        # to_choose = {**level.start_pool_options, **level.non_start_pool_options}

        response["payload"] = {
            "status": True,
            "log": ret_log,
            # "turn": ,

        }

        return JsonResponse(response)


    def post(self, request):
        """
        max 1 active game per player
        """

        # create game

        # creator_username = request.username
        #
        # unquoted_body = urllib.parse.unquote(request.body)
        # body = urllib.parse.parse_qs(unquoted_body)
        #
        # try:
        #     capacity = body["capacity"][0]
        # except KeyError:
        #     capacity = request.data["capacity"]

        print(f"{creator_username=}")
        print(f"{capacity=}")


        response = get_auth_ok_response_template(request)
        # response["payload"] = create_game(creator_username, name, capacity)

        return JsonResponse(response)

    def put(self, request, level_id):
        """add new entry to log"""

        print(f"{level_id=}")

        response = get_auth_ok_response_template(request)

        # print("todo log")

        username = request.username
        r = username_to_id(username=username, level_id=level_id)
        if not r["status"]:
            return r

        player_id = r["payload"]
        token_id = request.data["tokenId"]

        r = get_log(level_id)
        if not r["status"]:
            return r

        log = r["payload"]

        # print(f"{player_id=}")
        # print(f"{token_id=}")

        # todo level id fix
        print("what will be added?")

        print(f"{log=}")

        add_entry_to_log(log, player_id, token_id)

        #
        # print(f"{request.data=}")
        #
        # if "leave" in request.data:
        #     response["payload"] = leave_level(name, username)
        #
        # if "join" in request.data:
        #     response["payload"] = join_game(name, username)

        return JsonResponse(response)

def username_to_id(username, level_id):
    """
    username -> player_id ->
    join_index
    """

    # # fixme it is not passed level id, it is passed level name
    # level_id = _get_level_model().objects.get(name=level_id,is_active=True).id

    r = get_player_order_model().objects.get(user__username=username, level_id=level_id)


    r = r.join_index

    return {"status": True,
            "payload": r}