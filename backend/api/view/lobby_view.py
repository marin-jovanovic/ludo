from django.http import JsonResponse
from rest_framework.views import APIView

# from backend.api.auth.main import create_user
from backend.api.cqrs_c.users import auth_user
from backend.api.view.comm import get_auth_ok_response_template


class LoginView(APIView):

    def get(self, request):
        response = get_auth_ok_response_template(request)
        response['payload']['status'] = True
        response['payload']['payload'] = {
            'free rooms': {
                'room 1': {
                    'users': {
                        0: {'username': '1 user0'},
                        1: {'username': '1 user1'},
                    }
                },
                'room 4': {
                    'users': {
                        0: {'username': '4 user0'},
                    }
                },
            },
            'full rooms': {
                'room 2': {
                    'users': {
                        0: {'username': '2 user0'},
                        1: {'username': '2 user1'},
                        2: {'username': '2 user2'},
                        3: {'username': '2 user3'},
                    }
                },
                'room 3': {
                    'users': {
                        0: {'username': '3 user0'},
                        1: {'username': '3 user1'},
                        2: {'username': '3 user2'},
                        3: {'username': '3 user3'},
                    }
                },
            }
        }
        # response["payload"] = auth_user(username, password)

        return JsonResponse(response)

    def post(self, request, username):
        # return access token for provided username and password

        password = request.headers['password']

        response = get_auth_ok_response_template(request)
        response["payload"] = auth_user(username, password)

        return JsonResponse(response)
