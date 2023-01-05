from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.acceptance_log import create_entry_if_not_exists
from backend.api.model.acceptance_log import get_acceptance_log_model
from backend.api.view.comm import get_auth_ok_response_template


class AcceptanceLogView(APIView):

    def get(self, request, level_id):

        response = get_auth_ok_response_template(request)

        # "performedEntries"
        # table game_log
        # id -> index

        r = get_acceptance_log_model().objects \
            .filter(level_id=level_id, user__username=request.username) \
            .values_list("log_entry", "log_entry__instruction_id") \
            .order_by("log_entry__instruction_id")

        ret = {}
        for id_, index in r:
            ret[index] = id_

        for i in ret.items():
            print(i)

        response["payload"] = {
            "status": True,
            "performedEntries": ret
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
