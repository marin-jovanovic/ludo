from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.acceptance_log import create_entry_if_not_exists
from backend.api.view.comm import get_auth_ok_response_template


class AcceptanceLogView(APIView):

    def get(self, request, level_id):

        response = get_auth_ok_response_template(request)

        r = get_logs_for_this_level(level_id)
        if not r["status"]:
            return JsonResponse(response)

        l = r["payload"]

        num_of_players = 2

        from collections import defaultdict
        ret = defaultdict(list)
        c = 0
        for i in l:
            # print(i)

            ret[i["log_entry_id"]].append(i["user_id"])

        for i in ret.items():
            print(i)

        from backend.api.model.player_order import get_player_order_model
        from backend.api.model.player import get_user_model

        user_id = get_user_model().objects.get(username = request.username).id
        print(f"{user_id=}")

        what_i_have_done = {}
        # c = 0
        for en, (entry_index, users_performed)  in enumerate(ret.items()):
            if user_id in users_performed:
                what_i_have_done[en]  = entry_index

        print(f"{what_i_have_done=}")

        # user_playing = get_user_model().objects.get(username = request.username).currently_playing_id
        # print(f"{user_playing=}")
        #
        # join_index = get_player_order_model().objects.get(user_id__username=request.username, level_id=user_playing).join_index
        # print(f"{join_index=}")

        # # if exist return
        # r = get_acceptance_log_model().objects.filter(
        #     level=level_o,
        #     log_entry=log_entry_o,
        #     user=user_o,
        #     accepted=True
        # ).exists()
        #
        # #
        #     name = models.TextField(unique=False)
        #
        #     capacity = models.IntegerField()
        #
        #     is_active = models.BooleanField(default=True)

        # level = models.ForeignKey(
        #     get_level_model(),
        #     on_delete=models.SET_NULL,
        #     null=True
        # )
        #
        #
        # log_entry = models.ForeignKey(
        #     get_level_log_model(),
        # )
        #
        #
        # user = models.ForeignKey(
        #     get_user_model()
        # )
        #
        # accepted =models.BooleanField(default=False)

        response["payload"] = {
            "status": True,
            "performedEntries": what_i_have_done
        }

        return JsonResponse(response)

    def post(self, request, level_id, entry_id):
        """add new entry to log"""

        response = get_auth_ok_response_template(request)

        r = create_entry_if_not_exists(level_id, entry_id, request.username)
        if not r["status"]:
            return JsonResponse(response)

        response["payload"] = {
            "status": True
        }

        return JsonResponse(response)

import json

from backend.api.cqrs_q.level import level_get_model_by_id
from backend.api.cqrs_q.user import get_user
from backend.api.model.acceptance_log import \
    acceptance_log_entry_created_notifier
from backend.api.model.acceptance_log import get_acceptance_log_model
from backend.api.model.level_log import get_level_log_model


def get_logs_for_this_level(level_id, ):
    # todo add check if this user can call this function
    # is someone else performing this move for this user

    # print(f"{level_id=}")

    r = level_get_model_by_id(level_id)
    if not r["status"]:
        return r

    level_o = r["payload"]
    #
    # r = get_user(username)
    # if not r["status"]:
    #     return r

    # user_o = r["payload"]

    # print(f"{level_o=}")
    # print(f"{user_o=}")

    # log_entry_o = get_level_log_model().objects.get(
    #     instruction_id=entry_id,
    #     game_id=level_o
    # )
    #
    # print(f"{log_entry_o=}")

    r = get_acceptance_log_model().objects.filter(
        level=level_o,
    ).values()

    r = list(r)

    # for i in r:
    #     print(i)


    # is_first_time = not r
    # print(f"{is_first_time=}")
    #
    #
    #
    #
    # # if exist return
    # r = get_acceptance_log_model().objects.filter(
    #     level=level_o,
    #     log_entry=log_entry_o,
    #     user=user_o,
    #     accepted=True
    # ).exists()
    #
    #
    # if r:
    #     print("already in db")
    #     return {
    #         "status": True
    #     }


    return {
        "status": True,
        "payload": r
    }
    # r = get_acceptance_log_model().objects.filter(level__id=level_id)
    #
    # print(r)
