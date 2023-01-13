from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.model.user_connection import get_user_connection_model
from backend.api.view.comm import get_auth_ok_response_template


class UserConnectionRequestView(APIView):

    def get(self, request):
        # get basic game info
        response = get_auth_ok_response_template(request)

        """user/connection/requests"""

        r = get_user_connection_model().objects.filter(
            user_2_id=request.user_id,
            accepted=False
        )

        ret = {}
        for i in r:
            ret[i.user_1.id] = {
                "userId": i.user_1.id,
                "userUsername": i.user_1.username,
            }

        response["payload"] = {
            "status": True,
            "userConnections": ret

        }

        return JsonResponse(response)
