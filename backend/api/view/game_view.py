import json
import urllib

from django.http import JsonResponse
from rest_framework.views import APIView

# from backend.api.auth.main import create_user
from backend.api.cqrs_c.users import auth_user
from backend.api.cqrs_c.game import create_game, leave_game, join_game, \
    get_games, get_specific_game
from backend.api.view.comm import get_auth_ok_response_template
from backend.api.model.game_log import add_entry

class GameView(APIView):

    def get(self, request, name):

        print("get games")
        response = get_auth_ok_response_template(request)
        response['payload'] = get_specific_game(name)

        # response['payload'] = {
        #     "status": True,
        #     "payload": {
        #         # "turn":
        #         # "init order": [0, 2, 3, 5],
        #
        #
        #     }
        # }
        #     # get_games()



        return JsonResponse(response)

    # GET 	Retrieve information about the REST API resource
    # POST 	Create a REST API resource
    # PUT 	Update a REST API resource
    # DELETE 	Delete a REST API resource or related component

    # todo observers

    def post(self, request, name):

        creator_username = request.username

        unquoted_body = urllib.parse.unquote(request.body)
        body = urllib.parse.parse_qs(unquoted_body)

        try:
            token = body["token"][0]
            action = body["action"][0]
        except KeyError:
            token = request.data["token"]
            action = request.data["action"]

        dice_result = None

        response = get_auth_ok_response_template(request)
        response["payload"] = add_entry(name, creator_username, token, dice_result, action)

        return JsonResponse(response)
