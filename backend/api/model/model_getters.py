from django.apps import apps


def _get_message_model():
    return apps.get_model("api.message")


def _get_game_model():
    return apps.get_model("api.level")


def _get_player_order_model():
    return apps.get_model("api.playerorder")


def get_game_log_model():
    return apps.get_model("api.gamelog")


