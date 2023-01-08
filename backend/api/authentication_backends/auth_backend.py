from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

from backend.test.auth import create_profile


class AuthBackend(BaseBackend):
    """
    dummy backend, used for bypassing default auth by django

    Use the login name and a hash of the password.
    """

    def authenticate(self, request, username=None, password=None):

        username = "-1"
        password = "-1"

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            user = create_profile(username, username,
                                  password)


        user.is_active = True
        user.save()

        return user
