from django.db import models

from backend.api.comm.comm import Notifier
from backend.api.model.player import get_user_model_as_string
from backend.api.model.level import _get_level_model

game_created_notifier = Notifier()
game_left_notifier = Notifier()
game_join_notifier = Notifier()
games_notifier = Notifier()
message_notifier = Notifier()


class Message(models.Model):
    # primary key
    # id

    game = models.ForeignKey(_get_level_model(),
                             on_delete=models.SET_NULL, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    sender = models.ForeignKey(get_user_model_as_string(),
                               on_delete=models.SET_NULL, null=True)
    # on delette cascade?

    content = models.TextField()


