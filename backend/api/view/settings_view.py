import pathlib
# todo add all settings that are hardcoded (game settings, number of players, ...)
import re

from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_q.user import is_username_in_db
from backend.api.model.user import get_user_model
from backend.api.view.comm import get_auth_ok_response_template, \
    get_auth_err_response_template


def extract_number(input_str: str) -> str:
    # Use a regular expression to find one or more digits at the end of the string
    match = re.search(r'\d+$', input_str)
    if match:
        # Return the first group (the matched digits)
        return match.group(0)
    else:
        # If no match was found, return an empty string
        return ""


def get_profile_picture(user_id):
    root_dir = pathlib.Path(__file__).parent.parent.parent.parent.resolve()
    profile_pictures_dir = root_dir / "profile_pic"
    this_user_profile_pictures_dir = profile_pictures_dir / str(user_id)
    safe_create(profile_pictures_dir)
    safe_create(this_user_profile_pictures_dir)
    safe_name = safe_create_dir(this_user_profile_pictures_dir / "pp")
    safe_name = pathlib.Path(safe_name).name
    last_n = extract_number(safe_name)
    last_n = int(last_n)
    last_img_suf = last_n - 1
    pat = this_user_profile_pictures_dir / f"pp_{last_img_suf}"
    try:
        with open(pat, "rb") as f:
            t = f.read()
            t = base64.b64encode(t)
            c = t.decode("utf-8")

            c = "data:image/png;base64," + c

    except FileNotFoundError:
        c = None
    return c


class SettingsView(APIView):
    """
    todo on settings view
    """

    def get(self, request, resource_id=None):
        """


        """
        response = get_auth_ok_response_template(request)
        user_id = request.user_id

        profile_photo = get_profile_picture(user_id)

        response["payload"] = {
            "status": True,
            "username": request.username,
            "userProfilePhoto": profile_photo

        }

        return JsonResponse(response)

    def post(self, request, resource_id=None):
        response = get_auth_ok_response_template(request)

        username = request.data['username']
        email = request.data['email']
        photo = request.data['profilePhoto']

        print(f"{username=}")
        print(f"{email=}")
        print(f"{len(photo)=}")

        if not is_username_in_db(request.username):
            print("username not in db")
            response = get_auth_err_response_template(request)
            return JsonResponse(response)

        user = get_user_model().objects.get(
            username=request.username)

        if username:
            print("not implemented")
            user.username = username
            print(f"{user.username=}")
        if email:
            print("not implemented")
            user.email = email
            print(f"{user.email=}")

        if photo:
            create_image(photo, request.user_id)

        user.save()

        response = get_auth_ok_response_template(request)
        response["payload"]["status"] = True
        return JsonResponse(response)


import base64
import os

def safe_create(dir_path):
    try:
        os.makedirs(dir_path)
    except OSError:
        pass


def create_image(data, user_id):
    root_dir = pathlib.Path(__file__).parent.parent.parent.parent.resolve()

    profile_pictures_dir = root_dir / "profile_pic"
    this_user_profile_pictures_dir = profile_pictures_dir / str(user_id)

    safe_create(profile_pictures_dir)
    safe_create(this_user_profile_pictures_dir)

    in_img = data
    in_img = in_img[22:]

    # we can add extension .png
    safe_name = safe_create_dir(this_user_profile_pictures_dir / "pp")

    with open(safe_name, "wb") as f:
        f.write(base64.b64decode(in_img))

    return True




def safe_create_dir(dir_name):
    i = 1
    while True:
        new_dir_name = f"{dir_name}_{i}"
        if not os.path.exists(new_dir_name):
            break
        i += 1

    return new_dir_name
