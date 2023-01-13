from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.level import create_game, leave_level, join_level, \
    get_active_levels, in_which_level_is_user
from backend.api.model.level import get_level_model
from backend.api.model.level import notify_join_leave
from backend.api.model.player_order import get_player_order_model
from backend.api.model.user import get_user_model
from backend.api.view.comm import get_auth_ok_response_template


class LevelView(APIView):

    def get(self, request, level_id=None):
        # get basic game info
        response = get_auth_ok_response_template(request)

        # todo get in chunks (e.g. 10 by 10 with index and total number of pages in res)
        # todo add filters

        if level_id:

            r = get_player_order_model().objects.filter(level_id=level_id)

            id_to_order = {
                i.user_id: i.join_index for i in r
            }

            m = {}

            for id_, join_id in id_to_order.items():
                # todo add is active flag, when filtering in future
                r = get_user_model().objects.get(id=id_)

                m[id_] = {"username": r.username, "joinId": join_id}

            capacity = get_level_model().objects.get(id=level_id).capacity

            response["payload"] = {
                "status": True,
                "users": m,
                "capacity": capacity
            }

        else:

            r = get_active_levels()
            if not r["status"]:
                return JsonResponse(response)

            active_levels = r["payload"]

            r = in_which_level_is_user(request.username)
            if not r["status"]:
                return JsonResponse(response)

            response["payload"] = {
                "status": True,
                "inLevel": r["payload"],
                "levels": active_levels,
            }

        return JsonResponse(response)

    # todo observers

    # maybe level_id=None, level_name=None
    def post(self, request, level_id):
        """
        create level

        max 1 active game per player


        """

        level_name = level_id

        capacity = request.data["capacity"]

        response = get_auth_ok_response_template(request)
        response["payload"] = create_game(request.username, level_name,
                                          capacity)

        return JsonResponse(response)

    def put(self, request, level_id):
        """join or leave level"""

        username = request.username

        response = get_auth_ok_response_template(request)

        if "leave" in request.data:
            response["payload"] = leave_level(username)

        if "join" in request.data:
            response["payload"] = join_level(level_id, username)

        notify_join_leave()

        print(f"{response['payload']=}")

        return JsonResponse(response)
