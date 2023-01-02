from backend.api.cqrs_q.level import __check_game_name_exists, __get_game
from backend.api.model.message import get_message_model


def get_messages(game):
    r = __check_game_name_exists(game)
    if not r["payload"]:
        return {"status": False, "payload": "gamen ot exist"}

    r = __get_game(game)
    if not r["payload"]:
        # print(r)
        # print("r payload prsnet")
        return {"status": False, "payload": "game not exiswt"}
    else:
        game_o = r["payload"]

    # r = {}
    r = []
    for i in get_message_model().objects.filter(game=game_o).order_by(
            'timestamp'):
        # print(i.timestamp)
        # print(i.sender)
        # print(i.content)

        r.append({"timestamp": str(i.timestamp), "sender": i.sender.username,
                  "content": i.content})

    return {"status": True, "payload": r}
