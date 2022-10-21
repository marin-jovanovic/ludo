import json
import urllib

from django.http import JsonResponse
from rest_framework.views import APIView

# from backend.api.auth.main import create_user
from backend.api.cqrs_c.users import auth_user
from backend.api.model.game import create_game, leave_game, join_game, get_games
from backend.api.view.comm import get_auth_ok_response_template


class LobbyView(APIView):

    def get(self, request):

        print("get games")
        response = get_auth_ok_response_template(request)
        response['payload'] = get_games()



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

        capacity = body["capacity"][0]

        print(f"{creator_username=}")
        print(f"{capacity=}")

        response = get_auth_ok_response_template(request)
        response["payload"] = create_game(creator_username, name, capacity)

        return JsonResponse(response)

    def put(self, request, name):

        username = request.username

        unquoted_body = urllib.parse.unquote(request.body)
        body = urllib.parse.parse_qs(unquoted_body)

        response = get_auth_ok_response_template(request)

        if "leave" in body:
            leave = body["leave"][0]

            if leave:

                response["payload"] = leave_game(name, username)

        if "join" in body:
            join = body["join"][0]

            if join:
                response["payload"] = join_game(name, username)

        return JsonResponse(response)

