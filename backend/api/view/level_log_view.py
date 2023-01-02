from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.game_log import add_entry
from backend.api.game.game import add_entry_to_log, get_log_api
from backend.api.model.level_log import get_level_log_model
from backend.api.model.level import get_level_model
from backend.api.model.player_order import get_player_order_model
from backend.api.view.comm import get_auth_ok_response_template


def level_log_get(level_id):
    log = get_level_log_model().objects.filter(game_id=level_id,
                                               game_id__is_active=True).order_by(
        "instruction_id").values()

    log = list(log)

    return {
        "status": True,
        "payload": log
    }


class LevelLogView(APIView):

    def get(self, request, level_id):

        response = get_auth_ok_response_template(request)

        r = level_log_get(level_id)
        if not r["status"]:
            return r

        log = r["payload"]

        ret_log = {}

        for entry in log:
            # todo del instruction_id from value, and all other non used entries
            ret_log[entry["instruction_id"]] = entry

        opt = get_log_api(log)

        t = join_id_to_username_and_user_id(opt["turn"], level_id)
        if not t["status"]:
            return JsonResponse(response)

        ids = t["payload"]

        response["payload"] = {
            "status": True,
            "log": ret_log,
            "legalMoves": opt["legalMoves"],
            **ids,
        }

        return JsonResponse(response)

    def put(self, request, level_id):
        """add new entry to log"""

        response = get_auth_ok_response_template(request)

        # not trusting user which user is performing action
        r = username_to_id(username=request.username, level_id=level_id)
        if not r["status"]:
            return JsonResponse(response)

        player_id = r["payload"]

        r = level_log_get(level_id)
        if not r["status"]:
            return r

        log = r["payload"]

        # determinate if this user can perform this action

        # try:
        last_entry = log[-1]
        print(f"{last_entry=}")

        turn = last_entry["player"]

        print(f"{turn=} {player_id=}")
        if turn != player_id:
            print(80 * "-")
            print("can not do this, players are not matching")
            print(80 * "-")
            return JsonResponse(response)

        # except Exception as e:
        #     print("err", e)

        token_id = request.data["tokenId"]
        r = add_entry_to_log(log, player_id, token_id)

        log_diff = r["logDiff"]

        legal_moves = r["legalMoves"]
        t = join_id_to_username_and_user_id(r["turn"], level_id)
        if not t["status"]:
            return JsonResponse(response)

        ids = t["payload"]

        # add to db log diff

        r = level_id_to_name(level_id)

        if not r["status"]:
            return r

        level_name = r["payload"]

        for i in log_diff:

            i["game"] = level_name
            add_entry(**i)

        response["payload"] = {
            "status": True,
            **ids,
            "legalMoves": legal_moves
        }

        return JsonResponse(response)


def level_id_to_name(level_id):
    r = get_level_model().objects.get(id=level_id, is_active=True)

    print(r.name)

    return {
        "status": True,
        "payload": r.name
    }


def join_id_to_username_and_user_id(join_index, level_id):
    """join index (level index) -> username"""

    print(f"{join_index=}")

    t = int(join_index)

    level_exists = get_player_order_model().objects.filter(level_id=level_id).exists()

    player_order = get_player_order_model()

    try:

        r = get_player_order_model().objects.get(
            level_id=level_id,
            join_index=t
        )

    except player_order.DoesNotExist:
        if level_exists:
            print("err user not in level")
        else:
            print("err uncaught err")

        return {"status": False}

    return {"status": True,
            "payload": {"userUsername": r.user.username, "userId": r.user.id}}


def username_to_id(username, level_id):
    """
    username -> player_id ->
    join_index
    """

    r = get_player_order_model().objects.get(user__username=username,
                                             level_id=level_id)

    r = r.join_index

    return {"status": True,
            "payload": r}
