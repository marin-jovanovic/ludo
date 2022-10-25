# from backend.api.model.game import _get_game_model
from django.apps import apps
from django.db import models


# def _get_game_model():
#     return apps.get_model("api.Game")

def get_game_model():
    return "api.game"


class Users(models.Model):
    """
    when user creates game
    game_role = "creator"

    when user join game
    game_role = "joined"
    """

    # alternate primary key
    username = models.TextField()

    password_hash = models.TextField()
    access_token = models.TextField(null=True)

    # todo check if this is desired action
    #   if user deletes it's profile while game is in progress
    #   then game will be deleted
    currently_playing = models.ForeignKey(get_game_model(), null=True,
                                          on_delete=models.SET_NULL)

    game_role = models.TextField(null=True)

# def get_game_model():


def get_user_model():
    return apps.get_model("api.Users")
