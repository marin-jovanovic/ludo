from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template


class UserView(APIView):
    """
    middleware handles business logic
    """

    def get(self, request, user_id):
        """
        return empty payload
        logic handled in middleware
        """

        response = get_auth_ok_response_template(request)

        from backend.api.model.user import get_user_model
        r = get_user_model().objects.get(id=user_id)

        print(f"{r=}")

        # assuming obj is a model instance
        # serialized_obj = serializers.serialize('json', [r, ])
        # print(f"{serialized_obj=}")

        # serialized_obj = JSON.
        # del serialized_obj[""]

        # from django.core import serializers
        #
        # serial = serializers.serialize("json", [r])
        # ...
        # # .next() pulls the first object out of the generator
        # # .object retrieves django object the object from the DeserializedObject
        # obj = next(serializers.deserialize("json", serial)).object

        # print(f"{obj=}")
        #
        # for i in obj.items():
        #     print(i)

        # r = list(r)
        #
        # for i in serialized_obj.items():
        #     print(i)

        response["payload"] = {
            "status": True,
            "id": r.id,
            "username": r.username,
            "currentlyPlaying": r.currently_playing
            # **serialized_obj
        }

        # ["status"] = True
        #
        # response["payload"]
        #
        return JsonResponse(response)
