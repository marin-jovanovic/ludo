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

    performed = models.BooleanField()

from backend.api.cqrs_q.game import __get_game

def is_any_entry_present(game):
    r = __get_game(game)
    if r["status"]:
        game_o = r["payload"]
    else:
        return r
    try:
        any_entries = GameLog.objects.filter(game=game_o)

        if bool(any_entries):
            return {"status": True, "payload": True}
        else:
            return {"status": True, "payload": False}

        # print(f"{any_entries=}")

        # print(bool(any_entries), )

        # .exists()
    except GameLog.DoesNotExist:
        return {"status": True, "payload": False}
        # any_entries = None

    # print(f"{any_entries=}")


def get_entries(game):
    r = __get_game(game)
    if r["status"]:
        game_o = r["payload"]
    else:
        return r
    try:
        any_entries = GameLog.objects.filter(game=game_o)
            # .exists()
        return  {"status": True, "payload": {i.instruction_id:
                                                 {
                                                     "username": i.player.username,
                                                     "token": i.token,
                                                     "diceResult": i.dice_result,
                                                     "action": i.action,
                                                     "performed": i.performed
                                                 }

        for i in any_entries
        }}
    except GameLog.DoesNotExist:
        any_entries = None
        return  {"status": False,}

    # print(f"{any_entries=}")
