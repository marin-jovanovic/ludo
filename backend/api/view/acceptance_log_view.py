from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.acceptance_log import create_entry_if_not_exists
from backend.api.model.acceptance_log import get_acceptance_log_model
from backend.api.view.comm import get_auth_ok_response_template


class AcceptanceLogView(APIView):

    def get(self, request, level_id):

        response = get_auth_ok_response_template(request)

        # only for this user
        # "performedEntries"
        # table game_log
        # id -> index

        r = get_acceptance_log_model().objects \
            .filter(level_id=level_id, user__username=request.username) \
            .values_list("log_entry", "log_entry__instruction_id") \
            .order_by("log_entry__instruction_id")

        performed_entries = {}
        for id_, index in r:
            performed_entries[index] = id_

        for i in performed_entries.items():
            print(i)

        # global

        r = get_acceptance_log_model().objects \
            .filter(level_id=level_id) \
            .values_list("log_entry", "log_entry__instruction_id") \
            .order_by("log_entry__instruction_id")

        global_performed_entries = {}
        for id_, index in r:
            global_performed_entries[index] = id_

        for i in global_performed_entries.items():
            print(i)

        response["payload"] = {
            "status": True,
            "performedEntries": performed_entries,
            "globalPerformedEntries": global_performed_entries,
        }

        return JsonResponse(response)

    def post(self, request, level_id, entry_id):
        """add new entry to log"""
        print("post")
        response = get_auth_ok_response_template(request)

        # todo check for payload

        if "payload" in request.data:
            print("fixme not used, remove this calls")

        # if "payload" in request.data:
        #
        #     payload = request.data["payload"]
        #
        #     print(f"{payload=}")
        #
        #     print(type(payload))
        #
        #     if "instruction" not in payload:
        #         print(f"instruction not in payload {payload=}")
        #         return JsonResponse(response)
        #
        #     instruction = payload["instruction"]
        #
        #     if instruction == "moveToken":
        #         username = payload["username"]
        #         token_id = payload["tokenId"]
        #
        #         if username != request.username:
        #             print(f"username mismatch {username=} {request.username=}")
        #             return JsonResponse(response)
        #
        #         print(f"{username=} {type(username)=}")
        #         print(f"{token_id=} {type(token_id)=}")
        #
        #         print("move token")
        #
        #     else:
        #         print("err not implemented instruction")
        #         return JsonResponse(response)
        #
        #     return JsonResponse(response)
        #
        #
        # else:


        r = create_entry_if_not_exists(level_id, entry_id, request.username)
        if not r["status"]:
            return JsonResponse(response)

        response["payload"] = {
            "status": True
        }

        return JsonResponse(response)
