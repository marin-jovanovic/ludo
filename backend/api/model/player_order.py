from django.apps import apps
from django.db import models

from backend.api.model.level import get_level_model
from backend.api.model.user import get_user_model_as_string


class PlayerOrder(models.Model):
    level_id = models.ForeignKey(
        get_level_model(),
        on_delete=models.SET_NULL,
        null=True
    )

    join_index = models.IntegerField()

    turn_index = models.IntegerField(null=True)

    user = models.ForeignKey(
        get_user_model_as_string(),
        on_delete=models.SET_NULL,
        null=True
    )

    game_joined_timestamp = models.DateTimeField(auto_now_add=True)

    index_won = models.IntegerField(null=True)

    index_left = models.IntegerField(null=True)

    colour = models.TextField()



def get_player_order_model():
    return apps.get_model(get_player_order_model_as_string())


def get_player_order_model_as_string():
    return "api.playerOrder"
