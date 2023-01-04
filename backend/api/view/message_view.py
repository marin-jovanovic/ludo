from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.message import create_message
from backend.api.cqrs_q.message import get_messages
from backend.api.view.comm import get_auth_ok_response_template


class MessageView(APIView):

    # todo identification for one on one messaging

    def get(self, request, level_id):
        """
        for initial getting messages
        """

        print(f"get messages {level_id=}")

        response = get_auth_ok_response_template(request)
        response['payload'] = get_messages(level_id)

        return JsonResponse(response)

    # todo observers

    def post(self, request, level_id):
        sender = request.data["sender"]
        level_id = request.data["game"]
        content = request.data["content"]

        response = get_auth_ok_response_template(request)
        response["payload"] = create_message(sender=sender, level_id=level_id, content=content)

        return JsonResponse(response)
