from django.apps import apps
from django.db import models

from backend.api.comm.comm import Notifier

dice_notifier = Notifier()

from backend.api.model.users import get_user_model
from backend.api.model.game import _get_game_model


class DiceHistory(models.Model):

    game_id = models.ForeignKey(
        _get_game_model(),
        on_delete=models.SET_NULL,
        null=True
    )

    roll_id = models.IntegerField()

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True
    )

    result = models.IntegerField()


def _get_dice_history_model():
    return apps.get_model("api.dicehistory")
