from backend.api.cqrs_q.level import level_get_filter_id
from backend.api.model.message import get_message_model


def get_messages(level_id):
    # r = __check_game_name_exists(game)
    # if not r["status"]:
    #     return {"status": False, "t": "__check_game_name_exists"}

    r = level_get_filter_id(level_id)
    if not r["status"]:
        return {"status": False, "t": "__get_game"}

    game_o = r["payload"]

    r = []
    for i in get_message_model().objects.filter(game=game_o).order_by(
            'timestamp'):
        # print(i.timestamp)
        # print(i.sender)
        # print(i.content)

        r.append({"timestamp": str(i.timestamp), "sender": i.sender.username,
                  "content": i.content})

    return {"status": True, "payload": r}
