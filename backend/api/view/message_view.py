import urllib

from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.view.comm import get_auth_ok_response_template
from backend.api.model.message import create_message

from backend.api.model.message import get_messages

class MessageView(APIView):

    def get(self, request, game):

        response = get_auth_ok_response_template(request)
        response['payload'] = get_messages(game)

        return JsonResponse(response)

    # todo observers

    def post(self, request, game=None):


        unquoted_body = urllib.parse.unquote(request.body)
        body = urllib.parse.parse_qs(unquoted_body)

        try:
            sender = body["sender"][0]
            game = body["game"][0]
            content = body["content"][0]
        except KeyError:
            sender = request.data["sender"]
            game = request.data["game"]
            content = request.data["content"]

        print(f"{sender=}")
        print(f"{game=}")
        print(f"{content=}")

        response = get_auth_ok_response_template(request)
        response["payload"] = create_message(sender, game, content)

        return JsonResponse(response)

