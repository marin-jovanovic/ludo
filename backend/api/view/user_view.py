from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template
from backend.api.model.user import get_user_model


class UserView(APIView):
    """
    middleware handles business logic
    """

    def get(self, request, user_id=None):
        """
        return empty payload
        logic handled in middleware
        """

        response = get_auth_ok_response_template(request)

        if user_id:

            r = get_user_model().objects.get(id=user_id)

            print(f"{r=}")

            response["payload"] = {
                "status": True,
                "id": r.id,
                "username": r.username,
                "currentlyPlaying": r.currently_playing
            }

            return JsonResponse(response)

        else:
            print("user view")

            print(f"{request.data=}")
            print(f"{request.body=}")
            print(f"{request.headers=}")

            # page = request.data["page"]
            #
            #
            #
            # print(f"{page=}")
            #
            # response["payload"] = {
            #     "status": True,
            #
            #     "users": {
            #         0: {
            #             "userId": 1,
            #             "userUsername": "johndoe",
            #
            #         },
            #         1: {
            #             "userId": 2,
            #             "userUsername": "janedoe",
            #         },
            #     },
            #     "meta": {
            #         "totalUsers": 100,
            #         "totalPages": 10,
            #         "currentPage": 1,
            #         "perPage": 10,
            #         "thisPage": 2,
            #
            #     }
            # }


            return JsonResponse(response)

    # def post(self, user_id):
    #     print("send ")
