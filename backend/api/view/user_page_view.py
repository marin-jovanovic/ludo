from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.model.user import get_user_model
from backend.api.view.comm import get_auth_ok_response_template


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

        print("user view")

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
