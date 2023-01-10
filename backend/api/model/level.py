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

    """
    user creates game
    game is done -> set is_active flag
    user creates game with same name -> all ok

    integrity rule
        name + is_active=True = unique
        name

    """
    name = models.TextField(unique=False)

    capacity = models.IntegerField()

    is_active = models.BooleanField(default=True)


def get_level_model():
    return apps.get_model(get_level_model_as_string())


def get_level_model_as_string():
    return "api.level"


#///////////////////////

import json

from django.apps import apps
from django.db import models

from backend.api.comm.comm import Notifier

level_join_left_notifier = Notifier()

def notify_join_leave():
    msg = json.dumps({
        "msg": "someone joined or left"
    })
    level_join_left_notifier.notify(msg)
