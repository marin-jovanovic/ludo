from django.apps import apps
from django.db import models

import backend.api.cqrs_q.game
from backend.api.comm.comm import Notifier

dice_notifier = Notifier()

from backend.api.model.users import get_user_model
from backend.api.model.game import _get_game_model
from backend.api.cqrs_q.users import is_username_in_db
from backend.api.cqrs_q.game import __check_game_name_exists
from django.db.models import Max
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


def add_roll(game, user, result):
    r = is_username_in_db(user)
    if not r["status"]:
        return r
    else:
        u_o = r["payload"]

    r = __check_game_name_exists(game)
    if not r["status"]:
        return r
    else:
        g_o = r["payload"]

    last_roll = _get_dice_history_model().objects.filter(game_id=g_o).aggregate(Max("roll_id"))

    print(f"{last_roll=}")

    dh = DiceHistory(
        game_id = g_o,
        roll_id=last_roll+1,
        user=u_o,
        result=result
    )

    dh.save()

    return {"status": True}


def _get_dice_history_model():
    return apps.get_model("api.dicehistory")
