from django.contrib.auth.backends import BaseBackend

from django.contrib.auth.models import User


class AuthBackend(BaseBackend):
    """
    dummy backend, used for bypassing default auth by django

    Use the login name and a hash of the password.
    """

    def authenticate(self, request, username=None, password=None):
        print("auth backend")
        print(80 * "-")
        print(f"{username=} {password=}")

        username = "-1"
        password = "-1"

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            user = User.objects.create_user(username, username,
                                            password)

            # user = User.objects.get(username=username)

        user.is_active = True
        user.save()

        return user
