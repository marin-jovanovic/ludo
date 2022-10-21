
from django.http import JsonResponse
from rest_framework.views import APIView

# from backend.api.model.user import User
from backend.api.view.comm import get_auth_ok_response_template


class SettingsView(APIView):

    def get(self, request):

        print("get settings")

        response = get_auth_ok_response_template(request)

        # s = get_settings(username=request.username)

        response["payload"] = {
            "status": True,
            "username": request.username
        }
        return JsonResponse(response)

    def post(self, request):
        print("post settings")
        print(request.data)

        # zoomUserLocation
        # update_settings(request.username, request.data)

        response = get_auth_ok_response_template(request)
        response["payload"]["status"] = True
        return JsonResponse(response)

