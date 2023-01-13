from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.model.message import get_message_model
from backend.api.view.comm import get_auth_ok_response_template


class DirectMessageView(APIView):

    # todo identification for one on one messaging

    def get(self, request, user_id):
        """
        for initial getting messages
        """

        response = get_auth_ok_response_template(request)

        messages = get_message_model().objects.filter(Q(
            sender_id=request.user_id,
            receiver=user_id

        ) | Q(
            sender_id=user_id,
            receiver=request.user_id

        )
                                                      ).order_by("timestamp")

        ret = {}
        for e, i in enumerate(messages):
            print(i)
            ret[e] = {
                "senderId": i.sender_id,
                "receiverId": i.receiver_id,
                "timestamp": i.timestamp,
                "content": i.content
            }

        response["payload"] = {
            "status": True,
            "messages": ret
        }

        return JsonResponse(response)

    # todo observers

    def post(self, request, user_id):
        print(f"{request.data=}")
        content = request.data["content"]

        response = get_auth_ok_response_template(request)

        print("create message")

        message_model = get_message_model()

        g = message_model(
            receiver_id=user_id,
            sender_id=request.user_id,
            content=content,
        )
        g.save()

        return JsonResponse(response)
