from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.acceptance_log import create_entry_if_not_exists
from backend.api.view.comm import get_auth_ok_response_template


class AcceptanceLogView(APIView):

    def get(self, request, level_id):

        response = get_auth_ok_response_template(request)

        #
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

