import json

from backend.api.cqrs_q.level import level_get_filter_id
from backend.api.cqrs_q.user import get_user
from backend.api.model.message import Message, message_notifier


def create_message(sender, level_id, content):
    print("create message")

    r = get_user(sender)
    if not r["status"]:
        return r

    user_o = r["payload"]

    r = level_get_filter_id(level_id)
    if not r["status"]:
        return {"status": False, "_": "__get_game"}

    game_o = r["payload"]

    g = Message(
        game=game_o,
        sender=user_o,
        content=content,
        # timestamp=
    )
    g.save()

    # print("game created", g.name, g.capacity)

    msg = json.dumps({
        "source": "msg created",
        "game": g.game.name,

        "timestamp": str(g.timestamp),
        "sender": g.sender.username,
        "content": g.content

    })

    print(f"{msg=}")

    message_notifier.notify(msg)

    print("message created")

    return {"status": True}
