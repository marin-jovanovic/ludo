from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template
from backend.api.model.user import get_user_model


class UserPageView(APIView):
    """
    middleware handles business logic
    """

    def get(self, request, page_id):
        """
        return empty payload
        logic handled in middleware
        """

        response = get_auth_ok_response_template(request)

        # if user_id:
        #
        #     r = get_user_model().objects.get(id=user_id)
        #
        #     print(f"{r=}")
        #
        #     response["payload"] = {
        #         "status": True,
        #         "id": r.id,
        #         "username": r.username,
        #         "currentlyPlaying": r.currently_playing
        #     }
        #
        #     return JsonResponse(response)
        #
        # else:
        print("user view")

        # print(f"{request.data=}")
        # print(f"{request.body=}")
        # print(f"{request.headers=}")

        # page = request.data["page"]



        # print(f"{page=}")

        r = get_user_model().objects.all()

        print(f"{r=}")
        print(f"{type(r)=}")
        users = {}

        # for e, i in enumerate(r):
        for i in r:

            users[i.id] = {
                "userId": i.id,
                "userUsername": i.username,
                # "currentlyPlaying": r.currently_playing
            }

        # users = {}
        # for i in range(20):
        #     users[i] = {
        #         "userId": i * 26,
        #         "userUsername": "johndoe" + str(i + 2),
        #
        #     }

        response["payload"] = {
            "status": True,
            "users": users,
            "meta": {
                "totalUsers": 100,
                "totalPages": 10,
                "currentPage": 1,
                "perPage": 10,
                "thisPage": 2,
            }
        }


        return JsonResponse(response)

