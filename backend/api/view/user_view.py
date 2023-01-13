from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.model.user import get_user_model
from backend.api.view.comm import get_auth_ok_response_template


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

            # print(f"{request.data=}")
            # print(f"{request.body=}")
            # print(f"{request.headers=}")

            return JsonResponse(response)

    # def post(self, user_id):
    #     print("send ")
