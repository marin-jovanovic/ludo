import pathlib

from django.http import JsonResponse, FileResponse
from rest_framework.views import APIView

from backend.api.cqrs_q.user import is_username_in_db
from backend.api.view.comm import get_auth_ok_response_template, \
    get_auth_err_response_template
from backend.api.model.user import get_user_model

# todo add all settings that are hardcoded (game settings, number of players, ...)
import re

def extract_number(input_str: str) -> str:
    # Use a regular expression to find one or more digits at the end of the string
    match = re.search(r'\d+$', input_str)
    if match:
        # Return the first group (the matched digits)
        return match.group(0)
    else:
        # If no match was found, return an empty string
        return ""

class SettingsView(APIView):
    """
    todo on settings view
    """

    def get(self, request, resource_id=None):
        """


        """
        response = get_auth_ok_response_template(request)

        root_dir = pathlib.Path(__file__).parent.parent.parent.parent.resolve()
        print(f"{root_dir=}")

        p = root_dir / "profile_pic"

        try:
            os.makedirs(p)
        except OSError as e:
            print(f"{e=}")
            # return

        p = root_dir / "profile_pic" / request.username

        try:
            os.makedirs(p)
        except OSError as e:
            print(f"{e=}")
            # return

        # in_img = data
        # in_img = in_img[22:]

        # we can add extension .png
        safe_name = safe_create_dir(p / "pp")

        safe_name =  pathlib.Path(safe_name).name

        print(f"{safe_name=}")

        last_n = extract_number(safe_name)
        print(f"{last_n=}")
        last_n = int(last_n)
        last_img_suf = last_n - 1

        pat = p / f"pp_{last_img_suf}"


        try:
            with open(pat, "rb") as f:
                t = f.read()
                t = base64.b64encode(t)
                c = t.decode("utf-8")

                # print(f"{c=}")

                c = "data:image/png;base64," + c


        except FileNotFoundError:
            print("not found")

            c = None

        # print(f"{t=}")

        # print(t.decode("utf-8"))


        # print(f"{c=}")

        # encoded_b2 = "".join([format(n, '08b') for n in t])
        # print(f"{encoded_b2=}")
        # last = safe_name - 1

        # last_file_name = safe_create_dir()

        # photo = t

        response["payload"] = {
            "status": True,
            "username": request.username,
            "userProfilePhoto": c
            # "song": 1,
            # "songPayload": song_data

        }

        # return FileResponse(song_path.open("rb"))

        return JsonResponse(response)


    def post(self,request, resource_id=None):
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
            user.profile_picture = photo

            create_image(photo, request.username)

        user.save()

        response = get_auth_ok_response_template(request)
        response["payload"]["status"] = True
        return JsonResponse(response)
        #
        # response["payload"] = {
        #     "status": True,
        # }
        #
        # return JsonResponse(response)
        #


import base64


def create_image(data, username):
    root_dir = pathlib.Path(__file__).parent.parent.parent.parent.resolve()

    p = root_dir / "profile_pic"

    try:
        os.makedirs(p)
    except OSError as e:
        # print(f"{e=}")
        # return
        pass

    p = root_dir / "profile_pic" / username

    try:
        os.makedirs(p)
    except OSError as e:
        # print(f"{e=}")
        pass
        # return

    in_img = data
    in_img = in_img[22:]

    # we can add extension .png
    safe_name = safe_create_dir(p / "pp")

    print(f"{safe_name=}")

    # check if this is created

    with open(safe_name, "wb") as f:
        t = f.write(base64.b64decode(in_img))
        print(f"{t=}")
    print("created")

    return True

import os


def safe_create_dir(dir_name):
    i = 1
    while True:
        new_dir_name = f"{dir_name}_{i}"
        if not os.path.exists(new_dir_name):
            break
        i += 1

    return new_dir_name

