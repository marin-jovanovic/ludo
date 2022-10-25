from django.apps import apps
from django.db import models

from backend.api.comm.comm import Notifier

game_created_notifier = Notifier()
game_left_notifier = Notifier()
game_join_notifier = Notifier()
games_notifier = Notifier()


class Game(models.Model):
    # primary key
    # id

    # alternate primary key
    name = models.TextField(unique=True)

    capacity = models.IntegerField()


def _get_game_model():
    return apps.get_model("api.game")
