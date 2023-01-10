from backend.api.cqrs_q.level import level_get_model_by_id
from backend.api.cqrs_q.user import get_user
from backend.api.model.player_order import get_player_order_model


def player_order_create_entry(username, level_id):
    r = level_get_model_by_id(level_id)
    if not r["status"]:
        print("get game err")
        return r
    else:
        g_o = r["payload"]

    last_index = get_player_order_model().objects.filter(level_id=g_o)

    max_index = 0
    for i in last_index:
        if i.user.username == username:
            # fixme
            # user is in this order

            # this is something that should not occur
            # but it is not an error

            print("fixme already in add to order")
            return {"status": True}
        max_index += 1

    r = get_user(username)
    if not r["status"]:
        return r

    u_o = r["payload"]

    player_order = get_player_order_model()

    g = player_order(
        level_id=g_o,
        join_index=max_index,
        # turn_index
        user=u_o,
    )
    g.save()

    print("player order created")

    return {"status": True}
