from django.db import models

from django.apps import apps
from django.db import models
from backend.api.model.player import get_user_model, get_user_model_as_string
from backend.api.model.level import _get_level_model, get_level_model_as_string


class GameLog(models.Model):
    # primary key
    # id

    game = models.ForeignKey(
        get_level_model_as_string(),
        on_delete=models.SET_NULL,
        null=True
    )

    instruction_id = models.IntegerField()

    # pl

    player = models.IntegerField()

    # player = models.ForeignKey(
    #     # "api.miniPersonPlayer",
    #     get_user_model(),
    #     on_delete=models.SET_NULL,
    #     null=True
    # )

    # if null then it is global action
    token = models.IntegerField(null=True)
    dice_result = models.IntegerField(null=True)

    # if previous null
    # todo extract in separate table
    action = models.TextField()

    performed = models.BooleanField()


def game_log_model():
    return apps.get_model(game_log_model_as_string())


def game_log_model_as_string():
    return "api.gamelog"

