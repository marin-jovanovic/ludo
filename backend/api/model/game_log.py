from django.db import models
from backend.api.model.users import get_user_model
from backend.api.model.game import _get_game_model


class GameLog(models.Model):
    # primary key
    # id

    game = models.ForeignKey(
        _get_game_model(),
        on_delete=models.SET_NULL,
        null=True
    )

    instruction_id = models.IntegerField()

    # pl

    player = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True
    )

    # if null then it is global action
    token = models.IntegerField(null=True)
    dice_result = models.IntegerField(null=True)

    # if previous null
    # todo extract in separate table
    action = models.TextField()

