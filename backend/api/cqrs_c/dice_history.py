from django.db.models import Max

from backend.api.cqrs_q.game import __check_game_name_exists
from backend.api.cqrs_q.users import is_username_in_db
from backend.api.model.dice_history import _get_dice_history_model, DiceHistory


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
