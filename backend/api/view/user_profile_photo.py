import pathlib
import re

from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_q.user import is_username_in_db
from backend.api.model.user import get_user_model
from backend.api.view.comm import get_auth_ok_response_template, \
    get_auth_err_response_template
from backend.api.view.settings_view import get_profile_picture


class UserProfilePhotoView(APIView):
    """
    todo on settings view
    """

    def get(self, request, user_id):
        """


        """
        response = get_auth_ok_response_template(request)

        profile_photo = get_profile_picture(user_id)

        response["payload"] = {
            "status": True,
            "username": request.username,
            "userProfilePhoto": profile_photo
        }

        return JsonResponse(response)




