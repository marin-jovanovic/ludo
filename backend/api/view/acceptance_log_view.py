from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.acceptance_log import create_entry_if_not_exists
from backend.api.cqrs_q.level_log import get_last_performed_by_all_users, \
    get_last_performed_by_this_user, get_any
from backend.api.view.comm import get_auth_ok_response_template
from backend.api.model.user import get_user_model


class AcceptanceLogView(APIView):

    def get(self, request, level_id):

        response = get_auth_ok_response_template(request)
        user_id = get_user_model().objects.get(username=request.username).id


        last_e_all = get_last_performed_by_all_users(level_id)

        last_e_this = get_last_performed_by_this_user(level_id=level_id, user_id=user_id)

        last_e_any = get_any(level_id)

        response["payload"] = {
            "status": True,
            "lastExecutedByAll": last_e_all,
            "lastExecutedThisUser": last_e_this,
            "lastExecutedByAny": last_e_any
        }


        print(f"{last_e_all=}")
        print(f"{last_e_this=}")
        print(f"{last_e_any=}")
        return JsonResponse(response)

    def post(self, request, level_id, entry_id):
        """add new entry to log"""
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

