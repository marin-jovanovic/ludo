from django.apps import apps
from django.db import models

from backend.api.comm.comm import Notifier
from backend.api.model.level import get_level_model
from backend.api.model.user import get_user_model_as_string, get_user_model

# game_created_notifier = Notifier()
# game_left_notifier = Notifier()
# game_join_notifier = Notifier()
# games_notifier = Notifier()
message_notifier = Notifier()


class Message(models.Model):
    # primary key
    # id

    game = models.ForeignKey(get_level_model(),
                             on_delete=models.SET_NULL, null=True)

    receiver = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_requests_created'
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    sender = models.ForeignKey(get_user_model_as_string(),
                               on_delete=models.SET_NULL, null=True)
    # on delette cascade?

    content = models.TextField()


def get_message_model():
    return apps.get_model(get_message_model_as_string())


def get_message_model_as_string():
    return "api.message"
