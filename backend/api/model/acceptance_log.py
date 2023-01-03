from django.apps import apps
from django.db import models

from backend.api.comm.comm import Notifier

# game_created_notifier = Notifier()
# game_left_notifier = Notifier()
# game_join_notifier = Notifier()
# games_notifier = Notifier()


from backend.api.model.level_log import get_level_log_model
from backend.api.model.player import get_user_model
from backend.api.model.level import get_level_model

from backend.api.comm.comm import Notifier
from backend.api.model.level import get_level_model
from backend.api.model.player import get_user_model_as_string

acceptance_log_entry_created_notifier = Notifier()
# game_left_notifier = Notifier()
# game_join_notifier = Notifier()
# games_notifier = Notifier()
# message_notifier = Notifier()


class AcceptanceLog(models.Model):
    # primary key
    # id

    # alternate primary key

    level = models.ForeignKey(
        get_level_model(),
        on_delete=models.SET_NULL,
        null=True
    )

    log_entry = models.ForeignKey(
        get_level_log_model(),
        on_delete=models.SET_NULL,
        null=True
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete = models.SET_NULL,
        null=True
    )

    accepted = models.BooleanField(default=False)



def get_acceptance_log_model():
    return apps.get_model(get_acceptance_log_model_as_string())


def get_acceptance_log_model_as_string():
    return "api.acceptanceLog"
