from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.level import create_game, leave_level, join_level, \
    get_active_levels, in_which_level_is_user
from backend.api.model.level import get_level_model
from backend.api.model.player_order import get_player_order_model
from backend.api.model.user import get_user_model
from backend.api.view.comm import get_auth_ok_response_template
from backend.api.model.level import notify_join_leave
from backend.api.model.user_connection import get_user_connection_model


class UserConnectionView(APIView):

    def get(self, request, connection_id=None):
        # get basic game info
        response = get_auth_ok_response_template(request)

        if connection_id:
            print("todo")

        else:

            r = get_user_model().objects.all().values("id", "username")
            r = list(r)

            ret = {}
            for e, i in enumerate(r):
                i["lastMessageContent"] = "encMsgCont"
                i["lastMessageTimestamp"] = "12:31"
                ret[e] = i




            response["payload"] = {
                "status": True,
                "userConnections": ret

            }

        return JsonResponse(response)

    # todo observers

    # maybe level_id=None, level_name=None
    def post(self, request, user_id):
        """send connection request / confirm"""
        response = get_auth_ok_response_template(request)


        l_c = get_user_connection_model().objects.filter(
            user_1_id=user_id,
            user_2_id=request.user_id,
            accepted=False
        ).exists()

        if l_c:
            print("accepting")
            r = get_user_connection_model().objects.filter(
                user_1_id=user_id,
                user_2_id=request.user_id,
                accepted=False
            )

            r.accepted = True
            r.save()

            response["payload"]["status"] = True
            return JsonResponse(response)

        r_c = get_user_connection_model().objects.filter(
            user_2_id=user_id,
            user_1_id=request.user_id,
            accepted=False
        ).exists()

        if r_c:
            print("accepting")
            r = get_user_connection_model().objects.filter(
                user_2_id=user_id,
                user_1_id=request.user_id,
                accepted=False
            )

            r.accepted = True
            r.save()

            response["payload"]["status"] = True
            return JsonResponse(response)

        print("requesting")

        user_connection_model = get_user_connection_model()

        r = user_connection_model(
            user_2_id=user_id,
            user_1_id=request.user_id,
            accepted=False
        )

        r.save()

        #
        # r_c = get_user_connection_model().objects.filter(
        #     user_2_id=user_id,
        #     user_1_id=request.user_id,
        #     accepted=False
        # ).exists()
        #
        # if l_c or r_c:
        #     print("req sent, this is accepting")
        #
        # t = get_user_connection_model().

        # level_name = level_id
        #
        # capacity = request.data["capacity"]
        #
        # response = get_auth_ok_response_template(request)
        # response["payload"] = create_game(request.username, level_name,
        #                                   capacity)

        response["payload"]["status"] = True
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
