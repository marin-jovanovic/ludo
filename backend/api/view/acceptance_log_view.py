from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.acceptance_log import create_entry_if_not_exists
from backend.api.cqrs_q.level_log import get_last_performed_by_all_users, \
    get_last_performed_by_this_user, get_any
from backend.api.model.user import get_user_model
from backend.api.view.comm import get_auth_ok_response_template

from backend.api.cqrs_c._cleanup import clean

class AcceptanceLogView(APIView):

    @transaction.atomic
    def get(self, request, level_id):

        # clean(level_id)

        response = get_auth_ok_response_template(request)
        # user_id = get_user_model().objects.get(username=request.username).id

        last_e_all = get_last_performed_by_all_users(level_id)
        print(f"{last_e_all=}")


        from backend.api.model.player_order import get_player_order_model
        user_join_index = get_player_order_model().objects.get(
            user_id__username=request.username, level_id=level_id
        ).join_index

        last_e_this = get_last_performed_by_this_user(level_id=level_id,
                                                    user_join_index=user_join_index)
        print(f"{last_e_this=}")

        last_e_any = get_any(level_id)
        print(f"{last_e_any=}")

        response["payload"] = {
            "status": True,
            "lastExecutedByAll": last_e_all,
            "lastExecutedThisUser": last_e_this,
            "lastExecutedByAny": last_e_any
        }

        return JsonResponse(response)

    @transaction.atomic
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
