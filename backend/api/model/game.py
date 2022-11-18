from django.apps import apps
from django.db import models

from backend.api.comm.comm import Notifier
from backend.api.model.users import get_user_model

game_created_notifier = Notifier()
game_left_notifier = Notifier()
game_join_notifier = Notifier()
games_notifier = Notifier()


class Game(models.Model):
    # primary key
    # id

    # alternate primary key
    name = models.TextField(unique=True)

    capacity = models.IntegerField()


def _get_game_model():
    return apps.get_model("api.game")


class Tile(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()

    game = models.ForeignKey(
        Game,
        on_delete=models.SET_NULL,
        null=True
    )


class Token(models.Model):
    where = models.ForeignKey(
        Tile,
        on_delete=models.SET_NULL,
        null=True
    )

    name = models.IntegerField()

    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True
    )


def move_token(owner, token_name, step):
    print(f"move token {owner=} {token_name=} {step=}")
