from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.level import leave_level, join_level
from backend.api.model.level import notify_join_leave
from backend.api.model.user_connection import get_user_connection_model
from backend.api.view.comm import get_auth_ok_response_template


class UserConnectionView(APIView):

    def get(self, request, connection_id=None):
        # get basic game info
        response = get_auth_ok_response_template(request)

        if connection_id:
            print("not impl yet connection_id")

        else:
            print("get all connections")

            connections = {}

            r = get_user_connection_model().objects.filter(
                user_1_id=request.user_id,
                accepted=True
            )

            for i in r:
                connections[i.user_2.id] = {
                    "userId": i.user_2.id,
                    "userUsername": i.user_2.username,
                }

            r = get_user_connection_model().objects.filter(
                user_2_id=request.user_id,
                accepted=True
            )

            for i in r:
                connections[i.user_1.id] = {
                    "userId": i.user_1.id,
                    "userUsername": i.user_1.username,
                }

            response["payload"] = {
                "status": True,
                "userConnections": connections

            }

        # if not connection_id:
        #     """user/connection/requests"""
        #     print("not connection_id")
        #     # r = get_user_connection_model().objects.filter(
        #     #     user_2_id=request.user_id,
        #     #     accepted=False
        #     # )
        #     #
        #     # ret = {}
        #     # for i in r:
        #     #     ret[i.user_1.id] = {
        #     #         "userId": i.user_1.id,
        #     #         "userUsername": i.user_1.username,
        #     #     }
        #     #
        #     # response["payload"] = {
        #     #     "status": True,
        #     #     "userConnections": ret
        #     #
        #     # }
        #     #
        #     #
        #
        # elif connection_id:
        #     print("todo")

        return JsonResponse(response)

    # todo observers

    def delete(self, request, user_id):
        response = get_auth_ok_response_template(request)

        r = get_user_connection_model().objects.filter(
            user_1_id=request.user_id,
            user_2_id=user_id,
            accepted=True
        ).exists()

        if r:
            print("first type")

            get_user_connection_model().objects.get(
                user_1_id=request.user_id,
                user_2_id=user_id,
                accepted=True
            ).delete()

        r = get_user_connection_model().objects.filter(
            user_2_id=request.user_id,
            user_1_id=user_id,
            accepted=True
        ).exists()

        if r:
            print("second type")

            get_user_connection_model().objects.get(
                user_2_id=request.user_id,
                user_1_id=user_id,
                accepted=True
            ).delete()

        return JsonResponse(response)

    # maybe level_id=None, level_name=None
    def post(self, request, user_id):
        """send connection request / confirm

        1 -> sending
        2 -> accepting
        """
        response = get_auth_ok_response_template(request)

        l_c = get_user_connection_model().objects.filter(
            user_1_id=user_id,
            user_2_id=request.user_id,
            accepted=False
        ).exists()

        if l_c:
            print("accepting")
            r = get_user_connection_model().objects.get(
                user_1_id=user_id,
                user_2_id=request.user_id,
                accepted=False
            )

            r.accepted = True
            r.save()

            response["payload"]["status"] = True
            return JsonResponse(response)

        l_c = get_user_connection_model().objects.filter(
            user_2_id=user_id,
            user_1_id=request.user_id,
            accepted=False
        ).exists()

        if l_c:
            print("already sent")

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
