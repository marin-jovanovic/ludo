from django.db.models import Max

from backend.api.cqrs_q.level import level_get_model
from backend.api.model.level_log import get_level_log_model

def add_entry(game, player, token, dice_result, action, performed=False):
    r = level_get_model(game)
    if r["status"]:
        game_o = r["payload"]
    else:
        print("get game err")
        return r

    instr_id = get_level_log_model().objects.filter(game=game_o).aggregate(Max("instruction_id"))["instruction_id__max"]

    if not isinstance(instr_id, int):
        instr_id = -1

    game_log_model = get_level_log_model()

    e = game_log_model(
        game=game_o,
        instruction_id=instr_id + 1,
        # player=user_o,
        player=player,
        token=token,
        dice_result=dice_result,
        action=action,
        performed=performed
    )
    e.save()

    return {"status": True}
