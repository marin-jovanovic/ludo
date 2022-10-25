from django.apps import apps
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

from backend.api.cqrs_q.game import __get_game
from backend.api.cqrs_c.users import get_user
from django.db.models import Max

def add_entry(game, player, token, dice_result, action):
    r = __get_game(game)
    if r["status"]:
        game_o = r["payload"]
    else:
        return r

    r = get_user(player)
    if r["status"]:
        user_o = r["payload"]
    else:
        return r

    instr_id = GameLog.objects.filter(game=game_o).aggregate(Max("instruction_id"))["instruction_id__max"]

    if not isinstance(instr_id, int):
        instr_id = -1

    e = GameLog(
        game=game_o,
        instruction_id=instr_id+1,
        player=user_o,
        token=token,
        dice_result=dice_result,
        action=action,
    )
    e.save()

    return {"status": True}