from django.db.models import Max

from backend.api.cqrs_q.game import __get_game
from backend.api.cqrs_q.users import get_user
from backend.api.model.game_log import GameLog


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
