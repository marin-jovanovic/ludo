import json

from backend.api.cqrs_q.level import level_get_model_by_id
from backend.api.cqrs_q.user import get_user
from backend.api.model.acceptance_log import get_acceptance_log_model
from backend.api.model.level_log import get_level_log_model
from backend.api.model.acceptance_log import acceptance_log_entry_created_notifier

def create_entry_if_not_exists(level_id, entry_id, username):
    print(f"{level_id=}")
    print(f"{entry_id=}")

    r = level_get_model_by_id(level_id)
    if not r["status"]:
        return r

    level_o = r["payload"]

    r = get_user(username)
    if not r["status"]:
        return r

    user_o = r["payload"]

    print(f"{level_o=}")
    print(f"{user_o=}")

    log_entry_o = get_level_log_model().objects.get(
        instruction_id=entry_id,
        game_id=level_o
    )

    print(f"{log_entry_o=}")

    # if exist return
    r = get_acceptance_log_model().objects.filter(
        level=level_o,
        log_entry=log_entry_o,
        user=user_o,
        accepted=True
    ).exists()

    if r:
        print("already in db")
        return {
            "status": True
        }

    acceptance_log = get_acceptance_log_model()

    e = acceptance_log(
        level=level_o,
        log_entry=log_entry_o,
        user=user_o,
        accepted=True
    )
    e.save()

    msg = json.dumps({
        "source": "msg created",
        "game": g.game.name,

        "timestamp": str(g.timestamp),
        "sender": g.sender.username,
        "content": g.content

    })

    print(f"{msg=}")

    acceptance_log_entry_created_notifier.notify(msg)


    return {
        "status": True
    }
    # r = get_acceptance_log_model().objects.filter(level__id=level_id)
    #
    # print(r)
