from django.apps import apps
from django.db import models

from backend.api.comm.comm import Notifier

game_created_notifier = Notifier()
game_left_notifier = Notifier()
game_join_notifier = Notifier()
games_notifier = Notifier()


class Level(models.Model):
    # primary key
    # id

    # alternate primary key
    # name = models.TextField(unique=True)
    capacity = models.IntegerField()

    is_active = models.BooleanField(default=True)


def _get_level_model():
    return "api.level"

    return apps.get_model(get_level_model_as_string())


def get_level_model_as_string():
    return "api.level"
