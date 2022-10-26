from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.game.game import get_start_pool
from backend.api.view.comm import get_auth_ok_response_template


class BoardView(APIView):

    def get(self, request, name, resource):
        # get basic game info

        print("get board,", name, resource)
        response = get_auth_ok_response_template(request)

        if name != "1":
            print("not impl")

        if resource == "startPool":
            response['payload'] = {
                "status": True,
                "payload": get_start_pool()
            }
            # get_start_pool()

        return JsonResponse(response)


