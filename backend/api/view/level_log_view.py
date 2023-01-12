from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_q.level_log import get_last_performed_by_all_users
from backend.api.cqrs_q.level import level_id_to_name
from backend.api.cqrs_q.player_order import join_id_to_username_and_user_id, \
    username_to_id
from backend.api.game.main import add_entry_to_log, get_log_api
from backend.api.model.level_log import get_level_log_model
from backend.api.view.comm import get_auth_ok_response_template


def level_log_get(level_id):
    log = get_level_log_model()\
        .objects\
        .filter(game_id=level_id)\
        .order_by("instruction_id")\
        .values()

    log = list(log)

    return {
        "status": True,
        "payload": log
    }


class LevelLogView(APIView):

    def get(self, request, level_id):

        response = get_auth_ok_response_template(request)

        log = get_level_log_model() \
            .objects \
            .filter(game_id=level_id) \
            .order_by("instruction_id") \
            .values()

        log = list(log)

        last_e_all = get_last_performed_by_all_users(level_id)

        only_first_entry = not last_e_all['status']

        print(f"{last_e_all=}")

        # if not last_e_all['status']:
        #     only_first = True

        ret_log = {}

        for e, entry in enumerate(log):
            # print('instruction id get', entry)

            ret_log[entry["instruction_id"]] = {
                "action": entry["action"],
                "diceResult": entry["dice_result"],
                "levelId": entry["game_id"],
                "entryId": entry["id"],
                "entryIndex": entry["instruction_id"],
                # todo load from acc log
                # "performed": entry["performed"],
                "userJoinIndex": entry["player"],
                "tokenId": entry["token"]
            }


            if only_first_entry:
                break

            if e > last_e_all["entryIndex"]:
                break

            # if not entry["performed"]:
            #     break

        opt = get_log_api(log, level_id)

        if not opt["turn"] and not opt["legalMoves"]:

            response["payload"] = {
                "status": True,
                "log": ret_log,
                "legalMoves": [],
                "userUsername": None,
                "userId": None
            }

        else:

            t = join_id_to_username_and_user_id(opt["turn"], level_id)
            if not t["status"]:
                return JsonResponse(response)

            ids = t["payload"]

            response["payload"] = {
                "status": True,
                "log": ret_log,
                "legalMoves": opt["legalMoves"],
                "userUsername": ids["userUsername"],
                "userId": ids["userId"]
            }

        return JsonResponse(response)

    @transaction.atomic
    def put(self, request, level_id):
        """add new entry to log"""

        """
        threats:
        user2 send instead user1
        
        user1 chooses user2 token
        
        user1 chooses immovable token
        
        """

        print(f"level log put {request.data=} {request.username=}")

        response = get_auth_ok_response_template(request)

        # not trusting user which user is performing action
        r = username_to_id(username=request.username, level_id=level_id)
        if not r["status"]:
            return JsonResponse(response)

        player_id = r["payload"]

        r = level_log_get(level_id)
        if not r["status"]:
            return JsonResponse(response)

        log = r["payload"]

        provided_entry_id = request.data["entryId"]
        # determinate if this user can perform this action

        last_entry = log[-1]
        true_last_entry = last_entry["id"]

        if true_last_entry != provided_entry_id:
            # they are not making decision for the last entry
            print(f"err not last entry id {true_last_entry=} {provided_entry_id=}")
            return JsonResponse(response)

        turn = last_entry["player"]

        if turn != player_id:
            print(f"err can not do this, players are not matching {turn=} {player_id=}")
            return JsonResponse(response)

        token_id = request.data["tokenId"]

        # lllllllllllllllllllllllllllllllllllllllllllllllllllll

        r = add_entry_to_log(log, player_id, token_id, level_id)

        log_diff_as_dict = r["logDiffAsDict"]

        print("log diff dict (from view function)")
        for index, entry in log_diff_as_dict.items():
            print(index, entry)
        print()

        legal_moves = r["legalMoves"]
        t = join_id_to_username_and_user_id(r["turn"], level_id)
        if not t["status"]:
            return JsonResponse(response)

        ids = t["payload"]

        from backend.api.model.level import get_level_model
        from backend.api.model.acceptance_log import get_acceptance_log_model

        acceptance_log_model = get_acceptance_log_model()
        capacity = get_level_model().objects.get(id=level_id).capacity

        for index, entry in log_diff_as_dict.items():

            game_log_model = get_level_log_model()

            r = game_log_model(
                game_id=level_id,
                instruction_id=index,
                player=entry["player"],
                token=entry['token'],
                dice_result=entry['dice_result'],
                action=entry["action"],
            )
            r.save()

            for player_index in range(capacity):

                q = acceptance_log_model(
                    level_id=level_id,
                    log_entry =r,
                    user_join_index=player_index,
                    accepted=False,
                    is_first=r.player==player_index,
                )
                q.save()

            print(f"get or create {index=} {entry=} {r=}")

        response["payload"] = {
            "status": True,
            "userUsername": ids["userUsername"],
            "userId": ids["userId"],
            "legalMoves": legal_moves
        }

        return JsonResponse(response)


