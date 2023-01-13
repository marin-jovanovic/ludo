def construct_goes(player):
    """
    for determine_order
    """

    return {
        # "game": None,
        "player": player,
        "token": None,
        "dice_result": None,
        "action": "goes"
    }


def construct_roll(player, roll):
    """
    @player rolled @roll

    """
    return {
        "player": player,
        "token": None,
        "dice_result": roll,
        "action": "roll"
    }


def user_choose(player, roll):
    """
    @player rolled @roll

    """
    return {
        "player": player,
        "token": None,
        "dice_result": roll,
        "action": "choose"
    }


def construct_tie():
    """
    for determine_order
    """
    return {
        "player": None,
        "token": None,
        "dice_result": None,
        "action": "tie"
    }


# todo not implemented
# def skip(player):
#     """
#     player skip its turn; no action
#
#     """
#
#     return {
#         # "game": None,
#         "player": player,
#         "token": None,
#         "dice_result": None,
#         "action": "skip"
#     }


def move_token(player, token, step):
    return {
        'player': player,
        'token': token,
        'dice_result': step,
        'action': "move"
    }


def log_eat_token(player, token):
    return {
        'player': player,
        'token': token,
        'dice_result': None,
        'action': "eaten"
    }


def log_won(player):
    return {
        'player': player,
        'token': None,
        'dice_result': None,
        'action': "won"
    }
