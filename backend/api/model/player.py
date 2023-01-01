from django.apps import apps
from django.db import models

from backend.api.model.level import get_level_model_as_string


class User(models.Model):
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
    currently_playing = models.ForeignKey(get_level_model_as_string(),
                                          null=True,
                                          on_delete=models.SET_NULL)

    game_role = models.TextField(null=True)


def get_user_model():
    return apps.get_model(get_user_model_as_string())


def get_user_model_as_string():
    return "api.user"
